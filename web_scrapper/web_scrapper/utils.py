from typing import Dict

headers: Dict[str, str] = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:98.0) Gecko/20100101 Firefox/98.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-User": "?1",
    "Cache-Control": "max-age=0",
}

amazon_url: str = """ https://www.amazon.com/s?k=amazon+shopping+online+website&adgrpid=152
        753934915&hvadid=673397238237&hvdev=c&hvlocphy=
        9070372&hvnetw=g&hvqmt=b&hvrand=9675813140351476259&hvtargid=kwd-1283712009298&hydadcr
        =22394_13507777&tag=hydglogoo-20&ref=pd_sl_42mumgtcax_b
        """

GHANA_JOBS_URL: str = "https://www.ghanajob.com/"


class ContentNotFoundException(Exception):
    def __init__(self, *args: object, message: str) -> None:
        super().__init__(*args)
        self.message = message
