import imghdr
import time

import requests

from .errors import (ApiError, Banned, InvalidRtfsLibrary, InvalidToken,
                     MaxRetryReached, NotFound, TagAlreadyAssigned)
from .responses import (RTFMResponse, RTFSResponse, cdnresponse, cdnstats,
                        cdnupload, xkcdcomic, xkcdresponse)


class sync_client:
    def __init__(self, token: str=None, *, retry: int=5):
        self.token=token

        self.retry=int(retry)

        self.base_url="https://idevision.net/api/"

    def _request(self, method, url, **kwargs):
        headers = kwargs.pop("headers", {})

        if self.token: headers["Authorization"] = self.token
        
        if not headers: headers = None

        for _ in range(self.retry):
            with requests.request(method, url, headers=headers or None, **kwargs) as response:
                if response.status_code in [200, 201]:
                    try:
                        return response.json()
                    except:
                        return response
                elif response.status_code in [400, 500]:
                    raise ApiError(response.reason)
                elif response.status_code == 403:
                    raise Banned()
                elif response.status_code == 429:
                    wait = float(response.headers["ratelimit-retry-after"])
                    time.sleep(wait)
                    continue
                elif response.status_code == 401:
                    raise InvalidToken(response.reason)
                elif response.status_code == 404:
                    if method == "DELETE":
                        return response
                    raise NotFound

        raise MaxRetryReached(self.retry)

    def sphinxrtfm(self, location, query, *, show_labels=False, label_labels=False):
        response = self._request("GET", f"{self.base_url}public/rtfm.sphinx", params={"location": location, "query": query, "show-labels": "true" if show_labels else "false", "label-labels": "true" if label_labels else "false"})

        return RTFMResponse(response["nodes"], response["query_time"])

    def rustrtfm(self, crate, query):
        response = self._request("GET", f"{self.base_url}public/rtfm.rustdoc", params={"location": crate, "query": query})

        return RTFMResponse(response["nodes"], response["query_time"])

    def rtfs(self, library, query, *, source=False):
        if library == "dpy": library = "discord.py"
        if library == "dpy2": library = "discord.py-2"

        allowed = {"twitchio", "wavelink", "discord.py", "discord.py-2", "aiohttp"}

        if library not in allowed:
            raise InvalidRtfsLibrary(library, *allowed)

        response = self._request("GET", f"{self.base_url}public/rtfs", params={"library": library, "query": query, "format": "links" if not source else "source"})

        return RTFSResponse(response["nodes"], response["query_time"])

    def ocr(self, image, *, filetype=None):
        if not filetype:
            filetype = imghdr.what(image)

        response = self._request("GET", f"{self.base_url}public/ocr", params={"filetype": filetype}, data=image)

        return response["data"].strip()

    def xkcd(self, query):
        response = self._request("GET", f"{self.base_url}public/xkcd", params={"search": query})

        return xkcdresponse([xkcdcomic(node["num"], node["posted"], node["safe_title"], node["title"], node["alt"], node["transcript"], node["news"], node["image_url"], node["url"]) for node in response["nodes"]], response["query_time"])

    def xkcd_tag(self, tag, number):
        response = self._request("PUT", f"{self.base_url}public/xkcd/tags", json={"tag": tag, "num": number})

        if response.reason.startswith("Tag"):
            raise TagAlreadyAssigned(response.reason)

    def homepage(self, links):
        return self._request("POST", f"{self.base_url}homepage", json=links)
    
    def cdn(self, image, *, filetype=None):
        if not filetype:
            filetype = imghdr.what(image)

        response = self._request("POST", f"{self.base_url}cdn", headers={"File-Name": filetype}, data=image)
        
        return cdnresponse(response["url"], response["slug"], response["node"])
    
    def cdn_stats(self):
        response = self._request("GET", f"{self.base_url}cdn")

        return cdnstats(response["upload_count"], response["uploaded_today"], response["last_upload"])
    
    def cdn_get(self, node, slug):
        response = self._request("GET", f"{self.base_url}cdn/{node}/{slug}")
        
        return cdnupload(response["url"], response["timestamp"], response["author"], response["views"], response["node"], response["size"], response["expiry"])

    def cdn_delete(self, node, slug):
        return self._request("DELETE", f"{self.base_url}cdn/{node}/{slug}")