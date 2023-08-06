"""Prod-ready HTTP client with timeout and retries by default."""
import email.parser
import importlib.metadata
import re
import typing as t
import warnings

import orjson
import requests
from fw_utils import AttrDict, attrify
from pydantic import AnyHttpUrl, BaseSettings
from requests import Request, exceptions
from requests.adapters import HTTPAdapter
from requests.cookies import cookiejar_from_dict
from requests.sessions import Session
from requests.structures import CaseInsensitiveDict
from urllib3.util.retry import Retry

__version__ = importlib.metadata.version(__name__)
__all__ = [
    "AnyAuth",
    "HttpClient",
    "HttpConfig",
    "load_useragent",
]

RETRY_METHODS = ["DELETE", "GET", "HEAD", "POST", "PUT", "OPTIONS"]
RETRY_STATUSES = [429, 500, 502, 503, 504]
KILOBYTE = 1 << 10
MEGABYTE = 1 << 20

AnyAuth = t.Union[
    str,  # authorization header (custom - the others are built in to requests)
    t.Tuple[str, str],  # basic auth user/pass
    t.Callable[[Request], Request],  # any callable modifying the request
    requests.auth.AuthBase,  # same as above, implemented as a class
]


class HttpConfig(BaseSettings):
    """HTTP client configuration."""

    class Config:
        """Enable envvar config using prefix 'FW_HTTP_'."""

        env_prefix = "FW_HTTP_"

    client_name: str
    client_version: str
    client_info: t.Dict[str, str] = {}

    baseurl: t.Optional[AnyHttpUrl]
    cookies: t.Dict[str, str] = {}
    headers: t.Dict[str, str] = {}
    params: t.Dict[str, str] = {}
    cert: t.Optional[t.Union[str, t.Tuple[str, str]]]
    auth: t.Optional[AnyAuth]
    proxies: t.Dict[str, str] = {}
    verify: bool = True
    trust_env: bool = True
    connect_timeout: float = 5
    read_timeout: float = 15
    max_redirects: int = 30
    stream: bool = False
    response_hooks: t.List[t.Callable] = []
    retry_backoff_factor: float = 0.5
    retry_allowed_methods: t.List[str] = RETRY_METHODS
    retry_status_forcelist: t.List[int] = RETRY_STATUSES
    retry_total: int = 5


class HttpClient(Session):  # pylint: disable=too-many-instance-attributes
    """Prod-ready HTTP client with timeout and retries by default."""

    def __init__(self, config: t.Optional[HttpConfig] = None, **kwargs) -> None:
        """Init client instance using attrs from HttpConfig."""
        super().__init__()
        self.config = config = config or HttpConfig(**kwargs)
        self.baseurl = config.baseurl or ""
        self.cookies = cookiejar_from_dict(config.cookies)
        self.headers.update(config.headers)
        self.headers["User-Agent"] = dump_useragent(
            config.client_name,
            config.client_version,
            **config.client_info,
        )
        self.params.update(config.params)  # type: ignore
        self.cert = config.cert
        if isinstance(config.auth, str):
            self.headers["Authorization"] = config.auth
        else:
            self.auth = config.auth
        self.proxies = config.proxies
        self.verify = config.verify
        self.trust_env = config.trust_env
        self.timeout = (config.connect_timeout, config.read_timeout)
        self.max_redirects = config.max_redirects
        self.stream = config.stream
        self.hooks = {"response": config.response_hooks}
        retry = Retry(
            backoff_factor=config.retry_backoff_factor,
            allowed_methods=config.retry_allowed_methods,
            status_forcelist=config.retry_status_forcelist,
            raise_on_redirect=False,
            raise_on_status=False,
            total=config.retry_total,
        )
        adapter = HTTPAdapter(max_retries=retry)
        self.mount("http://", adapter)
        self.mount("https://", adapter)

    # pylint: disable=arguments-differ
    def request(  # type: ignore
        self, method: str, url: str, raw: bool = False, **kwargs
    ):
        """Send request and return loaded JSON response (AttrDict)."""
        # prefix relative paths with baseurl
        if not url.startswith("http"):
            url = f"{self.baseurl}{url}"
        # set authorization header from simple str auth kwarg
        if isinstance(kwargs.get("auth"), str):
            headers = kwargs.setdefault("headers", {})
            headers["Authorization"] = kwargs.pop("auth")
        # use the session timeout by default
        kwargs.setdefault("timeout", self.timeout)
        response = super().request(method, url, **kwargs)
        response.__class__ = Response  # cast as subclass
        # raise if there was an http error (eg. 404)
        if not raw:
            response.raise_for_status()
        # return response when streaming or raw=True
        if raw or self.stream or kwargs.get("stream"):
            return response
        # don't load empty response as json
        if not response.content:
            return None
        return response.json()


