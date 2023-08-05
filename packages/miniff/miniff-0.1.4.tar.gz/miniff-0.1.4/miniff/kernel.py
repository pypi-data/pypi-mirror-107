from .potentials import eval_potentials, NestedLocalPotential
from .ml import __assert_dimension_count__, __assert_same_dimension__  # TODO: implement kernel.py independent of this import
from .util import dict_reduce, lattice_up_to_radius, cartesian
from .units import load, dump
from ._util import adf as _adf

import numpy as np
from scipy.sparse import coo_matrix
from scipy.optimize import minimize
from scipy.spatial import cKDTree

from functools import partial
from itertools import product
from warnings import warn


class OptimizationWarning(UserWarning):
    pass


def encode_species(species, lookup, default=None):
    """
    Transforms species into an array of integers encoding species.

    Parameters
    ----------
    species : list, tuple, np.ndarray
        Species to encode.
    lookup : dict
        A lookup dictionary.
    default : int
        The default value to replace non-existing entries. If None,
        raises KeyError.

    Returns
    -------
    result : np.ndarray
        The resulting integer array.
    """
    result = []
    for i in species:
        try:
            result.append(lookup[i])
        except KeyError:
            if default is not None:
                result.append(default)
            else:
                raise KeyError(f"Could not encode specimen '{i}' with lookup {lookup}. "
                               "Set `default=-1`, for example, to assign unknown species")
    return np.array(result, dtype=np.int32)


def encode_potentials(potentials, lookup, default=None):
    """
    Encodes potentials to have species as integers.

    Parameters
    ----------
    potentials : list, tuple
        Potentials to encode.
    lookup : dict
        A lookup dictionary.
    default : int
        The default value to replace non-existing entries. If None,
        raises KeyError.

    Returns
    -------
    result : list
        The resulting list of potentials.
    """
    result = list(
        i.copy(tag=encode_species(i.tag.split("-"), lookup, default=default) if i.tag is not None else None)
        for i in potentials
    )
    for i in result:
        # TODO: avoid infinite recursion here
        if isinstance(i, NestedLocalPotential):
            i.descriptors = encode_potentials(i.descriptors, lookup, default=default)
    return result


class SpeciesEncoder:
    def __init__(self, species):
        """
        A mixin for encoding species into integers.

        Parameters
        ----------
        species : list, tuple, np.ndarray
            A collection of species.
        """
        species = np.array(species)
        self.species, self.spec_encoded_row = np.unique(species, return_inverse=True)
        self.spec_encoded_row = self.spec_encoded_row.astype(np.int32)
        self.species_lookup = dict(zip(self.species, np.arange(len(self.species))))

    def encode_species(self, species, default=None):
        """
        Transforms species into an array of integers encoding species.

        Parameters
        ----------
        species : list, tuple
            Species to encode.
        default : int
            The default value to replace non-existing entries. If None,
            raises KeyError.

        Returns
        -------
        result : np.ndarray
            The resulting integer array.
        """
        return encode_species(species, self.species_lookup, default=default)
    encode = encode_species

    def encode_potentials(self, potentials, default=None):
        """
        Encodes potentials to have species as integers.

        Parameters
        ----------
        potentials : list, tuple
            Potentials to encode.
        default : int
            The default value to replace non-existing entries. If None,
            raises KeyError.

        Returns
        -------
        result : np.ndarray
            The resulting integer array.
        """
        return encode_potentials(potentials, self.species_lookup, default=default)


