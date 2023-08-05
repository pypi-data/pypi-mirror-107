import numericalunits as nu
import torch
from itertools import chain
from functools import partial, wraps
from collections import namedtuple, Counter, OrderedDict
import warnings
from math import isnan
import numpy as np
from scipy.optimize import root_scalar
import logging
from pathlib import Path
import matplotlib
from matplotlib import pyplot

from .potentials import behler2_descriptor_family, PotentialRuntimeWarning, behler_turning_point,\
    behler4_descriptor_family, behler5_descriptor_family, potential_from_state_dict, behler5x_descriptor_family
from .ml import fw_cauldron, fw_cauldron_charges, Dataset, Normalization, potentials_from_ml_data, learn_cauldron,\
    cpu_copy
from .kernel import NeighborWrapper, Cell
from .util import dict_reduce
from .units import UnitsDict, check_units_known
from .presentation import plot_convergence, plot_diagonal, text_bars


def behler_nn(n_inputs, n_internal=15, n_layers=3, bias=True, activation=None):
    """
    Behler choice for neural network potential.

    Parameters
    ----------
    n_inputs : int
        Input count.
    n_internal : int
        Internal dimension size.
    n_layers : int
        Linear layer count.
    bias : bool, list
        If True, use bias in linear layers (optionally, defined per-layer).
    activation
        Activation layer class (defaults to Sigmoid).

    Returns
    -------
    result : torch.nn.Sequential
        The resulting neural network.
    """
    if isinstance(bias, (list, tuple)):
        if len(bias) != n_layers:
            raise ValueError(f"len(bias) = {len(bias)} != n_layers = {n_layers}")
    else:
        bias = (bias,) * n_layers
    if activation is None:
        activation = torch.nn.Sigmoid

    if n_layers == 1:
        layers = [torch.nn.Linear(n_inputs, 1, bias=bias[0])]
    else:
        layers = [
            torch.nn.Linear(n_inputs, n_internal, bias=bias[0]),
            *sum((
                (activation(), torch.nn.Linear(n_internal, n_internal, bias=b))
                for b in bias[1:-1]
            ), tuple()),
            activation(),
            torch.nn.Linear(n_internal, 1, bias=bias[-1]),
        ]
    return torch.nn.Sequential(*layers)


def default_behler_descriptors(arg, n, a, left=1, common_eta=True):
    """
    Default Behler descriptor choice.
    
    Parameters
    ----------
    arg : dict, list, tuple
        A dict with minimal distance between atoms
        per specimen pair or wrapped cells to deduce
        these distances from.
    n : int
        Descriptor count.
    a : float
        The function cutoff.
    left : float
        Left boundary factor.
    common_eta : bool
        Pick common etas.

    Returns
    -------
    descriptors : dict
        A dict with descriptors.
    """
    def _eta_for_tp(_tp):
        if _tp > a / 2:
            raise ValueError(f"The turning point requested {_tp} is more than half-way to the cutoff {a}")

        def _target(_x):
            return behler_turning_point(a, _x, 0) - _tp

        bracket = 0, 10000 / a ** 2

        return root_scalar(_target, bracket=bracket, method='bisect').root

    if not isinstance(arg, dict):
        arg = dict_reduce((
            w.pair_reduction_function(lambda x, r, c: x.min() if len(x) > 0 else None)
            for w in arg
        ), min)

    etas = {}
    for k, d in arg.items():
        d *= left
        if d > a / 2:
            raise ValueError(f"The minimal interatomic distance {d} for entity {k} "
                             f"is more than half-way to the cutoff {a}")
        etas[k] = _etas = []
        for tp in np.linspace(d, a / 2, n):
            _etas.append(_eta_for_tp(tp))

    if common_eta:
        _etas = np.mean(list(etas.values()), axis=0)
        etas = {k: _etas for k in etas}

    descriptors_raw = {
        k: list(behler2_descriptor_family(a=a, eta=eta, r_sphere=0, tag=k) for eta in v)
        for k, v in etas.items()
    }

    all_species = sorted(set(sum((i.split("-") for i in descriptors_raw), [])))

    descriptors = {}
    for i_s1, s1 in enumerate(all_species):
        for s2 in all_species[i_s1:]:
            tags = f"{s1}-{s2}", f"{s2}-{s1}"

            d = None
            for sp in tags:
                if sp in descriptors_raw:
                    d = descriptors_raw.pop(sp)

            if d is not None:
                if s1 not in descriptors:
                    descriptors[s1] = []
                descriptors[s1] += list(i.copy(tag=tags[0]) for i in d)

                if s1 != s2:
                    if s2 not in descriptors:
                        descriptors[s2] = []
                    descriptors[s2] += list(i.copy(tag=tags[1]) for i in d)
    return descriptors


def default_behler_descriptors_3(arg, a, eta=0, zeta=(1, 2, 4, 16), family=4, cos_theta0=-1, amount_5x="full"):
    """
    Default Behler descriptor choice.

    Parameters
    ----------
    arg : dict, list, tuple
        A dict with minimal distance between atoms
        per specimen pair or wrapped cells to deduce
        these distances from.
    a : float
        The function cutoff.
    eta : float, list
        A list of etas.
    zeta : float, tuple, list
        A list of zetas.
    family : {4, 5, "5x", LocalPotentialFamily}
        Descriptor family to employ. Integers stand for
        type-4 or type-5 descriptor kinds.
    cos_theta0 : float, tuple, list
        A list of angles where the '5x' descriptor vanishes.
        Ignored for other descriptors.
    amount_5x : {"full", "half"}
        Includes all or a half of eta combinations. Useful for
        sorted large etas.

    Returns
    -------
    descriptors : dict
        A dict with descriptors.
    """
    assert amount_5x in {"full", "half"}
    if len(arg) == 0:
        raise ValueError("Empty input")
    if isinstance(eta, (int, float)):
        eta = eta,
    if isinstance(zeta, (int, float)):
        zeta = zeta,
    if isinstance(cos_theta0, (int, float)):
        cos_theta0 = cos_theta0,
    if isinstance(family, (int, str)):
        family = {4: behler4_descriptor_family, 5: behler5_descriptor_family, "5x": behler5x_descriptor_family}[family]
    if not isinstance(arg[0], str):
        _species = set()
        for i in arg:
            _species |= set(i.values)
        arg = _species

    arg = sorted(arg)
    descriptors = {k: [] for k in arg}
    for p1 in arg:
        for i, p2 in enumerate(arg):
            for p3 in arg[i:]:
                tag = f"{p1}-{p2}-{p3}"
                for _i_eta, _eta in enumerate(eta):
                    if family is behler5x_descriptor_family:
                        if amount_5x == "full":
                            _etas2 = eta[_i_eta:]
                        elif amount_5x == "half":
                            _etas2 = eta[_i_eta:len(eta) - _i_eta]
                        else:
                            raise ValueError(f"Unknown amount_5x={amount_5x}")
                        for _eta2 in _etas2:
                            for _cos in cos_theta0:
                                descriptors[p1].append(family(eta1=_eta, eta2=_eta2, cos_theta0=_cos, a=a, tag=tag))
                    else:
                        for _zeta in zeta:
                            for l in 1, -1:
                                descriptors[p1].append(family(eta=_eta, l=l, zeta=_zeta, a=a, tag=tag))
    return descriptors


def parse_runner_input(f, strict=True):
    """
    Parses RuNNer input file for atomic descriptors.
    
    Parameters
    ----------
    f : str, file
        File or file name to parse.
    strict : bool
        Defines the behavior on unrecognized data: raises
        ``ValueError`` when True or ignores when False.
        
    Returns
    -------
    result : list
        A list of descriptors.
    """
    result = []
    if isinstance(f, (str, Path)):
        f = open(f, 'r')

    for line in f:
        line = line.strip()
        if line.startswith("#") or len(line) == 0:
            pass
        elif line.startswith("symfunction_short"):
            params = line.split()[1:]
            descriptor_id = params[1]

            if descriptor_id == '2':
                a1, descriptor_id, a2, eta, r_sphere, a = params[:6]
                eta, r_sphere, a = map(float, (eta, r_sphere, a))
                result.append(behler2_descriptor_family(
                    eta=eta / nu.aBohr ** 2,
                    r_sphere=r_sphere * nu.aBohr,
                    a=a * nu.aBohr,
                    tag=f"{a1}-{a2}",
                ))

            elif descriptor_id == '3':
                a1, descriptor_id, a2, a3, eta, l, zeta, a = params[:8]
                eta, l, zeta, a = map(float, (eta, l, zeta, a))
                result.append(behler4_descriptor_family(
                    eta=eta / nu.aBohr ** 2,
                    l=l,
                    zeta=zeta,
                    a=a * nu.aBohr,
                    tag=f"{a1}-{a2}-{a3}",
                ))  # By fact, descriptor_id == '3' means fourth Behler function from Behler's paper

            else:
                if strict:
                    raise ValueError(f"Unknown descriptor {repr(descriptor_id)}")
                else:
                    pass
        else:
            if strict:
                raise ValueError(f"Cannot parse '{line}'")
            else:
                pass

    return result


