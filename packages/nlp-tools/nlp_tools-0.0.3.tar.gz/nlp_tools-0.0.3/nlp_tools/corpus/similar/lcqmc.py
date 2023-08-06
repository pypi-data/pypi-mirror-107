from typing import Tuple, List
from nlp_tools import macros as k
import os
from nlp_tools.corpus import DataReader
from nlp_tools import utils
import logging
import json



class LCQMC(object):
    __corpus_name__ = 'lcqmc'

    @classmethod
    def load_data(cls,
                  file_path: str ,
                  shuffle: bool = True) -> Tuple[List[List[str]], List[List[str]]]:
        """
                Load dataset as sequence labeling format, char level tokenized

                features: ``[['海', '钓', '比', '赛', '地', '点', '在', '厦', '门', ...], ...]``

                labels: ``[[海', '钓', '比', '赛', '地', '点', , ...], ...]``

                Args:
                    file_path: file ablsute path
                    shuffle: should shuffle or not, default True.

                Returns:
                    dataset_features and dataset labels
                """
        x_data = []
        y_data = []
        with open(file_path,'r',encoding='utf-8') as fread:
            for index, line in enumerate(fread):
                x1,x2,label = line.strip().split("\t")
                x_data.append([x1,x2])
                y_data.append(label)

        if shuffle:
            x_data, y_data = utils.unison_shuffled_copies(x_data, y_data)
        logging.debug(f"loaded {len(x_data)} samples from {file_path}. Sample:\n"
                      f"x[0]: {x_data[0]}\n"
                      f"y[0]: {y_data[0]}")
        return x_data, y_data

if __name__ == "__main__":
    data_path =r'F:\nlp_data\similary\lcqmc\dev.txt'
    a, b = LCQMC.load_data(data_path)
    print(a[:2])
    print(b[:2])
    print("Hello world")