class Cell:
    def __init__(self, vectors, coordinates, values, meta=None):
        """
        A minimal implementation of a box with points.

        Parameters
        ----------
        vectors : np.ndarray, list, tuple
            Box vectors.
        coordinates : np.ndarray, list, tuple
            Point coordinates in the box basis.
        values : np.ndarray, list, tuple
            Point specifiers.
        meta : dict
            Optional metadata.
        """
        vectors = np.asanyarray(vectors)
        coordinates = np.asanyarray(coordinates)
        values = np.asanyarray(values)

        inputs = locals()

        __assert_dimension_count__(inputs, "vectors", 2, "coordinates", 2, "values", 1)
        __assert_same_dimension__(inputs, "basis size", "coordinates", 1, "vectors", 0)
        self.vectors = vectors
        self.coordinates = coordinates
        self.values = values
        if meta is None:
            self.meta = {}
        else:
            self.meta = dict(meta)

    @property
    def size(self):
        return len(self.coordinates)

    def copy(self):
        """
        A copy of the box.

        Returns
        -------
        copy : Cell
            The copy.
        """
        return Cell(self.vectors.copy(), self.coordinates.copy(), self.values.copy(), self.meta)

    def cartesian(self):
        """
        Cartesian coordinates of points.

        Returns
        -------
        coords : np.ndarray
            The coordinates.
        """
        return self.coordinates @ self.vectors

    def transform_from_cartesian(self, coordinates):
        """
        Transforms coordinates from cartesian.

        Parameters
        ----------
        coordinates : np.ndarray
            Coordinates to transform.

        Returns
        -------
        result : ndarray
            The transformed coordinates.
        """
        return coordinates @ np.linalg.inv(self.vectors)

    def distances(self, cutoff=None, other=None):
        """
        Computes inter-point distances.

        Parameters
        ----------
        cutoff : float
            Cutoff for obtaining distances.
        other : Cell, np.ndarray
            Other cell to compute distances to

        Returns
        -------
        result : np.ndarray, csr_matrix
            The resulting distance matrix.
        """
        this = self.cartesian()
        if other is None:
            other = this
        elif isinstance(other, Cell):
            other = other.cartesian()

        if cutoff is None:
            return np.linalg.norm(this[:, np.newaxis] - other[np.newaxis, :], axis=-1)
        else:
            this = cKDTree(this)
            other = cKDTree(other)
            return this.sparse_distance_matrix(other, max_distance=cutoff, )

    @property
    def volume(self):
        return abs(np.linalg.det(self.vectors))

    def repeated(self, *args):
        """
        Prepares a supercell.

        Parameters
        ----------
        *args
            Repeat counts along each vector.

        Returns
        -------
        supercell : Cell
            The resulting supercell.
        """
        args = np.array(args, dtype=int)
        x = np.prod(args)
        vectors = self.vectors * args[np.newaxis, :]
        coordinates = np.tile(self.coordinates, (x, 1))
        coordinates /= args[np.newaxis, :]
        coordinates.shape = (x, *self.coordinates.shape)
        values = np.tile(self.values, x)
        shifts = list(np.linspace(0, 1, i, endpoint=False) for i in args)
        shifts = np.meshgrid(*shifts)
        shifts = np.stack(shifts, axis=-1)
        shifts = shifts.reshape(-1, shifts.shape[-1])
        coordinates += shifts[:, np.newaxis, :]
        coordinates = coordinates.reshape(-1, coordinates.shape[-1])
        return Cell(vectors, coordinates, values)

    @classmethod
    def from_state_dict(cls, data):
        data = dict(data)
        assert data.pop("type") in ("dfttools.utypes.CrystalCell", "dfttools.types.UnitCell")
        meta = data.pop("meta", None)
        v = data.pop("vectors")
        c = data.pop("coordinates")
        a = data.pop("values")
        b = data.pop("c_basis", None)
        if data:
            raise ValueError(f"Do not recognize additional data: {data}")
        result = Cell(vectors=v, coordinates=c, values=a, meta=meta)
        if b == "cartesian":
            result.coordinates = result.transform_from_cartesian(result.coordinates)
        elif b is None:
            pass
        else:
            raise ValueError(f"Unknown coordinate basis: {b}")
        return result

    def state_dict(self):
        result = dict(
            type="dfttools.utypes.CrystalCell",
            vectors=self.vectors,
            coordinates=self.coordinates,
            values=self.values,
            meta=self.meta,
        )
        return result

    @classmethod
    def load(cls, f):
        """
        Load Cell(s) from stream.

        Parameters
        ----------
        f : file
            File-like object.

        Returns
        -------
        result: list, Cell
            The resulting Cell(s).
        """
        json = load(f)
        squeeze = isinstance(json, dict)
        if squeeze:
            json = [json]
        result = [cls.from_state_dict(i) for i in json]
        if squeeze:
            return result[0]
        else:
            return result

    @staticmethod
    def save(cells, f):
        """
        Saves cells.

        Parameters
        ----------
        cells : list, Cell
            Cells to save.
        f : file
            File-like object.
        """
        if isinstance(cells, (list, tuple, np.ndarray)):
            dump([i.state_dict() for i in cells], f)
        else:
            dump(cells.state_dict(), f)


