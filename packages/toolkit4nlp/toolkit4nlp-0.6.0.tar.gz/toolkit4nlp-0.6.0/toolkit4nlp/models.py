# -*- coding: utf-8 -*-
# @Date    : 2020/6/29
# @Author  : mingming.xu
# @Email   : xv44586@gmail.com
# @File    : models.py
import six
import json
import numpy as np

from toolkit4nlp.layers import *
from keras.models import Model
from toolkit4nlp.utils import remove_arguments, string_matching, insert_arguments


class Transformer(object):
    """
    base class
    """

    def __init__(self,
                 vocab_size,  # 词表大小
                 hidden_size,  # 编码维度
                 num_hidden_layers,  # Transformer总的层数
                 num_attention_heads,  # Attention头数
                 intermediate_size,  # FeedForward 层的隐层维度
                 hidden_act=None,  # FeedFoward 层的激活函数
                 dropout_rate=None,  # dropout 比例
                 embedding_size=None,  # embedding 层维度
                 attention_key_size=None,  # attentioin 中 Q, K 的head size
                 sequence_length=None,  # 是否固定序列长度
                 layers=None,  # 外部传人的layer
                 name=None,  # 模型名
                 prefix=None,  # layer name 的前缀
                 keep_tokens=None,  # 自定义保留token
                 with_residual_attention=False,  # attention scores 残差
                 skip_weights_from_checkpoints=[],  # 从checkpoints中load weights 跳过的权重，会同时作用在trainable_weights 和 variables
                 **kwargs):
        """
        """
        if keep_tokens is not None:
            vocab_size = len(keep_tokens)

        self.vocab_size = vocab_size
        self.hidden_size = hidden_size
        self.num_hidden_layers = num_hidden_layers
        self.num_attention_heads = num_attention_heads
        if hidden_size % num_attention_heads != 0:
            raise ValueError('The hidden size {hidden_size} is not a multiple of the number of attention heads {'
                             'num_attention_heads}')
        self.attention_head_size = hidden_size // num_attention_heads
        self.attention_key_size = attention_key_size or self.attention_head_size
        self.intermediate_size = intermediate_size
        self.hidden_act = hidden_act
        self.dropout_rate = dropout_rate or 0
        self.embedding_size = embedding_size or hidden_size
        self.sequence_length = sequence_length
        self.position_bias = None
        self.layers = layers or {}
        self.name = name
        self.prefix = prefix or ''
        self.keep_tokens = keep_tokens
        self.with_residual_attention = with_residual_attention
        self.attention_bias = None  # 包含对attention 的偏移，如attention mask
        self.attention_scores = None  # 记录attention scores，用来实现residual attention
        self.skip_weights_from_checkpoints = skip_weights_from_checkpoints
        self.built = False

    def build(self,
              layer_norm_cond=None,
              layer_norm_cond_hidden_size=None,
              layer_norm_cond_hidden_act=None,
              additional_input_layers=None,
              **kwargs):
        """构建模型
        layer_norm_*为实现conditional layer normalization时使用。
        additional_input_layers 为新增的输入
        """
        if self.built:
            return None

        # inputs
        inputs = self.get_inputs()
        self.set_inputs(inputs, additional_input_layers)
        # conditional layer norm
        self.layer_norm_conds = [
            layer_norm_cond,
            layer_norm_cond_hidden_size,
            layer_norm_cond_hidden_act or 'linear'
        ]
        # call
        outputs = self.call(inputs)
        self.set_outputs(outputs)
        # model
        self.model = Model(self.inputs, self.outputs, name=self.name)

        self.built = True

    def call(self, inputs):
        """模型的计算图
        """
        # embedding
        outputs = self.apply_embeddings(inputs)

        # main transformer layers
        for _ in range(self.num_hidden_layers):
            outputs = self.apply_transformer_layers(outputs, _)

        # task related layers
        outputs = self.apply_task_related(outputs)
        return outputs

    def prefixed(self, name):
        """增加前缀
        """
        if name is not None:
            return self.prefix + name

    def apply(self, inputs=None, layer=None, name=None, arguments=None, **kwargs):
        """
         记录layer信息方便后续mapping权重服务；重用同名layer;
         layer(name=layer_name, **kwargs)(inputs, **arguments)
        :param inputs: 上一层的输出
        :param layer: 具体layer
        :param name: 层的名字
        :param arguments: 计算时使用参数
        :param kwargs: 初始化参数
        :return:
        """
        if layer is Dropout and self.dropout_rate == 0:
            return inputs

        arguments = {} if arguments is None else arguments

        # add prefix
        name = self.prefixed(name)
        kwargs['name'] = name

        if name not in self.layers:
            current_layer = layer(**kwargs)
            name = current_layer.name
            self.layers[name] = current_layer

        if inputs is None:
            return self.layers[name]

        return self.layers[name](inputs, **arguments)

    def get_inputs(self):
        raise NotImplementedError

    def apply_embeddings(self, inputs):
        raise NotImplementedError

    def apply_transformer_layers(self, inputs, idx):
        raise NotImplementedError

    def apply_task_related(self, inputs):
        raise NotImplementedError

    def set_inputs(self, inputs, additional_input_layers=None):
        """设置input 和 inputs
        """
        if inputs is None:
            inputs = []
        elif not isinstance(inputs, list):
            inputs = [inputs]

        inputs = inputs[:]
        if additional_input_layers is not None:
            if not isinstance(additional_input_layers, list):
                additional_input_layers = [additional_input_layers]
            inputs.extend(additional_input_layers)

        self.inputs = inputs
        if len(inputs) > 1:
            self.input = inputs
        else:
            self.input = inputs[0]

    def set_outputs(self, outputs):
        """设置output 和 outputs
        """
        if not isinstance(outputs, list):
            outputs = [outputs]

        outputs = outputs[:]
        self.outputs = outputs
        if len(outputs) > 1:
            self.output = outputs
        else:
            self.output = outputs[0]

    @property
    def initializer(self):
        """
        截断正态分布初始化
        """
        return keras.initializers.TruncatedNormal(stddev=0.02)

    def load_variable(self, checkpoint, name):
        return tf.train.load_variable(checkpoint, name)

    def load_embeddings(self, embeddings):
        if self.keep_tokens:
            return embeddings[self.keep_tokens]
        return embeddings

    def create_variable(self, name, value):
        return tf.Variable(initial_value=value, name=name)

    def variable_mapping(self):
        # keras 层与checkpoint变量直接的映射关系
        return {}

    def load_weights_from_checkpoint(self, checkpoint, mapping=None):
        """根据 mapping 从 checkpoint 加载权重
        """
        mapping = mapping or self.variable_mapping()
        mapping = {self.prefixed(k): v for k, v in mapping.items()}
        mapping = {k: v for k, v in mapping.items() if k in self.layers}

        weights_values_pairs = []
        for layer_name, variables in mapping.items():
            weights = self.layers[layer_name].trainable_weights

            # skip weights by names
            if self.skip_weights_from_checkpoints:
                weights = [w for w in weights if not string_matching(w.name, self.skip_weights_from_checkpoints)]
                variables = [v for v in values if not string_matching(v, self.skip_weights_from_checkpoints)]
            values = [self.load_variable(checkpoint, v) for v in variables]
            weights_values_pairs.extend(zip(weights, values))

        K.batch_set_value(weights_values_pairs)

    def save_weights_as_checkpoint(self, checkpoint_path, mapping=None):
        """根据mapping 将权重保存为 checkpoint格式
        """
        mapping = mapping or self.variable_mapping()
        mapping = {self.prefixed(k): v for k, v in mapping.items()}
        mapping = {k: v for k, v in mapping.items() if k in self.layers}

        with tf.Graph().as_default():
            for layer_name, variables in mapping.items():
                layer = self.layers[layer_name]
                weights = K.batch_get_value(layer.trainable_weights)
                for variable, weight in zip(variables, weights):
                    self.create_variable(variable, weight)
            with tf.Session() as sess:
                sess.run(tf.global_variables_initializer())
                saver = tf.train.Saver()
                saver.save(sess, checkpoint_path, write_meta_graph=False)

    def simplify(self, inputs):
        """过滤列表中的None"""
        inputs = [i for i in inputs if i is not None]
        if len(inputs) == 1:
            return inputs[0]
        return inputs

    def compute_attention_bias(self, inputs):
        return self.attention_bias

    def apply_attention(self, inputs, attention_name, arguments):
        # attention 层有很多变体，所以单独抽出来一个方法，来适应不同变体
        x = self.apply(inputs,
                       MultiHeadAttention,
                       name=attention_name,
                       head_nums=self.num_attention_heads,
                       head_size=self.attention_head_size,
                       arguments=arguments,
                       kernel_initializer=self.initializer,
                       with_residual_attention=self.with_residual_attention)
        if self.with_residual_attention:
            x, att_scores = x
            self.attention_scores = att_scores

        return x