def parse_lammps_input(f, simplify=True):
    """
    Parse LAMMPS input for NN potential.

    Parameters
    ----------
    f : file
        Text file to parse.
    simplify : bool
        Attempt to simplify the resulting module.

    Returns
    -------
    result : dict
        A dict of potentials.
    """
    behler2_parameter_order = "a", "eta", "r_sphere"
    behler4_parameter_order = "a", "eta", "zeta", "l"

    def _array(_x, dtype=float):
        return np.array(tuple(map(dtype, _x)))

    descriptors = {}
    scales = {}
    layers = {}

    lines = iter(f)
    for line in lines:
        if line.startswith("POT"):
            _, element, _ = line.split()
            descriptors[element] = []
            scales[element] = []
            layers[element] = []
            _id, n_descriptors = next(lines).split()
            assert _id == "SYM"
            n_descriptors = int(n_descriptors)
            for i in range(n_descriptors):
                parameters_all = next(lines).split()
                parameters = _array(parameters_all[:5])
                parameters[1] *= nu.angstrom
                parameters[2] /= nu.angstrom ** 2
                elements = parameters_all[5:]
                if parameters[0] == 2:
                    parameters[3] *= nu.angstrom
                    parameters = dict(zip(behler2_parameter_order, parameters[1:]))
                    descriptors[element].append(behler2_descriptor_family(
                        **parameters, tag="-".join([element] + list(elements))
                    ))
                elif parameters[0] == 4:
                    parameters = dict(zip(behler4_parameter_order, parameters[1:]))
                    if elements[0] == elements[1]:
                        parameters["epsilon"] = 0.5  # No double-counting
                    descriptors[element].append(behler4_descriptor_family(
                        **parameters, tag="-".join([element] + list(elements))
                    ))
                else:
                    raise NotImplementedError(f"Unknown descriptor {parameters[0]}")

            for block in "scale1", "scale2":
                _id, *parameters = next(lines).split()
                assert _id == block
                assert len(parameters) == n_descriptors
                scales[element].append(_array(parameters))

            _id, n_layers, *net_shape = next(lines).split()
            assert _id == "NET"
            n_layers = int(n_layers)
            net_shape = _array(net_shape, dtype=int)
            assert net_shape[n_layers] == 1
            net_shape = net_shape[:n_layers + 1]

            input_dims = n_descriptors
            for i, output_dims in enumerate(net_shape):
                _id, _ix, kind = next(lines).split()
                assert _id == "LAYER"
                assert float(_ix) == i

                weights = []
                bias = []
                for j in range(output_dims):
                    _id, *x = next(lines).split()
                    assert _id == f"w{j:d}"
                    weights.append(_array(x))

                    _id, b = next(lines).split()
                    assert _id == f"b{j:d}"
                    bias.append(float(b))

                linear = torch.nn.Linear(input_dims, output_dims, bias=True)
                linear.weight = torch.nn.Parameter(torch.tensor(np.array(weights)))
                linear.bias = torch.nn.Parameter(torch.tensor(np.array(bias)))
                layers[element].append(linear)

                if kind == "sigmoid":
                    layers[element].append(torch.nn.Sigmoid())
                elif kind == "linear":
                    pass
                else:
                    raise NotImplementedError(f"Unknown layer: {kind}")

                input_dims = int(output_dims)

    nn = []
    for _, _layers in sorted(layers.items()):
        nn.append(torch.nn.Sequential(*_layers))

    normalization = Normalization(
        energy_scale=torch.tensor(np.array(nu.eV)),
        features_scale=[torch.tensor(v[1]) for _, v in sorted(scales.items())],
        energy_offsets=torch.tensor(np.zeros((len(scales), 1), dtype=float)),
        features_offsets=[torch.tensor(v[0]) for _, v in sorted(scales.items())],
    )
    return potentials_from_ml_data(nn=nn, descriptors=descriptors, normalization=normalization, simplify=simplify)


def torch_load(f, **kwargs):
    """
    Wraps torch.load to load to CPU.

    Parameters
    ----------
    f : str, Path
        The file name.
    kwargs
        Other arguments.

    Returns
    -------
    The deserialized result.
    """
    defaults = dict(map_location=torch.device('cpu'))
    defaults.update(kwargs)
    return torch.load(f, **defaults)


def load_potentials(f, deserializer=torch_load):
    """
    Loads a list of potentials from a file.
    
    Parameters
    ----------
    f : str, Path
        The file name.
    deserializer : Callable
        Deserializer routine.

    Returns
    -------
    result : list
        A list of potentials.
    """
    return list(map(potential_from_state_dict, deserializer(f)))


def save_potentials(potentials, f, serializer=torch.save):
    """
    Saves a list of potentials to a file.

    Parameters
    ----------
    potentials : list
        A list of potentials.
    f : str, Path
        The file to save to.
    serializer : Callable
        Serializer routine.
    """
    serializer(list(i.state_dict() for i in potentials), f)


loss_result = namedtuple("loss_result", ("loss_id", "loss_value", "reference", "prediction", "components"))


def energy_loss(networks, data, criterion, w_energy, w_gradients, energies_p=False):
    """
    Energy loss function.

    Parameters
    ----------
    networks : list
        A list of networks to learn.
    data : Dataset
        The dataset to compute loss function of.
    criterion : torch.nn.Module
        Loss criterion.
    w_energy : float
        Energy weight in the loss function.
    w_gradients : float
        Gradients weight in the loss function.
    energies_p : bool
        If True, compares partial energies.

    Returns
    -------
    result : loss_result
        The resulting loss and accompanying information.
    """
    result = fw_cauldron(networks, data, grad=w_gradients != 0, energies_p=energies_p)
    if w_gradients != 0:
        e, g = result
    else:
        e = result
        g = None

    if energies_p:
        energy_loss_results = []
        de = 0
        for e_, data_ in zip(e, data.per_point_datasets):
            de_ = criterion(e_, data_.energies_p)
            de += de_
            energy_loss_results.append(loss_result(
                loss_id=f"partial energy {data_.tag}",
                loss_value=de_,
                reference=data_.energies_p,
                prediction=e_,
                components=None,
            ))

        energy_loss_result = loss_result(
            loss_id="energy",
            loss_value=de,
            reference=None,
            prediction=None,
            components=tuple(energy_loss_results),
        )
    else:
        de = criterion(e, data.per_cell_dataset.energy)

        energy_loss_result = loss_result(
            loss_id="energy",
            loss_value=de,
            reference=data.per_cell_dataset.energy,
            prediction=e,
            components=None,
        )

    if w_gradients == 0:
        return energy_loss_result

    else:
        dg = criterion(g, data.per_cell_dataset.energy_g)
        gradients_loss_result = loss_result(
            loss_id="gradients",
            loss_value=dg,
            reference=data.per_cell_dataset.energy_g,
            prediction=g,
            components=None,
        )

        loss = de * w_energy + dg * w_gradients

        return loss_result(
            loss_id="total",
            loss_value=loss,
            reference=None,
            prediction=None,
            components=(energy_loss_result, gradients_loss_result),
        )


def charges_loss(networks, data, criterion):
    """
    Charges loss function.

    Parameters
    ----------
    networks : list
        A list of networks to learn.
    data : Dataset
        The dataset to compute loss function of.
    criterion : torch.nn.Module
        Loss criterion.

    Returns
    -------
    result : loss_result
        The resulting loss and accompanying information.
    """
    charges = fw_cauldron_charges(networks, data)
    loss = 0
    loss_components = []
    for charge, ppd in zip(charges, data.per_point_datasets):
        l = criterion(charge, ppd.charges)
        loss_components.append(loss_result(
            loss_id=ppd.tag,
            loss_value=l,
            reference=ppd.charges,
            prediction=charge,
            components=None,
        ))
        loss += l

    return loss_result(
        loss_id="total",
        loss_value=loss,
        reference=None,
        prediction=None,
        components=tuple(loss_components),
    )


LBFGS = partial(torch.optim.LBFGS, line_search_fn="strong_wolfe")


