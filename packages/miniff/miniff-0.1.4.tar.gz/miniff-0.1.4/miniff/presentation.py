from numericalunits import nu_eval
from .potentials import behler2_descriptor_family, behler_turning_point
from .kernel import profile_directed_strain, Cell

from matplotlib import pyplot
from matplotlib.axes import Axes
import numpy as np

from functools import reduce


unicode_block_elements = " ▁▂▃▄▅▆▇█"


def text_bars(values, mn=None, mx=None, palette=unicode_block_elements):
    """
    A text bar plot.

    Parameters
    ----------
    values : Iterable
        Evenly distributed values as a 1D array.
    mn : float
        The minimal value.
    mx : float
        The maximal value.
    palette : str
        The palette to draw with.

    Returns
    -------
    result : str
        A character bar plot.
    """
    if mn is None:
        mn = min(values)
    if mx is None:
        mx = max(values)
    if mn == mx:
        mx = mn + 1
    spacing = (mx - mn) / (len(palette) - 1)
    return "".join(palette[int(round(min(max(i - mn, 0), mx - mn) / spacing))] for i in values)


def plot_rdf(r, data, ax=None, legend=True, length_unit="angstrom", xlabel=True, ylabel=True, **kwargs):
    """
    Plot radial distribution function.

    Parameters
    ----------
    r : np.ndarray, list
        Radial points.
    data : dict
        Radial distribution functions.
    ax : Axes
        `matplotlib` axes to plot on.
    legend : str, bool
        If True, creates a legend. If "labels" creates labels but
        does not invoke the legend. Otherwise puts neither plot
        labels nor the legend.
    length_unit : str
        A valid `numericalunits` string expression for units.
    xlabel : bool, str
        x axis label.
    ylabel : bool, str
        y axis label.
    kwargs
        Passed to `ax.plot`.

    Returns
    -------
    ax : Axes
        `matplotlib` axes.
    """
    if legend not in (True, False, 'labels'):
        raise ValueError("The 'legend' argument has to be either True, False, or 'labels'")
    if ax is None:
        ax = pyplot.gca()
    scale = nu_eval(length_unit)
    r = np.array(r)
    for k, v in sorted(data.items()):
        ax.plot(r / scale, np.array(v) * (scale ** 3), label=k if legend is not False else None, **kwargs)

    if xlabel is True:
        ax.set_xlabel(f"r ({length_unit})")
    elif xlabel:
        ax.set_xlabel(xlabel)
    if ylabel is True:
        ax.set_ylabel(f"Density (atoms / [{length_unit}]^3)")
    elif ylabel:
        ax.set_ylabel(ylabel)
    if legend is True:
        ax.legend()

    return ax


def plot_adf(a, data, ax=None, legend=True, xlabel=True, ylabel=True, **kwargs):
    """
    Plot angular distribution function.

    Parameters
    ----------
    a : np.ndarray
        Angular points.
    data : dict
        ADF.
    ax : Axes
        `matplotlib` axes to plot on.
    legend : str, bool
        If True, creates a legend. If "labels" creates labels but
        does not invoke the legend. Otherwise puts neither plot
        labels nor the legend.
    xlabel : bool, str
        x axis label.
    ylabel : bool, str
        y axis label.
    kwargs
        Passed to `ax.plot`.

    Returns
    -------
    ax : Axes
        `matplotlib` axes.
    """
    if xlabel is True:
        xlabel = "angle (degrees)"
    if ylabel is True:
        ylabel = "Density (a.u.)"
    result = plot_rdf(a / np.pi * 180, data, ax=ax, legend=legend, length_unit="1", xlabel=xlabel, ylabel=ylabel,
                      **kwargs)
    return result


