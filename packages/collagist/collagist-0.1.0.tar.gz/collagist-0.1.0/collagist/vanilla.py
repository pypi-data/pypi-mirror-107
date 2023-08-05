import torch
from torch import Tensor
from typing import Sequence

__all__ = ["vanilla_collage"]


def vanilla_collage(images: Sequence[Tensor], n_row: int, n_column: int):
    """vanilla collage
    params:
        - images: sequence of images of shape (..., C, H, W)
        - n_row: int > 0, number of rows
        - n_column: int > 0, number of columns
    """
    size = None
    for img in images:
        assert isinstance(
            img, Tensor
        ), f"The input images should be tensors of shape (..., C, H, W)."
        if size is None:
            size = img.size()
        else:
            assert (
                size == img.size()
            ), f"The list of images should be uniform in size ({size}) but get {img.size()}."

    rows = []
    for r in range(n_row):
        _new_row = []
        for c in range(n_column):
            _new_row.append(images[r * n_column])
        row_img = torch.cat(_new_row, dim=-1)
        rows.append(row_img)
    final_img = torch.cat(rows, dim=-2)

    return final_img