class SimpleClosure:
    def __init__(self, networks, loss_function, dataset=None, criterion=None, optimizer=None,
                 optimizer_kwargs=None, loss_function_kwargs=None):
        """
        A simple closure for learning NN potentials.

        Parameters
        ----------
        networks : list
            A list of networks to learn.
        loss_function : Callable
            A function `loss(networks, data, criterion, **loss_kwargs)`
            returning `loss_result` tuple.
        dataset : Dataset
            Default dataset to compute the loss for.
        criterion : torch.nn.Module
            Loss criterion, defaults to MSE with 'sum' reduction.
        optimizer : torch.optim.Optimizer
            Optimizer, defaults to Adam.
        optimizer_kwargs : dict
            Additional optimizer arguments.
        loss_function_kwargs : dict
            Loss function arguments.
        """
        if criterion is None:
            criterion = torch.nn.MSELoss()
        if optimizer is None:
            optimizer = LBFGS
        if optimizer_kwargs is None:
            optimizer_kwargs = {}
        if loss_function_kwargs is None:
            loss_function_kwargs = {}
        self.networks = networks
        self.loss_function = loss_function
        self.dataset = dataset
        self.criterion = criterion
        self.__optimizer__ = optimizer
        self.__optimizer_kwargs__ = optimizer_kwargs
        self.optimizer = self.optimizer_init()
        self.loss_function_kwargs = loss_function_kwargs

        self.last_loss = None

    def optimizer_init(self, optimizer=None, **kwargs):
        """
        Initialize the optimizer.

        Parameters
        ----------
        optimizer
            Optimizer class.
        kwargs
            Arguments to the constructor.

        Returns
        -------
        optimizer
            The resulting optimizer object.
        """
        if optimizer is None:
            optimizer = self.__optimizer__
        opt_args = self.__optimizer_kwargs__.copy()
        opt_args.update(kwargs)
        self.optimizer = optimizer(self.learning_parameters(), **opt_args)
        return self.optimizer

    def learning_parameters(self):
        """
        Learning parameters.

        Returns
        -------
        params : Iterable
            Parameters to learn.
        """
        return chain(*tuple(i.parameters() for i in self.networks))

    def loss(self, dataset=None, save=True):
        """
        The loss function.

        Parameters
        ----------
        dataset : Dataset
            The dataset to compute loss function of.
        save : bool
            If True, stores the result in ``self.last_loss``.

        Returns
        -------
        result : stats_tuple
            The resulting loss and accompanying information.
        """
        if dataset is None:
            if self.dataset is None:
                raise ValueError("No dataset provided and the default dataset is None")
            dataset = self.dataset
        loss = self.loss_function(self.networks, dataset, self.criterion, **self.loss_function_kwargs)
        if save:
            self.last_loss = loss
        return loss

    def propagate(self, dataset=None):
        """
        Propagates the closure.

        Parameters
        ----------
        dataset : torch.utils.data.Dataset
            The dataset to compute loss function of.

        Returns
        -------
        result : torch.Tensor
            The resulting loss.
        """
        self.optimizer.zero_grad()
        loss_tuple = self.loss(dataset=dataset)
        loss = loss_tuple.loss_value
        if isnan(loss.item()):
            raise RuntimeError(f"Optimizer is not stable with loss={loss}")
        loss.backward()
        return loss

    def __call__(self, dataset=None):
        return self.propagate(dataset=dataset)

    def optimizer_step(self):
        """
        Performs an optimization step.
        """
        return self.optimizer.step(self)


def simple_energy_closure(networks, dataset=None, criterion=None, optimizer=None, optimizer_kwargs=None,
                          w_energy=1, w_gradients=0, energies_p=False):
    """
    Energy and forces closure.

    Parameters
    ----------
    networks : list
        A list of networks to learn.
    dataset : Dataset
        Default dataset to compute loss for.
    criterion : torch.nn.Module
        Loss criterion, defaults to MSE.
    optimizer : torch.optim.Optimizer
        Optimizer, defaults to Adam.
    optimizer_kwargs : dict
        Additional optimizer arguments.
    w_energy : float
        Energy weight in the loss function.
    w_gradients : float
        Gradients weight in the loss function.
    energies_p : bool
        If True, considers the loss of partial energy.

    Returns
    -------
    closure : SimpleClosure
        The closure function.
    """
    return SimpleClosure(networks, energy_loss, dataset=dataset, criterion=criterion, optimizer=optimizer,
                         optimizer_kwargs=optimizer_kwargs,
                         loss_function_kwargs=dict(w_energy=w_energy, w_gradients=w_gradients, energies_p=energies_p))


def simple_charges_closure(networks, dataset=None, criterion=None, optimizer=None, optimizer_kwargs=None):
    """
    Charges closure.

    Parameters
    ----------
    networks : list
        A list of networks to learn.
    dataset : Dataset
        Default dataset to compute loss for.
    criterion : torch.nn.Module
        Loss criterion, defaults to MSE.
    optimizer : torch.optim.Optimizer
        Optimizer, defaults to Adam.
    optimizer_kwargs : dict
        Additional optimizer arguments.

    Returns
    -------
    closure : SimpleClosure
        The closure function.
    """
    return SimpleClosure(networks, charges_loss, dataset=dataset, criterion=criterion, optimizer=optimizer,
                         optimizer_kwargs=optimizer_kwargs)


def requires_fields(*names):
    """
    A decorator to ensure that the listed class fields are set.

    Parameters
    ----------
    names
        A list of fields.

    Returns
    -------
    decorator : Callable
        The decorator.
    """
    def _decorator(_f):
        @wraps(_f)
        def _sub(_self, *_args, **_kwargs):
            for i in names:
                if getattr(_self, i) is None:
                    raise RuntimeError(f"Attribute '{i}' is required at this stage")
            return _f(_self, *_args, **_kwargs)
        return _sub
    return _decorator


def pull(a):
    """
    Pulls array to numpy.

    Parameters
    ----------
    a : torch.Tensor

    Returns
    -------
    result : np.ndarray
        The resulting array.
    """
    return a.detach().cpu().numpy()


class Workflow:
    def __init__(self, dtype=torch.float64, log=None, seed=None, mpl_backend=None, mpl_save_ext="png", units=None,
                 units_are_known=False, tag=None):
        """
        A class defining a typical workflow.

        Parameters
        ----------
        dtype : torch.dtype
            Default floating point data type for all tensors involved.
        log : logging.Logger
            The logger for this.
        seed
            Initialize torch and numpy with the provided seed.
        mpl_backend : str
            Matplotlib backend.
        mpl_save_ext : str
            Default matplotlib save image format.
        units : dict, str
            A dictionary with units ('length', 'energy', 'force', ...)
            to print and to plot. Uses default eV-angstrom units if
            'default' passed.
        units_are_known : bool
            Indicates units in numericalunits are set and known. If True,
            the corresponding warning will not be raised.
        tag : str
            Tag for output files.
        """
        self.dtype = dtype
        if log is None:
            self.log = logging.getLogger(__name__)
        else:
            self.log = log

        if seed is not None:
            np.random.seed(seed)
            torch.manual_seed(seed)

        if mpl_backend is not None:
            matplotlib.use(mpl_backend)

        self.mpl_save_ext = mpl_save_ext
        if units is None:
            units = dict()
        elif units == "default":
            units = dict(energy="meV", length="angstrom", force="meV/angstrom")
        self.units = UnitsDict(units)
        if tag is not None:
            self.tag = str(tag)
        else:
            self.tag = None

        self.cells = None  # A list of cells
        self._cutoff = None  # neighbor cutoff
        self.cells_nw = None  # wrapped cells
        if not units_are_known:
            check_units_known(self.log)

    @classmethod
    def load_cells_individual(cls, filename):
        """
        Load a single piece of the dataset.

        Parameters
        ----------
        filename : str, Path
            The path to load.

        Returns
        -------
        result : list
            A list of Cells.
        """
        with open(filename, 'r') as f:
            return Cell.load(f)

    def load_cells(self, filenames, root=None, append=False):
        """
        Loads cells (structural data) from files.

        Parameters
        ----------
        filenames : str, list, tuple, Path
            File names or patterns to load.
        root : str, Path
            The root folder to load from.
        append : bool
            If True, appends the data to previously loaded cells.

        Returns
        -------
        result : np.ndarray
            The resulting cells.
        """
        self.log.info("Loading cells ...")
        root = Path() if root is None else Path(root)
        if not isinstance(filenames, (list, tuple)):
            filenames = [filenames]
        result = []
        for pattern in filenames:
            if isinstance(pattern, str):
                self.log.info(f"  pattern {pattern}")
                fns = sorted(root.glob(pattern))
                if len(fns) == 0:
                    self.log.error(f"Pattern {pattern} not found in {root}")
                    raise ValueError(f"File not found or no match for pattern '{pattern}'")
                for fn in fns:
                    self.log.info(f"    file {fn}")
                    result.extend(self.load_cells_individual(fn))
            elif isinstance(pattern, Path):
                self.log.info(f"  file {pattern}")
                result.extend(self.load_cells_individual(pattern))
            elif isinstance(pattern, (list, tuple, np.ndarray)):
                assert all(isinstance(i, Cell) for i in pattern)
                result.extend(pattern)
            elif isinstance(pattern, Cell):
                result.append(pattern)
            else:
                raise ValueError(f"Unknown input: {pattern}")
        result = np.array(result)
        if append and self.cells is not None:
            self.cells = np.concatenate([self.cells, result])
            self.log.info(f"Total structure count: {len(self.cells):d} (+{len(result):d})")
        else:
            self.cells = result
            self.log.info(f"Total structure count: {len(result):d}")
        return result

    @requires_fields("cells")
    def reorder_cells(self, order):
        """
        Reorders cells.

        Parameters
        ----------
        order : str
            Order of cells: 'random'.

        Returns
        -------
        result : list
            Ordered cells.
        """
        if order == "random":
            self.log.info(f"Randomize sample order")
            self.cells = np.random.permutation(self.cells)
        else:
            raise ValueError(f"Unknown order: {order}")
        return self.cells

    @requires_fields("cells")
    def subset_cells(self, subset):
        """
        Retrieves a subset of cells.

        Parameters
        ----------
        subset : int
            The subset size. Currently only takes a subset
            beginning from the first cell.

        Returns
        -------
        result : np.ndarray
            Subset cells.
        """
        self.log.info(f"Subset of size {subset:d} requested")
        self.cells = self.cells[:subset]
        return self.cells

    @requires_fields("cells")
    def save_cells(self, destination):
        """
        Save cells into a file.

        Parameters
        ----------
        destination : str, file
            The file to save to.
        """
        self.log.info(f"Saving {len(self.cells):d} structures to {destination} ...")
        if isinstance(destination, str):
            with open(destination, 'w') as f:
                Cell.save(self.cells, f)
        else:
            Cell.save(self.cells, destination)

    @property
    def cutoff(self):
        return self._cutoff

    @cutoff.setter
    def cutoff(self, cutoff):
        self.log.info(f"Cutoff = {self.units.repr1(cutoff, 'length')}")
        self._cutoff = cutoff

    @requires_fields("cells", "_cutoff")
    def compute_neighbors(self, parallel=False, pool_kwargs=None, **kwargs):
        """
        Computes neighbors (images) data.

        Parameters
        ----------
        parallel : bool
            If True, computes in parallel.
        pool_kwargs : dict
            Arguments to Pool.
        kwargs
            Arguments to NeighborWrapper constructor.

        Returns
        -------
        cells_nw : list
            A list of wrapped cells.
        """
        self.log.info(f"Computing neighbors for {len(self.cells):d} structures (parallel={parallel}) ...")
        if parallel:
            if pool_kwargs is None:
                pool_kwargs = dict()
            worker = partial(NeighborWrapper, cutoff=self.cutoff, **kwargs)
            pool = torch.multiprocessing.Pool(**pool_kwargs)
            cells_nw = pool.map(worker, self.cells, chunksize=100)
            pool.close()
        else:
            cells_nw = list(NeighborWrapper(i, cutoff=self.cutoff, **kwargs) for i in self.cells)
        n_imgs = np.array(list(len(i.shift_vectors) for i in cells_nw))
        self.log.info(f"  image count: min {n_imgs.min():d} max {n_imgs.max():d} avg {np.mean(n_imgs):.1f}")
        self.cells_nw = cells_nw
        return cells_nw


