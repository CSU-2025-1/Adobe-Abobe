import aiohttp

_session = None


async def get_session() -> aiohttp.ClientSession:
    global _session
    if _session is None or _session.closed:
        conn = aiohttp.TCPConnector(limit=100, limit_per_host=50)
        _session = aiohttp.ClientSession(connector=conn)
    return _session
