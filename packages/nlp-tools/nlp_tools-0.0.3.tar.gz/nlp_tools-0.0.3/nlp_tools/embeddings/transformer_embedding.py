import codecs
import json
from typing import Dict,List,Any,Optional

#from nlp_tools.third_model.bert4keras.bert4keras.models import build_transformer_model
from bert4keras.tokenizers import  load_vocab
from bert4keras.models import build_transformer_model

from nlp_tools.embeddings.abc_embedding import ABCEmbedding
from nlp_tools.logger import logger

class TransformerEmbedding(ABCEmbedding):
    """
    TransformerEmbedding is based on bert4keras.
    The embeddings itself are wrapped into our simple embedding interface so that they can be used like any other embedding.
    """
    def to_dict(self) -> Dict[str, Any]:
        info_dic = super(TransformerEmbedding, self).to_dict()
        info_dic['config']['vocab_path'] = self.vocab_path
        info_dic['config']['config_path'] = self.config_path
        info_dic['config']['checkpoint_path'] = self.checkpoint_path
        info_dic['config']['model_type'] = self.model_type
        return info_dic

    def __init__(self,
                 vocab_path: str,
                 config_path: str,
                 checkpoint_path: str,
                 model_type: str = 'bert',
                 simplified = True,
                 keep_tokens = None,
                 **kwargs: Any):
        """

        Args:
            vocab_path: vocab file path, example `vocab.txt`
            config_path: model config path, example `config.json`
            checkpoint_path: model weight path, example `model.ckpt-100000`
            model_type: transfer model type, {bert, albert, nezha, gpt2_ml, t5}
            kwargs: additional params
        """
        self.vocab_path = vocab_path
        self.config_path = config_path
        self.checkpoint_path = checkpoint_path
        self.model_type = model_type
        self.vocab_list: List[str] = []
        self.simplified = simplified
        self.keep_tokens = keep_tokens
        kwargs['segment'] = True
        super(TransformerEmbedding, self).__init__(**kwargs)

    def load_embed_vocab(self) -> Optional[Dict[str, int]]:
        if self.simplified:
            token2idx, self.keep_tokens = load_vocab(
                dict_path=self.vocab_path,
                simplified=self.simplified,
                startswith=['[PAD]', '[UNK]', '[CLS]', '[SEP]'],
            )
        else:
            token2idx = load_vocab(
                dict_path=self.vocab_path,
            )

        top_words = [k for k, v in list(token2idx.items())[:50]]
        logger.debug('------------------------------------------------')
        logger.debug("Loaded transformer model's vocab")
        logger.debug(f'config_path       : {self.config_path}')
        logger.debug(f'vocab_path      : {self.vocab_path}')
        logger.debug(f'checkpoint_path : {self.checkpoint_path}')
        logger.debug(f'Top 50 words    : {top_words}')
        logger.debug('------------------------------------------------')

        return token2idx
        #return None

    def build_embedding_model(self,
                              bert_application='encoder',
                              return_keras_model=True,
                              **kwargs: Dict) -> None:
        if self.embed_model is None:
            config_path = self.config_path
            with open(config_path, 'r') as f:
                config = json.loads(f.read())
            if 'max_position' in config:
                self.max_position = config['max_position']
            else:
                self.max_position = config.get('max_position_embeddings')


            bert_model = build_transformer_model(config_path=self.config_path,
                                                 checkpoint_path=self.checkpoint_path,
                                                 model=self.model_type,
                                                 application=bert_application,
                                                 keep_tokens=self.keep_tokens,  # 只保留keep_tokens中的字，精简原字表
                                                 **kwargs)
            self.embed_model = bert_model
            self.embedding_size = bert_model.output.shape[-1]