diag_plot_props = namedtuple("diag_plot_props", ("scale", "unit", "title"))


def minimum_loss_save_policy(tag, loss, state):
    """
    A saving policy triggering whenever a global minimum in the loss function occurs.

    Parameters
    ----------
    tag : str
        Dataset tag.
    loss : loss_result
        The loss.
    state
        The state object from the previous call.

    Returns
    -------
    do_save : bool
        Indicates whether saving needs to be performed.
    state
        Whatever data needs to be passed to the next call of this function.
    """
    v = loss.loss_value.detach().item()
    if state is None:
        return True, v
    return v < state, min(v, state)


class FitWorkflow(Workflow):
    def __init__(self, **kwargs):
        """
        A class defining a typical workflow for potential fitting.

        Parameters
        ----------
        kwargs
            Arguments to Workflow.
        """
        super().__init__(**kwargs)

        self.descriptors = None  # a dict with descriptors
        self.datasets = {}  # a dictionary specifying datasets (values) for each purpose (keys)
        self.normalization = None  # dataset normalization
        self.nn = None  # neural networks
        self.closure = None  # closure
        self.losses = None  # a dictionary of loss functions
        self.nn_potentials = None  # neural-network potentials
        self.datasets_stat = {}  # dataset statistics

        self.on_plot_update = None  # action to perform whenever plot is updated
        self.figures = None  # plot figures
        self.axes = None  # plot axes
        self.nb_display_handles = None  # Notebook plots
        self.__diag_scale__ = None  # scale for the diagonal plot
        self.__inset_indicator_patches__ = []  # patches indicating insets to be removed each time plots are updated
        self.__diagonal_inset_plot_ranges__ = None  # inset ranges: either a number or a list of ranges
        self.__history_plot_annotations__ = {}  # annotations on the convergence history plot
        self.__history_plot_annotation_objects__ = []  # annotation objects to be removed on update

    @requires_fields("cells_nw")
    def init_default_descriptors(self, n=6, a=None, left=1, common_grid=True, three_point=True,
                                 three_point_family=4, **kwargs):
        """
        Provides a default set of descriptors.

        Parameters
        ----------
        n : int
            Descriptor radial sampling.
        a : float
            Descriptor cutoff. Defaults to 12 aBohr.
        left : float
            Left descriptor edge.
        common_grid : bool
            If True, all species share the same radial grid.
        three_point : bool, str
            If True, include three-point descriptors with the largest cutoff value and ``eta=0``.
            If 'all', include three-point descriptors with all etas.
        three_point_family : int
            Determines which descriptor family to use for 3-point descriptors:
            type-4 or type-5 descriptors.
        kwargs
            Arguments to ``default_behler_descriptors_3``. Ignored if ``three_point`` is False.

        Returns
        -------
        descriptors : dict
            The resulting descriptor set.
        """
        assert three_point in (False, True, 'all')
        if a is None:
            a = 12 * nu.aBohr
        self.log.info(f"Preparing default descriptor set ...")
        self.log.info(f"  n = {n:d}")
        self.log.info(f"  a = {self.units.repr1(a, 'length')}")
        self.log.info(f"  left edge = {left:f}")
        self.log.info(f"  common grid: {common_grid}")
        self.log.info(f"  3p: {three_point}, family: {three_point_family}")
        descriptors = default_behler_descriptors(self.cells_nw, n=n, a=a, left=left, common_eta=common_grid)
        all_descriptors = sum(map(tuple, descriptors.values()), tuple())
        all_etas = sorted(set(i.parameters["eta"] for i in all_descriptors))
        self.log.info(f"  etas: {all_etas}")
        if three_point:
            for k, v in default_behler_descriptors_3(
                self.cells_nw, a=a,
                eta=0 if three_point is True else all_etas,
                family=three_point_family,
                **kwargs
            ).items():
                descriptors[k].extend(v)
        self.descriptors = descriptors
        return descriptors

    def load_descriptors(self, arg):
        """
        Load descriptors from a file or a dictionary.

        Parameters
        ----------
        arg : str, Path, dict
            File with descriptors to parse or a dictionary with descriptors.

        Returns
        -------
        descriptors : dict
            The resulting descriptors.
        """
        if isinstance(arg, (str, Path)):
            self.log.info(f"Loading descriptors from {arg} ...")
            self.descriptors = parse_runner_input(arg)
        else:
            self.descriptors = arg
        return self.descriptors

    @requires_fields("descriptors")
    def compute_cutoff(self):
        """
        Computes descriptor cutoff and returns it.

        Returns
        -------
        result : float
            The cutoff value.
        """
        self.cutoff = max((max((i.cutoff for i in dsc), default=0) for dsc in self.descriptors.values()), default=0)
        return self.cutoff

    @requires_fields("cells_nw", "descriptors")
    def compute_descriptors(self, parallel=False, chunksize=None, source=None, destination="learn", pool_kwargs=None,
                            **kwargs):
        """
        Computes descriptors.

        Parameters
        ----------
        parallel : bool, str
            If True, computes in multiple processes.
        chunksize : int, None
            The size of a single task in parallel mode. Defaults to 100.
        source : list, None
            Which cells to take.
        destination : str
            The destination for the dataset in ``self.datasets``.
        pool_kwargs : dict
            Arguments to Pool constructor in parallel mode.
        kwargs
            Arguments to `ml.learn_cauldron`.

        Returns
        -------
        result : Dataset
            The resulting dataset.
        """
        self.log.info("Descriptors:")
        for k, v in sorted(self.descriptors.items()):
            n_desc = Counter(i.family.tag for i in v)
            self.log.info(f"  {k}: {len(v)}")
            for _k, _v in sorted(n_desc.items()):
                self.log.info(f"    {_k}: {_v:d}")
        if source is None:
            source = self.cells_nw
        self.log.info(f"Computing descriptors for {len(source):d} structures (parallel={parallel}) ...")
        if parallel == "openmp":
            kwargs["prefer_parallel"] = True
            parallel = False
        elif parallel:
            if "prefer_parallel" in kwargs:
                v = kwargs["prefer_parallel"]
                if v is not False:
                    self.log.warning(f"The argument 'prefer_parallel' is explicitly set to {v}. It is advised to set "
                                     f"this argument to False to avoid interference and deadlocks between "
                                     f"multiprocessing, OpenMP and torch")
            else:
                kwargs["prefer_parallel"] = False

        worker = partial(learn_cauldron, descriptors=self.descriptors, normalize=False, **kwargs)

        if parallel:
            # Disable OpenMP because it causes deadlocks
            num_omp_threads = torch.get_num_threads()
            torch.set_num_threads(1)

            if chunksize is None:
                chunksize = 100
            n_parts = int(np.ceil(len(source) / chunksize))
            if pool_kwargs is None:
                pool_kwargs = dict()
            pool = torch.multiprocessing.Pool(**pool_kwargs)
            self.log.info(f"  chunk size: {chunksize:d} parts total: {n_parts}")
            result = Dataset.cat(pool.map(
                worker,
                (source[i * chunksize:(i + 1) * chunksize] for i in range(n_parts)),
                chunksize=1,
            ))
            pool.close()
            torch.set_num_threads(num_omp_threads)
        else:
            result = worker(source)

        self.datasets[destination] = result
        return result

    def compute_normalization(self, source="learn", **kwargs):
        """
        Computes the normalization.

        Parameters
        ----------
        source : str, Dataset
            The dataset to deduce the normalization from.
        kwargs
            Arguments to `Normalization.from_dataset`.

        Returns
        -------
        norm : Normalization
            The normalization of the dataset.
        """
        if isinstance(source, str):
            source = self.datasets[source]
        self.log.info("Computing the normalization ...")
        defaults = dict(scale_energy=1000, offset_energy=True)
        defaults.update(kwargs)
        self.normalization = Normalization.from_dataset(source, **defaults)
        self.log.info("Energy offsets:")
        for k, v in zip(sorted(self.descriptors), self.normalization.energy_offsets.numpy().squeeze(axis=1)):
            self.log.info(f"  {k} = {self.units.repr1(v, 'energy')}")
        e_scale = self.normalization.energy_scale.item()
        self.log.info(f"Energy scale = {self.units.repr1(e_scale, 'energy')}")
        return self.normalization

    @requires_fields("normalization")
    def apply_normalization(self, *names, nn=False, nn_output="energy"):
        """
        Applies the normalization.

        Parameters
        ----------
        names
            Dataset names to apply the normalization to.
        nn : bool
            If True, applies the normalization to neural networks.
        nn_output : str
            Neural network output to deduce the normalization component.
            Used only if ``nn=True``.
        """
        if len(names) == 0:
            names = sorted(self.datasets.keys())
        self.log.info(f"Normalizing {len(names):d} datasets ...")
        energy_collection = []
        for k in names:
            self.log.info(f"  {k} ...")
            self.normalization.fw(self.datasets[k], inplace=True)
            energy_collection.append(self.datasets[k].per_cell_dataset.energy)
        mn_e = min(torch.min(i).item() for i in energy_collection)
        mx_e = max(torch.max(i).item() for i in energy_collection)
        self.log.info(f"Energy distribution |{mn_e:.6f} - {mx_e:.6f}| = {mx_e - mn_e:.6f}:")
        for k, e in zip(names, energy_collection):
            h = torch.histc(e, 100, mn_e, mx_e).numpy()
            self.log.info(f"  {k: <10} ░{text_bars(h)}░ max: {h.max():.0f}")
        if nn:
            if self.nn is None:
                raise ValueError("Neural networks are None")
            self.log.info(f'Normalizing neural networks with output "{nn_output}" ...')
            _nn = list(
                self.normalization.apply_to_module(n, i, fw=True, output=nn_output)
                for i, n in enumerate(self.nn)
            )
            self.nn = _nn

    @requires_fields("datasets")
    def split_dataset(self, fraction=0.1, source="learn", destination="test"):
        """
        Splits a dataset into two.
        Useful for preparing test sets.

        Parameters
        ----------
        source : str
            The dataset to split.
        destination : str
            The destination to write the split part to.
        fraction : float, int
            The fraction of the data that ends up in ``destination`` in case of float,
            or the corresponding number of entries in case of integer.

        Returns
        -------
        new_source : Dataset
            The source dataset.
        destination : Dataset
            The destination dataset.
        """
        d = self.datasets[source]
        n = d.per_cell_dataset.n_samples
        if isinstance(fraction, float):
            n_learn = int(round(n * (1 - fraction)))
        elif isinstance(fraction, int):
            n_learn = n - fraction
        else:
            raise ValueError(f"Unknown fraction: {fraction}")
        if n_learn == 0:
            raise ValueError(f"Empty source dataset n={n} n_learn={n_learn}")
        if n_learn == n:
            raise ValueError("Empty destination dataset (the source dataset ot the fraction value are too small)")
        n_test = n - n_learn
        self.log.info(f"Splitting the dataset '{source}'[{n:d}] -> '{source}'[{n_learn:d}] + '{destination}'[{n_test:d}]")
        dl = Dataset.from_tensors(d[:n_learn], like=d)
        dt = Dataset.from_tensors(d[n_learn:], like=d)
        self.datasets[source] = dl
        self.datasets[destination] = dt
        return dl, dt

    def _log_distributions(self, data, bins, margin, log_descriptors):
        distributions = []
        for ppd in data.per_point_datasets:
            self.log.info(f"  {ppd.tag}")
            d_specimen = ppd.get_features_hist(bins=bins, margin=margin).numpy()
            distributions.append(d_specimen)
            for i, (h_bins, h_data) in enumerate(d_specimen):
                mn, mx = h_bins[0], h_bins[-1]
                if log_descriptors:
                    self.log.info(f"    {i: 3d}: {self.descriptors[ppd.tag][i]}")
                else:
                    self.log.info(f"    {i: 3d}:")
                self.log.info(f"         |{mn:.6f} - {mx:.6f}| = {mx - mn:.6f}")
                self.log.info(f"         ░{text_bars(h_data[:-1], mn=0)}░ max: {h_data.max():.0f}")
        return distributions

    @requires_fields("datasets", "descriptors")
    def compute_descriptor_stats(self, dataset="learn", bins=100, margin=0):
        """
        Computes descriptor statistics.

        Parameters
        ----------
        dataset : str
            The dataset to process.
        bins : int
            Histogram bins count.
        margin : float
            Margins for bin edges.

        Returns
        -------
        distributions : list
            A list of descriptor distributions.
        """
        self.log.info(f"Computing descriptor distributions for `{dataset}`...")
        data = self.datasets[dataset]
        distributions = self._log_distributions(data, bins, margin, True)
        self.datasets_stat[dataset] = distributions
        return distributions

    @requires_fields("datasets", "descriptors", "datasets_stat")
    def filter_descriptors(self, dataset="learn", min_spread=1e-2):
        """
        Filters out non-representative descriptors.

        Parameters
        ----------
        dataset : str
            The dataset to analyze.
        min_spread : float
            The required minimal spread of descriptor values.

        Returns
        -------
        descriptors : dict
            Filtered descriptors.
        """
        stats = self.datasets_stat[dataset]
        self.log.info("Filtering by width ...")
        filters = []
        for i in stats:
            filters.append((i[:, 0, -1] - i[:, 0, 0]) >= min_spread)

        d_keys = sorted(self.descriptors)
        for specimen_ix, (fltr, specimen) in enumerate(zip(filters, d_keys)):

            total = len(fltr)
            remaining = fltr.sum()
            filtered = total - remaining
            self.log.info(f"Specimen #{specimen_ix:d} total: {total}, filtered: {filtered} remaining: {remaining}")
            self.log.info("  applying to descriptors ...")
            self.descriptors[specimen] = tuple(i for i, j in zip(self.descriptors[specimen], fltr) if j)

    def init_nn(self, init=behler_nn, **kwargs):
        """
        Initializes neural networks into a random state.

        Parameters
        ----------
        init : Callable
            A function that initializes a neural network.
        kwargs
            Arguments to `SequentialSoleEnergyNN`.

        Returns
        -------
        result : list
            A list of initialized networks (torch Modules).
        """
        self.log.info("Initializing neural networks ...")
        sample = self.datasets["learn"]
        nn = []
        for i in sample.per_point_datasets:
            nf = i.n_features
            self.log.info(f"  {i.tag}: n_features = {nf}")
            nn.append(init(n_inputs=nf, **kwargs).to(dtype=self.dtype))
        self.nn = nn
        return nn

    @requires_fields("nn")
    def cuda(self):
        """Moves data to CUDA."""
        self.log.info("Moving NNs to CUDA ...")
        for i in self.nn:
            i.cuda()
        self.log.info("Moving datasets to CUDA ...")
        for dataset in self.datasets.values():
            for piece in dataset.datasets:
                piece.tensors = list(i if i is None else i.cuda() for i in piece.tensors)

    @requires_fields("nn")
    def init_closure(self, closure=None, primary="learn", **kwargs):
        """
        Initializes the closure.

        Parameters
        ----------
        closure : Callable
            The closure initialization function.
        primary : str
            The name of the primary learning dataset.
        kwargs
            Arguments to `simple_energy_closure`.

        Returns
        -------
        result : SimpleClosure
            The closure.
        """
        if closure is None:
            closure = simple_energy_closure
        d = self.datasets[primary]
        self.log.info("Init closure ...")
        self.closure = closure(self.nn, d, **kwargs)
        self.log.info(f"  closure: {self.closure}")
        self.log.info(f"  optimizer: {self.closure.optimizer}")
        self.log.info(f"  loss function: {self.closure.loss_function}")
        self.log.info(f"  loss arguments: {self.closure.loss_function_kwargs}")
        if "w_gradients" in kwargs and kwargs["w_gradients"] > 0:
            self.log.info("Enabling gradients in the dataset")
            for k, v in sorted(self.datasets.items()):
                self.log.info(f"  {k}")
                for i in v.per_point_datasets:
                    i.features.requires_grad = True
        return self.closure

    @requires_fields("closure")
    def update_loss(self):
        """
        Propagates and computes loss function(s).
        
        Parameters
        ----------

        Returns
        -------
        loss : dict
            A dictionary with loss functions.
        """
        self.log.info("Updating loss functions ...")
        result = {}
        for k, v in self.datasets.items():
            result[k] = self.closure.loss(dataset=v, save=False)
            self.log.info(f"  {k}={pull(result[k].loss_value).item():.3e}")
        self.losses = result
        return result

    def __on_plot_update__(self):
        if self.on_plot_update == "save":
            self.save_plots()
        elif self.on_plot_update == "show":
            for i in self.figures.values():
                i.show()
        elif self.on_plot_update == "notebook":
            if self.nb_display_handles is None:
                from IPython import display
                self.nb_display_handles = handles = dict()
                for k, fig in self.figures.items():
                    handles[k] = display.display(fig, display_id=True)
            else:
                for k, handle in self.nb_display_handles.items():
                    handle.update(self.figures[k])
        elif self.on_plot_update is not None:
            self.on_plot_update(self)

    @requires_fields("figures")
    def save_plots(self):
        for k, fig in self.figures.items():
            fig.savefig(f"{k}.{self.mpl_save_ext}" if self.tag is None else f"{self.tag}-{k}.{self.mpl_save_ext}")

    @requires_fields("normalization")
    def __init_plot_scales__(self):
        e_scale = self.normalization.energy_scale.item()
        self.__diag_scale__ = [diag_plot_props(
            scale=e_scale / self.units.get_uv("energy", 1),
            unit=self.units.get("energy", None),
            title="Energy per atom",
        )]
        if self.normalization.length_scale is not None:
            f_scale = e_scale / self.normalization.length_scale.item()
            self.__diag_scale__.append(diag_plot_props(
                scale=f_scale / self.units.get_uv("force", 1),
                unit=self.units.get("force", None),
                title="Force component",
            ))

    @requires_fields("normalization")
    def init_plots(self, on_plot_update=None, inset=0.1, inset_size=0.4, inset_offset=0.03, **kwargs):
        """
        Initializes runtime plots.

        Parameters
        ----------
        on_plot_update : str, Callable, None
            Action to perform whenever plots are updated:
            - 'save': save into pdf files;
            - 'show': run ``pyplot.show``;
            - 'notebook': create plots in the notebook nd update them;
            - Callable: any custom callable taking this workflow as an input.
        inset : float, list, tuple
            If non-zero, inset the most dense part of the diagonal plot. The
            number corresponds to the fraction of the original plot shown in
            the inset. If list specified, insets the specific range of the
            diagonal plot.
        inset_size : float
            The actual size of the inset plot.
        inset_offset : float
            Offset of the inset plot.
        kwargs
            Arguments to ``self.update_plots``.
        """
        self.__init_plot_scales__()
        if isinstance(inset, float):
            inset = [inset] * len(self.__diag_scale__)
        if isinstance(inset, tuple):
            inset = [inset]
        self.on_plot_update = on_plot_update
        self.figures = f = {}
        self.axes = a = {}
        self.__diagonal_inset_plot_ranges__ = inset
        n = len(self.__diag_scale__) + 1
        f["convergence"], (*a["diagonal"], a["convergence"]) = pyplot.subplots(
            1, n, figsize=(6 * n, 6), dpi=150)
        a["diagonal-inset"] = adi = []
        for host, _ in zip(a["diagonal"], inset):
            inset_ax = host.inset_axes([1 - inset_offset - inset_size, inset_offset, inset_size, inset_size])
            inset_ax.set_xticklabels('')
            inset_ax.set_yticklabels('')
            adi.append(inset_ax)

        self.update_plots(update=False, **kwargs)

    @requires_fields("losses")
    def update_plots(self, update=True, diag_kwargs=None, conv_kwargs=None):
        """Updates plots."""
        if diag_kwargs is None:
            diag_kwargs = dict()
        if conv_kwargs is None:
            conv_kwargs = dict()
        losses = sorted(self.losses.items())
        labels, losses = zip(*losses)
        plot_convergence(
            list(pull(loss.loss_value).item() for loss in losses),
            append=update,
            ax=self.axes["convergence"],
            labels=labels[:len(losses)],
            **conv_kwargs
        )
        for i in self.__history_plot_annotation_objects__:
            i.remove()
        self.__history_plot_annotation_objects__ = []
        for k, v in sorted(self.__history_plot_annotations__.items()):
            self.__history_plot_annotation_objects__.append(
                self.axes["convergence"].annotate(
                    k, xy=v, ha='center', va='top', xytext=(0, -10),
                    textcoords="offset points",
                    bbox=dict(boxstyle="square", fc="white", ec="black"))
            )
        plot_buckets = []
        for i_loss, (loss_label, loss) in enumerate(zip(labels, losses)):
            loss_components = [loss] if loss.components is None else loss.components
            for i_component, (ls, (sc_v, sc_u, sc_t)) in enumerate(zip(loss_components, self.__diag_scale__)):
                if len(plot_buckets) < i_component + 1:
                    plot_buckets.append([])
                if sc_t == "Energy per atom":
                    _n_atoms = self.datasets[loss_label].per_cell_dataset.mask.sum(dim=1, keepdim=True)
                    plot_buckets[i_component].extend((
                        pull(ls.reference / _n_atoms).squeeze() * sc_v,
                        pull(ls.prediction / _n_atoms).squeeze() * sc_v,
                    ))
                else:
                    plot_buckets[i_component].extend((
                        pull(ls.reference).squeeze() * sc_v,
                        pull(ls.prediction).squeeze() * sc_v,
                    ))
        dins_ax = self.axes["diagonal-inset"]
        for i in self.__inset_indicator_patches__:
            i.remove()
        self.__inset_indicator_patches__.clear()
        for i_ax, (ax, bucket, (sc_v, sc_u, sc_t)) in enumerate(zip(self.axes["diagonal"], plot_buckets, self.__diag_scale__)):
            plot_diagonal(
                *bucket,
                ax=ax,
                replace=update,
                unit_label=sc_u,
                **diag_kwargs
            )
            if not update:
                ax.set_title(sc_t)
            if i_ax < len(dins_ax):
                ax_inset = dins_ax[i_ax]
                inset_range = self.__diagonal_inset_plot_ranges__[i_ax]
                if isinstance(inset_range, float):
                    npts = 10
                    n_bins = int(npts / inset_range)
                    hist, bin_edges = np.histogram(bucket[0], n_bins)
                    hist = np.convolve(hist, np.ones(npts), mode='valid')
                    mloc = np.argmax(hist)
                    self.__diagonal_inset_plot_ranges__[i_ax] = inset_range = bin_edges[mloc], bin_edges[mloc + npts]
                plot_diagonal(
                    *bucket,
                    ax=ax_inset,
                    replace=update,
                    unit_label=sc_u,
                    xlabel=None,
                    ylabel=None,
                    window=inset_range,
                    **diag_kwargs
                )
                rect, lines = ax.indicate_inset_zoom(ax_inset)
                self.__inset_indicator_patches__.append(rect)
                if lines is not None:
                    self.__inset_indicator_patches__.extend(lines)
            ax.legend()
        self.__on_plot_update__()

    @requires_fields("losses")
    def plot_distributions(self, which=None, **kwargs):
        """
        Plot distribution of energies, forces and other quantities available.

        Parameters
        ----------
        which
            Specify which datasets to include in order.
        kwargs
            Arguments to ``pyplot.hist``.

        Returns
        -------
        figure
            The resulting figure.
        """
        if which is None:
            which = sorted(self.losses.keys())
        n = len(self.__diag_scale__)
        figure, axes = pyplot.subplots(1, n, figsize=(6 * n, 6), dpi=150, squeeze=False)
        axes = axes.squeeze(0)
        for i, dataset_label in enumerate(which):
            loss = self.losses[dataset_label]
            loss_components = [loss] if loss.components is None else loss.components
            for ax, loss_component, (sc_v, sc_u, sc_t) in zip(axes, loss_components, self.__diag_scale__):
                ax.hist(pull(loss_component.reference).ravel() * sc_v, label=dataset_label, zorder=i, **kwargs)
                ax.set_xlabel(f"{sc_t} ({sc_u})")
        for ax in axes:
            ax.legend()
        return figure

    @requires_fields("closure")
    def epoch(self, cleanup=True, epoch_size=1):
        """
        Runs an optimizer epoch.

        Parameters
        ----------
        cleanup : bool
            if True, cleans up the optimizer memory before running the epoch.
        epoch_size : int
            Number of optimizer steps taken at once.

        Returns
        -------
        loss
            The resulting loss data.
        """
        self.log.info(f"Running epoch with cleanup={cleanup} and epoch_size={epoch_size:d}...")
        if cleanup:
            self.closure.optimizer_init()
        for i in range(epoch_size):
            self.closure.optimizer_step()
        loss = self.closure.last_loss
        self.log.info(f"  loss={pull(loss.loss_value).item():.3e}")
        return loss

    @requires_fields("nn", "descriptors", "normalization")
    def build_potentials(self, nn_output="energy", stats="learn"):
        """
        Initializes NN potentials.

        Returns
        -------
        potentials : list
            A list of potentials.
        nn_output : str
            Neural network output to deduce the normalization component.
        stats : str
            The source of descriptor distributions.
        """
        self.nn_potentials = potentials_from_ml_data(
            [cpu_copy(i) for i in self.nn], self.descriptors, normalization=self.normalization, output=nn_output,
            descriptor_fidelity_histograms=self.datasets_stat[stats] if stats is not None else None)
        return self.nn_potentials

    @requires_fields("nn_potentials")
    def save_potentials(self, filename):
        """
        Saves potentials as a file.

        Parameters
        ----------
        filename : str
            Save location.
        """
        self.log.info(f"Saving potentials to {filename}")
        save_potentials(self.nn_potentials, filename)

    def load_potentials(self, potentials):
        """
        Load previously saved result.

        Parameters
        ----------
        potentials : str, list
            File name to load from or a list of potentials.

        Returns
        -------
        nn_potentials : list
            Loaded potentials.
        """
        self.log.info(f"Restoring potentials from {potentials} ...")
        if isinstance(potentials, (str, Path)):
            self.nn_potentials = load_potentials(potentials)
        else:
            self.nn_potentials = potentials
        self.nn = list(i.parameters["nn"] for i in self.nn_potentials)
        self.descriptors = {p.tag: p.descriptors for p in self.nn_potentials}
        return self.nn_potentials

    def check_conflicts(self, learn_cauldron_kwargs, closure_kwargs):
        """
        Checks inputs for possible conflicts.

        Parameters
        ----------
        learn_cauldron_kwargs : dict
            Arguments to ``learn_cauldron``.
        closure_kwargs : dict
            Arguments to closures.
        """
        if not learn_cauldron_kwargs.get("grad", False) and closure_kwargs.get("w_gradients", 0) != 0:
            self.log.error("Workflow conflict: inconsistent gradient settings")
            raise ValueError("Gradient fitting was requested but no gradient information will be prepared by "
                             "`learn_cauldron`. Please set learn_cauldron_kwargs['grad'] = True")

    def prepare(self, fn_cells,
                cells_order="random",
                cells_subset=None,
                cells_append=False,
                descriptors=None,
                filter_descriptors=False,
                filter_descriptors_kwargs=None,
                cutoff=None,
                nw_kwargs=None,
                fn_cells_root=None,
                parallel=False,
                parallel_descriptor_chunksize=None,
                learn_cauldron_kwargs=None,
                normalization_kwargs=None,
                test_set=0.1,
                nn_kwargs=None,
                cuda="auto",
                closure_kwargs=None,
                plot_kwargs=None,
                default_descriptor_kwargs=None,
                load=None,
                ):
        """
        Prepares the data for the workflow.
        """
        if cutoff is None:
            cutoff = 12 * nu.aBohr
        if nw_kwargs is None:
            nw_kwargs = {}
        if default_descriptor_kwargs is None:
            default_descriptor_kwargs = dict()
        if learn_cauldron_kwargs is None:
            learn_cauldron_kwargs = dict()
        if normalization_kwargs is None:
            normalization_kwargs = dict()
        if nn_kwargs is None:
            nn_kwargs = dict()
        if closure_kwargs is None:
            closure_kwargs = dict()
        if plot_kwargs is None:
            plot_kwargs = dict()
        if filter_descriptors_kwargs is None:
            filter_descriptors_kwargs = dict()
        if cuda == "auto":
            cuda = torch.cuda.is_available()

        self.check_conflicts(learn_cauldron_kwargs, closure_kwargs)

        self.load_cells(fn_cells, root=fn_cells_root, append=cells_append)
        if cells_order is not None:
            self.reorder_cells(cells_order)
        if cells_subset is not None:
            self.subset_cells(cells_subset)
        if test_set is not None and not isinstance(test_set, float):
            result = self.load_cells(test_set, root=fn_cells_root, append=True)
            test_set = len(result)
        if load is not None:
            self.load_potentials(load)
            self.compute_cutoff()
            self.compute_neighbors(parallel=parallel, **nw_kwargs)
        else:
            if descriptors is not None:
                self.load_descriptors(descriptors)
                self.compute_cutoff()
                self.compute_neighbors(parallel=parallel, **nw_kwargs)
            else:
                self.cutoff = cutoff
                self.compute_neighbors(parallel=parallel, **nw_kwargs)
                if "a" not in default_descriptor_kwargs:
                    default_descriptor_kwargs["a"] = self.cutoff
                self.init_default_descriptors(**default_descriptor_kwargs)
        if filter_descriptors:
            self.compute_descriptors(parallel=False, source=self.cells_nw[:100], destination="__temp__")
            self.compute_descriptor_stats(dataset="__temp__")
            self.filter_descriptors(dataset="__temp__", **filter_descriptors_kwargs)
            del self.datasets["__temp__"]
            del self.datasets_stat["__temp__"]
        self.compute_descriptors(parallel=parallel, chunksize=parallel_descriptor_chunksize, **learn_cauldron_kwargs)
        self.compute_normalization(**normalization_kwargs)
        if test_set is not None:
            self.split_dataset(fraction=test_set)
        self.compute_descriptor_stats()
        self.apply_normalization(nn=load)
        if normalization_kwargs.get("pca_features", None) is not None:
            self.log.info("Descriptor distributions after PCA:")
            self._log_distributions(self.datasets["learn"], 100, 0, False)
        if load is None:
            self.init_nn(**nn_kwargs)
        if cuda:
            self.cuda()
        self.init_closure(**closure_kwargs)
        self.update_loss()
        self.init_plots(**plot_kwargs)

    def run(self, n_epochs=1000, epoch_size=1, cleanup_optimizer=True, save=False, save_policy=None, save_fn="{tag}.pt",
            after_epoch=None, plot_kwargs=None):
        """
        Runs the training scenario.

        Parameters
        ----------
        n_epochs : int
            Number of epochs to run.
        epoch_size : int
            Size of the epoch.
        cleanup_optimizer : bool
            if True, cleans up the optimizer memory before running each epoch.
        save : str, bool, None
            If set, saves intermediate potentials data to the desired location.
        save_policy : Callable
            A ``function(tag, loss, state) -> do_save, state`` which is called
            to determine whether saving is needed.
        save_fn : str
            A formatting string to generate potential filenames based on the
            dataset name.
        after_epoch : Callable
            A callback ``function(self) -> bool`` to run after each epoch.
            If the returned value becomes False exits the epoch loop.
        plot_kwargs : dict
            Keyword arguments to plot functions.
        """
        if plot_kwargs is None:
            plot_kwargs = dict()
        if save_policy is None:
            save_policy = minimum_loss_save_policy
        assert save in {False, True}
        save_policy_states = {}
        for epoch in range(n_epochs):
            self.log.info(f"Epoch {epoch:d}")
            self.epoch(cleanup=cleanup_optimizer, epoch_size=epoch_size)
            self.update_loss()
            if save:
                self.build_potentials()
                for k, v in sorted(self.losses.items()):
                    do_save, new_state = save_policy(k, v, save_policy_states.get(k, None))
                    save_policy_states[k] = new_state
                    if do_save:
                        fname = save_fn.format(tag=k)
                        self.save_potentials(fname)
                        self.__history_plot_annotations__[fname] = epoch + 1, v.loss_value.detach().item()
            self.update_plots(**plot_kwargs)
            if after_epoch is not None:
                if after_epoch(self) is False:
                    self.log.info("Exit reason: `after_epoch`")
                    break
        else:
            self.log.info("Exit reason: final iteration")


