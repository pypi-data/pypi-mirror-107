from typing import Dict,Any
from abc import ABC, abstractmethod
class ABCTokenizer(ABC):
    """Abstract base class for all implemented tokenizers.
    """

    def to_dict(self) -> Dict[str, Any]:
        return {
            '__class_name__': self.__class__.__name__,
            '__module__': self.__class__.__module__,
            'config':{}
        }

    def tokenize(self, text: str):
        """
        Tokenize text into token sequence
        Args:
            text: target text sample

        Returns:
            List of tokens in this sample
        """
        raise NotImplementedError

    def encode(self,text,**kwargs):
        raise NotImplementedError