def dump_useragent(name: str, version: str, **kwargs: str) -> str:
    """Return parsable UA string for given name, version and extra keywords."""
    info = "; ".join(f"{k}:{v}" for k, v in sorted(kwargs.items()))
    info_str = f" ({info})" if kwargs else ""
    return f"{name}/{version}{info_str}"


def load_useragent(useragent: str) -> t.Dict[str, str]:
    """Return name, version and extra keywords parsed from UA string."""
    name, _, useragent = useragent.partition("/")
    version, _, useragent = useragent.partition(" ")
    info = {}
    info_str = useragent.strip("()")
    if info_str:
        for item in info_str.split("; "):
            key, value = item.split(":", maxsplit=1)
            info[key] = value
    return AttrDict(name=name, version=version, **info)


class Response(requests.Response):
    """Response class with multipart message splitting and attrified JSON support.

    The chunk size defaults are overridden on the iter methods:
     * iter_content() - 1 MB
     * iter_lines()   - 1 KB

    Multipart references:
      https://www.w3.org/Protocols/rfc1341/7_2_Multipart.html
      https://github.com/requests/toolbelt/blob/0.9.1/requests_toolbelt/multipart/decoder.py#L74
      https://github.com/MGHComputationalPathology/dicomweb-client/blob/v0.51.0/src/dicomweb_client/api.py#L697
    """

    def iter_content(self, chunk_size=MEGABYTE, decode_unicode=False):
        return super().iter_content(
            chunk_size=chunk_size,
            decode_unicode=decode_unicode,
        )

    def iter_lines(self, chunk_size=KILOBYTE, decode_unicode=False, delimiter=None):
        return super().iter_lines(
            chunk_size=chunk_size,
            decode_unicode=decode_unicode,
            delimiter=delimiter,
        )

    def iter_parts(self, **kwargs) -> t.Iterator["Part"]:
        """Yield individual message parts from a multipart response."""
        content_type = self.headers["content-type"]
        media_type, *ct_info = [ct.strip() for ct in content_type.split(";")]
        if not media_type.lower().startswith("multipart"):
            raise ValueError(f"Media type is not multipart: {media_type}")
        for item in ct_info:
            attr, _, value = item.partition("=")
            if attr.lower() == "boundary":
                boundary = value.strip('"')
                break
        else:
            # Some servers set the media type to multipart but don't provide a
            # boundary and just send a single frame in the body - yield as is.
            yield Part(self.content, split_header=False)
            return
        message = b""
        delimiter = f"\r\n--{boundary}".encode()
        preamble = True
        with self:
            for chunk in self.iter_content(**kwargs):
                message += chunk
                if preamble and delimiter[2:] in message:
                    _, message = message.split(delimiter[2:], maxsplit=1)
                    preamble = False
                while delimiter in message:
                    content, message = message.split(delimiter, maxsplit=1)
                    yield Part(content)
        if not message.startswith(b"--"):
            warnings.warn("Last boundary is not a closing delimiter")

    def json(self, **kwargs):
        """Return loaded JSON response with attribute access enabled."""
        try:
            return attrify(super().json(**kwargs))
        except orjson.JSONDecodeError:
            message = f"Invalid JSON: {truncate(self.content, 20)}"
            # TODO switch to exceptions.InvalidJSONError when available
            # raise InvalidJSONError(message, response=self) from None
            raise ValueError(message) from None

    def raise_for_status(self) -> None:
        """Raise ClientError for 4xx / ServerError for 5xx responses."""
        try:
            super().raise_for_status()
        except exceptions.HTTPError as exc:
            exc.__class__ = ClientError if self.status_code < 500 else ServerError
            raise


