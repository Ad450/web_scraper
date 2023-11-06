from typing import Dict
from abc import abstractmethod, ABC


# This is a base class for all page observers
# All page observers must implement this interface
class PageObserver(ABC):
    hashes: Dict[str, any]

    def __init__(self, hashes: Dict[str, any]) -> None:
        super().__init__()
        self.hashes = hashes

    @abstractmethod
    def compute_hash(self, **Kwargs: any) -> None:
        pass

    @abstractmethod
    def save_hash_to_db(self) -> None:
        pass

    @abstractmethod
    def compare_hashes(self) -> None:
        pass
