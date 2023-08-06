#
# Compatibility with R-derived file formats
#


def read_rds(filename: PathLike) -> MuData:
    """
    Read a MultiAssayExperiment object from .rds file

    Parameters
    ----------
    filename: os.PathLike
            Path to the .rds file
    """
    import rpy2.robjects as ro
    from rpy2.robjects import r, pandas2ri

    readRDS = ro.r["readRDS"]

    from rpy2.robjects.packages import importr

    seurat = importr("Seurat")

    import pandas as pd

    obj = readRDS(filename)

    if tuple(obj.rclass)[0] == "MultiAssayExperiment":
        colData = obj.slots["colData"]
        obs = pandas2ri.rpy2py_dataframe(r.as_data_frame(colData))
        obs.index = np.array(r.rownames(colData))

        mods = {}
        experiments = obj.slots["ExperimentList"]
        data = experiments.slots["listData"]
        mod_names = tuple(data.names)
        for i, mod in enumerate(mod_names):
            mods[mod] = AnnData(
                X=np.array(data[i]).T,
                obs=pd.DataFrame(index=tuple(data[i].colnames)),
                var=pd.DataFrame(index=tuple(data[i].rownames)),
            )

        mdata = MuData(mods)
        mdata.obs = obs
    elif tuple(obj.rclass)[0] == "Seurat":
        from scipy.sparse import csr_matrix

        def dgc_to_csr(mx):
            # To convert p in dgCMatrix to j in csr_matrix
            p_to_j = lambda p: np.hstack([np.repeat(i, p[i + 1] - p[i]) for i in range(len(p) - 1)])

            x = np.array(mx.slots["x"])
            i = np.array(mx.slots["i"])
            p = np.array(mx.slots["p"])
            j = p_to_j(p)
            nrow, ncol = mx.slots["Dim"]

            return csr_matrix((x, (i, j)), shape=(nrow, ncol))

        metadata = obj.slots["meta.data"]
        obs = pandas2ri.rpy2py_dataframe(r.as_data_frame(metadata))

        ads = {}

        mods = list(obj.slots["assays"].names)
        # Requires Seurat above 3.2
        # which doesn't work with rpy2
        mods = [i for i in mods if i != "ATAC" and i != "SCT"]
        for i, mod in enumerate(mods):
            assay = obj.slots["assays"][i]
            n_obs, n_vars = r.dim(assay)
            count_mx = assay.slots["counts"]

            counts = dgc_to_csr(count_mx).T
            normalised = dgc_to_csr(assay.slots["data"]).T
            scaled = np.array(assay.slots["scale.data"])

            var_names, obs_names = map(np.array, count_mx.slots["Dimnames"])

            if len(assay.slots["meta.features"]) > 0:
                var = pandas2ri.rpy2py_dataframe(r.as_data_frame(assay.slots["meta.features"]))
            else:
                var = pd.DataFrame(index=var_names)

            if len(assay.slots["var.features"]) > 0:
                # TODO
                pass

            if scaled.shape[0] == n_vars:
                x = scaled
            elif normalised.shape[0] == n_vars:
                x = normalised
            else:
                x = counts

            ad = AnnData(X=x, obs=pd.DataFrame(index=obs_names), var=var)
            ad.layers["counts"] = counts
            if normalised.shape[0] == n_vars:
                ad.layers["normalised"] = normalised
            ads[mod] = ad

        # Neighbours

        nei = obj.slots["neighbors"]

        if len(nei) > 0:
            # TODO
            pass

        # Graphs

        gra = obj.slots["graphs"]

        if len(gra) > 0:
            # TODO
            pass

        # Reductions

        obsm = {}

        red = obj.slots["reductions"]
        basis_names = list(red.names)
        for i, basis in enumerate(basis_names):
            reduction = red[i]
            red_key = "X_" + basis.lower()
            # for slotname in reduction.slotnames():

            slotnames = list(reduction.slotnames())

            mod_used = None

            if "assay.used" in slotnames:
                slotvalue = reduction.slots["assay.used"]
                if len(slotvalue) == 1:
                    mod_used = slotvalue[0]

            if "cell.embeddings" in slotnames:
                basis_array = np.array(reduction.slots["cell.embeddings"])
                if mod_used is not None and mod_used in mods:
                    ads[mod_used].obsm[red_key] = basis_array
                else:
                    obsm[red_key] = basis_array

            # TODO: 'feature.loadings', 'feature.loadings.projected', 'stdev', 'key', 'jackstraw', 'misc'

        mdata = MuData(ads)
        mdata.obs = obs
        mdata.obsm = obsm

    else:
        raise ValueError(
            "Cannot recognise a MultiAssayExperiment or a Seurat object in the .rds file"
        )

    return mdata
