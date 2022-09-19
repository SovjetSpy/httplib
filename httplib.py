from dataclasses import dataclass, field
from datetime import datetime
import socket
import os

DELIM = '\r\n'

CODES = {
    100: 'Continue',
    101: 'Switching Protocols',
    102: 'Processing',
    103: 'Early Hints',
    200: 'OK',
    201: 'Created',
    202: 'Accepted',
    203: 'Non-Authoritative Information',
    204: 'No Content',
    205: 'Reset Content',
    206: 'Partial Content',
    207: 'Multi-Status',
    208: 'Already Reported',
    226: 'IM Used',
    300: 'Multiple Choices',
    301: 'Moved Permanently',
    302: 'Found',
    303: 'See Other',
    304: 'Not Modified',
    305: 'Use Proxy',
    307: 'Temporary Redirect',
    308: 'Permanent Redirect',
    400: 'Bad Request',
    401: 'Unauthorized',
    402: 'Payment Required	',
    403: 'Forbidden',
    404: 'Not Found',
    405: 'Method Not Allowed',
    406: 'Not Acceptable',
    407: 'Proxy Authentication Required',
    408: 'Request Timeout',
    409: 'Conflict',
    410: 'Gone',
    411: 'Length Required',
    412: 'Precondition Failed',
    413: 'Content Too Large',
    414: 'URI Too Long',
    415: 'Unsupported Media Type',
    416: 'Range Not Satisfiable',
    417: 'Expectation Failed',
    421: 'Misdirected Request',
    422: 'Unprocessable Content',
    423: 'Locked',
    424: 'Failed Dependency',
    425: 'Too Early',
    426: 'Upgrade Required',
    428: 'Precondition Required',
    429: 'Too Many Requests',
    431: 'Request Header Fields Too Large',
    451: 'Unavailable For Legal Reasons',
    500: 'Internal Server Error',
    501: 'Not Implemented',
    502: 'Bad Gateway',
    503: 'Service Unavailable',
    504: 'Gateway Timeout',
    505: 'HTTP Version Not Supported',
    506: 'Variant Also Negotiates',
    507: 'Insufficient Storage',
    508: 'Loop Detected',
    510: 'Not Extended',
    511: 'Network Authentication Required'
}

