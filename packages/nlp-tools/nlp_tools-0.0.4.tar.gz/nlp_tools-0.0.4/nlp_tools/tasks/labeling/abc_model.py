# encoding: utf-8

# author: BrikerMan
# contact: eliyar917@gmail.com
# blog: https://eliyar.biz

# file: abc_model.py
# time: 4:30 下午

from abc import ABC
from typing import List, Dict, Any, Union, Optional

import numpy as np
import tensorflow as tf

import nlp_tools
from nlp_tools.embeddings import ABCEmbedding, BareEmbedding,TransformerEmbedding,BertEmbedding
from nlp_tools.generators import CorpusGenerator, BatchDataSet
from nlp_tools.layers import KConditionalRandomField
from nlp_tools.logger import logger
from nlp_tools.metrics.sequence_labeling import get_entities
from nlp_tools.metrics.sequence_labeling import sequence_labeling_report
from nlp_tools.processors import SequenceProcessor
from nlp_tools.tasks.abs_task_model import ABCTaskModel
from nlp_tools.types import TextSamplesVar
from nlp_tools.optimizer import MultiOptimizer

from tensorflow.keras.optimizers import Adam


class ABCLabelingModel(ABCTaskModel, ABC):
    """
    Abstract Labeling Model
    """

    def __init__(self,
                 embedding: ABCEmbedding = None,
                 sequence_length: int = None,
                 hyper_parameters: Dict[str, Dict[str, Any]] = None,
                 text_processor=None,
                 label_processor=None):
        """

        Args:
            embedding: embedding object
            sequence_length: target sequence length
            hyper_parameters: hyper_parameters to overwrite
        """
        super(ABCLabelingModel, self).__init__()
        if embedding is None:
            embedding = BareEmbedding()  # type: ignore

        if hyper_parameters is None:
            hyper_parameters = self.default_hyper_parameters()

        self.tf_model: Optional[tf.keras.Model] = None
        self.embedding = embedding
        self.hyper_parameters = hyper_parameters
        self.sequence_length = sequence_length
        if not text_processor:
            self.text_processor: SequenceProcessor = SequenceProcessor()
        else:
            self.text_processor = text_processor


        if not label_processor:
            self.label_processor: SequenceProcessor = SequenceProcessor(build_in_vocab='labeling',
                                                                    min_count=1,
                                                                    build_vocab_from_labels=True)
        else:
            self.label_processor = label_processor

        self.crf_layer: Optional[KConditionalRandomField] = None

    def build_model(self,
                    x_data: TextSamplesVar,
                    y_data: TextSamplesVar) -> None:
        """
        Build Model with x_data and y_data

        This function will setup a :class:`CorpusGenerator`,
         then call :meth:`ABCClassificationModel.build_model_gen` for preparing processor and model

        Args:
            x_data:
            y_data:

        Returns:

        """

        train_gen = CorpusGenerator(x_data, y_data)
        self.build_model_generator([train_gen])

    def build_model_generator(self,
                              generators: List[CorpusGenerator]) -> None:

        if self.embedding.vocab2idx:
            self.text_processor.vocab2idx = self.embedding.vocab2idx
            self.text_processor.idx2vocab = dict([(v, k) for k, v in self.text_processor.vocab2idx.items()])
        if not self.text_processor.vocab2idx:
            self.text_processor.build_vocab_generator(generators)
        self.label_processor.build_vocab_generator(generators)
        self.embedding.setup_text_processor(self.text_processor)

        if self.sequence_length is None:
            self.sequence_length = self.embedding.get_seq_length_from_corpus(generators)

        if self.tf_model is None:
            self.build_model_arc()
            self.compile_model()
        print(self.get_input_and_output_names_from_model())




    def build_model_arc(self) -> None:
        raise NotImplementedError

    def compile_model(self,
                      loss: Any = None,
                      optimizer: Any = None,
                      metrics: Any = None,
                      **kwargs: Any) -> None:

        if loss is None:
            loss = 'sparse_categorical_crossentropy'


        if type(self.embedding) in [TransformerEmbedding,BertEmbedding] :
            total_layers = self.tf_model.layers
            transfomer_layers = self.embedding.embed_model.layers
            no_transformer_layers = [layer for layer in total_layers if layer not in transfomer_layers]
            optimizer_list = [
                Adam(),
                Adam(learning_rate=1e-5)
            ]
            optimizers_and_layers = [(optimizer_list[0], no_transformer_layers), (optimizer_list[1], transfomer_layers)]
            optimizer = MultiOptimizer(optimizers_and_layers)




        if optimizer is None:
            optimizer = Adam()
        if metrics is None:
            metrics = ['accuracy']

        self.tf_model.compile(loss=loss,
                              optimizer=optimizer,
                              metrics=metrics,
                              **kwargs)

    def fit(self,
            x_train: TextSamplesVar,
            y_train: TextSamplesVar,
            x_validate: TextSamplesVar = None,
            y_validate: TextSamplesVar = None,
            batch_size: int = 64,
            epochs: int = 5,
            callbacks: List[tf.keras.callbacks.Callback] = None,
            fit_kwargs: Dict = None) -> 'tf.keras.callbacks.History':
        """
        Trains the model for a given number of epochs with given data set list.

        Args:
            x_train: Array of train feature data (if the model has a single input),
                or tuple of train feature data array (if the model has multiple inputs)
            y_train: Array of train label data
            x_validate: Array of validation feature data (if the model has a single input),
                or tuple of validation feature data array (if the model has multiple inputs)
            y_validate: Array of validation label data
            batch_size: Number of samples per gradient update, default to 64.
            epochs: Number of epochs to train the model.
                An epoch is an iteration over the entire `x` and `y` data provided.
            callbacks: List of `tf.keras.callbacks.Callback` instances.
                List of callbacks to apply during training.
                See :py:class:`tf.keras.callbacks`.
            fit_kwargs: fit_kwargs: additional arguments passed to :meth:`tf.keras.Model.fit`

        Returns:
            A :py:class:`tf.keras.callback.History`  object. Its `History.history` attribute is
            a record of training loss values and metrics values
            at successive epochs, as well as validation loss values
            and validation metrics values (if applicable).
        """
        train_gen = CorpusGenerator(x_train, y_train)
        if x_validate is not None:
            valid_gen = CorpusGenerator(x_validate, y_validate)
        else:
            valid_gen = None
        return self.fit_generator(train_sample_gen=train_gen,
                                  valid_sample_gen=valid_gen,
                                  batch_size=batch_size,
                                  epochs=epochs,
                                  callbacks=callbacks,
                                  fit_kwargs=fit_kwargs)

    def fit_generator(self,
                      train_sample_gen: CorpusGenerator,
                      valid_sample_gen: CorpusGenerator = None,
                      batch_size: int = 64,
                      epochs: int = 5,
                      callbacks: List['tf.keras.callbacks.Callback'] = None,
                      fit_kwargs: Dict = None) -> 'tf.keras.callbacks.History':
        self.build_model_generator([g for g in [train_sample_gen, valid_sample_gen] if g])

        train_set = BatchDataSet(train_sample_gen,
                                 text_processor=self.text_processor,
                                 label_processor=self.label_processor,
                                 segment=self.embedding.segment,
                                 seq_length=self.sequence_length,
                                 max_position=self.embedding.max_position,
                                 batch_size=batch_size)

        if fit_kwargs is None:
            fit_kwargs = {}
        if valid_sample_gen:
            valid_set = BatchDataSet(valid_sample_gen,
                                     text_processor=self.text_processor,
                                     label_processor=self.label_processor,
                                     segment=self.embedding.segment,
                                     seq_length=self.sequence_length,
                                     max_position=self.embedding.max_position,
                                     batch_size=batch_size)
            fit_kwargs['validation_data'] = valid_set.take()
            fit_kwargs['validation_steps'] = len(valid_set)

        for x, y in train_set.take(1):
            logger.debug('fit input shape: {}'.format(np.array(x).shape))
            logger.debug('fit input shape: {}'.format(np.array(y).shape))
        return self.tf_model.fit(train_set.take(),
                                 steps_per_epoch=len(train_set),
                                 epochs=epochs,
                                 callbacks=callbacks,
                                 **fit_kwargs)

    def predict(self,
                x_data: TextSamplesVar,
                *,
                batch_size: int = 32,
                truncating: bool = False,
                predict_kwargs: Dict = None) -> List[List[str]]:
        """
        Generates output predictions for the input samples.

        Computation is done in batches.

        Args:
            x_data: The input data, as a Numpy array (or list of Numpy arrays if the model has multiple inputs).
            batch_size: Integer. If unspecified, it will default to 32.
            truncating: remove values from sequences larger than `model.embedding.sequence_length`
            predict_kwargs: arguments passed to :meth:`tf.keras.Model.predict`

        Returns:
            array(s) of predictions.
        """
        if predict_kwargs is None:
            predict_kwargs = {}
        with nlp_tools.utils.custom_object_scope():
            if truncating:
                seq_length = self.sequence_length
            else:
                seq_length = None

            tensor = self.text_processor.transform(x_data,
                                                   segment=self.embedding.segment,
                                                   seq_length=seq_length,
                                                   max_position=self.embedding.max_position)
            logger.debug('predict seq_length: {}, input: {}'.format(seq_length, np.array(tensor).shape))
            pred = self.tf_model.predict(tensor, batch_size=batch_size, verbose=1, **predict_kwargs)
            pred = pred.argmax(-1)

            lengths = [len(sen) for sen in x_data]

            res: List[List[str]] = self.label_processor.inverse_transform(pred,  # type: ignore
                                                                          lengths=lengths)
            logger.debug('predict output: {}'.format(np.array(pred).shape))
            logger.debug('predict output argmax: {}'.format(pred))
        return res

    def predict_entities(self,
                         x_data: TextSamplesVar,
                         batch_size: int = 32,
                         join_chunk: str = ' ',
                         truncating: bool = False,
                         predict_kwargs: Dict = None) -> List[Dict]:
        """Gets entities from sequence.

        Args:
            x_data: The input data, as a Numpy array (or list of Numpy arrays if the model has multiple inputs).
            batch_size: Integer. If unspecified, it will default to 32.
            truncating: remove values from sequences larger than `model.embedding.sequence_length`
            join_chunk: str or False,
            predict_kwargs: arguments passed to :meth:`tf.keras.Model.predict`

        Returns:
            list: list of entity.
        """
        if isinstance(x_data, tuple):
            text_seq = x_data[0]
        else:
            text_seq = x_data
        res = self.predict(x_data,
                           batch_size=batch_size,
                           truncating=truncating,
                           predict_kwargs=predict_kwargs)
        new_res = [get_entities(seq) for seq in res]
        final_res = []
        for index, seq in enumerate(new_res):
            seq_data = []
            for entity in seq:
                res_entities: List[str] = []
                for i, e in enumerate(text_seq[index][entity[1]:entity[2] + 1]):
                    # Handle bert tokenizer
                    if e.startswith('##') and len(res_entities) > 0:
                        res_entities[-1] += e.replace('##', '')
                    else:
                        res_entities.append(e)
                value: Union[str, List[str]]
                if join_chunk is False:
                    value = res_entities
                else:
                    value = join_chunk.join(res_entities)

                seq_data.append({
                    "entity": entity[0],
                    "start": entity[1],
                    "end": entity[2],
                    "value": value,
                })

            final_res.append({
                'tokenized': x_data[index],
                'labels': seq_data
            })
        return final_res

    def evaluate(self,
                 x_data: TextSamplesVar,
                 y_data: TextSamplesVar,
                 batch_size: int = 32,
                 digits: int = 4,
                 truncating: bool = False) -> Dict:
        y_pred = self.predict(x_data,
                              batch_size=batch_size,
                              truncating=truncating)
        y_true = [seq[:len(y_pred[index])] for index, seq in enumerate(y_data)]

        new_y_pred = []
        for x in y_pred:
            new_y_pred.append([str(i) for i in x])
        new_y_true = []
        for x in y_true:
            new_y_true.append([str(i) for i in x])

        report = sequence_labeling_report(y_true, y_pred, digits=digits)
        return report


    def get_tfserver_http_inputs(self,input_data):
        '''
        根据输入，生成tf-server需要的输入数据格式
        '''


        segment_texts = self.text_processor.text_tokenizer.tokenize(input_data)
        if segment_texts and type(segment_texts[0]) == str :
            segment_texts = [list(segment_text) for segment_text in segment_texts]
        tensor_datas = self.text_processor.transform(segment_texts)

        tensors = []
        for key,value  in zip(self.model_node_names['inputs'],tensor_datas):
            for index in range(len(value)):
                if len(tensors)-1 < index:
                    tensors.append({})
                tensors[index][key] = value[index].tolist()
        return tensors,segment_texts

    def get_tfserver_http_result_labels(self,origin_sentences,preditions):

        tokened_sentences = [self.text_processor.text_tokenizer.tokenize(sentence) for sentence in origin_sentences]
        lengths = [len(sen) for sen in tokened_sentences]

        pred = np.array(preditions).argmax(-1)
        pred_labels = self.label_processor.inverse_transform(pred,lengths=lengths)
        return pred_labels


