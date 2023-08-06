# Necessary imports
import aiohttp
from .errors import *
from .objects import *
import requests
import random

class Client:
    """Represent a client

    Parameters
    ----------
    key (str): Your API authentication key.
    version (str) (optional): The version number of API. It is 3 by default set it to 2 if you want to use v2.
    Methods
    -------
    get_ai_response(message: str, lang: str = 'en', type: str = 'stable'): Get random AI response.
    get_image(type: str = 'any'): Get a random image.
    get_joke(type: str = 'any'): Get a random joke.
    close(): Closes the session.
    """
    def __init__(self, key: str, version: str = "3"):
        self.key = key
        self.version = version
        self.session = requests.Session()
        if version == "3":
            self.url = f"https://api.pgamerx.com/v3"
            self.session.headers.update({'x-api-key': self.key})
        elif version == "4":
            self.url = "https://api.pgamerx.com/beta"
            self.session.headers.update({'x-api-key': self.key})
        elif version == "2":
            self.url = "https://api.pgamerx.com"
        else:
            raise InvalidVersionError

    def get_joke(self, type: str = "any"):
        if self.version == "4":
            raise MethodNotSupported
        if type not in ["any", "dev", "spooky", "pun"]:
            raise InvalidTypeError

        try:
            if self.version == "3":
                r = self.session.get(f"{self.url}/joke/{type}")
            else:
                r = self.session.get(f"{self.url}/joke/{type}?api_key={self.key}")
            r_json = r.json()
        except Exception as exc:
            if isinstance(exc, aiohttp.InvalidURL):
                raise RateLimitError
            elif isinstance(exc, RuntimeError):
                raise ClientClosedError
            else:
                raise exc

        if r.status_code == 200:
            if r_json["error"] is False:
                return Joke(r_json)
            else:
                raise HTTPError
        elif r.status_code == 401:
            raise AuthError(Exception)
        else:
            raise HTTPError

    def get_ai_response(self, message: str, type: str = "stable", lang: str = "en", unique_id: str = "", dev_name: str = "", bot_name: str = ""):
        if type not in ["stable", "unstable"]:
            raise InvalidTypeError

        try:
            if self.version == "4":
                r = self.session.get(f"{self.url}/ai?message={message}&type={type}&language={lang}&uid={unique_id}&master={dev_name}&bot={bot_name}")
                if r.status_code == 200:
                    r_json = r.json()
                    return r_json["message"]
                elif r.status_code in [401, 403]:
                    raise AuthError
                else:
                    raise HTTPError
            elif self.version == "3":
                r = self.session.get(f"{self.url}/ai/response?message={message}&type={type}&language={lang}&unique_id={unique_id}&dev_name={dev_name}&bot_name={bot_name}")
                r_json = r.json()
                if r.status_code == 200:
                    if r_json[0]["success"] is True:
                        return r_json[0]["message"]
                    else:
                        raise HTTPError
                elif r.status_code == 401:
                    raise AuthError(Exception)
                else:
                    raise HTTPError
            elif self.version == "2":
                r = self.session.get(f"{self.url}/ai/response?message={message}&type={type}&language={lang}&unique_id={unique_id}&dev_name={dev_name}&bot_name={bot_name}&api_key={self.key}")
                r_json = r.json()
                if len(r_json) == 1:
                    return r_json[0]
                else:
                    raise HTTPError
        except Exception as exc:
            if isinstance(exc, aiohttp.InvalidURL):
                raise RateLimitError
            elif isinstance(exc, RuntimeError):
                raise ClientClosedError
            else:
                raise exc

    def get_image(self, type: str = "any"):
        if self.version == "4":
            raise MethodNotSupported
        if type == "any":
            type = random.choice(["aww", "duck", "dog", "cat", "memes", "dankmemes", "holup", "art", "harrypottermemes", "facepalm"])
        elif type not in ["aww", "duck", "dog", "cat", "memes", "dankmemes", "holup", "art", "harrypottermemes", "facepalm"]:
            raise InvalidTypeError

        try:
            if self.version == "3":
                r = self.session.get(f"{self.url}/image/{type}")
            else:
                r = self.session.get(f"{self.url}/image/{type}?api_key={self.key}")
        except Exception as exc:
            if isinstance(exc, aiohttp.InvalidURL):
                raise RateLimitError
            elif isinstance(exc, RuntimeError):
                raise ClientClosedError
            else:
                raise exc

        if r.status_code == 200:
            data = r.json()
            img = self.session.get(data[0])
            content = img.content
            return Image(content, data[0])
        elif r.status_code == 401:
            raise AuthError(Exception)
        else:
            raise HTTPError

    def close(self):
        self.session.close()