FILE_EXTENSIONS = {
    "evy": "application/envoy",
    "fif": "application/fractals",
    "spl": "application/futuresplash",
    "hta": "application/hta",
    "acx": "application/internet-property-stream",
    "hqx": "application/mac-binhex40",
    "doc": "application/msword",
    "dot": "application/msword",
    "bin": "application/octet-stream",
    "class": "application/octet-stream",
    "dms": "application/octet-stream",
    "exe": "application/octet-stream",
    "lha": "application/octet-stream",
    "lzh": "application/octet-stream",
    "oda": "application/oda",
    "axs": "application/olescript",
    "pdf": "application/pdf",
    "prf": "application/pics-rules",
    "p10": "application/pkcs10",
    "crl": "application/pkix-crl",
    "ai": "application/postscript",
    "eps": "application/postscript",
    "ps": "application/postscript",
    "rtf": "application/rtf",
    "setpay": "application/set-payment-initiation",
    "setreg": "application/set-registration-initiation",
    "xlc": "application/vnd.ms-excel",
    "xlm": "application/vnd.ms-excel",
    "xls": "application/vnd.ms-excel",
    "xlt": "application/vnd.ms-excel",
    "xlw": "application/vnd.ms-excel",
    "xla": "application/vnd.ms-excel",
    "msg": "application/vnd.ms-outlook",
    "sst": "application/vnd.ms-pkicertstore",
    "cat": "application/vnd.ms-pkiseccat",
    "stl": "application/vnd.ms-pkistl",
    "pot": "application/vnd.ms-powerpoint",
    "pps": "application/vnd.ms-powerpoint",
    "ppt": "application/vnd.ms-powerpoint",
    "mpp": "application/vnd.ms-project",
    "wcm": "application/vnd.ms-works",
    "wdb": "application/vnd.ms-works",
    "wks": "application/vnd.ms-works",
    "wps": "application/vnd.ms-works",
    "hlp": "application/winhlp",
    "bcpio": "application/x-bcpio",
    "cdf": "application/x-cdf",
    "z": "application/x-compress",
    "tgz": "application/x-compressed",
    "cpio": "application/x-cpio",
    "csh": "application/x-csh",
    "dcr": "application/x-director",
    "dir": "application/x-director",
    "dxr": "application/x-director",
    "dvi": "application/x-dvi",
    "gtar": "application/x-gtar",
    "gz": "application/x-gzip",
    "hdf": "application/x-hdf",
    "ins": "application/x-internet-signup",
    "isp": "application/x-internet-signup",
    "iii": "application/x-iphone",
    "js": "application/x-javascript",
    "latex": "application/x-latex",
    "mdb": "application/x-msaccess",
    "crd": "application/x-mscardfile",
    "clp": "application/x-msclip",
    "dll": "application/x-msdownload",
    "m13": "application/x-msmediaview",
    "m14": "application/x-msmediaview",
    "mvb": "application/x-msmediaview",
    "wmf": "application/x-msmetafile",
    "mny": "application/x-msmoney",
    "pub": "application/x-mspublisher",
    "scd": "application/x-msschedule",
    "trm": "application/x-msterminal",
    "wri": "application/x-mswrite",
    "nc": "application/x-netcdf",
    "pma": "application/x-perfmon",
    "pmc": "application/x-perfmon",
    "pml": "application/x-perfmon",
    "pmr": "application/x-perfmon",
    "pmw": "application/x-perfmon",
    "p12": "application/x-pkcs12",
    "pfx": "application/x-pkcs12",
    "p7b": "application/x-pkcs7-certificates",
    "spc": "application/x-pkcs7-certificates",
    "p7r": "application/x-pkcs7-certreqresp",
    "p7c": "application/x-pkcs7-mime",
    "p7m": "application/x-pkcs7-mime",
    "p7s": "application/x-pkcs7-signature",
    "sh": "application/x-sh",
    "shar": "application/x-shar",
    "swf": "application/x-shockwave-flash",
    "sit": "application/x-stuffit",
    "sv4cpio": "application/x-sv4cpio",
    "sv4crc": "application/x-sv4crc",
    "tar": "application/x-tar",
    "tcl": "application/x-tcl",
    "tex": "application/x-tex",
    "texi": "application/x-texinfo",
    "texinfo": "application/x-texinfo",
    "roff": "application/x-troff",
    "t": "application/x-troff",
    "tr": "application/x-troff",
    "man": "application/x-troff-man",
    "me": "application/x-troff-me",
    "ms": "application/x-troff-ms",
    "ustar": "application/x-ustar",
    "src": "application/x-wais-source",
    "cer": "application/x-x509-ca-cert",
    "crt": "application/x-x509-ca-cert",
    "der": "application/x-x509-ca-cert",
    "pko": "application/ynd.ms-pkipko",
    "zip": "application/zip",
    "au": "audio/basic",
    "snd": "audio/basic",
    "mid": "audio/mid",
    "rmi": "audio/mid",
    "mp3": "audio/mpeg",
    "aif": "audio/x-aiff",
    "aifc": "audio/x-aiff",
    "aiff": "audio/x-aiff",
    "m3u": "audio/x-mpegurl",
    "ra": "audio/x-pn-realaudio",
    "ram": "audio/x-pn-realaudio",
    "wav": "audio/x-wav",
    "bmp": "image/bmp",
    "cod": "image/cis-cod",
    "gif": "image/gif",
    "ief": "image/ief",
    "jpe": "image/jpeg",
    "jpeg": "image/jpeg",
    "png": "image/png",
    "jpg": "image/jpeg",
    "jfif": "image/pipeg",
    "svg": "image/svg+xml",
    "tif": "image/tiff",
    "tiff": "image/tiff",
    "ras": "image/x-cmu-raster",
    "cmx": "image/x-cmx",
    "ico": "image/x-icon",
    "pnm": "image/x-portable-anymap",
    "pbm": "image/x-portable-bitmap",
    "pgm": "image/x-portable-graymap",
    "ppm": "image/x-portable-pixmap",
    "rgb": "image/x-rgb",
    "xbm": "image/x-xbitmap",
    "xpm": "image/x-xpixmap",
    "xwd": "image/x-xwindowdump",
    "mht": "message/rfc822",
    "mhtml": "message/rfc822",
    "nws": "message/rfc822",
    "css": "text/css",
    "323": "text/h323",
    "htm": "text/html",
    "html": "text/html",
    "stm": "text/html",
    "uls": "text/iuls",
    "bas": "text/plain",
    "c": "text/plain",
    "h": "text/plain",
    "txt": "text/plain",
    "rtx": "text/richtext",
    "sct": "text/scriptlet",
    "tsv": "text/tab-separated-values",
    "htt": "text/webviewhtml",
    "htc": "text/x-component",
    "etx": "text/x-setext",
    "vcf": "text/x-vcard",
    "mp2": "video/mpeg",
    "mpa": "video/mpeg",
    "mpe": "video/mpeg",
    "mpeg": "video/mpeg",
    "mpg": "video/mpeg",
    "mpv2": "video/mpeg",
    "mp4": "video/mp4",
    "mov": "video/quicktime",
    "qt": "video/quicktime",
    "lsf": "video/x-la-asf",
    "lsx": "video/x-la-asf",
    "asf": "video/x-ms-asf",
    "asr": "video/x-ms-asf",
    "asx": "video/x-ms-asf",
    "avi": "video/x-msvideo",
    "movie": "video/x-sgi-movie",
    "flr": "x-world/x-vrml",
    "vrml": "x-world/x-vrml",
    "wrl": "x-world/x-vrml",
    "wrz": "x-world/x-vrml",
    "xaf": "x-world/x-vrml",
    "xof": "x-world/x-vrml"
}