class BERT(Transformer):
    """
    Google Bert
    """

    def __init__(self,
                 max_position,  # 序列最大长度
                 with_pool=False,  # 是否包含pooler部分
                 with_nsp=False,  # 是否包含NSP部分
                 with_mlm=False,  # 是否包含mlm部分
                 type_vocab_size=2,  # segment type 的种类
                 shared_segment_embeddings=False,  # segment 与 token 是否共用embedding
                 **kwargs
                 ):
        super(BERT, self).__init__(**kwargs)
        self.max_position = max_position

        self.with_pool = with_pool
        self.with_nsp = with_nsp
        self.with_mlm = with_mlm
        self.type_vocab_size = type_vocab_size
        self.shared_segment_embeddings=shared_segment_embeddings
        # nsp need pooler
        if with_nsp and not with_pool:
            self.with_pool = True

    def get_inputs(self):
        # 新增type_vocab_size，来过滤segment-inputs
        token_in = self.apply(layer=Input,
                              name='Input-Token',
                              shape=(self.sequence_length,))
        inputs = [token_in]
        if self.type_vocab_size > 0:
            segment_in = self.apply(layer=Input,
                                name='Input-Segment',
                                shape=(self.sequence_length,))
            inputs.append(segment_in)

        return inputs

    def apply_embeddings(self, inputs):
        """token_embedding + segment_embedding + position_embedding
        """
        inputs = inputs[:]
        x = inputs.pop(0)
        if self.type_vocab_size > 0:
            s = inputs.pop(0)
        # condition layer norm
        z = self.layer_norm_conds[0]

        x = self.apply(inputs=x,
                     layer=Embedding,
                     name='Embedding-Token',
                     input_dim=self.vocab_size,
                     output_dim=self.embedding_size,
                     embeddings_initializer=self.initializer,
                     mask_zero=True
                     )
        if self.type_vocab_size > 0:
            if self.shared_segment_embeddings:
                name = 'Embedding-Token'
            else:
                name = 'Embedding-Segment'
            s = self.apply(s,
                           Embedding,
                           name=name,
                           input_dim=self.type_vocab_size,
                           output_dim=self.embedding_size,
                           embeddings_initializer=self.initializer,
                                           )
            x = self.apply([x, s], Add, name='Embedding-Token-Segment')
        x = self.apply(x,
                       PositionEmbedding,
                       name='Embedding-Position',
                       input_dim=self.max_position,
                       output_dim=self.embedding_size,
                       embeddings_initializer=self.initializer,
                       merge_mode='add')

        x = self.apply(inputs=self.simplify([x, z]),
                       layer=LayerNormalization,
                       conditional=(z is not None),
                       condition_hidden_units=self.layer_norm_conds[1],
                       condition_hidden_activation=self.layer_norm_conds[2],
                       condition_hidden_initializer=self.initializer,
                       name='Embedding-Norm')
        x = self.apply(x,
                       Dropout,
                       name='Embedding-Dropout',
                       rate=self.dropout_rate)
        if self.hidden_size != self.embedding_size:
            x = self.apply(x,
                           Dense,
                           name='Embedding-Mapping',
                           units=self.hidden_size,
                           kernel_initializer=self.initializer)

        return x

    def apply_transformer_layers(self, inputs, idx):
        """
        Att --> Dropout --> Add --> LN --> FFN --> Dropout -->  Add --> LN
        """
        attention_name = 'Transformer-%d-MultiHeadSelfAttention' % idx
        feed_forward_name = 'Transformer-%d-FeedForward' % idx
        attention_bias = self.compute_attention_bias(idx)

        x_pre, x = inputs, [inputs, inputs, inputs]
        z = self.layer_norm_conds[0]
        arguments = {'a_bias': None}
        if attention_bias is not None:
            arguments['a_bias'] = True
            x.append(attention_bias)

        # self-attention
        x = self.apply_attention(x, attention_name, arguments)

        x = self.apply(x,
                       Dropout,
                       name='%s-Dropout' % attention_name,
                       rate=self.dropout_rate)

        x = self.apply([x_pre, x],
                       Add,
                       name='%s-Add' % attention_name
                       )

        x = self.apply(inputs=self.simplify([x, z]),
                       layer=LayerNormalization,
                       conditional=(z is not None),
                       condition_hidden_units=self.layer_norm_conds[1],
                       condition_hidden_activation=self.layer_norm_conds[2],
                       condition_hidden_initializer=self.initializer,
                       name='%s-Norm' % attention_name,
                       )

        # feedforward
        x_pre = x
        x = self.apply(x,
                       FeedForward,
                       name=feed_forward_name,
                       units=self.intermediate_size,
                       activation=self.hidden_act,
                       kernel_initializer=self.initializer
                       )
        x = self.apply(x,
                       Dropout,
                       name='%s-Dropout' % feed_forward_name,
                       rate=self.dropout_rate)
        x = self.apply([x_pre, x],
                       Add,
                       name='%s-Add' % feed_forward_name)
        x = self.apply(inputs=self.simplify([x, z]),
                       layer=LayerNormalization,
                       conditional=(z is not None),
                       condition_hidden_units=self.layer_norm_conds[1],
                       condition_hidden_activation=self.layer_norm_conds[2],
                       condition_hidden_initializer=self.initializer,
                       name='%s-Norm' % feed_forward_name)
        return x

    def apply_task_related(self, inputs):
        """
        跟据不同task加不同的layer产生不同的outputs
        :param inputs:
        :return:
        """
        x = inputs
        outputs = [x]
        z = self.layer_norm_conds[0]
        if self.with_pool:
            # pooler 提取cls向量
            x = self.apply(x, layer=Lambda, name='Pooler', function=lambda x: x[:, 0])
            pool_activation = 'tanh' if self.with_pool is True else self.with_pool
            x = self.apply(x,
                           layer=Dense,
                           name='Pooler-Dense',
                           units=self.hidden_size,
                           activation=pool_activation,
                           kernel_initializer=self.initializer)
            if self.with_nsp:
                # Next sentence prediction
                x = self.apply(x,
                               layer=Dense,
                               name='NSP-Proba',
                               units=2,
                               activation='softmax',
                               kernel_initializer=self.initializer)

            outputs.append(x)

        if self.with_mlm:
            # Mask language model, Dense --> Norm --> Embedding --> Biasadd --> softmax
            x = outputs[0]
            x = self.apply(x,
                           layer=Dense,
                           name='MLM-Dense',
                           units=self.embedding_size,
                           activation=self.hidden_act,
                           kernel_initializer=self.initializer)
            x = self.apply(inputs=self.simplify([x, z]),
                           layer=LayerNormalization,
                           conditional=(z is not None),
                           condition_hidden_units=self.layer_norm_conds[1],
                           condition_hidden_activation=self.layer_norm_conds[2],
                           condition_hidden_initializer=self.initializer,
                           name='MLM-Norm',
                           )
            # 重用embedding-token layer
            x = self.apply(x, Embedding, 'Embedding-Token', arguments={'mode': 'dense'})
            x = self.apply(x, BiasAdd, 'MLM-Bias')
            mlm_activation = 'softmax' if self.with_mlm is True else self.with_mlm
            x = self.apply(x, Activation, 'MLM-Activation', activation=mlm_activation)
            outputs.append(x)

        if len(outputs) == 1:
            return outputs[0]
        if len(outputs) == 2:
            return outputs[1]

        return outputs[1:]

    def load_variable(self, checkpoint, name):
        """加载单个变量的函数
        """
        variable = super(BERT, self).load_variable(checkpoint, name)
        if name == 'cls/seq_relationship/output_weights':
            return variable.T
        elif name in ['bert/embeddings/word_embeddings',
                      'cls/predictions/output_bias', ]:
            return self.load_embeddings(variable)
        else:
            return variable

    def variable_mapping(self):
        """映射到官方BERT权重格式
        """
        mapping = {
            'Embedding-Token': ['bert/embeddings/word_embeddings'],
            'Embedding-Segment': ['bert/embeddings/token_type_embeddings'],
            'Embedding-Position': ['bert/embeddings/position_embeddings'],
            'Embedding-Norm': [
                'bert/embeddings/LayerNorm/beta',
                'bert/embeddings/LayerNorm/gamma',
            ],
            'Embedding-Mapping': [
                'bert/encoder/embedding_hidden_mapping_in/kernel',
                'bert/encoder/embedding_hidden_mapping_in/bias',
            ],
            'Pooler-Dense': [
                'bert/pooler/dense/kernel',
                'bert/pooler/dense/bias',
            ],
            'NSP-Proba': [
                'cls/seq_relationship/output_weights',
                'cls/seq_relationship/output_bias',
            ],
            'MLM-Dense': [
                'cls/predictions/transform/dense/kernel',
                'cls/predictions/transform/dense/bias',
            ],
            'MLM-Norm': [
                'cls/predictions/transform/LayerNorm/beta',
                'cls/predictions/transform/LayerNorm/gamma',
            ],
            'MLM-Bias': ['cls/predictions/output_bias'],
        }

        for i in range(self.num_hidden_layers):
            prefix = 'bert/encoder/layer_%d/' % i
            mapping.update({
                'Transformer-%d-MultiHeadSelfAttention' % i: [
                    prefix + 'attention/self/query/kernel',
                    prefix + 'attention/self/query/bias',
                    prefix + 'attention/self/key/kernel',
                    prefix + 'attention/self/key/bias',
                    prefix + 'attention/self/value/kernel',
                    prefix + 'attention/self/value/bias',
                    prefix + 'attention/output/dense/kernel',
                    prefix + 'attention/output/dense/bias',
                ],
                'Transformer-%d-MultiHeadSelfAttention-Norm' % i: [
                    prefix + 'attention/output/LayerNorm/beta',
                    prefix + 'attention/output/LayerNorm/gamma',
                ],
                'Transformer-%d-FeedForward' % i: [
                    prefix + 'intermediate/dense/kernel',
                    prefix + 'intermediate/dense/bias',
                    prefix + 'output/dense/kernel',
                    prefix + 'output/dense/bias',
                ],
                'Transformer-%d-FeedForward-Norm' % i: [
                    prefix + 'output/LayerNorm/beta',
                    prefix + 'output/LayerNorm/gamma',
                ],
            })

        return mapping