def plot_strain_profile(potentials, cell, limits=(0.9, 1.1), direction=(1, 1, 1),
                        ax=None, energy_unit="Ry", xlabel=True, ylabel=True,
                        mark_points=None, origin=None, profile_kwargs=None, **kwargs):
    """
    Plot energy as a function of strain.

    Parameters
    ----------
    potentials : list
        Potentials to profile.
    cell : Cell
        The original cell.
    limits : tuple
        Lower and upper strain bounds.
    direction : list, tuple, np.ndarray
        Strain direction.
    ax : Axes
        `matplotlib` axes to plot on.
    energy_unit : str
        A valid `numericalunits` string expression for units.
    xlabel : bool, str
        x axis label.
    ylabel : bool, str
        y axis label.
    mark_points : list, tuple
        Marks special points on the potential profile.
    origin : str, float
       Energy origin: either float number of 'left', 'right', or 'median'.
    profile_kwargs : dict
        Arguments to ``kernel.profile_directed_strain``.
    kwargs
        Arguments to pyplot.plot.

    Returns
    -------
    ax : Axes
        `matplotlib` axes.
    """
    if ax is None:
        ax = pyplot.gca()

    if energy_unit is not None:
        energy_unit_val = nu_eval(energy_unit)
    else:
        energy_unit_val = 1

    if profile_kwargs is None:
        profile_kwargs = dict()

    strain = np.linspace(*limits)
    val = profile_directed_strain(potentials, cell, strain, direction, **profile_kwargs) / energy_unit_val

    if origin is None:
        origin = 0
    elif isinstance(origin, str):
        origin = dict(
            left=val[0],
            right=val[-1],
            median=.5 * (np.max(val) + np.min(val)),
        )[origin]

    ax.plot(strain, val - origin, **kwargs)

    if mark_points is not None:
        mark_points = np.array(mark_points)
        mark_points_val = profile_directed_strain(potentials, cell, mark_points, direction, **profile_kwargs) / energy_unit_val
        ax.scatter(mark_points, mark_points_val - origin, marker="x", color="black")

    if xlabel is True:
        ax.set_xlabel(f"{direction} expansion")
    elif xlabel:
        ax.set_xlabel(xlabel)
    if ylabel is True:
        ax.set_ylabel(f"Energy ({energy_unit})")
    elif ylabel:
        ax.set_ylabel(ylabel)

    return ax


def plot_potential_2(potentials, limits=None, pair=None, ax=None, energy_unit="Ry",
                     length_unit="angstrom", xlabel=True, ylabel=True, mark_points=None,
                     origin=None, **kwargs):
    """
    Plot potential profile between a pair of points.

    Parameters
    ----------
    potentials : LocalPotential, list
        The potential to plot.
    limits : tuple
        Limits in absolute units. Defaults to `(potential.cutoff / 10, potential.cutoff)`.
    pair : str
        Pair to plot.
    ax : Axes
        `matplotlib` axes to plot on.
    energy_unit : str
        A valid `numericalunits` string expression for units.
    length_unit : str
        A valid `numericalunits` string expression for units.
    xlabel : bool, str
        x axis label.
    ylabel : bool, str
        y axis label.
    mark_points : list, tuple
        Marks special points on the potential profile.
    origin : str, float
       Energy origin: either float number of 'left', 'right', or 'median'.
    kwargs
        Arguments to pyplot.plot.

    Returns
    -------
    ax : Axes
        `matplotlib` axes.
    """
    if not isinstance(potentials, (list, tuple)):
        potentials = [potentials]

    if pair is None:
        if len(potentials) == 1 and potentials[0].get_kernel_by_name("kernel").coordination_number == 2:
            if potentials[0].tag is None:
                potentials = [potentials[0].copy(tag="1-2")]
            pair = potentials[0].tag
        else:
            raise ValueError(f"Please specify which pair to profile using 'pair' arg")

    if xlabel is True:
        xlabel = f"r ({length_unit})"

    if limits is None:
        cutoff = max(i.cutoff for i in potentials)
        limits = (cutoff / 10, cutoff)

    a = nu_eval(length_unit)
    cell = Cell(
        [(2 * a, 0, 0), (0, 2 * a, 0), (0, 0, 2 * a)],
        [(0, 0, 0), (.5, 0, 0)],
        pair.split("-"),
    )
    return plot_strain_profile(
        potentials, cell,
        limits=np.array(limits) / a,
        direction=(1, 0, 0), ax=ax, energy_unit=energy_unit, xlabel=xlabel, ylabel=ylabel,
        mark_points=np.array(mark_points) / a if mark_points is not None else None,
        origin=origin, profile_kwargs=dict(pbc=False), **kwargs
    )