class NeighborWrapper(SpeciesEncoder):
    def __init__(self, cell, normalize=True, cutoff=None, x=None, pbc=True, reciprocal_cutoff=None):
        """
        Sparse inter-atomic distance data and local potential computations.

        Parameters
        ----------
        cell
            The unit cell with atom coordinates.
        x
            The number of cell replica included in distance calculation.
        normalize : bool
            Normalizes the cell if True.
        cutoff : float
            Cutoff for distances.
        x : tuple
            Image counts for periodic boundary conditions. Computes image counts
            from `cutoff` by default.
        pbc : bool
            Periodic boundary conditions.
        reciprocal_cutoff : float
            If set, computes the reciprocal grid.
        """
        self.shift_vectors = self.cell = self.cutoff = self.sparse_pair_distances = self.species =\
            self.spec_encoded_row = self.cartesian_row = self.cartesian_col = self.species_lookup =\
            self.reciprocal_cutoff = self.reciprocal_grid = None
        self._cart2cry_transform_matrix = None
        self.set_cell(cell, normalize=normalize)
        if cutoff is not None or x is not None:
            self.set_cutoff(cutoff=cutoff, x=x, pbc=pbc)
            if cutoff is not None:
                self.compute_distances(cutoff)
        if reciprocal_cutoff is not None:
            self.compute_reciprocal_grid(reciprocal_cutoff)

    @property
    def size(self) -> int:
        return self.cell.size

    @property
    def meta(self) -> dict:
        return self.cell.meta

    @property
    def vectors(self) -> np.ndarray:
        return self.cell.vectors

    @property
    def coordinates(self) -> np.ndarray:
        return self.cell.coordinates

    @property
    def values(self) -> np.ndarray:
        return self.cell.values

    def set_cutoff(self, cutoff=None, x=None, pbc=True):
        """
        Sets the real-space cutoff and computes the real-space grid.

        Parameters
        ----------
        cutoff : float
            Maximal distance computed (smaller=faster).
        x : list, tuple, np.ndarray
            Image counts for periodic boundary conditions. Computes image counts
            from `cutoff` by default.
        pbc : bool
            Periodic boundary conditions.
        """
        if pbc:
            if x is not None:
                self.shift_vectors = cartesian(tuple(
                    np.arange(-i, i + 1)
                    for i in x
                )) @ self.vectors
            elif cutoff is not None:
                self.shift_vectors = lattice_up_to_radius(cutoff, self.vectors, cover=True, zero=True)
            else:
                raise ValueError("Periodic boundary conditions specified but neither cutoff nor image counts provided")
        else:
            self.shift_vectors = np.zeros((1, 3))

    def set_cell(self, cell, normalize=True):
        """
        Set a new unit cell to work with.

        Parameters
        ----------
        cell
            The unit cell with atom coordinates.
        normalize : bool
            Normalizes the cell if True.
        """
        self.cell = cell.copy()
        if normalize:
            self.cell.coordinates %= 1
        self.cutoff = self.sparse_pair_distances = self.species = self.spec_encoded_row = self.cartesian_row =\
            self.cartesian_col = self.reciprocal_cutoff = self.reciprocal_grid = None
        self._cart2cry_transform_matrix = np.linalg.inv(self.cell.vectors)
        self.cartesian_row = cell.cartesian()

    def set_cell_cartesian(self, cartesian, normalize=True):
        """
        Sets new cartesian coordinates.

        Parameters
        ----------
        cartesian
            Atomic coordinates.
        normalize : bool
            Normalizes the cell if True.
        """
        self.cell.coordinates = np.array(cartesian @ self._cart2cry_transform_matrix)
        self.cartesian_row = cartesian
        if normalize:
            self.cell.coordinates %= 1
            self.cartesian_row = self.cell.coordinates @ self.cell.vectors

    def compute_distances(self, cutoff=None):
        """
        Compute sparse distances and masks using CKDTree by scipy.

        Parameters
        ----------
        cutoff : float
            Maximal distance computed (smaller=faster).
        """
        if cutoff is None:
            cutoff = self.cutoff
        if cutoff is None:
            raise ValueError("No cutoff specified")
        # Create a super-cell with neighbors
        self.cartesian_col = (self.cartesian_row[np.newaxis, :, :] + self.shift_vectors[:, np.newaxis, :]).reshape(-1, 3)

        # Collect close neighbors
        t_row = cKDTree(self.cartesian_row)
        t_col = cKDTree(self.cartesian_col)

        spd = t_row.sparse_distance_matrix(t_col, cutoff, output_type="coo_matrix")

        # Get rid of the-diagonal
        mask = spd.row + len(self.shift_vectors) // 2 * len(self.cartesian_row) != spd.col
        self.sparse_pair_distances = coo_matrix((spd.data[mask], (spd.row[mask], spd.col[mask])), shape=spd.shape).tocsr()

        # Encode species in integers
        SpeciesEncoder.__init__(self, self.cell.values)

        self.cutoff = cutoff

    def compute_reciprocal_grid(self, reciprocal_cutoff):
        """
        Computes the reciprocal grid.

        Parameters
        ----------
        reciprocal_cutoff : float
            The value of the reciprocal cutoff.
        """
        reciprocal_vectors = 2 * np.pi * np.linalg.inv(self.vectors.T)
        self.reciprocal_grid = lattice_up_to_radius(reciprocal_cutoff, reciprocal_vectors, zero=False)
        self.reciprocal_cutoff = reciprocal_cutoff

    def pair_reduction_function(self, f, fmt="{}-{}"):
        """
        Pair reduction function.

        Parameters
        ----------
        f : Callable
            A function reducing pair-specific distances,
            see `self.rdf` for an example.
        fmt : str
            A format string for keys.

        Returns
        -------
        result : dict
            Pair function values.
        """
        if self.species is None:
            raise ValueError("No distance information available: please run .compute_distances")
        result = {}
        distances = self.sparse_pair_distances.tocoo()
        pair_id = self.spec_encoded_row[distances.row] * len(self.species) + self.spec_encoded_row[
            distances.col % distances.shape[0]]
        for i_s1, s1 in enumerate(self.species):
            for i_s2, s2 in enumerate(self.species[i_s1:]):
                i_s2 += i_s1
                k = fmt.format(s1, s2)
                pid = i_s1 * len(self.species) + i_s2
                mask = pair_id == pid
                spd = distances.data[mask]
                val = f(spd, i_s1, i_s2)
                if val is not None:
                    result[k] = val
        return result

    def rdf(self, r, sigma, fmt="{}-{}"):
        """
        Computes the radial distribution function.

        Parameters
        ----------
        r : np.ndarray, float
            Radius values.
        sigma : float
            Smearing.
        fmt : str
            A format string for keys.

        Returns
        -------
        result : dict
            Radial distribution function values.
        """
        if not isinstance(r, np.ndarray):
            r = np.array([r], dtype=float)
            squeeze = True
        else:
            squeeze = False
        factor = 1 / sigma / (2 * np.pi) ** .5

        def f(spd, row, col):
            weights = np.exp(- (spd[:, np.newaxis] - r[np.newaxis, :]) ** 2 / 2 / sigma ** 2).sum(axis=0)
            return weights * factor / 4 / np.pi / r ** 2 / (self.spec_encoded_row == row).sum()

        result = self.pair_reduction_function(f, fmt=fmt)
        if squeeze:
            return {k: v[0] for k, v in result.items()}
        else:
            return result

    def adf(self, theta, sigma, cutoff, fmt="{}-[{},{}]"):
        """
        Computes the angular distribution function.

        Parameters
        ----------
        theta : np.ndarray, float
            Radius values.
        sigma : float
            Smearing.
        cutoff : float
            Radial cutoff value.
        fmt : str
            A format string for keys.

        Returns
        -------
        result : dict
            Radial distribution function values.
        """
        if not isinstance(theta, np.ndarray):
            r = np.array([theta], dtype=float)
            squeeze = True
        else:
            squeeze = False
        factor = 1 / sigma / (2 * np.pi) ** .5
        result = {}

        for i_s1, s1 in enumerate(self.species):
            for i_s2, s2 in enumerate(self.species):
                for i_s3, s3 in enumerate(self.species[i_s2:]):
                    i_s3 += i_s2
                    k = fmt.format(s1, s2, s3)

                    out = result[k] = np.zeros_like(theta)
                    _adf(
                        self.sparse_pair_distances.indptr,
                        self.sparse_pair_distances.indices,
                        self.sparse_pair_distances.data,
                        self.cartesian_row,
                        self.cartesian_col,
                        cutoff, theta, sigma,
                        self.spec_encoded_row,
                        np.array([i_s1, i_s2, i_s3], dtype=np.int32),
                        out,
                    )
                    out *= factor
        if squeeze:
            return {k: v[0] for k, v in result.items()}
        else:
            return result

    def eval(self, potentials, kname, squeeze=True, ignore_missing_species=False, out=None, **kwargs):
        """
        Calculates potentials: values, gradients and more.

        Parameters
        ----------
        potentials : list, LocalPotential
            A list of potentials or a single potential.
        kname : str, None
            Function to evaluate: 'kernel', 'kernel_gradient' or whatever
            other kernel function set for all potentials in the list.
        squeeze : bool
            If True, returns a single array whenever a single potential
            is passed.
        ignore_missing_species : bool
            If True, no error is raised whenever a specimen in the
            potential description is not found in the cell.
        out : np.ndarray
            The output buffer `[n_potentials, n_atoms]` for
            kname == "kernel" and `[n_potentials, n_atoms, n_atoms, 3]`
            for kname == "kernel_gradient". Any kind of reduction including
            `resolved=False` and calls `self.total`, `self.grad` calls will
            use the buffer for intermediate results but will still allocate
            a new array for the output.
        kwargs
            Other arguments to `eval_potentials`.

        Returns
        -------
        result : np.ndarray
            The result of the potential computation given the cell data.
        """
        sole = not isinstance(potentials, (list, tuple))
        if sole:
            potentials = potentials,

        potentials = list(potentials)
        encoded_potentials = self.encode_potentials(potentials, default=-1 if ignore_missing_species else None)

        additional_inputs = dict(volume=self.cell.volume)
        if "charges" in self.meta:
            additional_inputs["charges"] = np.array(self.meta["charges"], dtype=float)
        if self.reciprocal_grid is not None:
            additional_inputs["k_grid"] = self.reciprocal_grid
        out = eval_potentials(encoded_potentials, kname, self.sparse_pair_distances, self.cartesian_row,
                              self.cartesian_col, self.spec_encoded_row, pre_compute_r=False,
                              additional_inputs=additional_inputs, cutoff=self.cutoff, out=out, **kwargs)
        if sole and squeeze:
            return out[0]
        else:
            return out

    def total(self, potentials, kname="kernel", squeeze=False, resolving=False, **kwargs):
        """
        Total energy as a sum of all possible potential terms.

        Note that this function totally ignores any symmetry issues related to
        double-counting, etc.

        Parameters
        ----------
        potentials : list, LocalPotential
            A list of potentials or a single potential.
        kname : str, None
            Function to evaluate: 'kernel', 'kernel_gradient' or whatever
            other kernel function set for all potentials in the list.
        squeeze : bool
            If True, returns a single array whenever a single potential
            is passed.
        resolving : bool
            If True, runs species-resolving kernels.
        kwargs
            Other arguments to `eval`.

        Returns
        -------
        energy : float
            The total energy value.
        """
        return self.eval(potentials, kname, squeeze=squeeze, resolving=resolving, **kwargs).sum(axis=0)

    def grad(self, potentials, kname="kernel_gradient", **kwargs):
        """
        Total energy gradients.

        Similarly to `self.total`, this function totally ignores
        any symmetry issues related to double-counting, etc.

        Parameters
        ----------
        potentials : list, LocalPotential
            A list of potentials or a single potential.
        kname : str, None
            Function to evaluate: 'kernel', 'kernel_gradient' or whatever
            other kernel function set for all potentials in the list.
        kwargs
            Other arguments to `total`.

        Returns
        -------
        gradients : np.ndarray
            Total energy gradients.
        """
        return self.total(potentials, kname=kname, **kwargs)

    def relax(self, potentials, rtn_history=False, normalize=True, inplace=False, prefer_parallel=None,
              driver=minimize, **kwargs):
        """
        Finds the local minimum of the base cell.

        Parameters
        ----------
        potentials : list
            Potential to use.
        rtn_history : bool
            If True, returns intermediate atomic configurations.
        normalize : bool
            Normalizes the cell at each step if True.
        interstitial : Callable
            A function `interstitial(energy)` returning a modified
            energy and its derivative with respect to the old energy value.
        inplace : bool
            If True, modifies this wrapper to enclose the relaxed cell.
        prefer_parallel : bool
            A flag to prefer parallel potential computations.
        driver : Callable
            The minimizer.
        kwargs
            Keyword arguments to `scipy.optimize.minimize`.

        Returns
        -------
        cell : CrystalCell, list
            Either final unit cell or a history of all unit cells during the relaxation.
        """
        if not inplace:
            orig_cartesian = self.cell.cartesian()

        if rtn_history:
            _history = []

            def _cell_logger(cell, same):
                if same:
                    _history[-1] = cell
                else:
                    _history.append(cell)
        else:
            _cell_logger = None
        wrapper = ScalarFunctionWrapper(self, potentials, normalize=normalize, prefer_parallel=prefer_parallel,
                                        cell_logger=_cell_logger)

        result = driver(
            wrapper.f,
            x0=orig_cartesian.reshape(-1),
            jac=wrapper.g,
            **kwargs)

        if not result.success:
            warn(str(result.message), OptimizationWarning)

        # Set metadata for the final cell
        wrapper.maybe_update(result.x)
        wrapper.f(result.x)
        wrapper.g(result.x)
        result = wrapper.get_current_cell()

        # Restore
        if not inplace:
            self.set_cell_cartesian(orig_cartesian)
            self.compute_distances()

        if rtn_history:
            return _history
        else:
            return result


