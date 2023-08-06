from abc import ABC
from typing import Dict,List,Optional,Any,Tuple
import numpy as np

from nlp_tools.generators import  CorpusGenerator
from nlp_tools.types import TextSamplesVar
from nlp_tools.tokenizer import ABCTokenizer,ListTokenizer,BertTokenizer,DoNothingTokenizer
from nlp_tools.utils import load_data_object


class ABCProcessor(ABC):
    def to_dict(self) -> Dict[str, Any]:
        return {
            'config': {
                'token_pad': self.token_pad,
                'token_unk': self.token_unk,
                'token_bos': self.token_bos,
                'token_eos': self.token_eos,
                'vocab2idx': self.vocab2idx,
                'segment': self.segment,

            },
            'text_tokenizer': self.text_tokenizer.to_dict(),

            '__class_name__': self.__class__.__name__,
            '__module__': self.__class__.__module__,
        }

    def __init__(self,text_tokenizer=None, **kwargs: Any) -> None:
        self.text_tokenizer: ABCTokenizer = text_tokenizer

        self.vocab2idx = kwargs.get('vocab2idx', {})
        if self.text_tokenizer == None:
            self.text_tokenizer = DoNothingTokenizer()
        elif type(text_tokenizer) == BertTokenizer:
            self.vocab2idx = text_tokenizer._token_dict
        self.idx2vocab = dict([(v, k) for k, v in self.vocab2idx.items()])


        self.segment = False

        self.token_pad: str = kwargs.get('token_pad', '[PAD]')  # type: ignore
        self.token_unk: str = kwargs.get('token_unk', '[UNK]')  # type: ignore
        self.token_bos: str = kwargs.get('token_bos', '[CLS]')  # type: ignore
        self.token_eos: str = kwargs.get('token_eos', '[SEP]')  # type: ignore

        self._sequence_length_from_saved_model: Optional[int] = None



    def _override_load_model(self,config:Dict) -> None:
        self.text_tokenizer: ABCTokenizer = load_data_object(config['text_tokenizer'])
        if hasattr(self.text_tokenizer,'_token_dict'):
            self.vocab2idx = self.text_tokenizer._token_dict
            self.idx2vocab = dict([(v, k) for k, v in self.vocab2idx.items()])

    @property
    def vocab_size(self) -> int:
        return len(self.vocab2idx)

    @property
    def is_vocab_build(self) -> bool:
        return self.vocab_size != 0

    def build_vocab(self,
                    x_data: TextSamplesVar,
                    y_data: TextSamplesVar) -> None:
        corpus_gen = CorpusGenerator(x_data, y_data)
        self.build_vocab_generator([corpus_gen])

    def build_vocab_generator(self,
                              generators: List[CorpusGenerator]) -> None:
        raise NotImplementedError

    def get_tensor_shape(self, batch_size: int, seq_length: int) -> Tuple:
        if self.segment:
            return 2, batch_size, seq_length
        else:
            return batch_size, seq_length

    def transform(self,
                  samples,
                  *,
                  seq_length: int = None,
                  max_position: int = None,
                  segment: bool = False) -> np.ndarray:
        raise NotImplementedError

    def inverse_transform(self,
                          labels: List[int],
                          *,
                          lengths: List[int] = None,
                          threshold: float = 0.5,
                          **kwargs: Any) -> List[str]:
        raise NotImplementedError


    def tokenize(self,text_or_list,**kwargs):
        if type(text_or_list) == str:
            return self.text_tokenizer.tokenize(text_or_list,**kwargs)
        elif type(text_or_list) == list:
            return [self.text_tokenizer.tokenize(text) for text in text_or_list]
        else:
            raise TypeError("存入参数有问题")
