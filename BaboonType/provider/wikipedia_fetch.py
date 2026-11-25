
from baboonmod.exceptions import PassageProviderError, UnsupportedPassageError
from baboonmod.passage import MAX_PASSAGE_WORDS, Passage
import requests

class WikipediaProvider:

    URL = "https://en.wikipedia.org/w/api.php"
    LICENSE_URL = "https://creativecommons.org/licenses/by-sa/4.0/"
    MAX_ATTEMPTS = 5

    def get_passage(self):

        for i in range(self.MAX_ATTEMPTS):

            try:
                return self._get_passage_once(requests)
            except UnsupportedPassageError:
                continue

        raise PassageProviderError(f"Wikipedia did not return an English-only passage after {self.MAX_ATTEMPTS} attempts.")

    def _get_passage_once(self, requests):
        headers = {
            "User-Agent": "TypingTest/1.0 pascalindromi@gmail.com"
        }

        params = {
            "action": "query",
            "generator": "random",
            "grnnamespace": 0,
            "grnlimit": 1,
            "prop": "extracts|info",
            "inprop": "url",
            "explaintext": 1,
            "exchars": 1200,
            "format": "json",
            "formatversion": 2
        }

        try:
            response = requests.get(
                self.URL,
                params=params,
                headers=headers,
                timeout=10
            )
            response.raise_for_status()
            data = response.json()

        except requests.RequestException as error:
            raise PassageProviderError(f"Wikipedia request failed: {error}")
        
        except ValueError:
            raise PassageProviderError("Wikipedia returned invalid JSON.")

        query = None
        pages = None

        if isinstance(data, dict):
            query = data.get("query")

        if isinstance(query, dict):
            pages = query.get("pages")

        if not isinstance(pages, list) or not pages or not isinstance(pages[0], dict):
            raise PassageProviderError("Wikipedia returned no usable article.")

        page = pages[0]
        extract = page.get("extract")
        title = page.get("title")
        source_url = page.get("fullurl")

        if not isinstance(extract, str) or not extract.strip():
            raise PassageProviderError("Wikipedia returned an empty article extract.")
        
        if not isinstance(title, str) or not title.strip():
            raise PassageProviderError("Wikipedia article is missing its title.")
        
        if not isinstance(source_url, str) or not source_url.startswith("https://en.wikipedia.org/wiki/"):
            raise PassageProviderError("Wikipedia article is missing a valid source URL.")

        content = " ".join(extract.split()[:MAX_PASSAGE_WORDS])

        try:
            return Passage(
                content=content,
                title=title,
                source_name="Wikipedia contributors",
                source_url=source_url,
                license_url=self.LICENSE_URL,
            )
        
        except UnsupportedPassageError:
            raise

        except ValueError as error:
            raise PassageProviderError(f"Wikipedia returned an unusable passage: {error}")