def plot_descriptors_2(descriptors, ax=None, length_unit="angstrom", xlabel=True, legend=True, **kwargs):
    """
    Plots two-point descriptor functions.

    Parameters
    ----------
    descriptors : dict
        A dictionary with atoms (keys) and descriptors.
    ax : Axes
        `matplotlib` axes to plot on.
    length_unit : str
        A valid `numericalunits` string expression for units.
    xlabel : bool, str
        x axis label.
    legend : bool
        If True, displays legend.
    kwargs
        Arguments to pyplot.plot.

    Returns
    -------
    ax : Axes
        `matplotlib` axes.
   """
    if ax is None:
        ax = pyplot.gca()

    for belongs_to, desc in sorted(descriptors.items()):
        for d in desc:

            if d.family is behler2_descriptor_family:
                try:
                    special = [behler_turning_point(**d.parameters)]
                except ValueError as e:
                    special = None
            else:
                special = None

            plot_potential_2(d, ax=ax, length_unit=length_unit, energy_unit="1",
                             xlabel=xlabel, ylabel=False, label=f"{belongs_to}: {d.tag}",
                             mark_points=special, **kwargs)
    if legend:
        ax.legend()

    return ax


def plot_convergence(y=None, append=True, ax=None, xlabel="Step", ylabel="Error", comment=None, grid=True,
                     labels=None):
    """
    Prepares convergence plots.

    Parameters
    ----------
    y : tuple, list, np.ndarray, float, None
        Error values.
    append : bool
        If True and `ax` is set, appends convergence data.
    ax : Axes
        `matplotlib` axes to plot on.
    xlabel : str
        x axis label.
    ylabel : str
        y axis label.
    comment : str
        An optional comment.
    grid : bool
        Plot grid.
    labels : list, tuple
        A list of labels for the legend.

    Returns
    -------
    ax : Axes
        `matplotlib` axis.
    """
    if y is None:
        y = [np.empty(0, dtype=float)]  # None = single empty convergence plot
    elif isinstance(y, int):
        y = [np.empty(0, dtype=float)] * y  # int = n empty convergence plots
    elif isinstance(y, float):
        y = [np.array([y])]  # float = single convergence point
    elif isinstance(y, np.ndarray):
        y = [y]  # array = single convergence array

    if comment is None:
        comment = ""

    y = tuple(map(np.array, y))
    for i in y:
        i.shape = i.size,

    def _plot_data(_y, prev=None):
        if prev is not None:
            _y = np.concatenate([prev, _y])
        return np.arange(len(_y)), _y

    if ax is None or not append:
        if ax is None:
            ax = pyplot.gca()
        ax.clear()

        if labels and len(labels) != len(y):
            raise ValueError(f"len(labels) = {len(labels):d} != len(y) = {len(y):d}")

        for i_data, data in enumerate(y):
            ax.semilogy(*_plot_data(data), label=labels[i_data] if labels else None)
        ax.text(0.05, 0.9, comment, transform=ax.transAxes)

        if xlabel:
            ax.set_xlabel(xlabel)
        if ylabel:
            ax.set_ylabel(ylabel)
        if grid:
            ax.grid(axis='y')
        if labels:
            ax.legend()

    else:
        plot_handles = ax.lines

        if len(plot_handles) < len(y):
            raise ValueError(f"len(ax.lines) = {len(plot_handles):d} < len(y) = {len(y):d}")
        if len(ax.texts) < 1:
            raise ValueError(f"len(ax.texts) = {len(ax.texts)} < 1")

        for handle, data in zip(plot_handles, y):
            if append:
                previous = handle.get_ydata()
            else:
                previous = None
            handle.set_data(*_plot_data(data, prev=previous))
        ax.texts[0].set_text(comment)

        ax.relim()
        ax.autoscale_view()

    return ax


