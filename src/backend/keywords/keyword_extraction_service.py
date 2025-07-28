import re
from typing import List

from src.backend.models.domain.docket import Docket


class KeywordExtractionService:
    """Service for extracting keywords from dockets."""

    def extract_keywords(self, dockets: List[Docket]) -> None:
        """Extracts keywords from each docket's title and summary and sets them in the docket's keywords field.
        Modifies the dockets in place and returns None.
        """
        for docket in dockets:
            words = self._get_all_words(docket)
            docket.keywords = list(words)

    def _get_all_words(self, docket: Docket) -> set[str]:
        """Returns a set of all unique words from the titles and summaries of the dockets.
        """
        all_words: set[str] = set()
        text = f"{docket.title} {docket.summary}"
        words = re.findall(r'\b\w+\b', text.lower())
        all_words.update(words)
        return all_words