class LM_Mask(object):
    """
    下三角Attention Mask，主要用于自回归语言模型
    """

    def compute_attention_bias(self, inputs=None):
        """重写attention mask 计算逻辑：全局下三角矩阵，形如：
        [[[[1, 0, 0]
        [1, 1, 0]
        [1, 1, 1]]]]
        """
        if self.attention_bias is None:
            def compute_lm_mask(segments):
                seq_len = K.shape(segments)[1]
                idx = K.arange(0, seq_len)
                mask = idx[None, :] <= idx[:, None]
                mask = K.cast(mask, K.floatx())
                return -(1 - mask[None, None]) * 1e12

            self.attention_bias = self.apply(inputs=self.inputs[0],
                                             layer=Lambda,
                                             function=compute_lm_mask,
                                             name='Attention-LM-Mask')

        return self.attention_bias


class UniLM_Mask(object):
    """
    UniLM形式的attention mask
    """

    def compute_attention_bias(self, inputs=None):
        """重写attention mask 计算逻辑,segment 1 全部为1，segment 2 中为下三角矩阵.
        假如 输入序列为 [CLS] [seg1] [SEP] [seg2] [SEP], 对应 mask 为：
        [[1，1，1, 0, 0]
        [1, 1, 1, 0, 0]
        [1, 1, 1, 0, 0]
        [1, 1, 1, 1, 0]
        [1, 1, 1, 1, 1,]]
        """
        if self.attention_bias is None:
            def compute_unilm_mask(segments):
                idx = K.cumsum(segments, axis=1)
                mask = idx[:, None, :] <= idx[:, :, None]
                mask = K.cast(mask, K.floatx())
                return -(1 - mask[:, None]) * 1e12

            self.attention_bias = self.apply(inputs=self.inputs[1],
                                             layer=Lambda,
                                             function=compute_unilm_mask,
                                             name='Attention-UniLM-Attention')

        return self.attention_bias


