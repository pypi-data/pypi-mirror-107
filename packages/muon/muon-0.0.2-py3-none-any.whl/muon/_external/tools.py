import sys
import os
from functools import reduce

import logging
from datetime import datetime
from time import strftime
from warnings import warn

import numpy as np
import pandas as pd
import scanpy as sc
import h5py
from natsort import natsorted
from anndata import AnnData
from .mudata import MuData

from typing import Union, Optional, List, Iterable, Mapping, Sequence, Type, Any
from types import MappingProxyType


#
# Connectivity: WNN
#
def wnn(mdata, n_neighbors: int = 15):

    assert len(mdata.mod) == 2, "WNN is only applicable to integrate 2 modalities"

    sc.pp.neighbors(mdata["prot"], knn=False, method="gauss", key_added="knn")
    sc.pp.neighbors(mdata["rna"], knn=False, method="gauss", key_added="knn")

    xs = np.array(list(range(mdata.shape[0])))

    rx = mdata["rna"].obsm["X_pca"]
    px = mdata["prot"].obsm["X_pca"]

    knn_rx = np.argsort(mdata["rna"].obsp["knn_distances"][xs, :], axis=1)

    knn_px = np.argsort(mdata["prot"].obsp["knn_distances"][xs, :], axis=1)

    # Within-modality predictions
    rs_hat_r = np.array(
        [
            np.array(rx[knn_rx[i, 1 : (n_neighbors + 1)], :].sum(axis=0)).squeeze() / n_neighbors
            for i, ix in enumerate(xs)
        ]
    )
    ps_hat_p = np.array(
        [
            np.array(px[knn_px[i, 1 : (n_neighbors + 1)], :].sum(axis=0)).squeeze() / n_neighbors
            for i, ix in enumerate(xs)
        ]
    )

    # Across-modality predictions
    rs_hat_p = np.array(
        [
            np.array(rx[knn_px[i, 1 : (n_neighbors + 1)], :].sum(axis=0)).squeeze() / n_neighbors
            for i, ix in enumerate(xs)
        ]
    )
    ps_hat_r = np.array(
        [
            np.array(px[knn_rx[i, 1 : (n_neighbors + 1)], :].sum(axis=0)).squeeze() / n_neighbors
            for i, ix in enumerate(xs)
        ]
    )

    # Sigmas
    n_anti_neighbors = 20
    sigma_rs_hat_r = np.array(
        [
            np.array(rx[knn_rx[i, -n_anti_neighbors:], :].sum(axis=0)).squeeze() / n_anti_neighbors
            for i, ix in enumerate(xs)
        ]
    )
    sigma_rs = euc_d(rx - sigma_rs_hat_r)

    sigma_ps_hat_p = np.array(
        [
            np.array(px[knn_px[i, -n_anti_neighbors:], :].sum(axis=0)).squeeze() / n_anti_neighbors
            for i, ix in enumerate(xs)
        ]
    )
    sigma_ps = euc_d(px - sigma_ps_hat_p)

    # Thetas
    from functools import partial

    euc_d = partial(np.linalg.norm, axis=1)

    r_knn_rs_1 = rx[knn_rx[:, 1], :]
    theta_rs_knn_r = np.exp(
        -np.max(
            np.vstack([euc_d(rx - rs_hat_r) - euc_d(rx - r_knn_rs_1), np.repeat(0, len(xs))]),
            axis=0,
        )
        / (sigma_rs - euc_d(rx - r_knn_rs_1))
    )
    theta_rs_knn_p = np.exp(
        -np.max(
            np.vstack([euc_d(rx - rs_hat_p) - euc_d(rx - r_knn_rs_1), np.repeat(0, len(xs))]),
            axis=0,
        )
        / (sigma_rs - euc_d(rx - r_knn_rs_1))
    )

    p_knn_ps_1 = px[knn_px[:, 1], :]
    theta_ps_knn_p = np.exp(
        -np.max(
            np.vstack([euc_d(px - ps_hat_p) - euc_d(px - p_knn_ps_1), np.repeat(0, len(xs))]),
            axis=0,
        )
        / (sigma_ps - euc_d(px - p_knn_ps_1))
    )
    theta_ps_knn_r = np.exp(
        -np.max(
            np.vstack([euc_d(px - ps_hat_r) - euc_d(px - p_knn_ps_1), np.repeat(0, len(xs))]),
            axis=0,
        )
        / (sigma_ps - euc_d(px - p_knn_ps_1))
    )

    s_rs = theta_rs_knn_r / (theta_rs_knn_p + 1e-4)
    s_ps = theta_ps_knn_p / (theta_ps_knn_r + 1e-4)

    ws_denom = np.sum(np.exp(np.array([s_rs, s_ps])), axis=0)
    w_rs = np.exp(s_rs) / ws_denom
    w_ps = np.exp(s_ps) / ws_denom

    mdata.obs["w_rna"] = w_rs
    mdata.obs["w_prot"] = w_ps

    from scipy.sparse import csr_matrix

    new_conn = csr_matrix(
        mdata["rna"].obsp["connectivities"].A * w_rs + mdata["prot"].obsp["connectivities"].A * w_ps
    )
    new_dist = csr_matrix(
        mdata["rna"].obsp["distances"].A * w_rs + mdata["prot"].obsp["distances"].A * w_ps
    )

    mdata.obsp["wnn_connectivities"] = new_conn
    mdata.obsp["wnn_distances"] = new_conn

    mdata.uns["wnn"] = {
        "connectivities_key": "wnn_connectivities",
        "distances_key": "wnn_distances",
        "params": {
            "method": "wnn",
            "metric": "euclidean",
            "n_neighbors": n_neighbors,
            "use_rep": "X_mofa",  # shouldn't be used, but key should exist
        },
    }

    return None
