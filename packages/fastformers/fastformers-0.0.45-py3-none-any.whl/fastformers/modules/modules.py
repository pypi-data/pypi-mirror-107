from typing import Optional

import math

import torch
from torch.nn import Module, ModuleList, Linear, Embedding, LayerNorm
from torch.nn.functional import gelu


from ..utils import neg_inf


class MultiHeadAttention(Module):
    def __init__(self, n_heads: int, dim: int):
        super().__init__()
        self.n_heads = n_heads
        self.dim_per_head = dim // n_heads
        self.scale = math.sqrt(self.dim_per_head)

        self.pre_attention = Linear(dim, dim * 3)
        self.out_lin = Linear(dim, dim)

    def forward(self, query: torch.Tensor, mask: torch.Tensor) -> torch.Tensor:
        batch_size, seq_len, dim = query.shape

        query = self.pre_attention(query)
        query = query.view(batch_size, seq_len, self.n_heads, self.dim_per_head, 3)
        query = query.transpose(1, 2).contiguous()
        query = query.view(batch_size * self.n_heads, seq_len, self.dim_per_head, 3)

        q = query[:, :, :, 0] / self.scale
        k_v = query[:, :, :, 1:]

        dot_prod = q.bmm(k_v[:, :, :, 0].transpose(1, 2))

        dot_prod.masked_fill_(mask, neg_inf(dot_prod.dtype == torch.float16))

        attn_weights = dot_prod.softmax(dim=-1, dtype=torch.float).type_as(query)

        out = self.out_lin(attn_weights.bmm(k_v[:, :, :, 1]).view(
            batch_size, self.n_heads, seq_len,
            self.dim_per_head).transpose(1, 2).contiguous().view(batch_size, seq_len, dim))

        return out


class TransformerFFN(Module):
    def __init__(self, dim: int, dim_hidden: int):
        super(TransformerFFN, self).__init__()
        self.lin1 = Linear(dim, dim_hidden)
        self.lin2 = Linear(dim_hidden, dim)

    def forward(self, tensor: torch.Tensor) -> torch.Tensor:
        tensor = self.lin1(tensor)
        tensor = gelu(tensor)
        tensor = self.lin2(tensor)
        return tensor


class TransformerEncoderLayer(Module):
    def __init__(self, n_heads: int, embedding_size: int, ffn_size: int):
        super().__init__()
        self.attention = MultiHeadAttention(n_heads, embedding_size)
        self.norm1 = LayerNorm(embedding_size)
        self.ffn = TransformerFFN(embedding_size, ffn_size)
        self.norm2 = LayerNorm(embedding_size)

    def forward(self, tensor: torch.Tensor, mask: torch.Tensor):
        residual = tensor
        tensor = self.attention(tensor, mask=mask)
        tensor = tensor + residual
        tensor = self.norm1(tensor)
        tensor = tensor + self.ffn(tensor)
        tensor = self.norm2(tensor)
        return tensor


class TransformerEncoder(Module):
    def __init__(self, n_heads: int, n_layers: int, embedding_size: int, ffn_size: int):
        super(TransformerEncoder, self).__init__()

        self.layers = ModuleList(TransformerEncoderLayer(n_heads, embedding_size, ffn_size) for _ in range(n_layers))
        self.n_heads = n_heads

    def forward(self, tensor: torch.Tensor, mask: torch.Tensor) -> torch.Tensor:
        bsz, seq_len = mask.shape
        attn_mask = ~mask.view(bsz, 1, -1, seq_len).repeat(1, self.n_heads, 1, 1).expand(
            -1, -1, seq_len, -1).view(bsz * self.n_heads, seq_len, seq_len)

        for layer in self.layers:
            tensor = layer.forward(tensor, attn_mask)

        return tensor * mask.unsqueeze(-1)


class TransformerDecoder(Module):
    def __init__(self, n_heads: int, n_layers: int, embedding_size: int, ffn_size: int):
        super().__init__()

        self.layers = ModuleList(TransformerDecoderLayer(n_heads, embedding_size, ffn_size) for _ in range(n_layers))
        self.n_heads = n_heads

    def process_decoder_mask(self, decoder_mask: torch.Tensor, decoder_length: int) -> torch.Tensor:
        bsz, seq_len = decoder_mask.shape
        mask = torch.tril(torch.ones(seq_len, seq_len, dtype=torch.bool, device=decoder_mask.device))
        mask = mask.unsqueeze(0)[:, -decoder_length:] & decoder_mask.unsqueeze(1)
        return ~mask.view(bsz, 1, -1, seq_len).repeat(1, self.n_heads, 1, 1).expand(
            -1, -1, decoder_length, -1).view(bsz * self.n_heads, decoder_length, seq_len)

    def process_encoder_mask(self, encoder_mask: torch.Tensor, decoder_length: int) -> torch.Tensor:
        bsz, encoder_length = encoder_mask.shape
        return ~encoder_mask.view(bsz, 1, -1, encoder_length).repeat(1, self.n_heads, 1, 1).expand(
            -1, -1, decoder_length, -1).view(bsz * self.n_heads, decoder_length, encoder_length)

    def forward(
            self, tensor: torch.Tensor, decoder_mask: torch.Tensor,
            encoder_mask: torch.Tensor, encoder_state: torch.Tensor
    ) -> torch.Tensor:

        decoder_length = tensor.shape[1]
        decoder_mask = self.process_decoder_mask(decoder_mask, decoder_length=decoder_length)
        encoder_mask = self.process_encoder_mask(encoder_mask, decoder_length=decoder_length)

        encoder_state = encoder_state.flatten(0, 1)

        for ind, layer in enumerate(self.layers):
            tensor = layer.forward(
                x=tensor, decoder_mask=decoder_mask, encoder_state=encoder_state[:, ind], encoder_mask=encoder_mask
            )

        return tensor


