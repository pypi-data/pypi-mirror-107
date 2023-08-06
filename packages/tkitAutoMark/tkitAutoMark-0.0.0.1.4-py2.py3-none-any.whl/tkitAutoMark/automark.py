# -*- coding: utf-8 -*-
from torch.utils.data import DataLoader, random_split
import pytorch_lightning as pl
import torch.nn as nn
# from reformer_pytorch import ReformerLM,Autopadder
# from performer_pytorch import PerformerLM

# https://pytorch-crf.readthedocs.io/en/stable/
from torchcrf import CRF

# from reformer_pytorch.generative_tools import TrainingWrapper
from tkitbilstm import BiLSTMAttention
import random
# import tqdm
# import gzip
# import numpy as np
import torch
import torch.optim as optim
from torch.nn import functional as F
from torch.utils.data import DataLoader, Dataset

from performer_pytorch import PerformerLM
# from transformers import BertTokenizer, BertModel,BertForMaskedLM,AutoModelForMaskedLM

from argparse import ArgumentParser
# hparams=parse_args()
# from transformers import AutoTokenizer,AutoModel,BertForMaskedLM,AutoModelForMaskedLM,BertModel,BertTokenizer
# https://pytorch-lightning.readthedocs.io/en/latest/common/lightning_module.html
from pytorch_lightning.metrics import functional as FM
from torch.nn import CrossEntropyLoss, MSELoss
# from omegaconf import OmegaConf

from tkit_transformer_xl import Transformer_xl
from tkit_mlp_pytorch import MLP


class AutoMark(pl.LightningModule):
    """NER类似标注
    参考 https://huggingface.co/transformers/_modules/transformers/models/bert/modeling_bert.html#BertForSequenceClassification
    """

    def __init__(self, max_seq_len=512, learning_rate=1e-4, depth=3, depth_mlp=1, memory_layers=[2, 3],
                 dropout=0.1, dim=128,num_labels=2, num_tokens=8021,
                 frequency=1, pretrained="PerformerLM128", bilstm_enabled=False, patience=100, causal=True, memory_transformer_xl=False, T_max=5, **kwargs):
        """[summary]
        初始化序列标注任务，优先使用performer

        Args:
            max_seq_len (int, optional): [description]. Defaults to 512.
            learning_rate ([type], optional): [description]. Defaults to 1e-4.
            depth (int, optional): [description]. Defaults to 3.
            depth_mlp (int, optional): [description]. Defaults to 1.
            memory_layers (list, optional): [description]. Defaults to [2, 3].
            dropout (float, optional): [description]. Defaults to 0.1.
            dim (int, optional): [description]. Defaults to 128.
            warmup (int, optional): [description]. Defaults to 1000.
            num_labels (int, optional): [description]. Defaults to 2.
            num_tokens (int, optional): [description]. Defaults to 8021.
            frequency (int, optional): [description]. Defaults to 10.
            pretrained (str, optional): [description]. Defaults to "PerformerLM128，memory_transformer_xl，bilstm".
            bilstm_enabled (bool, optional): [description]. Defaults to False.
            patience (int, optional): [description]. Defaults to 100.
            causal (bool, optional): [description]. Defaults to True.
            memory_transformer_xl (bool, optional): [description]. Defaults to False.
            T_max (int, optional): [description]. Defaults to 5.
        """
        super().__init__()
        self.save_hyperparameters()
        self.maxlen = max_seq_len
        # 是否启用bilstm
        self.bilstm_enabled = bilstm_enabled
#         print(**kwargs)
#         将参数存进hparams
#         conf = OmegaConf.create({"num_labels" : 2,**kwargs})

        self.num_labels = num_labels
        self.pretrained = pretrained

        if pretrained == "memory_transformer_xl":
            #         tokenizer = BertTokenizer.from_pretrained('hfl/chinese-electra-180g-small-ex-discriminator')
            #             from memory_transformer_xl import MemoryTransformerXL
            self.model = Transformer_xl(dim=self.hparams.dim, heads=8, seq_len=512, mem_write_iters=2,
                                        max_batch_size=8, lmem_len=512, mem_len=256, memory_layers=self.hparams.memory_layers,
                                        num_mem_kv=128, depth=self.hparams.depth, causal=self.hparams.causal, T_max=500, attn_dropout=0.1,
                                        memory_transformer_xl=True,
                                        ff_glu=False, ff_dropout=0.1, attn_layer_dropout=0.1, num_tokens=num_tokens,)

#         elif pretrained!="memory_transformer_xl" and self.hparams.memory_transformer_xl==False :
        elif pretrained == "memory_transformer_xlFalse":
            #             from tkit_transformer_xl import Transformer_xl
            self.model = Transformer_xl(dim=self.hparams.dim, heads=8, seq_len=512, mem_write_iters=2,
                                        max_batch_size=8, lmem_len=512, mem_len=256, memory_layers=self.hparams.memory_layers,
                                        num_mem_kv=128, depth=self.hparams.depth, causal=self.hparams.causal, T_max=500, attn_dropout=0.1,
                                        memory_transformer_xl=False, ff_glu=False, ff_dropout=0.1, attn_layer_dropout=0.1, num_tokens=num_tokens,)

        elif pretrained == "bilstm":
            #             from tkit_transformer_xl import Transformer_xl
            self.model = BiLSTMAttention(vocab_size=21128, dim=self.hparams.dim,
                                            n_hidden=self.hparams.dim, out_num_classes=self.hparams.dim, embedding_enabled=True)