class ChargeFitWorkflow(FitWorkflow):
    def __init__(self, **kwargs):
        if "tag" not in kwargs:
            kwargs["tag"] = "charge"
        super().__init__(**kwargs)

    def compute_descriptors(self, **kwargs):
        return super().compute_descriptors(extract_charges=True, **kwargs)

    def init_closure(self, **kwargs):
        return super().init_closure(closure=simple_charges_closure, **kwargs)

    def compute_normalization(self, source="learn", **kwargs):
        result = super().compute_normalization(source=source, **kwargs)
        self.log.info("Charges:")
        for k, s, o in zip(
                sorted(self.descriptors),
                self.normalization.charges_scale,
                self.normalization.charges_offsets,
        ):
            self.log.info(f"  {k} scale = {s.item():.3e} offset = {o.item():.3e}")
        return result

    def apply_normalization(self, *names, nn=False, nn_output="charge"):
        return super().apply_normalization(*names, nn=nn, nn_output=nn_output)

    def build_potentials(self, nn_output="charge"):
        return super().build_potentials(nn_output=nn_output)

    @requires_fields("normalization")
    def __init_plot_scales__(self):
        sample = next(iter(self.datasets.values()))
        self.__diag_scale__ = [
            diag_plot_props(scale=i.item(), unit="e", title=f"{d.tag} charge")
            for i, d in zip(self.normalization.charges_scale, sample.per_point_datasets)
        ]