class TransformerDecoderLayer(Module):
    def __init__(self, n_heads: int, embedding_size: int, ffn_size: int):
        super().__init__()
        self.dim = embedding_size

        self.self_attention = MultiHeadAttention(n_heads, embedding_size)
        self.norm1 = LayerNorm(embedding_size)

        self.encoder_attention = DecoderEncoderAttention(n_heads, embedding_size)
        self.norm2 = LayerNorm(embedding_size)

        self.ffn = TransformerFFN(embedding_size, ffn_size)
        self.norm3 = LayerNorm(embedding_size)

    def forward(
            self, x, decoder_mask: torch.Tensor, encoder_state: torch.Tensor, encoder_mask: torch.Tensor
    ) -> torch.Tensor:
        residual = x

        x = self.self_attention(query=x, mask=decoder_mask)

        x = x + residual
        x = self.norm1(x)

        x = self.encoder_attention(query=x, key=encoder_state[:, 0], value=encoder_state[:, 1], mask=encoder_mask) + x

        x = self.norm2(x)

        residual = x

        x = self.ffn(x)

        x = residual + x
        x = self.norm3(x)

        return x


class DecoderEncoderAttention(Module):
    def __init__(self, n_heads: int, dim: int):
        super().__init__()
        self.n_heads = n_heads
        self.dim_per_head = dim // n_heads
        self.scale = math.sqrt(self.dim_per_head)
        self.q_lin = Linear(dim, dim)
        self.out_lin = Linear(dim, dim)

    def forward(self, query: torch.Tensor, mask: torch.Tensor, key: torch.Tensor, value: torch.Tensor) -> torch.Tensor:
        batch_size, seq_len, dim = query.shape

        query = self.q_lin(query) / self.scale
        query = query.view(batch_size, seq_len, self.n_heads, self.dim_per_head).transpose(1, 2).contiguous()
        query = query.view(batch_size * self.n_heads, seq_len, self.dim_per_head)

        dot_prod = query.bmm(key.transpose(1, 2))

        dot_prod.masked_fill_(mask, neg_inf(dot_prod.dtype == torch.float16))

        attn_weights = dot_prod.softmax(dim=-1, dtype=torch.float).type_as(query)

        return self.out_lin(attn_weights.bmm(value).view(
            batch_size, self.n_heads, seq_len,
            self.dim_per_head).transpose(1, 2).contiguous().view(batch_size, seq_len, dim))


class Embeddings(Module):
    def __init__(self, vocab_size: int, dim: int, padding_idx: int, max_position_embeddings: int):
        super().__init__()
        self.word_embeddings = Embedding(vocab_size, dim, padding_idx=padding_idx)
        self.position_embeddings = Embedding(max_position_embeddings, dim)
        self.LayerNorm = LayerNorm(dim)

    def forward(self, input_ids: torch.Tensor) -> torch.Tensor:
        embeddings = self.word_embeddings(input_ids) + self.position_embeddings.weight[:input_ids.shape[1]]
        return self.LayerNorm(embeddings)


class MaskEmbeddings(Embeddings):
    def __init__(self, vocab_size: int, dim: int, padding_idx: int, max_position_embeddings: int):
        super().__init__(vocab_size, dim, padding_idx, max_position_embeddings)
        self.padding_idx = padding_idx

    @staticmethod
    def create_position_ids_from_input_ids(input_ids: torch.Tensor, padding_idx: int) -> torch.Tensor:
        mask = input_ids.ne(padding_idx)
        return torch.cumsum(mask, dim=1) * mask + padding_idx

    def forward(self, input_ids: torch.Tensor) -> torch.Tensor:
        position_ids = self.create_position_ids_from_input_ids(input_ids, self.padding_idx)
        embedded = self.word_embeddings(input_ids) + self.position_embeddings(position_ids)
        return self.LayerNorm(embedded)


class EmbeddingsWithTokenTypes(Module):
    def __init__(
            self, vocab_size: int, token_types: int, embedding_size: int, pad_token_id: int,
            max_position_embeddings: int
    ):
        super().__init__()
        self.word_embeddings = Embedding(vocab_size, embedding_size, padding_idx=pad_token_id)
        self.position_embeddings = Embedding(max_position_embeddings, embedding_size)
        self.token_type_embeddings = Embedding(token_types, embedding_size)
        self.LayerNorm = LayerNorm(embedding_size)

    def forward(self, input_ids: torch.Tensor, token_type_ids: Optional[torch.Tensor]):
        embeddings = self.word_embeddings(input_ids) + self.position_embeddings.weight[:input_ids.shape[1]] + (
            self.token_type_embeddings.weight[0] if token_type_ids is None
            else self.token_type_embeddings(token_type_ids))
        return self.LayerNorm(embeddings)


class TanhHead(Module):
    """Head for sentence-level classification tasks."""

    def __init__(self, input_dim: int, inner_dim: int, num_classes: int):
        super().__init__()
        self.dense = Linear(input_dim, inner_dim)
        self.out_proj = Linear(inner_dim, num_classes)

    def forward(self, hidden_states: torch.Tensor) -> torch.Tensor:
        hidden_states = self.dense(hidden_states)
        hidden_states = torch.tanh(hidden_states)
        return self.out_proj(hidden_states)