HAS_PAYLOAD_MAP = {
    "GET": False,
    "POST": True,
    "PUT": True,
    "DELETE": False
}

COOKIE_ATIBS = {
    'Path',
    'Max-Age',
    'Expires',
    'Domain',
    'SameSite',
    'Strict',
    'Lax',
    'HttpOnly'
}


@dataclass
class request_http_header:
    http_version: any = ("HTTP", 1.1)
    method: str = ''
    path: str = '/'
    fields: dict = field(default_factory=dict)
    cookies: dict = field(default_factory=dict)
    body: str = ''


@dataclass
class response_http_header:
    http_version: any = ("HTTP", 1.1)
    status: int = 200
    fields: dict = field(default_factory=dict)
    cookies: list = field(default_factory=list)
    body: bytes = b''


@dataclass
class cookie:
    name: str = ''
    value: any = ''
    Expration = None
    Max_Age = None
    Path = None


def cookie_to_string(c: cookie) -> str:
    s = c.name + '=' + c.value + '; '

    if c.Expration is not None:
        s += 'Expration=' + c.Expration + '; '

    if c.Path is not None:
        s += 'Path=' + c.Path + '; '

    if c.Max_Age is not None:
        s += 'Max-Age=' + c.Max_Age + '; '

    return s


def http_parser(text: str) -> request_http_header:
    header = request_http_header()

    info = text.split(DELIM)[0].split(' ')

    fields = text.split(DELIM)[1:]

    header.method = str(info[0])
    header.path = str(info[1])
    header.http_version = (
        str(info[2].split('/')[0]),
        float(info[2].split('/')[1])
    )

    for i in fields:
        if i == '':
            break

        key_val = i.split(": ")
        header.fields[key_val[0]] = key_val[1]

    return header


def decode_cookies(s: str) -> dict:
    ret = {}
    all_cookies = (
        (i.split('=')[0], i.split('=')[1])
        for i in s.split(": ")[1].rstrip(DELIM).split('; ')
        )
    current_cookie = ''
    for i in all_cookies:
        if not i[0] in COOKIE_ATIBS:
            current_cookie = i[0]
            ret[i[0]] = cookie(i[0], i[1])
        else:
            if 'Expration' == i[0]:
                ret[current_cookie].Experation = i[1]

            if 'Path' == i[0]:
                ret[current_cookie].path = i[1]

            if 'Max-Age' == i[0]:
                ret[current_cookie].Max_Age = i[1]
    return ret


def read_http(socket: socket.socket):
    try:
        osf = os.dup(socket.fileno())
        fd = os.fdopen(osf, 'rb')

        header = request_http_header()

        current = fd.readline().decode()

        has_payload = HAS_PAYLOAD_MAP.get(current.split(' ')[0])
        if (has_payload is None):
            return None

        header.method = current.split(' ')[0]
        header.path = current.split(' ')[1].rstrip(DELIM)

        current = fd.readline().decode()

        while (current != DELIM):
            if current.split(": ")[0] == 'Cookie':
                header.cookies = decode_cookies(current)
            header.fields[current.split(": ")[0]] = current.split(": ")[1].rstrip(DELIM)
            current = fd.readline().decode()

        if has_payload:
            length = int(header.fields['Content-Length'])

            header.body = fd.read(length)
    except Exception as _:
        return None

    return header


def send_plane_status(status: int, sock: socket.socket):
    server_header = response_http_header()
    server_header.status = status
    server_header.fields['Content-Type'] = 'text/plane'
    server_header.body = CODES[status].encode()

    sock.send(http_creator(server_header))


def path_to_contenttype(path: str) -> str:
    extension = path.split('.')[-1].lower()
    return FILE_EXTENSIONS[extension]


def http_creator(header: response_http_header) -> bytes:

    header.fields['Connection'] = 'close'
    header.fields['Content-Length'] = str(len(header.body))
    header.fields['Date'] = datetime.now().strftime('%a, %d %b %Y %H:%M:%S GMT')
    header.fields['Server'] = 'Joekkel_server'

    header_text: str = f'{header.http_version[0]}/{str(header.http_version[1])} \
                        {str(header.status)} {CODES[header.status]}{DELIM}'

    for k in header.fields:
        header_text += k + ": " + header.fields[k] + DELIM

    for i in header.cookies:
        header_text += 'Set-Cookie: ' + cookie_to_string(i) + DELIM

    header_text += DELIM

    return header_text.encode() + header.body
