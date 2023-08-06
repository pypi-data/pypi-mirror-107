# encoding: utf-8


import collections
import operator
from typing import Dict, List, Any, Optional, Union

import numpy as np
import tqdm
from tensorflow.keras.preprocessing.sequence import pad_sequences

from nlp_tools.generators import CorpusGenerator
from nlp_tools.logger import logger
from nlp_tools.processors.abc_processor import ABCProcessor
from nlp_tools.types import TextSamplesVar


class SequenceProcessor(ABCProcessor):
    """
    Generic processors for the sequence samples.
    """

    def to_dict(self) -> Dict[str, Any]:
        data = super(SequenceProcessor, self).to_dict()
        data['config'].update({
            'build_in_vocab': self.build_in_vocab,
            'min_count': self.min_count
        })
        return data

    def __init__(self,
                 build_in_vocab: str = 'text',
                 min_count: int = 3,
                 build_vocab_from_labels: bool = False,
                 **kwargs: Any) -> None:
        """

        Args:
            vocab_dict_type: initial vocab dict type, one of `text` `labeling`.
            **kwargs:
        """
        super(SequenceProcessor, self).__init__(**kwargs)

        self.build_in_vocab = build_in_vocab
        self.min_count = min_count
        self.build_vocab_from_labels = build_vocab_from_labels

        if build_in_vocab == 'text':
            self._initial_vocab_dic = {
                self.token_pad: 0,
                self.token_unk: 1,
                self.token_bos: 2,
                self.token_eos: 3
            }
        elif build_in_vocab == 'labeling':
            self._initial_vocab_dic = {
                self.token_pad: 0
            }
        else:
            self._initial_vocab_dic = {}




        self._showed_seq_len_warning = False

    def build_vocab_generator(self,
                              generators: List[CorpusGenerator]) -> None:
        if not self.vocab2idx:
            vocab2idx = self._initial_vocab_dic
            token2count: Dict[str, int] = {}
            for gen in generators:
                for sentence, label in tqdm.tqdm(gen, desc="Preparing text vocab dict"):
                    if self.build_vocab_from_labels:
                        target = label
                    else:
                        target = sentence
                    target = self.text_tokenizer.tokenize(target)

                    if type(target) == list:
                        for token in target:
                            count = token2count.get(token, 0)
                            token2count[token] = count + 1
                    elif type(target) == str:
                        count = token2count.get(target, 0)
                        token2count[target] = count + 1
            sorted_token2count = sorted(token2count.items(),
                                        key=operator.itemgetter(1),
                                        reverse=True)
            token2count = collections.OrderedDict(sorted_token2count)

            for token, token_count in token2count.items():
                if token not in vocab2idx and token_count >= self.min_count:
                    vocab2idx[token] = len(vocab2idx)
            self.vocab2idx = vocab2idx
            self.idx2vocab = dict([(v, k) for k, v in self.vocab2idx.items()])

            top_k_vocab = [k for (k, v) in list(self.vocab2idx.items())[:10]]
            logger.debug(f"--- Build vocab dict finished, Total: {len(self.vocab2idx)} ---")
            logger.debug(f"Top-10: {top_k_vocab}")

    def transform(self,
                  samples: TextSamplesVar,
                  *,
                  seq_length: int = None,
                  max_position: int = None,
                  segment: bool = True) -> np.ndarray:
        seq_length_from = ""

        # An ugly patch for tf-serving use case.
        if seq_length is None and self._sequence_length_from_saved_model is not None:
            seq_length = self._sequence_length_from_saved_model

        if seq_length is None:
            seq_length_from = "max length of the samples"
            seq_length = max([len(i) for i in samples]) + 2
        if max_position is not None and max_position < seq_length:
            seq_length_from = "max embedding seq length"
            seq_length = max_position

        if seq_length_from and not self._showed_seq_len_warning:
            logger.warning(
                f'Sequence length is None, will use the {seq_length_from}, which is {seq_length}')
            self._showed_seq_len_warning = True

        numerized_samples = []
        for seq in samples:
            if self.token_bos in self.vocab2idx:
                seq = [self.token_bos] + seq + [self.token_eos]
            else:
                seq = [self.token_pad] + seq + [self.token_pad]
            if self.token_unk in self.vocab2idx:
                unk_index = self.vocab2idx[self.token_unk]
                numerized_samples.append([self.vocab2idx.get(token, unk_index) for token in seq])
            else:
                numerized_samples.append([self.vocab2idx[token] for token in seq])

        sample_index = pad_sequences(numerized_samples, seq_length, padding='post', truncating='post')
        token_ids = np.array(sample_index)

        if segment:
            segment_ids = np.zeros(token_ids.shape, dtype=np.int32)
            return token_ids, segment_ids
        else:
            return token_ids

    def inverse_transform(self,  # type: ignore[override]
                          labels: Union[List[List[int]], np.ndarray],
                          *,
                          lengths: List[int] = None,
                          threshold: float = 0.5,
                          **kwargs: Any) -> List[List[str]]:
        result = []
        for index, seq in enumerate(labels):
            labels_ = []
            for idx in seq:
                labels_.append(self.idx2vocab[idx])
            if lengths is not None:
                labels_ = labels_[1:lengths[index] + 1]
            else:
                labels_ = labels_[1:-1]
            result.append(labels_)
        return result

    def get_max_seq_length_from_corpus(self,
                                   generators: List[CorpusGenerator],
                                   *,
                                   use_label: bool = False,
                                   cover_rate: float = 0.95) -> int:
        """
        Calculate proper sequence length according to the corpus

        Args:
            generators:
            use_label:
            cover_rate:

        Returns:

        """
        seq_lens = []
        for gen in generators:
            for sentence, label in tqdm.tqdm(gen, desc="Calculating sequence length"):
                if use_label:
                    seq_lens.append(len(label))
                else:
                    seq_lens.append(len(sentence))
        if cover_rate == 1.0:
            target_index = -1
        else:
            target_index = int(cover_rate * len(seq_lens))
        sequence_length = sorted(seq_lens)[target_index]
        logger.debug(f'Calculated sequence length = {sequence_length}')
        return sequence_length



if __name__ == "__main__":
    pass
