import asyncio
import imghdr

import aiohttp

from .errors import (ApiError, Banned, InvalidRtfsLibrary, InvalidToken,
                     MaxRetryReached, NotFound, TagAlreadyAssigned)
from .responses import (RTFMResponse, RTFSResponse, cdnresponse, cdnstats,
                        cdnupload, xkcdcomic, xkcdresponse)


class async_client:
    def __init__(self, token: str=None, *, retry: int=5):
        self.token=token

        self.retry=int(retry)

        self.base_url="https://idevision.net/api/"

    async def _request(self, method, url, **kwargs):
        headers = kwargs.pop("headers", {})

        if self.token: headers["Authorization"] = self.token
        
        if not headers: headers = None

        async with aiohttp.ClientSession() as cs:
            for _ in range(self.retry):
                async with cs.request(method, url, headers=headers or None, **kwargs) as response:
                    if response.status in [200, 201]:
                        try:
                            return await response.json()
                        except:
                            return response
                    elif response.status in [400, 500]:
                        raise ApiError(response.reason)
                    elif response.status == 403:
                        raise Banned()
                    elif response.status == 429:
                        wait = float(response.headers["ratelimit-retry-after"])
                        await asyncio.sleep(wait)
                        continue
                    elif response.status == 401:
                        raise InvalidToken(response.reason)
                    elif response.status == 404:
                        if method == "DELETE":
                            return response
                        raise NotFound

        raise MaxRetryReached(self.retry)

    async def sphinxrtfm(self, location, query, *, show_labels=False, label_labels=False):
        response = await self._request("GET", f"{self.base_url}public/rtfm.sphinx", params={"location": location, "query": query, "show-labels": "true" if show_labels else "false", "label-labels": "true" if label_labels else "false"})

        return RTFMResponse(response["nodes"], response["query_time"])

    async def rustrtfm(self, crate, query):
        response = await self._request("GET", f"{self.base_url}public/rtfm.rustdoc", params={"location": crate, "query": query})

        return RTFMResponse(response["nodes"], response["query_time"])

    async def rtfs(self, library, query, *, source=False):
        if library == "dpy": library = "discord.py"
        if library == "dpy2": library = "discord.py-2"

        allowed = {"twitchio", "wavelink", "discord.py", "discord.py-2", "aiohttp"}

        if library not in allowed:
            raise InvalidRtfsLibrary(library, *allowed)

        response = await self._request("GET", f"{self.base_url}public/rtfs", params={"library": library, "query": query, "format": "links" if not source else "source"})

        return RTFSResponse(response["nodes"], response["query_time"])

    async def ocr(self, image, *, filetype=None):
        if not filetype:
            filetype = imghdr.what(image)

        response = await self._request("GET", f"{self.base_url}public/ocr", params={"filetype": filetype}, data=image)

        return response["data"].strip()

    async def xkcd(self, query):
        response = await self._request("GET", f"{self.base_url}public/xkcd", params={"search": query})

        return xkcdresponse([xkcdcomic(node["num"], node["posted"], node["safe_title"], node["title"], node["alt"], node["transcript"], node["news"], node["image_url"], node["url"]) for node in response["nodes"]], response["query_time"])

    async def xkcd_tag(self, tag, number):
        response = await self._request("PUT", f"{self.base_url}public/xkcd/tags", json={"tag": tag, "num": number})

        if response.reason.startswith("Tag"):
            raise TagAlreadyAssigned(response.reason)

    async def homepage(self, links):
        response = await self._request("POST", f"{self.base_url}homepage", json=links)

        return response
    
    async def cdn(self, image, *, filetype=None):
        if not filetype:
            filetype = imghdr.what(image)

        response = await self._request("POST", f"{self.base_url}cdn", headers={"File-Name": filetype}, data=image)
        
        return cdnresponse(response["url"], response["slug"], response["node"])
    
    async def cdn_stats(self):
        response = await self._request("GET", f"{self.base_url}cdn")

        return cdnstats(response["upload_count"], response["uploaded_today"], response["last_upload"])
    
    async def cdn_get(self, node, slug):
        response = await self._request("GET", f"{self.base_url}cdn/{node}/{slug}")
        
        return cdnupload(response["url"], response["timestamp"], response["author"], response["views"], response["node"], response["size"], response["expiry"])

    async def cdn_delete(self, node, slug):
        response = await self._request("DELETE", f"{self.base_url}cdn/{node}/{slug}")
        
        return response