class ScalarFunctionWrapper:
    def __init__(self, nw, potentials, normalize=True, prefer_parallel=None, cell_logger=None):
        """
        A wrapper providing interfaces to total energy and gradient evaluation.

        Parameters
        ----------
        nw : NeighborWrapper
            The (initial) structure. It will be overwritten.
        potentials : list, LocalPotential
            Potentials defining the total energy value.
        normalize : bool
            Normalizes the cell at each step if True.
        prefer_parallel : bool
            A flag to prefer parallel potential computations.
        cell_logger : Callable
            A function accumulating intermediate cell objects.
        """
        if nw.sparse_pair_distances is None:
            raise ValueError("No NeighborWrapper distance information available: please run `nw.compute_distances()`")
        self.nw = nw
        self.potentials = potentials
        self.normalize = normalize
        self.prefer_parallel = prefer_parallel
        self.cell_logger = cell_logger

        self._last_parameters = None
        self._last = {}

    def maybe_update(self, parameters):
        """
        Updates NeighborWrapper with the new coordinates.
        Performs dumb caching of the last call.

        Parameters
        ----------
        parameters : np.ndarray
            Cartesian coordinates presented as a 1D array.

        Returns
        -------
        cached : bool
            True if no operation was performed.
        """
        if parameters is not self._last_parameters:
            cartesian = parameters.reshape(-1, 3)
            self.nw.set_cell_cartesian(cartesian, normalize=self.normalize)
            self.nw.compute_distances()
            self._last_parameters = parameters
            self._last = {}
            return False
        return True

    def get_current_cell(self):
        """
        Gets the copy of the current cell.

        Returns
        -------
        result : Cell
            Current cell.
        """
        if "cell" not in self._last:
            cell = self._last["cell"] = self.nw.cell.copy()
        else:
            cell = self._last["cell"]
        if "total" in self._last:
            cell.meta["total-energy"] = self._last["total"]
        if "grad" in self._last:
            cell.meta["forces"] = - self._last["grad"]
        return cell

    def _maybe_log(self):
        if self.cell_logger is not None:
            same = "cell" in self._last
            self.cell_logger(self.get_current_cell(), same)

    def f(self, parameters):
        """
        Total energy value interface.

        Parameters
        ----------
        parameters : np.ndarray
            Cartesian coordinates presented as a 1D array.

        Returns
        -------
        energy : float
            The total energy value.
        """
        same_input = self.maybe_update(parameters)
        if same_input and self._last.get("total", None) is not None:
            result = self._last["total"]
        else:
            result = self._last["total"] = self.nw.total(self.potentials, prefer_parallel=self.prefer_parallel)
        self._maybe_log()
        return result

    def g(self, parameters):
        """
        Total energy gradient interface.

        Parameters
        ----------
        parameters : np.ndarray
            Cartesian coordinates presented as a 1D array.

        Returns
        -------
        gradient : np.ndarray
            The total energy gradient.
        """
        same_input = self.maybe_update(parameters)
        if same_input and self._last.get("grad", None) is not None:
            result = self._last["grad"]
        else:
            result = self._last["grad"] = self.nw.grad(self.potentials, prefer_parallel=self.prefer_parallel)
        self._maybe_log()
        return result.reshape(-1)