class GPT(LM_Mask, BERT):
    """
    OPENAI GPT
    """
    @insert_arguments(final_activation='softmax')
    @remove_arguments('with_pool', 'with_mlm', 'with_nsp')
    def __init__(self, **kwargs):
        super(GPT, self).__init__(**kwargs)

    def apply_embeddings(self, inputs):
        """token_embedding + segment_embedding + position_embedding, 其中 segment_embedding 共用 token_embedding
        与BERT 的主要区别是没有LayerNormalization
        """
        inputs = inputs[:]
        x = inputs.pop(0)
        if self.type_vocab_size > 0:
            s = inputs.pop(0)

        x = self.apply(inputs=x,
                     layer=Embedding,
                     name='Embedding-Token',
                     input_dim=self.vocab_size,
                     output_dim=self.embedding_size,
                     embeddings_initializer=self.initializer,
                     mask_zero=True
                     )

        if self.type_vocab_size > 0:
            if self.shared_segment_embeddings:
                name = 'Embedding-Token'
            else:
                name = 'Embedding-Segment'

            s = self.apply(s,
                           Embedding,
                           name=name,
                           input_dim=self.type_vocab_size,
                           output_dim=self.embedding_size,
                           embeddings_initializer=self.initializer,
                           )
            x = self.apply([x, s], Add, name='Embedding-Token-Segment')
        x = self.apply(x,
                       PositionEmbedding,
                       name='Embedding-Position',
                       input_dim=self.max_position,
                       output_dim=self.embedding_size,
                       embeddings_initializer=self.initializer,
                       merge_mode='add')

        x = self.apply(x,
                       Dropout,
                       name='Embedding-Dropout',
                       rate=self.dropout_rate)
        if self.hidden_size != self.embedding_size:
            x = self.apply(x,
                           Dense,
                           name='Embedding-Mapping',
                           units=self.hidden_size,
                           kernel_initializer=self.initializer)

        return x

    def apply_task_related(self, inputs):
        """
        Language Model部分
        """
        x = inputs
        x = self.apply(inputs=x,
                       layer=Embedding,
                       arguments={'mode': 'dense'},
                       name='Embedding-Token')
        x = self.apply(inputs=x,
                       layer=Activation,
                       activation=self.final_activation,
                       name='LM-Actication'
                       )
        return x

    def load_variable(self, checkpoint, name):
        variable = super(GPT, self).load_variable(checkpoint, name)
        if name == 'gpt/embeddings/word_embeddings':
            return self.load_embeddings(variable)
        else:
            return variable

    def variable_mapping(self):
        mapping = super(GPT, self).variable_mapping()
        mapping = {
            k: [i.replace('bert/','gpt/').replace('encoder', 'transformer') for i in v] for k, v in mapping.items()
        }
        return mapping


