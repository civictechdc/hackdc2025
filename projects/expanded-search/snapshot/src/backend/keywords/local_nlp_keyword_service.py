from typing import List

import spacy

from src.backend.models.domain.docket import Docket


class LocalNLPKeywordService:
    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")

    def extract_keywords(self, dockets: List[Docket]) -> None:
        """Uses spaCy to extract keywords and key phrases from each docket's title and summary.
        Modifies the dockets in place and returns None.
        """
        for docket in dockets:
            text = f"{docket.title} {docket.summary}"
            doc = self.nlp(text)
            # Extract noun chunks and named entities as keywords/phrases
            keywords = set()
            keywords.update(chunk.text.lower() for chunk in doc.noun_chunks)
            keywords.update(ent.text.lower() for ent in doc.ents)
            docket.keywords = keywords