def batch_rdf(cells, *args, inner=NeighborWrapper.rdf, **kwargs):
    """
    Averaged radial distribution function.

    Parameters
    ----------
    cells : list, tuple
        A collection of wrapped cells to process.
    inner : Callable
        The function computing distribution for a single cell.
    args
    kwargs
        Arguments to `NeighborWrapper.rdf`.

    Returns
    -------
    result : dict
        Radial distribution function values.
    """
    def mean(x):
        return sum(x) / len(x)
    return dict_reduce((inner(w, *args, **kwargs) for w in cells), mean)


def profile(potentials, f, *args, **kwargs):
    """
    Profiles a collection of potentials.

    Parameters
    ----------
    potentials : list
        Potentials to profile.
    f : Callable
        A function `f(x1, ...) -> UnitCell` preparing a unit cell
        for the given set of parameters.
    args
        Sampling of `x1`, ... arguments of the function `f`.
    kwargs
        Arguments to ``NeighborWrapper``.

    Returns
    -------
    energy : np.ndarray
        Energies on the multidimensional grid defined by `args`.
    """
    if not isinstance(potentials, (list, tuple)):
        potentials = potentials,

    result = np.empty(tuple(len(i) for i in args), dtype=float)
    result_shape = result.shape
    result.shape = result.size,

    cutoff = max(i.cutoff for i in potentials)

    for i, pt in enumerate(product(*args)):
        cell = f(*pt)
        wrapped = NeighborWrapper(cell, cutoff=cutoff, **kwargs)
        result[i] = wrapped.total(potentials, ignore_missing_species=True)

    result.shape = result_shape
    return result


