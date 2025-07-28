import json
from typing import List

from src.backend.models.domain.docket import Docket


# TODO: Move services to a service folder

class DocketExtractionService:
    """Service for extracting dockets from a JSON file.
    """

    def load_dockets_from_json(self, path: str) -> List[Docket]:
        """Loads dockets from a JSON file and returns a list of Docket instances.
        """
        with open(path, encoding='utf-8') as f:
            print(f"Loading dockets from {path}")
            data = json.load(f)
        return [Docket(**item) for item in data]
