import numpy as np
from scipy.optimize import root_scalar


def ewald_real_cutoff_error(r_cut, eta, volume, charge, scale=1):
    """
    An error associated with the real cutoff of Ewald summations.
    Eq. 4 in doi:10.1016/j.cplett.2005.05.106

    Parameters
    ----------
    r_cut : float
        Real-space cutoff.
    eta : float
        Gaussian charge screening parameter.
    volume : float
        Unit cell volume.
    charge : float
        Sum of individual charges squared.
    scale : float
        The scale: e^2 / 4 / π / ε0 = Hartree * aBohr

    Returns
    -------
    result : float
        The error estimate.
    """
    return charge / eta ** 2 / r_cut ** 1.5 / (2 * volume) ** .5 * np.exp(- (eta * r_cut) ** 2) * scale


def ewald_k_cutoff_error(k_cut, eta, volume, charge, scale=1):
    """
    An error associated with the k-space cutoff of Ewald summations.
    Eq. 5 in doi:10.1016/j.cplett.2005.05.106

    Parameters
    ----------
    k_cut : float
        k-space cutoff.
    eta : float
        Gaussian charge screening parameter.
    volume : float
        Unit cell volume.
    charge : float
        Sum of individual charges squared.
    scale : float
        The scale: e^2 / 4 / π / ε0 = Hartree * aBohr

    Returns
    -------
    result : float
        The error estimate.
    """
    return charge * 2 * eta / k_cut * ((k_cut * volume) ** -.5 + eta / np.pi) * np.exp(- (k_cut / 2 / eta) ** 2) * scale


def ewald_cutoffs(eta, volume, charge, scale=1, eps=1e-7):
    """
    Compute the required Ewald cutoffs for the given tolerance.

    Parameters
    ----------
    eta : float
        Gaussian charge screening parameter.
    volume : float
        Unit cell volume.
    charge : float
        Sum of individual charges squared.
    scale : float
        The scale: e^2 / 4 / π / ε0 = Hartree * aBohr
    eps : float
        The required tolerance.

    Returns
    -------
    r_cut : float
        Cutoff value in real space.
    k_cut : float
        Cutoff value in reciprocal space.
    """
    result = tuple(
        root_scalar(
            lambda *args: f(*args) - eps,
            (eta, volume, charge, scale),
            bracket=b,
            method="bisect",
        ).root
        for f, b in (
            (ewald_real_cutoff_error, (0.1 / eta, 40 / eta)),
            (ewald_k_cutoff_error, (0.1 * eta, 40 * eta))
        )
    )
    return result


def stat_cell(cells, squeeze=True):
    """
    Computes statistics for cell(s): volumes and charges.

    Parameters
    ----------
    cells : list, tuple, Cell
        Cell(s) to compute cutoffs for.
    squeeze : bool
        If True, squeezes the output for a single cell.

    Returns
    -------
    volume : np.ndarray, float
        Volume(s).
    charge : np.ndarray, float
        Sum(s) of charges squared.
    """
    if not isinstance(cells, (list, tuple)):
        cells = [cells]
    volume = np.array([i.volume for i in cells])
    charge = np.array([(np.abs(i.meta["charges"]) ** 2).sum() for i in cells])
    if squeeze and len(cells) == 1:
        return volume.item(), charge.item()
    else:
        return volume, charge
