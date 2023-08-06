# -*- coding: utf-8 -*-
import torch
import torch.optim as optim
from torch.nn import functional as F
# from torch.utils.data import DataLoader, random_split
import pytorch_lightning as pl
import torch.nn as nn

class BiLSTMAttention(pl.LightningModule):
    """
    Bilstm Attention包含
    是否是启用嵌入 ，默认不启用
    
    https://colab.research.google.com/drive/1jX8mvJ_8oulueGEMmLg3is5qRdhuDmgz#scrollTo=4YGiToFOZgXx
    """

    def __init__(self,vocab_size=8021, dim=10,n_hidden=10,out_num_classes=10,embedding_enabled=False,attention=True,**kwargs):
        """[summary]
        实现简单的双向长短记忆

        Args:
            vocab_size (int, optional): [字典大小 建议使用 https://github.com/CLUEbenchmark/CLUECorpus2020 里的词典8021，可以有效降低模型大小]. Defaults to 8021.
            dim (int, optional): [维度]. Defaults to 10.
            n_hidden (int, optional): [隐藏层]. Defaults to 10.
            out_num_classes (int, optional): [输出的维度]. Defaults to 10.
            embedding_enabled (bool, optional): [是否启用编码层]. Defaults to False.
            attention (bool, optional): [是启用注意力]. Defaults to False.
        """
        super().__init__()
        self.save_hyperparameters()
        if self.hparams.embedding_enabled:
            self.embedding = nn.Embedding(vocab_size, dim)
        else:
            pass
        self.lstm = nn.LSTM(dim, n_hidden, bidirectional=True)
        self.out = nn.Linear(n_hidden * 2, out_num_classes)


    def attention_net(self, lstm_output, final_state):
        hidden = final_state.view(-1, self.hparams.n_hidden * 2, 1)   # hidden : [batch_size, n_hidden * num_directions(=2), 1(=n_layer)]
        attn_weights = torch.bmm(lstm_output, hidden).squeeze(2) # attn_weights : [batch_size, n_step]
        soft_attn_weights = F.softmax(attn_weights, 1)
        # [batch_size, n_hidden * num_directions(=2), n_step] * [batch_size, n_step, 1] = [batch_size, n_hidden * num_directions(=2), 1]
        context = torch.bmm(lstm_output.transpose(1, 2), soft_attn_weights.unsqueeze(2)).squeeze(2)
        return context, soft_attn_weights.cpu().data.numpy() # context : [batch_size, n_hidden * num_directions(=2)]
    def forward(self, x):
        # in lightning, forward defines the prediction/inference actions
        if self.hparams.embedding_enabled:
            input = self.embedding(x) # input : [batch_size, len_seq, embedding_dim]
        else:
            input = x
        # print("input",input)
        #进行维度转换
        input = input.permute(1, 0, 2) # input : [len_seq, batch_size, embedding_dim]

        hidden_state = torch.zeros(1*2, len(x),  self.hparams.n_hidden).to(self.device) # [num_layers(=1) * num_directions(=2), batch_size, n_hidden]
        cell_state = torch.zeros(1*2, len(x),  self.hparams.n_hidden).to(self.device) # [num_layers(=1) * num_directions(=2), batch_size, n_hidden]

        # final_hidden_state, final_cell_state : [num_layers(=1) * num_directions(=2), batch_size, n_hidden]
        output, (final_hidden_state, final_cell_state) = self.lstm(input, (hidden_state, cell_state))
        output = output.permute(1, 0, 2) # output : [batch_size, len_seq, n_hidden]
        if self.hparams.attention:
            attn_output, attention = self.attention_net(output, final_hidden_state)
            out=self.out(attn_output)
            return output,out, attention # output hidden_state : [batch_size, len_seq, n_hidden] model : [batch_size, num_classes], attention : [batch_size, n_step]
        else:
            return output