class SDWorkflow(Workflow):
    def __init__(self, **kwargs):
        if "tag" not in kwargs:
            kwargs["tag"] = "relax"
        super().__init__(**kwargs)

        self.potentials = None  # potentials
        self.cells_result = None  # resulting cells

    def load_potentials(self, *potentials):
        """
        Load previously saved potential.

        Parameters
        ----------
        potentials
            File names to load from or an explicit list of potentials.

        Returns
        -------
        potentials : list
            The loaded potentials.
        """
        if len(potentials) == 0:
            potentials = ["learn.pt"]
        result = []
        for src in potentials:
            self.log.info(f"Restoring potentials from {src} ...")
            if isinstance(src, str):
                result.extend(list(map(potential_from_state_dict, torch.load(src))))
            elif isinstance(src, (list, tuple)):
                result.extend(src)
            else:
                result.append(src)
        self.potentials = result
        return result

    @requires_fields("potentials")
    def update_cutoff(self):
        """
        Updates the cutoff value.

        Returns
        -------
        cutoff : float
            The cutoff value.
        """
        self.cutoff = max(i.cutoff for i in self.potentials)
        return self.cutoff

    @staticmethod
    def worker(cell, potentials, **kwargs):
        cell, job_id = cell
        default_kwargs = dict(options=dict(maxiter=10000), method="L-BFGS-B", inplace=True)
        default_kwargs.update(kwargs)
        kwargs = default_kwargs

        warnings_fw = []
        with warnings.catch_warnings(record=True) as warnings_list:
            relaxed = cell.relax(potentials, **kwargs)
            if kwargs.get("rtn_history", False):
                _last = relaxed[-1]
            else:
                _last = relaxed
            _last.meta['flag-potential-warning'] = False
            for w in warnings_list:
                if issubclass(w.category, PotentialRuntimeWarning):
                    _last.meta['flag-potential-warning'] = True
                else:
                    warnings_fw.append(w)
        for w in warnings_fw:
            warnings.warn_explicit(
                message=w.message,
                category=w.category,
                filename=w.filename,
                lineno=w.lineno,
            )
        return relaxed, job_id

    @requires_fields("cells_nw", "potentials")
    def run(self, parallel=False, pool_kwargs=None, **kwargs):
        """
        Computes descriptors.

        Parameters
        ----------
        parallel : bool, str
            If True, computes in multiple processes.
        pool_kwargs : dict
            Arguments to Pool constructor in parallel mode.
        kwargs
            Arguments to ``self.worker``.

        Returns
        -------
        result : list
            The resulting structures.
        """
        self.log.info("Using potentials:")
        for p in self.potentials:
            self.log.info(f"  {p}")

        cells_with_id = zip(self.cells_nw, range(len(self.cells_nw)))

        if parallel == "openmp":
            kwargs["prefer_parallel"] = True
            parallel = False
        elif parallel:
            if "prefer_parallel" in kwargs:
                v = kwargs["prefer_parallel"]
                if v is not False:
                    self.log.warning(f"The argument 'prefer_parallel' is explicitly set to {v}. It is advised to set "
                                     f"this argument to False to avoid interference and deadlocks between "
                                     f"multiprocessing, OpenMP and torch")
            else:
                kwargs["prefer_parallel"] = False

        worker = partial(self.worker, potentials=self.potentials, **kwargs)
        if parallel:
            # Disable OpenMP because it causes deadlocks
            num_omp_threads = torch.get_num_threads()
            torch.set_num_threads(1)

            if pool_kwargs is None:
                pool_kwargs = dict()
            pool = torch.multiprocessing.Pool(**pool_kwargs)
            iterator = pool.imap_unordered(worker, cells_with_id)
        else:
            iterator = map(worker, cells_with_id)

        self.log.info(f"Started run (parallel={parallel})")
        self.cells_result = [None] * len(self.cells_nw)
        n_complete = 0
        n_total = len(self.cells_nw)
        for result, job_id in iterator:
            n_complete += 1
            self.cells_result[job_id] = result
            self.log.info(f"#{job_id} complete; remaining {n_total - n_complete:d} / {n_total} = "
                          f"{100 * (1 - n_complete / n_total):.0f}%")
        if parallel:
            pool.close()
        self.log.info("Processing done")

        if parallel:
            torch.set_num_threads(num_omp_threads)

        return self.cells_result

    def prepare(self, fn_cells, potentials="learn.pt",
                fn_cells_root=None,
                cells_order=None,
                cells_subset=None,
                nw_kwargs=None,
                ):
        if nw_kwargs is None:
            nw_kwargs = dict()
        self.load_cells(fn_cells, root=fn_cells_root)
        if cells_order is not None:
            self.reorder_cells(cells_order)
        if cells_subset is not None:
            self.subset_cells(cells_subset)
        self.load_potentials(potentials)
        self.update_cutoff()
        self.compute_neighbors(**nw_kwargs)