class GPT2(GPT):
    """
    GPT2
    """

    def get_inputs(self):
        x = self.apply(layer=Input, shape=(self.sequence_length,), name='Input-Token')
        return x

    def apply_embeddings(self, inputs):
        """
        GPT2的embedding 是token_embedding + position_embedding
        """
        x = inputs

        x = self.apply(inputs=x,
                       layer=Embedding,
                       input_dim=self.vocab_size,
                       output_dim=self.embedding_size,
                       embeddings_initializer=self.initializer,
                       mask_zero=True,
                       name='Embedding-Token'
                       )
        x = self.apply(inputs=x,
                       layer=PositionEmbedding,
                       input_dim=self.max_position,
                       output_dim=self.embedding_size,
                       merge_mode='add',
                       embeddings_initializer=self.initializer,
                       name='Embedding-Position')
        if self.embedding_size != self.hidden_size:
            x = self.apply(inputs=x,
                           layer=Dense,
                           units=self.hidden_size,
                           kernel_initializer=self.initializer,
                           name='Embedding-Mapping')

        return x

    def apply_transformer_layers(self, inputs, idx):
        """
        LN --> Att --> Dropout --> Add --> LN --> FFN --> Dropout --> Add
        """
        x = inputs
        z = self.layer_norm_conds[0]

        attention_name = 'Transformer-%d-MultiHeadSelfAttention' % idx
        feed_forward_name = 'Transformer-%d-FeedForward' % idx

        attention_bias = self.compute_attention_bias(idx)

        # self-attention
        x_pre = x

        x = self.apply(inputs=self.simplify([x, z]),
                       layer=LayerNormalization,
                       epsilon=1e-5,
                       conditional=(z is not None),
                       condition_hidden_units=self.layer_norm_conds[1],
                       condition_hidden_activation=self.layer_norm_conds[2],
                       condition_hidden_initializer=self.initializer,
                       name='%s-Norm' % attention_name,
                       )

        x = self.apply_attention([x, x, x, attention_bias], attention_name, arguments={'a_bias': True})

        x = self.apply(x,
                       Dropout,
                       name='%s-Dropout' % attention_name,
                       rate=self.dropout_rate)

        x = self.apply([x_pre, x],
                       Add,
                       name='%s-Add' % attention_name
                       )

        # feedforward
        x_pre = x
        x = self.apply(inputs=self.simplify([x, z]),
                       layer=LayerNormalization,
                       epsilon=1e-5,
                       conditional=(z is not None),
                       condition_hidden_units=self.layer_norm_conds[1],
                       condition_hidden_activation=self.layer_norm_conds[2],
                       condition_hidden_initializer=self.initializer,
                       name='%s-Norm' % feed_forward_name)
        x = self.apply(x,
                       FeedForward,
                       name=feed_forward_name,
                       units=self.intermediate_size,
                       activation=self.hidden_act,
                       kernel_initializer=self.initializer
                       )
        x = self.apply(x,
                       Dropout,
                       name='%s-Dropout' % feed_forward_name,
                       rate=self.dropout_rate)
        x = self.apply([x_pre, x],
                       Add,
                       name='%s-Add' % feed_forward_name)

        return x

    def apply_task_related(self, inputs):
        """GPT2做language model时先做了LanyerNormalization + Dropout，然后预测token
        """
        x = inputs
        z = self.layer_norm_conds[0]

        x = self.apply(inputs=self.simplify([x, z]),
                       layer=LayerNormalization,
                       epsilon=1e-5,
                       conditional=(z is not None),
                       condition_hidden_units=self.layer_norm_conds[1],
                       condition_hidden_activation=self.layer_norm_conds[2],
                       condition_hidden_initializer=self.initializer,
                       name='Output-Norm')
        x = self.apply(
            inputs=x,
            layer=Dropout,
            rate=self.dropout_rate,
            name='Output-Dropout'
        )
        x = super(GPT2, self).apply_task_related(x)
        return x

    def variable_mapping(self):
        mapping = super(GPT2, self).variable_mapping()
        mapping = {
            k: [i.replace('output/LayerNorm', 'input/LayerNorm') for i in v]
            for k, v in mapping.items()
        }
        mapping['Output-Norm'] = ['gpt/output/LayerNorm/beta', 'gpt/output/LayerNorm/gamma']
        return mapping


class GPT2ForSequenceClassification(GPT2):
    """
    GPT2 做分类任务，模型的改变主要是将lm_head 去掉拼了一个dense 层，同时只使用了最后一个'有效' token 对应的output
    当label ==1 时，做回归任务，当label > 1 时，为分类任务
    """
    def __init__(self, num_labels=1, pad_token_id=None, **kwargs):
        super(GPT2ForSequenceClassification, self).__init__(**kwargs)
        self.num_labels = num_labels
        self.pad_token_id = pad_token_id  # 用来寻找最后一个有效token 的位置，如果不指定，则选最后一个
        self.final_activation = 'sigmoid' if num_labels == 1 else 'softmax'

    def apply_task_related(self, inputs):
        """LanyerNormalization --> Dropout  --> GatherLastToken  --> Dense
        """
        x = inputs
        z = self.layer_norm_conds[0]

        x = self.apply(inputs=self.simplify([x, z]),
                       layer=LayerNormalization,
                       epsilon=1e-5,
                       conditional=(z is not None),
                       condition_hidden_units=self.layer_norm_conds[1],
                       condition_hidden_activation=self.layer_norm_conds[2],
                       condition_hidden_initializer=self.initializer,
                       name='Output-Norm')

        x = self.apply(
            inputs=x,
            layer=Dropout,
            rate=self.dropout_rate,
            name='Output-Dropout'
        )
        # extract last token output
        x = self.apply(
            inputs=[x, self.inputs[0]],
            layer=GatherLastToken,
            pad_token_id=self.pad_token_id,
        )

        x = self.apply(
            inputs=x,
            layer=Dense,
            units=self.num_labels,
            kernel_initializer=self.initializer,
            use_bias=False,
            name='Output-Score',
            activation=self.final_activation
        )

        return x

    def variable_mapping(self):
        mapping = super(GPT2ForSequenceClassification, self).variable_mapping()
        mapping['Output-Score'] = ['gpt/output/score']
        return mapping


class ELECTRA(BERT):
    @remove_arguments('with_mlm', 'with_pool')
    def __init__(self, max_position, **kwargs):
        super(ELECTRA, self).__init__(max_position, **kwargs)

    def variable_mapping(self):
        mapping = super(ELECTRA, self).variable_mapping()
        mapping = {k: [name.replace('bert/', 'electra/') for name in v] for k, v in mapping.items()}
        # embedding mapping
        mapping['Embedding-Mapping'] = [
            'electra/embeddings_project/kernel',
            'electra/embeddings_project/bias',
        ]
        return mapping

    def apply_task_related(self, inputs):
        return inputs


