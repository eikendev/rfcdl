import aiohttp
import asyncio
import logging
import random
import re
import requests

from .document import RFCDocument
from .util import clean_string, fetch_save

logger = logging.getLogger("rfcdl")


class RfcDownloader():
    URL_INDEX = "https://www.rfc-editor.org/rfc-index.txt"
    URL_RFC = "https://www.rfc-editor.org/rfc/rfc{number}.txt"
    PAT_DOCUMENT = (r"\n(\d{4}) (?!Not Issued).*?\(Format:(.*?)\)"
                    r".*?\(Status:([A-Z \n]+)\).*?\(DOI:(.*?)\)")

    def __init__(self, path, samples: int, limit: int, retries: int):
        if retries <= 0:
            raise ValueError("retries must be positive.")

        self.path = path
        self.samples = samples
        self.limit = limit
        self.retries = retries

        raw_list = self._fetch_list()
        self.documents = self._parse_documents(raw_list)

    def download(self, delete_obsolete=False):
        new_docs = {x.number for x in self.documents if not x.is_obsolete}

        obsolete_docs = len(self.documents) - len(new_docs)
        msg = "Filtering out {} obsolete documents."
        logger.debug(msg.format(obsolete_docs))

        old_docs = {x.stem for x in self.path.iterdir() if x.is_file()}

        to_remove = old_docs - new_docs
        msg = "Detected {} obsolete documents in {}."
        logger.info(msg.format(len(to_remove), self.path))

        # Remove old docs not included in new docs.
        if delete_obsolete:
            for fn in to_remove:
                name = fn + ".txt"
                f = self.path / name
                logger.info("Remove obsolete file: '%s'.", f)
                f.unlink()

        # Download new docs not included in old docs.
        to_add = new_docs - old_docs

        if self.samples > 0:
            msg = "Generating random sample of {} documents."
            logger.debug(msg.format(self.samples))
            to_add = random.sample(to_add, k=self.samples)

        msg = "Downloading {} files."
        logger.info(msg.format(len(to_add)))

        loop = asyncio.get_event_loop()
        func = self._download(to_add)
        loop.run_until_complete(func)
        loop.close()

    async def _download(self, docs):
        def init_task(session, doc):
            doc_int = int(doc)
            url = self.URL_RFC.format(number=doc_int)
            name = doc + ".txt"
            f = self.path / name

            task = fetch_save(session, url, f, retries=self.retries)
            return task

        connector = aiohttp.TCPConnector(limit=self.limit)

        async with aiohttp.ClientSession(connector=connector) as session:
            tasks = [init_task(session, doc) for doc in docs]
            results = await asyncio.gather(*tasks)

        logger.debug(results)

        dl_successful = results.count(True)
        dl_rate = dl_successful / float(len(results))
        msg = "total: {}, successful: {}, rate: {}"
        logger.info(msg.format(len(results), dl_successful, dl_rate))

    def _fetch_list(self):
        page = requests.get(self.URL_INDEX)

        return page.text

    def _parse_documents(self, raw_list):
        documents = set()

        document_pattern = re.compile(self.PAT_DOCUMENT, re.DOTALL)
        scan = re.finditer(document_pattern, raw_list)

        for match in scan:
            number = clean_string(match.group(1))
            format = clean_string(match.group(2))
            status = clean_string(match.group(3))
            doi = clean_string(match.group(4))

            match_str = clean_string(match.group(0).lower())
            is_obsolete = "obsoleted by" in match_str

            doc = RFCDocument(number, format, status, doi,
                              is_obsolete=is_obsolete)
            documents.add(doc)

        msg = "Parsed {} messages.".format(len(documents))
        logger.info(msg)

        return documents
