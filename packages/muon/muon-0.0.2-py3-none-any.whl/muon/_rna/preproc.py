from typing import Optional, Iterable, Tuple, Union
from numbers import Integral, Real
from warnings import warn

import numpy as np
import pandas as pd
from scipy.sparse import issparse, csr_matrix
from anndata import AnnData

from .. import MuData


def clr(adata: AnnData, inplace: bool = True) -> Union[None, AnnData]:
    """
    Apply the centered log ratio (CLR) transformation
    to normalize counts in adata.X.

    Args:
        data: AnnData object with protein expression counts.
        inplace: Whether to update adata.X inplace.
    """
    sparse = False
    if issparse(adata.X):
        sparse = True
    # Geometric mean of ADT counts
    x = adata.X
    g_mean = np.exp(np.log1p(x).sum(axis=0) / x.shape[0])
    # Centered log ratio
    clr = np.log1p(x / g_mean)

    if sparse:
        clr = csr_matrix(clr)

    if not inplace:
        adata = adata.copy()

    adata.X = clr

    return None if inplace else adata


def normalize_residuals(
    adata: AnnData, inplace: bool = True, clip: bool = True, theta: int = 100
) -> Union[None, AnnData]:
    """
    Compute analytical residuals for NB model with a fixed theta.
    Potentially clip outlier residuals to sqrt(N).

    Adapted from Lause et al., 2020.
    """
    counts_sum0 = np.sum(adata.X, axis=0, keepdims=True)
    counts_sum1 = np.sum(adata.X, axis=1, keepdims=True)
    counts_sum = np.sum(adata.X)

    # Calculate residuals
    mu = counts_sum1 @ counts_sum0 / counts_sum
    z = (adata.X - mu) / np.sqrt(mu + mu ** 2 / theta)

    # Clip values
    if clip:
        n = counts.n_obs
        z[z > np.sqrt(n)] = np.sqrt(n)
        z[z < -np.sqrt(n)] = -np.sqrt(n)

    if not inplace:
        adata = adata.copy()

    adata.X = z

    return None if inplace else adata
