__title__ = 'aminonf'
__author__ = 'NfrXDRA'
__license__ = 'MIT'
__version__ = '1.2'
from requests import get
from json import loads

__newest__ = loads(get("https://pypi.python.org/pypi/splaxm/json").text)["info"]["version"]

if __version__ != __newest__:
	print(f"New version of {__title__} available: {__newest__} (Using {__version__})")
print("this library make by NfrXDRA\n\n")