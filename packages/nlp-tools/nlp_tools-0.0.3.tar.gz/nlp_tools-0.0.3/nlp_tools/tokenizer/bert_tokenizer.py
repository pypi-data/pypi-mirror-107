from typing import Dict,Any

from nlp_tools.third_model.bert4keras.bert4keras.tokenizers import Tokenizer,load_vocab
from nlp_tools.tokenizer.base_tokenizer import ABCTokenizer
from bert4keras.tokenizers import load_vocab




class BertTokenizer(Tokenizer,ABCTokenizer):

    """
    Bert Like Tokenizer, ref: https://github.com/CyberZHG/keras-bert/blob/master/keras_bert/tokenizer.py

    """
    def to_dict(self) -> Dict[str, Any]:
        data = super(BertTokenizer, self).to_dict()
        data['config']['token_dict'] = self._token_dict
        data['config']['do_lower_case'] = self._do_lower_case
        data['config']['simplified'] = self.simplified
        data['config']['keep_tokens'] = self.keep_tokens
        return data

    def __init__(self,token_dict=None, do_lower_case=False,simplified=True,keep_tokens = None):
        self.simplified = simplified
        self.keep_tokens = keep_tokens
        if type(token_dict) != dict:
            if simplified:
                token_dict, self.keep_tokens = load_vocab(
                    dict_path=token_dict,
                    simplified=simplified,
                    startswith=['[PAD]', '[UNK]', '[CLS]', '[SEP]'],
                )
            else:
                token_dict = load_vocab(
                    dict_path=token_dict,
                )
        super(BertTokenizer,self).__init__(token_dict=token_dict,do_lower_case=do_lower_case)


    def tokenize(self, text, maxlen=None):
        tokens = super(BertTokenizer, self).tokenize(text,maxlen=maxlen)
        tokens = tokens[1:-1]
        return tokens

if __name__ == '__main__':
    a = BertTokenizer(token_dict='/home/qiufengfeng/nlp/pre_trained_model/chinese_L-12_H-768_A-12/chinese_L-12_H-768_A-12/vocab.txt')
    print(a.to_dict())
