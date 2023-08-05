import numpy as np

import logging
import sys


def num_grad(scalar_f, x, *args, x_name=None, eps=1e-4, **kwargs):
    """
    Numerical gradient.

    Parameters
    ----------
    scalar_f : function
        A function computing a scalar.
    x : np.ndarray
        The point to compute gradient at.
    x_name : str
        The name of the argument ``x`` in the target function.
    eps : float
        Numerical gradient step.
    *args
    **kwargs
        Other arguments to the function.

    Returns
    -------
    gradient : np.ndarray
        The gradient value(s).
    """
    if x_name is not None and len(args) != 0:
        raise ValueError("x_name is supported for keyword-only input arguments")

    def _target(_x):
        if x_name is None:
            return scalar_f(x, *args, **kwargs)
        else:
            return scalar_f(**{x_name: x}, **kwargs)

    x = np.array(x, dtype=float)
    y = np.array(_target(x))
    gradient = np.empty(y.shape + x.shape, dtype=y.dtype)

    for i in np.ndindex(*x.shape):
        x[i] += eps
        e2 = _target(x)
        x[i] -= 2 * eps
        e1 = _target(x)
        gradient[(Ellipsis,) + i] = (e2 - e1) / 2 / eps
        x[i] += eps
    return gradient


def diag1(a):
    """
    Creates a diagonal tensor from a multidimensional input tensor.

    Parameters
    ----------
    a : np.ndarray
        Diagonal values.

    Returns
    -------
    result : np.ndarray
        The resulting tensor with one more dimension.
    """
    n = len(a)
    result = np.zeros((n, n, *a.shape[1:]), dtype=a.dtype)
    x = np.arange(n)
    result[x, x, ...] = a
    return result


def masked_unique(a, return_inverse=False, fill_value=None):
    """
    A proper implementation of `np.unique` for masked arrays.

    Parameters
    ----------
    a : np.ma.masked_array
        The array to process.
    return_inverse : bool
        If True, returns the masked inverse.
    fill_value : int
        An optional value to fill the `return_inverse` array.

    Returns
    -------
    key : np.ndarray
        Unique entries.
    inverse : np.ma.masked_array, optional
        Integer masked array with the inverse.
    """
    key = np.unique(a, return_inverse=return_inverse)
    if return_inverse:
        key, inverse = key
        barrier = np.argwhere(key.mask)
        if len(barrier) > 0:
            barrier = barrier.squeeze()  # all indices after the barrier have to be shifted (char only?)
            inverse[inverse > barrier] -= 1  # shift everything after the barrier
            if fill_value is None:
                inverse[a.mask.reshape(-1)] = len(key) - 1  # shift masked stuff to the end
            else:
                inverse[a.mask.reshape(-1)] = fill_value
        inverse = np.ma.masked_array(data=inverse, mask=a.mask)
    key = key.data[np.logical_not(key.mask)]
    if return_inverse:
        return key, inverse
    else:
        return key


def dict_reduce(d, operation):
    """
    Reduces dictionary values.

    Parameters
    ----------
    d : Iterable
        Dictionaries to process.
    operation : Callable
        Operation on values.

    Returns
    -------
    result : dict
        A dictionary with reduced values.
    """
    result = {}

    for _d in d:
        for k, v in _d.items():
            if k not in result:
                result[k] = [v]
            else:
                result[k].append(v)

    return {k: operation(v) for k, v in result.items()}


def pyscf_coulomb_ewald(cell, charges=None, eta=None, r_cut=None, k_cut=None):
    """
    Computes electrostatic energy with Ewald summations using pyscf.

    Parameters
    ----------
    cell : Cell
        The cell.
    charges : np.ndarray
        Electrostatic charges in units of electron charge.
    eta : float
    r_cut : float
    k_cut : float
        Ewald summation parameters.

    Returns
    -------
    result : float
        The total electrostatic energy value in atomic units.
    """
    from pyscf.pbc.gto import Cell as pyscf_cell
    if charges is None:
        if "charges" not in cell.meta:
            raise ValueError("No charges specified")
        charges = cell.meta["charges"]
    c = pyscf_cell(a=cell.vectors, atom=zip(['na'] * cell.size, cell.cartesian()))
    c.unit = 'B'
    if k_cut is not None:
        c.ke_cutoff = k_cut ** 2 / 2
    c.ew_eta = eta
    c.ew_cut = r_cut
    c.build()
    c.atom_charges = lambda: np.array(charges)
    return c.ewald()


def cartesian(arrays):
    """
    Cartesian product of many coordinate arrays.

    Parameters
    ----------
    arrays : list, tuple
        Samplings along each axis.

    Returns
    -------
    result : np.ndarray
        The resulting coordinates of a many-dimensional grid.
    """
    x = list(i.ravel() for i in np.meshgrid(*arrays))
    return np.stack(x, axis=-1)


def lattice_up_to_radius(radius, lattice_vecs, cover=False, zero=True):
    """
    Computes grid point coordinates of the given lattice.

    Parameters
    ----------
    radius : float
        The cutoff radius.
    lattice_vecs : np.ndarray
        Lattice vectors.
    cover : bool
        If True, adds points to "cover" the grid.
    zero : bool
        If True, includes the origin (otherwise excludes it).

    Returns
    -------
    result : np.ndarray
        Grid points.
    """
    # Compute image count
    k_vecs = np.linalg.inv(lattice_vecs.T)
    k_lengths = np.linalg.norm(k_vecs, axis=-1)
    n_imgs = np.floor(k_lengths * radius).astype(int)

    if cover:
        n_imgs += 1
    combinations = cartesian([np.arange(-n_img, n_img + 1) for n_img in n_imgs])
    drs = combinations @ lattice_vecs
    if cover:
        selection = np.ones(len(drs), dtype=bool)
        for v in cartesian([[-1, 0, 1]] * len(lattice_vecs)):
            selection |= np.linalg.norm(drs + (v @ lattice_vecs)[None, :], axis=-1) < radius
        drs = drs[selection]
    else:
        selection = np.linalg.norm(drs, axis=-1) < radius
    if not zero:
        selection[len(selection) // 2] = False
    return drs[selection]


def default_logger(name="main", fmt="[%(levelname)s] %(asctime)s %(message)s", date_fmt="%H:%M:%S",
                   lvl=logging.INFO):
    """
    Prepares a default logger printing to stdout.

    Parameters
    ----------
    name : str
        Logger name.
    fmt : str
        Logger format string.
    date_fmt : str
        Date format.
    lvl : int
        Logger sink level.

    Returns
    -------
    logger
        The resulting logger.
    """
    logger = logging.getLogger(name)
    sink = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter(fmt, date_fmt)
    sink.setLevel(lvl)
    sink.setFormatter(formatter)
    logger.handlers = [sink]
    logger.setLevel(logging.DEBUG)
    return logger