class AsyncClient:
    """Represent an async client. This is same as `prsaw2.Client` but is suitable for async programs.

    Parameters
    ----------
    key (str): Your API authentication key.
    version (str) (optional): The version number of API. It is 3 by default set it to 2 if you want to use v2.
    Methods
    -------
    async get_ai_response(message: str, lang: str = 'en', type: str = 'stable'): Get random AI response.
    async get_image(type: str = 'any'): Get a random image.
    async get_joke(type: str = 'any'): Get a random joke.
    async close(): Closes the session.
    """
    def __init__(self, key: str, version: str = "3"):
        self.key = key
        self.version = version
        self.session = aiohttp.ClientSession(headers={'x-api-key': self.key})
        if version == "3":
            self.url = f"https://api.pgamerx.com/v3"
            self.session.headers.update({'x-api-key': self.key})
        elif version == "4":
            self.url = "https://api.pgamerx.com/beta"
            self.session.headers.update({'x-api-key': self.key})
        elif version == "2":
            self.url = "https://api.pgamerx.com"
        else:
            raise InvalidVersionError

    async def get_joke(self, type: str = "any"):
        if self.version == "4":
            raise MethodNotSupported
        if type not in ["any", "dev", "spooky", "pun"]:
            raise InvalidTypeError

        try:
            if self.version == "3":
                r = await self.session.get(f"{self.url}/joke/{type}")
            else:
                r = await self.session.get(f"{self.url}/joke/{type}?api_key={self.key}")
            r_json = await r.json()
        except Exception as exc:
            if isinstance(exc, aiohttp.InvalidURL):
                raise RateLimitError
            elif isinstance(exc, RuntimeError):
                raise ClientClosedError
            else:
                raise exc

        if r.status == 200:
            if r_json["error"] is False:
                return Joke(r_json)
            else:
                raise HTTPError
        elif r.status == 401:
            raise AuthError(Exception)
        else:
            raise HTTPError

    async def get_ai_response(self, message: str, type: str = "stable", lang: str = "en", unique_id: str = "", dev_name: str = "", bot_name: str = ""):
        if type not in ["stable", "unstable"]:
            raise InvalidTypeError

        try:
            if self.version == "4":
                r = await self.session.get(f"{self.url}/ai?message={message}&type={type}&language={lang}&uid={unique_id}&master={dev_name}&bot={bot_name}")
                if r.status == 200:
                    r_json = await r.json()
                    return r_json["message"]
                elif r.status in [401, 403]:
                    raise AuthError
                else:
                    raise HTTPError
            elif self.version == "3":
                r = await self.session.get(f"{self.url}/ai/response?message={message}&type={type}&language={lang}&unique_id={unique_id}&dev_name={dev_name}&bot_name={bot_name}")
                r_json = await r.json()
                if r.status == 200:
                    if r_json[0]["success"] is True:
                        return r_json[0]["message"]
                    else:
                        raise HTTPError
                elif r.status == 401:
                    raise AuthError(Exception)
                else:
                    raise HTTPError
            elif self.version == "2":
                r = await self.session.get(f"{self.url}/ai/response?message={message}&type={type}&language={lang}&unique_id={unique_id}&dev_name={dev_name}&bot_name={bot_name}&api_key={self.key}")
                r_json = await r.json()
                if len(r_json) == 1:
                    return r_json[0]
                else:
                    raise HTTPError
        except Exception as exc:
            if isinstance(exc, aiohttp.InvalidURL):
                raise RateLimitError
            elif isinstance(exc, RuntimeError):
                raise ClientClosedError
            else:
                raise exc

    async def get_image(self, type: str = "any"):
        if self.version == "4":
            raise MethodNotSupported
        if type == "any":
            type = random.choice(["aww", "duck", "dog", "cat", "memes", "dankmemes", "holup", "art", "harrypottermemes", "facepalm"])
        elif type not in ["aww", "duck", "dog", "cat", "memes", "dankmemes", "holup", "art", "harrypottermemes", "facepalm"]:
            raise InvalidTypeError

        try:
            if self.version == "3":
                r = await self.session.get(f"{self.url}/image/{type}")
            else:
                r = await self.session.get(f"{self.url}/image/{type}?api_key={self.key}")
        except Exception as exc:
            if isinstance(exc, aiohttp.InvalidURL):
                raise RateLimitError
            elif isinstance(exc, RuntimeError):
                raise ClientClosedError
            else:
                raise exc

        if r.status == 200:
            data = await r.json()
            img = await self.session.get(data[0])
            content = await img.read()
            return Image(content, data[0])
        elif r.status == 401:
            raise AuthError(Exception)
        else:
            raise HTTPError

    async def close(self):
        await self.session.close()