class NEZHA(BERT):
    """
    出自华为诺亚方舟实验室的NEZHA模型，结构上的改进是替换bert中的绝对位置编码为相对位置编码

    ref: [NEZHA: Neural Contextualized Representation for Chinese Language Understanding](http://arxiv.org/abs/1909.00204)
    """

    def __init__(self,
                 external_embedding_size=None,
                 external_embedding_weights=None,
                 **kwargs):
        """
        增加引入外部embedding
        """

        super(NEZHA, self).__init__(**kwargs)
        self.external_embedding_size = external_embedding_size  # 外部embedding 输出维度
        self.external_embedding_weights = external_embedding_weights  # 外部embedding 初始化权重

    def apply_embeddings(self, inputs):
        """
        embedding 是 token embedding 与 segment embedding 的和
        """
        x, s = inputs[:2]
        z = self.layer_norm_conds[0]
        token_embedding = self.apply(inputs=x,
                                     layer=Embedding,
                                     name='Embedding-Token',
                                     input_dim=self.vocab_size,
                                     output_dim=self.embedding_size,
                                     embeddings_initializer=self.initializer,
                                     mask_zero=True
                                     )
        segment_embedding = self.apply(s,
                                       Embedding,
                                       name='Embedding-Segment',
                                       input_dim=2,
                                       output_dim=self.embedding_size,
                                       embeddings_initializer=self.initializer,
                                       )
        token_with_segment = self.apply([token_embedding, segment_embedding], Add, name='Embedding-Token-Segment')

        # add External knowledge
        if self.external_embedding_size:
            external_embedding = self.apply(x,
                                            Embedding,
                                            name='Embedding-External',
                                            input_dim=self.vocab_size,
                                            output_dim=self.external_embedding_size,
                                            weights=[self.external_embedding_weights]
                                            )
            if self.external_embedding_size != self.embedding_size:
                external_embedding = self.apply(external_embedding,
                                                Dense,
                                                name='External-Embedding-Mapping',
                                                units=self.embedding_size,
                                                kernel_initializer=self.initializer)
            x = self.apply([token_with_segment, external_embedding], Add, name='Embedding-Token-Segment-External')
        else:
            x = token_with_segment

        x = self.apply(inputs=self.simplify([x, z]),
                       layer=LayerNormalization,
                       conditional=(z is not None),
                       condition_hidden_units=self.layer_norm_conds[1],
                       condition_hidden_activation=self.layer_norm_conds[2],
                       condition_hidden_initializer=self.initializer,
                       name='Embedding-Norm')
        x = self.apply(x,
                       Dropout,
                       name='Embedding-Dropout',
                       rate=self.dropout_rate)
        if self.hidden_size != self.embedding_size:
            x = self.apply(x,
                           Dense,
                           name='Embedding-Mapping',
                           units=self.hidden_size,
                           kernel_initializer=self.initializer)

        return x

    def apply_transformer_layers(self, inputs, idx):
        """
        Att --> Dropout --> Add --> LN --> FFN --> Dropout -->  Add --> LN
        """
        attention_name = 'Transformer-%d-MultiHeadSelfAttention' % idx
        feed_forward_name = 'Transformer-%d-FeedForward' % idx
        attention_bias = self.compute_attention_bias(idx)
        position_bias = self.compute_position_bias(inputs)

        x_pre, x = inputs, [inputs, inputs, inputs, position_bias]  # 加入相对位置编码
        z = self.layer_norm_conds[0]
        arguments = {'a_bias': None, 'position_bias': 'relative'}
        if attention_bias is not None:
            arguments['a_bias'] = True
            x.insert(3, attention_bias)

        x = self.apply_attention(x, attention_name, arguments)

        x = self.apply(x,
                       Dropout,
                       name='%s-Dropout' % attention_name,
                       rate=self.dropout_rate)

        x = self.apply([x_pre, x],
                       Add,
                       name='%s-Add' % attention_name
                       )

        x = self.apply(inputs=self.simplify([x, z]),
                       layer=LayerNormalization,
                       conditional=(z is not None),
                       condition_hidden_units=self.layer_norm_conds[1],
                       condition_hidden_activation=self.layer_norm_conds[2],
                       condition_hidden_initializer=self.initializer,
                       name='%s-Norm' % attention_name,
                       )

        # feedforward
        x_pre = x
        x = self.apply(x,
                       FeedForward,
                       name=feed_forward_name,
                       units=self.intermediate_size,
                       activation=self.hidden_act,
                       kernel_initializer=self.initializer
                       )
        x = self.apply(x,
                       Dropout,
                       name='%s-Dropout' % feed_forward_name,
                       rate=self.dropout_rate)
        x = self.apply([x_pre, x],
                       Add,
                       name='%s-Add' % feed_forward_name)
        x = self.apply(inputs=self.simplify([x, z]),
                       layer=LayerNormalization,
                       conditional=(z is not None),
                       condition_hidden_units=self.layer_norm_conds[1],
                       condition_hidden_activation=self.layer_norm_conds[2],
                       condition_hidden_initializer=self.initializer,
                       name='%s-Norm' % feed_forward_name)
        return x

    def compute_position_bias(self, inputs):
        """计算相对位置编码"""
        if self.position_bias is None:
            x = inputs
            self.position_bias = self.apply(
                inputs=[x, x],
                layer=RelativePositionEmbedding,
                name='Relative-Position-Embedding',
                input_dim=2 * 64 + 1,
                output_dim=self.attention_key_size,
                embedding_initializer='sinusoidal',
                trainable=False
            )

        return self.position_bias


class DBERT(BERT):
    """
    用连续的dgcnn来替换原始bert中的transformer block，来尝试压缩bert
    """

    def __init__(self, inner_hidden_size=None, **kwargs):
        prefix = kwargs.get('prefix', 'DBERT-')
        kwargs['prefix'] = prefix
        super(DBERT, self).__init__(**kwargs)
        self.inner_hidden_size = inner_hidden_size or self.attention_head_size  # dgcnn hidden dim

    def apply_transformer_layers(self, inputs, idx):
        """
            liner_in(inner_hid_dim) -> dgcnn(1) -> dgcnn(3) -> dgcnn(5) -> dgcnn(8) -> liner_out(hid_dim)
        """
        block_name = 'DBlock-%d-MultiDGCNN' % idx
        liner_in_name = 'DBlock-%d-MultiDGCNN-LinerIn' % idx
        liner_out_name = 'DBlock-%d-MultiDGCNN-LinerOut' % idx
        attention_mask = self.compute_attention_mask(idx)
        x = inputs
        x = self.apply(x,
                       Dense,
                       name=liner_in_name,
                       units=self.inner_hidden_size,
                       use_bias=False
                       )
        arguments = {}
        if attention_mask is not None:
            x.append(attention_mask)

        # dgcnn-block
        x = self.apply(x,
                       DGCNN,
                       name='{block_name}-DilationRate-{r}'.format(block_name=block_name, r=1),
                       dilation_rate=1,
                       dropout_rate=self.dropout_rate,
                       arguments=arguments)

        x = self.apply(x,
                       DGCNN,
                       name='{block_name}-DilationRate-{r}'.format(block_name=block_name, r=3),
                       dilation_rate=3,
                       dropout_rate=self.dropout_rate,
                       arguments=arguments)
        x = self.apply(x,
                       DGCNN,
                       name='{block_name}-DilationRate-{r}'.format(block_name=block_name, r=5),
                       dilation_rate=5,
                       dropout_rate=self.dropout_rate,
                       arguments=arguments)
        x = self.apply(x,
                       DGCNN,
                       name='{block_name}-DilationRate-{r}'.format(block_name=block_name, r=8),
                       dilation_rate=8,
                       dropout_rate=self.dropout_rate,
                       arguments=arguments)

        x = self.apply(x,
                       Dense,
                       name=liner_out_name,
                       units=self.hidden_size,
                       use_bias=False
                       )
        x = self.apply(x, LayerNormalization, name='DBlock-%d-MultiDGCNN-Norm' % idx)
        return x