class Part:
    """Single part of a multipart message with it's own headers and content."""

    def __init__(self, content: bytes, split_header: bool = True) -> None:
        """Initialize message part instance with headers and content."""
        if not split_header:
            headers = None
        elif b"\r\n\r\n" not in content:
            raise ValueError("Message part does not contain CRLF CRLF")
        else:
            header, content = content.split(b"\r\n\r\n", maxsplit=1)
            headers = email.parser.HeaderParser().parsestr(header.decode()).items()
        self.headers = CaseInsensitiveDict(headers or {})
        self.content = content


class ClientError(exceptions.HTTPError):
    """The server returned a response with 4xx status."""


class ServerError(exceptions.HTTPError):
    """The server returned a response with 5xx status."""


def request_exception_getattr(self, name: str):
    """Proxy the response and the request attributes for convenience."""
    try:
        return getattr(self.response, name)
    except AttributeError:
        pass
    try:
        return getattr(self.request, name)
    except AttributeError:
        pass
    raise AttributeError(f"{type(self).__name__} has no attribute {name!r}")


def request_exception_str(self) -> str:
    """Return the string representation of a RequestException."""
    return f"{self.method} {self.url} - {self.args[0]}"  # pragma: no cover


def connection_error_str(self) -> str:
    """Return the string representation of a ConnectionError."""
    msg = str(self.args[0])
    if "Errno" in msg:
        msg = re.sub(r".*(\[[^']*).*", r"\1", msg)
    if "read timeout" in msg:
        msg = re.sub(r'.*: ([^"]*).*', r"\1", msg)
    return f"{self.method} {self.url} - {msg}"


def http_error_str(self) -> str:
    """Return the string representation of an HTTPError."""
    msg = f"{self.method} {self.url} - {self.status_code} {self.reason}"
    # capture the request body we sent
    if request_body := truncate(self.body):
        join = "\n" if "\n" in request_body else " "
        msg += f"\nRequest:{join}{request_body}"
    # add anything the server had to say about the problem
    if response_content := truncate(self.content):
        join = "\n" if "\n" in response_content else " "
        msg += f"\nResponse:{join}{response_content}"
    return msg


def truncate(data: t.Optional[bytes], max_length: int = 256) -> str:
    """Return bytes truncated to the specified length as a string."""
    if not data:
        return ""
    data = data.rstrip()
    if len(data) > max_length:
        data = data[: max_length - 3].rstrip() + b"..."
    try:
        return data.decode()
    except UnicodeDecodeError:  # pragma: no cover
        return str(data)


# patch for performance - use orjson for loading and dumping
requests.models.complexjson = orjson  # type: ignore

# patch the exceptions for more useful default error messages
exceptions.RequestException.__getattr__ = request_exception_getattr  # type: ignore
exceptions.RequestException.__str__ = request_exception_str  # type: ignore
exceptions.ConnectionError.__str__ = connection_error_str  # type: ignore
exceptions.HTTPError.__str__ = http_error_str  # type: ignore

# convenience accessor for the available exceptions
errors = AttrDict(
    RequestException=exceptions.RequestException,
    ConnectionError=exceptions.ConnectionError,
    HttpError=exceptions.HTTPError,
    ClientError=ClientError,
    ServerError=ServerError,
)