#             self.classifier=MLP(depth=depth_mlp,dim=dim,input_dim=dim,out_dim=self.num_labels)
        else:
            self.model = PerformerLM(
                num_tokens=num_tokens,
                max_seq_len=4096,             # max sequence length
                dim=self.hparams.dim,                      # dimension
                depth=self.hparams.depth,                     # layers
                heads=8,                      # heads
                causal=False,                 # auto-regressive or not
                # number of random features, if not set, will default to (d * log(d)), where d is the dimension of each head
                nb_features=256,
                # how frequently to redraw the projection matrix, the more frequent, the slower the training
                feature_redraw_interval=1000,
                # defaults to softmax approximation, but can be set to True for generalized attention
                generalized_attention=False,
                # the kernel function to be used, if generalized attention is turned on, defaults to Relu
                kernel_fn=nn.LeakyReLU(),
                reversible=True,              # reversible layers, from Reformer paper
                ff_chunks=10,                 # chunk feedforward layer, from Reformer paper
                use_scalenorm=False,          # use scale norm, from 'Transformers without Tears' paper
                use_rezero=False,             # use rezero, from 'Rezero is all you need' paper
                #                 tie_embedding = False,          # multiply final embeddings with token weights for logits, like gpt decoder
                ff_glu=True,                  # use GLU variant for feedforward
                emb_dropout=0.1,              # embedding dropout
                ff_dropout=0.1,               # feedforward dropout
                attn_dropout=0.1,             # post-attn dropout
                # 4 heads are local attention, 4 others are global performers
                local_attn_heads=4,
                local_window_size=256,        # window size of local attention
                rotary_position_emb=True      # use rotary positional embedding, which endows linear attention with relative positional encoding with no learned parameters. should always be turned on unless if you want to go back to old absolute positional encoding
            )

        if pretrained == "bilstm":
            #             from tkit_transformer_xl import Transformer_xl
            #             self.model=LitBiLSTMAttention(vocab_size=21128,dim=self.hparams.dim,n_hidden=self.hparams.dim,out_num_classes=self.hparams.dim,embedding_enabled=True)
            self.classifier = MLP(depth=depth_mlp, dim=dim,
                                  input_dim=dim*2, out_dim=self.num_labels)
        else:
            self.classifier = MLP(depth=depth_mlp, dim=dim,
                                  input_dim=num_tokens, out_dim=self.num_labels)

        self.crf = CRF(self.num_labels, batch_first=True)
        self.f1_loss = F1_Loss_crf()
        self.learning_rate = learning_rate
        # self.warmup = warmup
        self.frequency = frequency  # 每多少次检查变化
        self.patience = patience  # 多少次不变化后更新
        self.T_max = T_max  # 默认设为step重置步数

    def forward(self, x, y=None, return_pred=False):
        """训练梯度"""
        # in lightning, forward defines the prediction/inference actions

        if self.hparams.pretrained == "bilstm":
            last_hidden_state, _, _ = self.model(x)
#             print(last_hidden_state.size())
            pass
        else:
            last_hidden_state = self.model(x)

        last_hidden_state = self.classifier(last_hidden_state)
#         last_hidden_state = self.dropout2(last_hidden_state) # 获取第一个输出
        # 调整矩阵形状.permute(1,0)
        loss = None
        if return_pred:
            pred = torch.tensor(self.crf.decode(
                last_hidden_state)).to(self.device)
        else:
            pred = None
        if y != None:
            #         print(last_hidden_state.size(),tags.size())
            #         loss=-1 * self.crf(last_hidden_state,tags,mask=attention_mask.byte(), reduction='token_mean')# reduction="token_mean",
            loss = -1 * self.crf(last_hidden_state, y, reduction='token_mean')
#         print(last_hidden_state.size(),attention_mask.size())
#         pred=torch.tensor(self.crf.decode(last_hidden_state,mask=attention_mask.byte())).to(self.device)

#         print("pred",pred)

        return pred, loss

    def training_step(self, batch, batch_idx):
        """一次batch训练"""
        # training_step defined the train loop.
        # It is independent of forward
#         print(batch[0].size(),batch[-1].size())
#         print(batch[0].view(-1,128).size(),batch[-1].view(-1,128).size())

        # 进行随机截断
#         from random import choice
#         ranCut=choice([1,2,4])
#         clen=int(self.maxlen/ranCut)
        _, loss = self(x=batch[0], y=batch[-1])
        # Logging to TensorBoard by default
#         print(('train_loss', loss))
        self.log('train_loss', loss)
        return loss

    def validation_step(self, batch, batch_idx):
        """单个批次验证"""
        # training_step defined the train loop.
        # It is independent of forward