def extend_with_language_model(BaseModel):
    """
    增加下三角mask矩阵，作为语言模型使用
    """

    class LanguageModel(LM_Mask, BaseModel):
        def __init__(self, *args, **kwargs):
            super(LanguageModel, self).__init__(*args, **kwargs)
            self.with_mlm = self.with_mlm or True  # mlm output

    return LanguageModel


def extend_with_unilm(BaseModel):
    """添加UniLM mask"""

    class UniLM(UniLM_Mask, BaseModel):
        """UnilM-V1: https://arxiv.org/pdf/1905.03197.pdf"""

        def __init__(self, *args, **kwargs):
            super(UniLM, self).__init__(*args, **kwargs)
            self.with_mlm = self.with_mlm or True  # mlm output

    return UniLM


def extend_with_residual_attention(BaseModel):
    """添加当前attention scores 与前一层attention scores的直通路"""

    class RealFormer(BaseModel):
        """RealFormer: https://arxiv.org/pdf/2012.11747.pdf"""

        def __init__(self, *args, **kwargs):
            super(RealFormer, self).__init__(*args, **kwargs)
            self.with_residual_attention = True

        def compute_attention_bias(self, inputs=None):
            """
            将residual attention scores 加入 attention bias
            :param inputs: transformer layer idx
            """
            att_bias = super(RealFormer, self).compute_attention_bias(inputs)

            if self.attention_scores is not None and att_bias is not None:
                att_bias = self.apply([self.attention_scores, att_bias],
                                      Add,
                                      name='Transformer-%d-Attention-bias-Add' % inputs,
                                      )

            att_bias = att_bias if att_bias is not None else self.attention_scores
            return att_bias

    return RealFormer


class ReZero(BERT):
    def __init__(self,
                 use_layernorm=None,  # None, pre, post, when None, then rezero
                 init_reweight=1.,  # init of reweight
                 reweight_trainable=True,
                 **kwargs,
                 ):
        super(ReZero, self).__init__(**kwargs)
        assert use_layernorm in [None, 'pre', 'post']
        self.use_layernorm = use_layernorm
        self.init_reweight = init_reweight
        self.reweight_trainable = reweight_trainable

    def apply_embeddings(self, inputs):
        """token_embedding + segment_embedding + position_embedding
        """
        x, s = inputs[:2]
        # condition layer norm
        z = self.layer_norm_conds[0]

        token_embedding = self.apply(inputs=x,
                                     layer=Embedding,
                                     name='Embedding-Token',
                                     input_dim=self.vocab_size,
                                     output_dim=self.embedding_size,
                                     embeddings_initializer=self.initializer,
                                     mask_zero=True
                                     )
        segment_embedding = self.apply(s,
                                       Embedding,
                                       name='Embedding-Segment',
                                       input_dim=self.type_vocab_size,
                                       output_dim=self.embedding_size,
                                       embeddings_initializer=self.initializer,
                                       )
        token_with_seg = self.apply([token_embedding, segment_embedding], Add, name='Embedding-Token-Segment')
        x = self.apply(token_with_seg,
                       PositionEmbedding,
                       name='Embedding-Position',
                       input_dim=self.max_position,
                       output_dim=self.embedding_size,
                       embeddings_initializer=self.initializer,
                       merge_mode='add')

        # if pre layernorm, then delete layernorm in this block
        if self.use_layernorm != 'pre':
            x = self.apply(inputs=self.simplify([x, z]),
                           layer=LayerNormalization,
                           conditional=(z is not None),
                           condition_hidden_units=self.layer_norm_conds[1],
                           condition_hidden_activation=self.layer_norm_conds[2],
                           condition_hidden_initializer=self.initializer,
                           name='Embedding-Norm')
        x = self.apply(x,
                       Dropout,
                       name='Embedding-Dropout',
                       rate=self.dropout_rate)
        if self.hidden_size != self.embedding_size:
            x = self.apply(x,
                           Dense,
                           name='Embedding-Mapping',
                           units=self.hidden_size,
                           kernel_initializer=self.initializer)

        return x

    def apply_transformer_layers(self, inputs, idx):
        """
        post: Att --> Dropout --> Add --> LN --> FFN --> Dropout -->  Add --> LN
        pre: LN --> Att --> Dropout --> Add --> LN --> FFN --> Dropout --> Add
        rezero: Att --> ReWeight --> Dropout --> Add --> FFN -->ReWeight --> Dropout --> Add
        """
        attention_name = 'Transformer-%d-MultiHeadSelfAttention' % idx
        feed_forward_name = 'Transformer-%d-FeedForward' % idx
        attention_bias = self.compute_attention_bias(idx)

        x_pre, x = inputs, inputs
        z = self.layer_norm_conds[0]
        arguments = {'a_bias': None}
        if attention_bias is not None:
            arguments['a_bias'] = True
            x.append(attention_bias)

        if self.use_layernorm == 'pre':
            x = self.apply(inputs=self.simplify([x, z]),
                           layer=LayerNormalization,
                           conditional=(z is not None),
                           condition_hidden_units=self.layer_norm_conds[1],
                           condition_hidden_activation=self.layer_norm_conds[2],
                           condition_hidden_initializer=self.initializer,
                           name='%s-Norm' % attention_name,
                           )

        x = [x, x, x]
        # self-attention
        x = self.apply_attention(x, attention_name, arguments)

        # reweight residual-connection
        x = self.apply(x,
                       ReWeight,
                       name='%s-ReWeight' % attention_name,
                       init_reweight=self.init_reweight,
                       trainable=self.reweight_trainable
                       )

        x = self.apply(x,
                       Dropout,
                       name='%s-Dropout' % attention_name,
                       rate=self.dropout_rate)

        x = self.apply([x_pre, x],
                       Add,
                       name='%s-Add' % attention_name
                       )
        if self.use_layernorm == 'post':
            x = self.apply(inputs=self.simplify([x, z]),
                           layer=LayerNormalization,
                           conditional=(z is not None),
                           condition_hidden_units=self.layer_norm_conds[1],
                           condition_hidden_activation=self.layer_norm_conds[2],
                           condition_hidden_initializer=self.initializer,
                           name='%s-Norm' % attention_name,
                           )

        # feedforward
        x_pre = x
        if self.use_layernorm == 'pre':
            x = self.apply(inputs=self.simplify([x, z]),
                           layer=LayerNormalization,
                           conditional=(z is not None),
                           condition_hidden_units=self.layer_norm_conds[1],
                           condition_hidden_activation=self.layer_norm_conds[2],
                           condition_hidden_initializer=self.initializer,
                           name='%s-Norm' % feed_forward_name
                           )

        x = self.apply(x,
                       FeedForward,
                       name=feed_forward_name,
                       units=self.intermediate_size,
                       activation=self.hidden_act,
                       kernel_initializer=self.initializer
                       )

        # reweight residual-connection
        x = self.apply(x,
                       ReWeight,
                       name='%s-ReWeight' % feed_forward_name,
                       init_reweight=self.init_reweight,
                       trainable=self.reweight_trainable
                       )
        x = self.apply(x,
                       Dropout,
                       name='%s-Dropout' % feed_forward_name,
                       rate=self.dropout_rate)

        x = self.apply([x_pre, x],
                       Add,
                       name='%s-Add' % feed_forward_name)
        if self.use_layernorm == 'post':
            x = self.apply(inputs=self.simplify([x, z]),
                           layer=LayerNormalization,
                           conditional=(z is not None),
                           condition_hidden_units=self.layer_norm_conds[1],
                           condition_hidden_activation=self.layer_norm_conds[2],
                           condition_hidden_initializer=self.initializer,
                           name='%s-Norm' % feed_forward_name)

        return x


