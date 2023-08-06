from tensorflow.keras.utils import get_file
from typing import Tuple, List
from nlp_tools import macros as k
from nlp_tools.corpus import DataReader
from nlp_tools import utils

import logging
import os
import glob
from tqdm import tqdm
import json

class ChineseDailyNerCorpus(object):
    """
        Chinese Daily New New Corpus
        https://github.com/zjy-ucas/ChineseNER/
        """
    __corpus_name__ = 'china-people-daily-ner-corpus'
    __zip_file__name = 'http://s3.bmio.net/kashgari/china-people-daily-ner-corpus.tar.gz'
    @classmethod
    def load_data(cls,
                  subset_name:str = 'train',
                  shuffle:bool = True,
                  corpus_path = None) -> Tuple[List[List[str]],List[List[str]]]:
        """
                Load dataset as sequence labeling format, char level tokenized

                features: ``[['海', '钓', '比', '赛', '地', '点', '在', '厦', '门', ...], ...]``

                labels: ``[['O', 'O', 'O', 'O', 'O', 'O', 'O', 'B-LOC', 'I-LOC', ...], ...]``

                Sample::

                    train_x, train_y = ChineseDailyNerCorpus.load_data('train')
                    test_x, test_y = ChineseDailyNerCorpus.load_data('test')

                Args:
                    subset_name: {train, test, valid}
                    shuffle: should shuffle or not, default True.

                Returns:
                    dataset_features and dataset labels
                """
        if corpus_path == None:
            corpus_path = get_file(cls.__corpus_name__,
                                   cls.__zip_file__name,
                                   cache_dir=k.DATA_PATH,
                                   untar=True)
        if subset_name == 'train':
            file_path = os.path.join(corpus_path,'example.train')
        elif subset_name == 'test':
            file_path = os.path.join(corpus_path,'example.test')
        else:
            file_path = os.path.join(corpus_path,'example.dev')

        x_data,y_data = DataReader.read_conll_format_file(file_path)
        if shuffle:
            x_data,y_data = utils.unison_shuffled_copies(x_data,y_data)
        logging.debug(f"loaded {len(x_data)} samples from {file_path}. Sample:\n"
                      f"x[0]: {x_data[0]}\n"
                      f"y[0]: {y_data[0]}")
        return x_data,y_data


class CONLL2003ENCorpus(object):
    __corpus__name__ = 'conll2003_en'
    __zip_file__name = 'http://s3.bmio.net/kashgari/conll2003_en.tar.gz'

    @classmethod
    def load_data(cls,
                  subset_name: str = 'train',
                  task_name: str = 'ner',
                  shuffle: bool = True) -> Tuple[List[List[str]],List[List[str]]]:
        corpus_path = get_file(cls.__corpus__name__,
                               cls.__zip_file__name,
                               cache_dir=k.DATA_PATH,
                               untar=True)

        if subset_name not in {'train', 'test', 'valid'}:
            raise ValueError()

        file_path = os.path.join(corpus_path, f'{subset_name}.txt')

        if task_name not in {'pos', 'chunking', 'ner'}:
            raise ValueError()

        data_index = ['pos', 'chunking', 'ner'].index(task_name) + 1

        x_data, y_data = DataReader.read_conll_format_file(file_path, label_index=data_index)
        if shuffle:
            x_data, y_data = utils.unison_shuffled_copies(x_data, y_data)
        logging.debug(f"loaded {len(x_data)} samples from {file_path}. Sample:\n"
                      f"x[0]: {x_data[0]}\n"
                      f"y[0]: {y_data[0]}")
        return x_data, y_data


class NerTwoLineCorpus(object):
    '''
        通用数据格式加载：
        x x x x x x x \n
        O O B-XXX I-XXX O O O \n
        \n\n
    '''
    __corpus__name__ = '通用NER数据加载类'

    @classmethod
    def load_data(cls,
                  glob_corpus_path,
                  subset_name: str = 'train',
                  task_name: str = 'ner',
                  shuffle: bool = True) -> Tuple[List[List[str]], List[List[str]]]:


        if subset_name not in {'train', 'test', 'valid'}:
            raise ValueError()


        if task_name not in {'pos', 'chunking', 'ner'}:
            raise ValueError()

        file_list = glob.glob(glob_corpus_path)
        x_data, y_data = [] ,[]
        for file in tqdm(file_list):
            with open(file,encoding='utf-8') as fread:
                lines = fread.read()
                train_lists = lines.split("\n\n")

                for item in train_lists:
                    if not item.strip():
                        continue
                    words_and_tags = item.strip().split("\n")
                    if len(words_and_tags) != 2:
                        print(words_and_tags)
                    else:
                        x_data.append(words_and_tags[0])#.split(" "))
                        y_data.append(words_and_tags[1])#.split(" "))



        if shuffle:
            x_data, y_data = utils.unison_shuffled_copies(x_data, y_data)
        logging.debug(f"loaded {len(x_data)} samples from {glob_corpus_path}. Sample:\n"
                      f"x[0]: {x_data[0]}\n"
                      f"y[0]: {y_data[0]}")
        return x_data, y_data



class JsonNerCorpus(object):
    '''

    '''

    def __init__(self):
        pass

    def generate_examples(self, filepath):
        with open(filepath, 'r', encoding="utf-8") as f:
            for line in f:
                if line != "" and line != "\n":
                    line_dict = json.loads(line.strip())
                    tokens = list(line_dict['text'])
                    ner_tags = ["O"] * len(line_dict['text'])
                    for inds, inde, label in line_dict['labels']:
                        if inde - inds == 1:
                            ner_tags[inds] = 'B-' + label
                        else:
                            for i in range(inds, inde):
                                if i == inds:
                                    ner_tags[i] = 'B-' + label
                                # elif i == (inde - 1):
                                #     ner_tags[i] = 'E-' + label
                                else:
                                    ner_tags[i] = 'I-' + label
                    yield tokens, ner_tags

    def load_data(self,
                  glob_path,
                  shuffle: bool = True,
                  corpus_path=None) -> Tuple[List[List[str]], List[List[str]]]:
        x_data = []
        y_data = []
        for file in glob.glob(glob_path):
            for x,y in self.generate_examples(file):
                x_data.append(x)
                y_data.append(y)

        if shuffle:
            x_data, y_data = utils.unison_shuffled_copies(x_data, y_data)
        return x_data, y_data

if __name__ == "__main__":
    glob_path = '/home/qiufengfeng/nlp/nlp_project/github_third/TransformersNer/ner_train/data/*test.json'
    a, b = JsonNerCorpus().load_data(glob_path)
    print(a)
    print(b)

