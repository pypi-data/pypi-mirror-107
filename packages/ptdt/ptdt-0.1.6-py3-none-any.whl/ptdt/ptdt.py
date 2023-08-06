import torch


def image(name: str, tensor: torch.Tensor):
    if tensor.ndim == 4:
        channel_dim = 1
    elif tensor.ndim == 3:
        channel_dim = 0
    else:
        raise ValueError("cannot handle tensor which doesn't have 3 or 4 dimension")

    print(f"{name}: {_basic(tensor)}")
    for c in range(tensor.shape[channel_dim]):
        if channel_dim == 1:
            t = tensor[:, c, ...]
        else:
            t = tensor[c, ...]
        print(f"  [{c}]: {_stat(t)}")


def tensor(name: str, tensor: torch.Tensor):
    print(f"{name}: {_basic(tensor)} {_stat(tensor)}")


def _basic(t: torch.Tensor):
    return f"shape={list(t.shape)} dtype={t.dtype}"


def _stat(t: torch.Tensor):
    t = t.to(torch.float64)
    return f"min={t.min().item():.3f} max={t.max().item():.3f} mean={t.mean().item():.3f} std={t.std().item():.3f}"