class ALBERT(BERT):
    def apply_transformer_layers(self, inputs, idx):
        """
        Att -->  Dropout --> Add --> LN --> FFN --> Dropout --> Add --> LN
        """
        attention_name = 'Transformer-MultiHeadSelfAttention'
        feed_forward_name = 'Transformer-FeedForward'
        attention_bias = self.compute_attention_bias(idx)

        x_pre, x = inputs, [inputs, inputs, inputs]
        z = self.layer_norm_conds[0]
        arguments = {'a_bias': None}
        if attention_bias is not None:
            arguments['a_bias'] = True
            x.append(attention_bias)

        x = self.apply_attention(x, attention_name, arguments)

        x = self.apply(x,
                       Dropout,
                       name='%s-Dropout' % attention_name,
                       rate=self.dropout_rate)

        x = self.apply([x_pre, x],
                       Add,
                       name='%s-Add' % attention_name
                       )

        x = self.apply(inputs=self.simplify([x, z]),
                       layer=LayerNormalization,
                       conditional=(z is not None),
                       condition_hidden_units=self.layer_norm_conds[1],
                       condition_hidden_activation=self.layer_norm_conds[2],
                       condition_hidden_initializer=self.initializer,
                       name='%s-Norm' % attention_name,
                       )

        # feedforward
        x_pre = x
        x = self.apply(x,
                       FeedForward,
                       name=feed_forward_name,
                       units=self.intermediate_size,
                       activation=self.hidden_act,
                       kernel_initializer=self.initializer
                       )
        x = self.apply(x,
                       Dropout,
                       name='%s-Dropout' % feed_forward_name,
                       rate=self.dropout_rate)
        x = self.apply([x_pre, x],
                       Add,
                       name='%s-Add' % feed_forward_name)
        x = self.apply(inputs=self.simplify([x, z]),
                       layer=LayerNormalization,
                       conditional=(z is not None),
                       condition_hidden_units=self.layer_norm_conds[1],
                       condition_hidden_activation=self.layer_norm_conds[2],
                       condition_hidden_initializer=self.initializer,
                       name='%s-Norm' % feed_forward_name)
        return x

    def variable_mapping(self):
        mapping = super(ALBERT, self).variable_mapping()

        prefix = 'bert/encoder/transformer/group_0/inner_group_0/'
        mapping.update({
            'Transformer-MultiHeadSelfAttention': [
                prefix + 'attention_1/self/query/kernel',
                prefix + 'attention_1/self/query/bias',
                prefix + 'attention_1/self/key/kernel',
                prefix + 'attention_1/self/key/bias',
                prefix + 'attention_1/self/value/kernel',
                prefix + 'attention_1/self/value/bias',
                prefix + 'attention_1/output/dense/kernel',
                prefix + 'attention_1/output/dense/bias',
            ],
            'Transformer-MultiHeadSelfAttention-Norm': [
                prefix + 'LayerNorm/beta',
                prefix + 'LayerNorm/gamma',
            ],
            'Transformer-FeedForward': [
                prefix + 'ffn_1/intermediate/dense/kernel',
                prefix + 'ffn_1/intermediate/dense/bias',
                prefix + 'ffn_1/intermediate/output/dense/kernel',
                prefix + 'ffn_1/intermediate/output/dense/bias',
            ],
            'Transformer-FeedForward-Norm': [
                prefix + 'LayerNorm_1/beta',
                prefix + 'LayerNorm_1/gamma',
            ],
        })

        return mapping


def build_transformer_model(
        config_path=None,
        checkpoint_path=None,
        model='bert',
        application='encoder',
        return_keras_model=True,
        **kwargs
):
    """根据配置文件构建模型，可选加载checkpoint权重
    """
    configs = {}
    if config_path is not None:
        configs.update(json.load(open(config_path)))
    configs.update(kwargs)
    # convert config name
    if 'max_position' not in configs:
        configs['max_position'] = configs.get('max_position_embeddings')
    if 'dropout_rate' not in configs:
        configs['dropout_rate'] = configs.get('hidden_dropout_prob')

    models = {
        'bert': BERT,
        'reberta': BERT,
        'nezha': NEZHA,
        'electra': ELECTRA,
        'albert': ALBERT,
        'dbert': DBERT,
        'rezero': ReZero,
        'gpt': GPT,
        'gpt2': GPT2,
    }

    if isinstance(model, six.string_types):
        model = model.lower()
        MODEL = models[model]
    else:
        MODEL = model

    application = application.lower()
    if application == 'lm':
        MODEL = extend_with_language_model(MODEL)
    elif application == 'unilm':
        MODEL = extend_with_unilm(MODEL)

    if kwargs.get('with_residual_attention'):
        MODEL = extend_with_residual_attention(MODEL)

    transformer = MODEL(**configs)
    transformer.build(**configs)

    if checkpoint_path is not None:
        transformer.load_weights_from_checkpoint(checkpoint_path)

    if return_keras_model:
        return transformer.model
    else:
        return transformer
