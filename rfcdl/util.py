import aiofiles
import logging
import re

logger = logging.getLogger("rfcdl")


def clean_string(s):
    s = s.replace("\n", " ")
    s = re.sub(r"\s{2,}", " ", s)
    s = s.strip()

    return s


async def fetch_save(session, url, path, retries=5):
    success = False

    for _ in range(retries):
        async with session.get(url) as resp:
            if resp.status != 200:
                continue

            content = await resp.read()
            encoding = resp.charset if resp.charset else "ISO-8859-1"

        content = content.decode(encoding)

        msg = "Saving file '{}'."
        logger.info(msg.format(path))

        async with aiofiles.open(path, mode="w") as f:
            await f.write(content)

        success = True
        break

    if not success:
        msg = "Could not retrieve '{}'."
        logger.warning(msg.format(path))

    return success