def profile_strain(potentials, cell, *args, **kwargs):
    """
    Profiles a collection of potentials by applying strain.

    Parameters
    ----------
    potentials : list
        Potentials to profile.
    cell : UnitCell
        The original cell.
    args
        Relative strains along all vectors.
    kwargs
        Arguments to ``NeighborWrapper``.

    Returns
    -------
    energy : np.ndarray
        Energies of strained cells.
    """
    cell_copy = cell.copy()

    def _f(*_strain):
        _s = np.ones(len(cell.vectors))
        _s[:len(_strain)] = _strain
        cell_copy.vectors = cell.vectors * _s[:, np.newaxis]
        return cell_copy

    return profile(potentials, _f, *args, **kwargs)


def profile_directed_strain(potentials, cell, strain, direction, **kwargs):
    """
    Profiles a collection of potentials by applying strain.

    Parameters
    ----------
    potentials : list
        Potentials to profile.
    cell : UnitCell
        The original cell.
    strain : Iterable
        The relative strain.
    direction : list, tuple, np.ndarray
        The strain direction.
    kwargs
        Arguments to ``NeighborWrapper``.

    Returns
    -------
    energy : np.ndarray
        Energies of strained cells.
    """
    cell_copy = cell.copy()
    direction = np.array(direction)

    def _f(_strain):
        cell_copy.vectors = cell.vectors * (direction * _strain + (1 - direction))[:, np.newaxis]
        return cell_copy

    return profile(potentials, _f, strain, **kwargs)
