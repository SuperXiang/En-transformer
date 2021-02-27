import torch
from en_transformer.utils import rot
from en_transformer import EGAT

def test_egat_equivariance():
    layer = EGAT(dim = 512, edge_dim = 4)

    R = rot(*torch.rand(3))
    T = torch.randn(1, 1, 3)

    feats = torch.randn(1, 16, 512)
    coors = torch.randn(1, 16, 3)
    edges = torch.randn(1, 16, 16, 4)

    feats1, coors1 = layer(feats, coors @ R + T, edges)
    feats2, coors2 = layer(feats, coors, edges)

    assert torch.allclose(feats1, feats2, atol = 1e-6), 'type 0 features are invariant'
    assert torch.allclose(coors1, (coors2 @ R + T), atol = 1e-6), 'type 1 features are equivariant'