def plot_diagonal(*args, replace=False, ax=None, xlabel="Reference", ylabel="Prediction", nmax=None,
                  unit_label=None, window=None, **kwargs):
    """
    Diagonal plot "reference" vs "data".

    Parameters
    ----------
    args
        Reference and prediction pairs.
    replace : bool
        If True and `ax` set, attempts to find previous data
        on the plot and to re-plot it.
    ax : Axes
        `matplotlib` axes to plot on.
    xlabel : str, None
        x axis label.
    ylabel : str, None
        y axis label.
    nmax : int
        Displays only few most outstanding values.
    unit_label : str
        Optional label to specify units in axes labels.
    window : tuple
        An optional window to constrain to.
    kwargs
        Arguments to `pyplot.scatter`.

    Returns
    -------
    ax : Axes
        `matplotlib` axis.
    """
    if unit_label is not None:
        if xlabel is not None:
            xlabel = f"{xlabel} ({unit_label})"
        if ylabel is not None:
            ylabel = f"{ylabel} ({unit_label})"

    if len(args) % 2 != 0:
        raise ValueError("Even argument count expected with reference-prediction pairs")

    _kwargs = dict(ls="none", marker="+")
    _kwargs.update(kwargs)
    kwargs = _kwargs

    args = tuple(np.array(i).ravel() for i in args)

    mn = min(i.min() for i in args)
    mx = max(i.max() for i in args)
    diag = np.array([mn, mx])

    args = list(zip(args[::2], args[1::2]))

    rmse = tuple(np.linalg.norm(reference - prediction) / reference.size ** .5 for reference, prediction in args)
    rmse_text = tuple(
        f"{_rmse:.3e}"
        if unit_label is None else
        f"{_rmse:.3e} {unit_label}"
        for _rmse in rmse
    )

    if nmax is not None:
        _args = []
        for reference, prediction in args:
            if nmax < len(reference):
                delta = np.abs(reference - prediction)
                ind = np.argpartition(delta, -nmax)[-nmax:]
                reference = reference[ind]
                prediction = prediction[ind]
            _args.append((reference, prediction))
        args = _args

    if window is not None:
        diag = np.array(window)

    if ax is None or not replace:
        if ax is None:
            ax = pyplot.gca()
        ax.plot(diag, diag, color="black", zorder=10)
        for (reference, prediction), label in zip(args, rmse_text):
            if window is not None:
                mask = reduce(np.logical_and, (
                    window[0] < reference,
                    reference < window[1],
                    window[0] < prediction,
                    prediction < window[1],
                ))
                reference = reference[mask]
                prediction = prediction[mask]
            ax.plot(reference, prediction, label=label, **kwargs)

        if xlabel:
            ax.set_xlabel(xlabel)
        if ylabel:
            ax.set_ylabel(ylabel)
        ax.set_aspect(1)
        ax.autoscale(tight=True)

    else:
        plot_handles = ax.lines
        if len(plot_handles) < len(args) + 1:
            raise ValueError(f"Expected at least {len(args) + 1:d} lines, found: {len(plot_handles):d}")
        plot_handles[0].set_data(diag, diag)
        for ph, (reference, prediction), label in zip(plot_handles[1:], args, rmse_text):
            if window is not None:
                mask = reduce(np.logical_and, (
                    window[0] < reference,
                    reference < window[1],
                    window[0] < prediction,
                    prediction < window[1],
                ))
                reference = reference[mask]
                prediction = prediction[mask]
            ph.set_data(reference, prediction)
            ph.set_label(label)
        ax.relim()
        ax.autoscale(tight=True)

    return ax
