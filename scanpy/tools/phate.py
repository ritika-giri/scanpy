"""Embed high-dimensional data using PHATE
"""
try:
    import phate as ph
except ImportError:
    pass

from .. import settings
from .. import logging as logg


def phate(
        adata,
        n_components=2,
        k=15,
        a=10,
        alpha_decay=None,
        n_landmark=2000,
        t='auto',
        potential_method='log',
        n_pca=100,
        knn_dist='euclidean',
        mds_dist='euclidean',
        mds='metric',
        n_jobs=None,
        random_state=None,
        verbose=None,
        copy=False):
    """PHATE [Moon17]_.

    Potential of Heat-diffusion for Affinity-based Trajectory Embedding (PHATE)
    embeds high dimensional single-cell data into two or three dimensions for
    visualization of biological progressions.

    For more information and access to the object-oriented interface,
    read the `PHATE Documentation <https://phate.readthedocs.io/>`_.
    For help, tutorials, bug reports, and R/MATLAB implementations,
    visit the `PHATE GitHub <https://github.com/KrishnaswamyLab/PHATE/>`_.

    Parameters
    ----------
    adata : :class:`~scanpy.api.AnnData`
        Annotated data matrix.

    n_components : `int`, optional (default: 2)
        number of dimensions in which the data will be embedded

    k : `int`, optional (default: 15)
        number of nearest neighbors on which to build kernel

    a : `int`, optional (default: `None`)
        sets decay rate of kernel tails.
        If None, alpha decaying kernel is not used

    alpha_decay : `bool` or `None` (default: `None`)
        forces the use of alpha decaying kernel
        If None, alpha decaying kernel is used for small inputs
        (n_samples < n_landmark) and not used otherwise

    n_landmark : `int`, optional (default: 2000)
        number of landmarks to use in fast PHATE

    t : `int` or 'auto', optional (default: 'auto')
        power to which the diffusion operator is powered
        sets the level of diffusion

    potential_method : {'log', 'sqrt'}, optional (default: 'log')
        Selects which transformation of the diffusional operator is used
        to compute the diffusion potential

    n_pca : `int`, optional (default: 100)
        Number of principal components to use for calculating
        neighborhoods. For extremely large datasets, using
        n_pca < 20 allows neighborhoods to be calculated in
        log(n_samples) time.

    knn_dist : string, optional (default: 'euclidean')
        recommended values: 'euclidean' and 'cosine'
        Any metric from `scipy.spatial.distance` can be used
        distance metric for building kNN graph

    mds_dist : string, optional (default: 'euclidean')
        recommended values: 'euclidean' and 'cosine'
        Any metric from `scipy.spatial.distance` can be used
        distance metric for MDS

    mds : {'classic', 'metric', 'nonmetric'}, optional (default: 'metric')
        Selects which MDS algorithm is used for dimensionality reduction

    n_jobs : `int` or `None`, optional (default: `sc.settings.n_jobs`)
        The number of jobs to use for the computation.
        If `None`, `sc.settings.n_jobs` is used.
        If -1 all CPUs are used. If 1 is given, no parallel computing code is
        used at all, which is useful for debugging.
        For n_jobs below -1, (n_cpus + 1 + n_jobs) are used. Thus for
        n_jobs = -2, all CPUs but one are used

    random_state : `int`, `numpy.RandomState` or `None`, optional (default: `None`)
        Random seed. Defaults to the global `numpy` random number generator

    verbose : `bool`, `int` or `None`, optional (default: `sc.settings.verbosity`)
        If `True` or an integer `>= 2`, print status messages.
        If `None`, `sc.settings.verbosity` is used.

    copy : `bool` (default: `False`)
        Return a copy instead of writing to `adata`.

    Returns
    -------
    Depending on `copy`, returns or updates `adata` with the following fields.

    X_phate : `np.ndarray`, (`adata.obs`, shape=[n_samples, n_components], dtype `float`)
        PHATE coordinates of data.

    Examples
    --------
    >>> import scanpy.api as sc
    >>> import phate
    >>> tree_data, tree_clusters = phate.tree.gen_dla(n_dim=100,
                                                      n_branch=20,
                                                      branch_length=100)
    >>> tree_data.shape
    (2000, 100)
    >>> adata = sc.AnnData(tree_data)
    >>> sc.tl.phate(adata, k=5, a=20, t=150)
    >>> adata.obsm['X_phate'].shape
    (2000, 2)
    >>> sc.pl.phate(adata)
    """
    logg.info('computing PHATE', r=True)
    adata = adata.copy() if copy else adata
    verbose = settings.verbosity if verbose is None else verbose
    if isinstance(verbose, int):
        verbose = verbose >= 2
    n_jobs = settings.n_jobs if n_jobs is None else n_jobs
    try:
        X_phate = ph.PHATE(
            n_components=n_components,
            k=k,
            a=a,
            alpha_decay=alpha_decay,
            n_landmark=n_landmark,
            t=t,
            potential_method=potential_method,
            n_pca=n_pca,
            knn_dist=knn_dist,
            mds_dist=mds_dist,
            mds=mds,
            n_jobs=n_jobs,
            random_state=random_state,
            verbose=verbose,
        ).fit_transform(adata)
    except NameError:
        raise ImportError(
            'You need to install the package `phate`: please run `pip install '
            '--user phate` in a terminal.')
    logg.info('    finished', time=True,
              end=' ' if settings.verbosity > 2 else '\n')
    # update AnnData instance
    adata.obsm['X_phate'] = X_phate  # annotate samples with tSNE coordinates
    logg.hint('added\n'
              '    \'X_phate\', PHATE coordinates (adata.obsm)')
    return adata if copy else None