class OneShotWorkflow(SDWorkflow):
    @staticmethod
    def worker(cell, potentials, **kwargs):
        default_kwargs = dict(ignore_missing_species=True)
        default_kwargs.update(kwargs)
        cell, job_id = cell
        result = cell.cell.copy()
        result.meta["total-energy"] = cell.total(potentials, **default_kwargs)
        return result, job_id


def run_workflow(workflow_class, init=None, prepare=None, run=None):
    """
    Runs the workflow and returns it.

    Parameters
    ----------
    workflow_class : class
        The workflow class.
    init
        Keyword arguments to workflow initialization.
    prepare
        Keyword arguments to workflow data preparation and processing.
    run
        Keyword arguments to workflow run phase.

    Returns
    -------
    result : Workflow
        The resulting workflow.
    """
    if init is None:
        init = {}
    if prepare is None:
        prepare = {}
    if run is None:
        run = {}
    workflow = workflow_class(**init)
    workflow.prepare(**prepare)
    workflow.run(**run)
    return workflow


fit = partial(run_workflow, workflow_class=FitWorkflow)
fit.__doc__ = """
    Runs the fit workflow and returns it.

    Parameters
    ----------
    init
        Keyword arguments to workflow initialization.
    prepare
        Keyword arguments to workflow data preparation and processing.
    run
        Keyword arguments to workflow run phase.

    Returns
    -------
    result : FitWorkflow
        The resulting workflow.
"""
test_direct = partial(run_workflow, workflow_class=OneShotWorkflow)
test_direct.__doc__ = """
    Runs the direct energy test workflow and returns it.

    Parameters
    ----------
    init
        Keyword arguments to workflow initialization.
    prepare
        Keyword arguments to workflow data preparation and processing.
    run
        Keyword arguments to workflow run phase.

    Returns
    -------
    result : OneShotWorkflow
        The resulting workflow.
"""
test_relax = partial(run_workflow, workflow_class=SDWorkflow)
test_relax.__doc__ = """
    Runs the batch-relax workflow and returns it.

    Parameters
    ----------
    init
        Keyword arguments to workflow initialization.
    prepare
        Keyword arguments to workflow data preparation and processing.
    run
        Keyword arguments to workflow run phase.

    Returns
    -------
    result : SDWorkflow
        The resulting workflow.
"""


def exec_workflows(description, rtn=True, log=None):
    """
    Constructs and executes workflows with the description provided.

    Parameters
    ----------
    description : OrderedDict
        Workflow description.
    rtn : bool
        If True, returns all workflows executed.
        Otherwise, returns only the last workflow.
    log : Logger
        The common logger.

    Returns
    -------
    result : list, Workflow
        The resulting workflow(s).
    """
    lookup = {"fit": fit, "test-direct": test_direct, "test-relax": test_relax}
    empty = {}
    result = []

    for job_workflow_name, job_arguments in description.items():
        workflow = lookup[job_workflow_name](
            init={"log": log, **job_arguments.pop("init", empty)},
            prepare=job_arguments.pop("prepare", empty),
            run=job_arguments.pop("run", empty),
        )
        if len(job_arguments):
            log.warning(f"Ignoring additional arguments to the stage: {job_arguments}")
        if rtn:
            result.append(workflow)
        else:
            result = workflow
    return result