#         print(batch[0].view(-1,128).size(),batch[-1].view(-1,128).size())
        pred, loss = self(x=batch[0], y=batch[-1], return_pred=True)
#         print(pred, batch[-1].view(-1,self.maxlen))
#         print(('val_loss', loss))
#         acc = FM.accuracy(torch.softmax(pred,dim=1), batch[1])

#         print(pred, batch[-1].view(-1,self.maxlen))
        acc = FM.accuracy(pred, batch[-1])
        f1 = self.f1_loss(pred, batch[-1])
#         print(f1)
        # Logging to TensorBoard by default
#         self.log('test_loss', loss)
        metrics = {'val_f1': f1, 'val_acc': acc, 'val_loss': loss}

        self.log_dict(metrics)
        return metrics

    def test_step(self, batch, batch_idx):
        """一次batch训练"""
        # training_step defined the train loop.
        # It is independent of forward

        pred, loss = self(x=batch[0], y=batch[-1], return_pred=True)
#         acc = FM.accuracy(pred, batch[-1])
#         print(torch.argmax(torch.softmax(pred,dim=1),dim=1),batch[-1])
#
        acc = FM.accuracy(pred, batch[-1])

        # print("pred", pred)
        # print("y", batch[-1])
        # Logging to TensorBoard by default
        metrics = {'test_acc': acc, 'test_loss': loss}
        self.log_dict(metrics)
        return metrics

    def configure_optimizers(self):
        """优化器 # 类似于余弦，但其周期是变化的，初始周期为T_0,而后周期会✖️T_mult。每个周期学习率由大变小； https://www.notion.so/62e72678923f4e8aa04b73dc3eefaf71"""
#         optimizer = torch.optim.AdamW(self.parameters(), lr=(self.learning_rate))

        # 只优化部分
        optimizer = torch.optim.AdamW(
            self.parameters(), lr=(self.learning_rate))
        #         使用自适应调整模型

#
#         scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(optimizer, self.T_max, eta_min=5e-8, last_epoch=-1, verbose=True)
#         T_mult=int(self.T_max/5)
        T_mult = 2
        scheduler = torch.optim.lr_scheduler.CosineAnnealingWarmRestarts(
            optimizer, T_0=self.T_max, T_mult=T_mult, eta_min=0, verbose=True)
#         https://github.com/PyTorchLightning/pytorch-lightning/blob/6dc1078822c33fa4710618dc2f03945123edecec/pytorch_lightning/core/lightning.py#L1119

        lr_scheduler = {
            #            'optimizer': optimizer,
            'scheduler': scheduler,
            #             'reduce_on_plateau': True, # For ReduceLROnPlateau scheduler
            'interval': 'epoch',  # epoch
            'frequency': self.frequency,
            'name': "lr_scheduler",
            'monitor': 'train_loss',  # 监听数据变化
            'strict': True,
        }

        return {'optimizer': optimizer, 'lr_scheduler': scheduler}


class F1_Loss_crf(nn.Module):
    '''Calculate F1 score. Can work with gpu tensors
    https://gist.github.com/SuperShinyEyes/dcc68a08ff8b615442e3bc6a9b55a354

    The original implmentation is written by Michal Haltuf on Kaggle.

    Returns
    -------
    torch.Tensor
        `ndim` == 1. epsilon <= val <= 1

    Reference
    ---------
    - https://www.kaggle.com/rejpalcz/best-loss-function-for-f1-score-metric
    - https://scikit-learn.org/stable/modules/generated/sklearn.metrics.f1_score.html#sklearn.metrics.f1_score
    - https://discuss.pytorch.org/t/calculating-precision-recall-and-f1-score-in-case-of-multi-label-classification/28265/6
    - http://www.ryanzhang.info/python/writing-your-own-loss-function-module-for-pytorch/
    '''

    def __init__(self, epsilon=1e-7, num_classes=65):
        super().__init__()
        self.epsilon = epsilon
        self.num_classes = num_classes

    def forward(self, y_pred, y_true,):
        """
        y_pred, y_true维度为2
        """
        assert y_pred.ndim == 2
        assert y_true.ndim == 2
        y_true = F.one_hot(y_true, self.num_classes).to(torch.float32)
        #
        y_pred = F.one_hot(y_pred, self.num_classes).to(torch.float32)

        y_pred = F.softmax(y_pred, dim=1)

        tp = (y_true * y_pred).sum(dim=0).to(torch.float32)
        tn = ((1 - y_true) * (1 - y_pred)).sum(dim=0).to(torch.float32)
        fp = ((1 - y_true) * y_pred).sum(dim=0).to(torch.float32)
        fn = (y_true * (1 - y_pred)).sum(dim=0).to(torch.float32)

        precision = tp / (tp + fp + self.epsilon)
        recall = tp / (tp + fn + self.epsilon)

        f1 = 2 * (precision*recall) / (precision + recall + self.epsilon)
        f1 = f1.clamp(min=self.epsilon, max=1-self.epsilon)
        return 1 - f1.mean()
