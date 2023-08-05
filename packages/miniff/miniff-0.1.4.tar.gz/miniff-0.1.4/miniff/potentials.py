from functools import partial
from inspect import getfullargspec
from collections import namedtuple

import numpy as np
from scipy.optimize import minimize_scalar, root_scalar
from scipy.sparse import csr_matrix

from . import _potentials
from ._util import calc_sparse_distances
from .util import num_grad

# This sets the default policy for preferring parallel routines over serial. It can be changed during runtime
_prefer_parallel = True


class PotentialRuntimeWarning(RuntimeWarning):
    pass


kernel_kind = namedtuple("kernel_kind", ("name", "parallel", "resolving"))


class PotentialKernel:
    def __init__(self, f, name, out_shape, coordination_number, is_parallel, is_resolving):
        """
        Potential kernel function. This wraps cython routines
        and provides workarounds for limiting cases.

        Parameters
        ----------
        f : Callable
            The callable function.
        name : str
            Kernel name.
        out_shape : str
            A code describing the output shape.
        coordination_number : int
            Coordination number of the potential.
        is_parallel : bool
            Indicates whether this kernel is parallel.
        is_resolving : bool
            Indicates whether this kernel is resolving
            (i.e. provides individual energies instead of the total energy).
        """
        if is_resolving:
            if len(out_shape) == 0 or out_shape[0] != 'r':
                raise ValueError(f"The first index of the resolving potential should be 'r', found: '{out_shape}'")

        self.f = f
        self.name = name
        self.out_shape = out_shape
        self.coordination_number = coordination_number
        self.is_parallel = is_parallel
        self.is_resolving = is_resolving

    def get_out_shape(self, n_atoms, n_coords=3):
        return self.compute_shape(self.out_shape, n_atoms, n_coords)

    @staticmethod
    def compute_shape(spec, n_atoms, n_coords=3):
        """
        Calculates shape of an array to receive the output of kernel functions.

        Parameters
        ----------
        spec : str
            A code specifying the shape.
        n_atoms : int
            Atoms count.
        n_coords : int
            Coordinates count.

        Returns
        -------
        out : tuple
            Array shape.
        """
        _code = dict(r=n_atoms, d=n_coords)
        return tuple(_code[i] for i in spec)

    def screen_inputs(self, r_indptr, r_indices, r_data, cartesian_row, cartesian_col, out, species_row, species_mask):
        # Types
        assert r_indptr.dtype == np.int32
        assert r_indices.dtype == np.int32
        assert r_data.dtype == float
        assert cartesian_row.dtype == float
        assert cartesian_col.dtype == float
        assert out.dtype == float
        assert species_row.dtype == np.int32
        assert species_mask.dtype == np.int32

        # Shapes
        rows = len(cartesian_row)
        cols = len(cartesian_col)
        assert cartesian_row.shape == (rows, 3)
        assert cartesian_col.shape == (cols, 3)

        # Sparse format checks
        assert r_indptr.shape == (rows + 1,)
        assert np.all(r_indptr[1:] - r_indptr[:-1] >= 0)
        nnz = r_indptr[-1]
        assert r_indices.shape == (nnz,)
        assert r_data.shape == (nnz,)
        if nnz != 0:
            assert 0 <= r_indices.min()
            assert r_indices.max() < cols

        out_shape = self.get_out_shape(rows)
        assert out.ndim == len(out_shape)
        assert all(i <= j for i, j in zip(out_shape, out.shape))
        assert species_row.shape == (rows,)
        assert species_mask.shape == (self.coordination_number,)

    def raw(self, r_indptr, r_indices, r_data, cartesian_row, cartesian_col, parameters, out=None,
            species_row=None, species_mask=None, **kwargs):
        """
        Wrapper for functions evaluating potentials and gradients.

        Parameters
        ----------
        r_indptr : np.ndarray
            Index pointers of a sparse csr pair distance array.
        r_indices : np.ndarray
            Column indices of a sparse csr pair distance array.
        r_data : np.ndarray, None
            Pre-computed distances between atom pairs corresponding to the above indices.
            If None, it will be recomputed from the cartesian coordinates data.
        cartesian_row : np.ndarray
            Cartesian coordinates corresponding to row indices.
        cartesian_col : np.ndarray
            Cartesian coordinates corresponding to column indices.
        parameters : dict
            Potential parameters.
        out : np.ndarray
            Output array.
        species_row : np.ndarray
            Atomic species with coordinates `cartesian_row` encoded as integers.
        species_mask : np.ndarray
            A mask to apply to species: for example, an array with two integers corresponding
            to specimen Bi and Se for pair potential Bi-Se.
        kwargs
            Other keyword arguments to kernel functions.

        Returns
        -------
            Results of kernel computation.
        """
        if species_row is None:
            species_row = np.zeros(len(r_indptr) - 1, dtype=np.int32)
        if species_mask is None:
            species_mask = np.zeros(self.coordination_number, dtype=np.int32)
        if r_data is None:
            r_data = calc_sparse_distances(r_indptr, r_indices, cartesian_row, cartesian_col)
        if out is None:
            out = np.zeros(self.get_out_shape(*cartesian_row.shape))
        out_ = out
        if out.ndim == 0:  # work-around for zero-dimensional inputs
            out_ = out_[None]
        self.screen_inputs(r_indptr, r_indices, r_data, cartesian_row, cartesian_col, out, species_row, species_mask)
        self.f(
            r_indptr, r_indices, r_data, cartesian_row, cartesian_col,
            **parameters, species_row=species_row, species_mask=species_mask, out=out_,
            **kwargs
        )
        return out

    def csr(self, r, cartesian_row, cartesian_col, parameters, out=None, species_row=None,
            species_mask=None, **kwargs):
        """
        Wrapper for functions evaluating potentials and gradients.

        Parameters
        ----------
        r : csr_matrix, np.ndarray
            CSR or dense matrix with distances.
        cartesian_row : np.ndarray
            Cartesian coordinates corresponding to row indices.
        cartesian_col : np.ndarray
            Cartesian coordinates corresponding to column indices.
        parameters : dict
            Potential parameters.
        out : np.ndarray
            Output array.
        species_row : np.ndarray
            Atomic species with coordinates `cartesian_row` encoded as integers.
        species_mask : np.ndarray
            A mask to apply to species: for example, an array with two integers corresponding
            to specimen Bi and Se for pair potential Bi-Se.
        kwargs
            Other keyword arguments to kernel functions.

        Returns
        -------
            Results of kernel computation.
        """
        if isinstance(r, np.ndarray):
            r = csr_matrix(r)
        return self.raw(r.indptr, r.indices, r.data, cartesian_row, cartesian_col, parameters,
                        out=out, species_row=species_row, species_mask=species_mask, **kwargs)

    def num_grad(self, pre_compute_r_functions=None, **kwargs):
        """
        Constructs a kernel evaluating numerical gradients of a potential.

        Parameters
        ----------
        pre_compute_r_functions : list
            A list of r-dependent quantities to pre-compute.
        kwargs
            Keyword arguments to `num_grad`.

        Returns
        -------
        f_grad : PotentialKernel
            A kernel computing numerical gradients.
        """
        return PotentialKernel(
            _KernelGrad(self, pre_compute_r_functions=pre_compute_r_functions, **kwargs),
            self.name + "_numgrad", self.out_shape + "rd", self.coordination_number, self.is_parallel,
            self.is_resolving)

    def accumulating(self):
        """
        Constructs a kernel evaluating accumulating potential.

        Returns
        -------
        f_accu: PotentialKernel
            A kernel accumulating potentials.
        """
        if not self.is_resolving:
            return self

        return PotentialKernel(_KernelAccu(self), self.name, self.out_shape[1:], self.coordination_number,
                               self.is_parallel, False)

    def __repr__(self):
        return f"{self.__class__.__name__}({self.f}, '{self.name}', '{self.out_shape}', {self.coordination_number}, " \
               f"is_parallel={self.is_parallel}, is_resolving={self.is_resolving})"

    def id_tuple(self):
        return kernel_kind(name=self.name, parallel=self.is_parallel, resolving=self.is_resolving)


class _KernelAccu:
    def __init__(self, f):
        """
        Constructs an accumulating kernel.

        Parameters
        ----------
        f : PotentialKernel
            The kernel to differentiate.
        """
        self.f = f

    def __call__(self, r_indptr, r_indices, r_data, cartesian_row, cartesian_col, species_row, species_mask, out,
                 **parameters):
        out_ = np.zeros(self.f.get_out_shape(*cartesian_row.shape))
        self.f.f(
            r_indptr, r_indices, r_data, cartesian_row, cartesian_col,
            **parameters, species_row=species_row, species_mask=species_mask, out=out_,
        )
        out[:] += out_.sum(axis=0)


class _KernelGrad:
    def __init__(self, f, pre_compute_r_functions=None, **kwargs):
        """
        Constructs a kernel evaluating numerical gradients of a potential.

        Parameters
        ----------
        f : PotentialKernel
            The kernel to differentiate.
        pre_compute_r_functions : list
            A list of r-dependent quantities to pre-compute.
        kwargs
            Keyword arguments to `num_grad`.
        """
        self.f = f
        self.pre_compute_r_functions = pre_compute_r_functions
        self.numgrad_kwargs = kwargs

    def _target(self, shift, r_indptr, r_indices, r_data, cartesian_row, cartesian_col, species_row, species_mask,
                **parameters):
        parameters = parameters.copy()
        n_images = cartesian_col.size // cartesian_row.size
        _cartesian_row = cartesian_row + shift
        _cartesian_col = cartesian_col + np.tile(shift, (n_images, 1))
        _r_data = calc_sparse_distances(r_indptr, r_indices, _cartesian_row, _cartesian_col)
        if self.pre_compute_r_functions is not None:
            parameters["pre_compute_r"] = pre_compute_r(_r_data, self.pre_compute_r_functions, parameters)
        return self.f.raw(r_indptr, r_indices, _r_data, _cartesian_row, _cartesian_col, parameters,
                          species_row=species_row, species_mask=species_mask)

    def __call__(self, r_indptr, r_indices, r_data, cartesian_row, cartesian_col, species_row, species_mask, out,
                 **parameters):
        all_kwargs = {**self.numgrad_kwargs, **parameters}
        if "eps" not in all_kwargs and "a" in all_kwargs:
            all_kwargs["eps"] = 1e-4 * all_kwargs["a"]
        out += num_grad(self._target, np.zeros_like(cartesian_row), r_indptr, r_indices, r_data, cartesian_row,
                        cartesian_col, species_row, species_mask, **all_kwargs)


def kernel_on_site(r_indptr, r_indices, r_data, cartesian_row, cartesian_col, v0, species_row, species_mask, out):
    """
    A simple constant on-site potential scalar value.
    Most input arguments are irrelevant.
    """
    out[species_row == species_mask[0]] += v0


def kernel_g_on_site(r_indptr, r_indices, r_data, cartesian_row, cartesian_col, v0, species_row, species_mask, out):
    """
    The gradient of on-site potential is zero.
    """
    pass


def kernel_dict(kernels):
    """
    Turns a list of kernels into a lookup dictionary.
    Checks for collisions.

    Parameters
    ----------
    kernels : list, tuple
        A list of kernels.

    Returns
    -------
    result : dict
        The resulting lookup dictionary.
    """
    result = {}
    for i in kernels:
        x = i.id_tuple()
        if x in result:
            raise ValueError(f"Found two or more kernels with the same role: {i}, {result[x]}")
        result[x] = i
    return result


class LocalPotential:
    def __init__(self, parameters, cutoff, kernels, family=None, tag=None, additional_inputs=None):
        """
        Potential wrapper.

        Parameters
        ----------
        parameters : dict
            Potential parameters.
        cutoff : Callable
            Cutoff function.
        kernels : dict
            A kernel lookup dictionary.
        family : LocalPotentialFamily
            A family this potential belongs to.
        tag : str
            Optional tag.
        additional_inputs : list
            A list of additional fields required to compute potentials.
        """
        self.parameters = {
            k: (np.array(v) if isinstance(v, (list, tuple)) else v)
            for k, v in parameters.items()
        }
        self.cutoff = cutoff
        self.kernels = dict(kernels)
        self.family = family
        self.tag = tag
        self.additional_inputs = list(additional_inputs) if additional_inputs is not None else None

    def get_all_parameters(self):
        """
        Retrieves a copy of a dict with all potential parameters.

        Returns
        -------
        parameters : dict
            A dict with parameters.
        """
        return self.parameters.copy()

    def get_kernel_by_name(self, kname, resolving=True, prefer_parallel=None, rtn_key=False):
        """
        Picks a potential kernel for the given requirements.

        Parameters
        ----------
        kname : str
            Kernel name.
        resolving : bool
            Indicates whether the kernel needs to be resolving.
        prefer_parallel : bool, None
            Indicates whether parallel kernel is preferred.
        rtn_key : bool
            If True, returns the potential key as well.

        Returns
        -------
        kernel : PotentialKernel
            The kernel requested.
        key
            The key.
        """
        if prefer_parallel is None:
            prefer_parallel = _prefer_parallel
        if prefer_parallel:
            k = kernel_kind(name=kname, parallel=True, resolving=resolving)
            try:
                if rtn_key:
                    return self.kernels[k], k
                else:
                    return self.kernels[k]
            except KeyError:
                pass
        k = kernel_kind(name=kname, parallel=False, resolving=resolving)
        if rtn_key:
            return self.kernels[k], k
        else:
            return self.kernels[k]

    @property
    def pre_compute_r_functions(self):
        if self.family is None:
            return None
        return self.family.pre_compute_r

    def pre_compute_r(self, r_data):
        """Pre-computes quantities for this potential."""
        if self.pre_compute_r_functions is None:
            raise ValueError("Nothing to pre-compute for this potential")
        return pre_compute_r(r_data, self.pre_compute_r_functions, self.parameters)

    def fun_csr_split(self, kname, r_indptr, r_indices, r_data, cartesian_row, cartesian_col, out=None,
                      species_row=None, species_mask=None, prefer_parallel=None, resolving=True, **kwargs):
        """CSR-split function adapter."""
        if self.family is not None and self.family.pre_compute_r is not None and "pre_compute_r" not in kwargs:
            f_r = self.pre_compute_r(r_data)
            kwargs["pre_compute_r"] = f_r
            kwargs["pre_compute_r_handles"] = np.arange(f_r.shape[1], dtype=np.int32)
        if self.additional_inputs:
            missing_keys = set(self.additional_inputs).difference(set(kwargs.keys()) | set(self.parameters.keys()))
            if missing_keys:
                raise ValueError(f"Following additional inputs are missing: {', '.join(sorted(missing_keys))}")
        return self.get_kernel_by_name(kname, prefer_parallel=prefer_parallel, resolving=resolving).raw(
            r_indptr, r_indices, r_data, cartesian_row, cartesian_col, self.parameters, out,
            species_row, species_mask, **kwargs
        )

    def fun_csr(self, kname, r, cartesian_row, cartesian_col, **kwargs):
        """CSR input function adapter."""
        if isinstance(r, np.ndarray):
            r = csr_matrix(r)
        return self.fun_csr_split(kname, r.indptr, r.indices, r.data, cartesian_row, cartesian_col, **kwargs)

    def __call__(self, kind, r, *args, **kwargs):
        if isinstance(r, tuple):
            assert len(r) == 3
            return self.fun_csr_split(kind, r[0], r[1], r[2], *args, **kwargs)
        if isinstance(r, (csr_matrix, np.ndarray)):
            return self.fun_csr(kind, r, *args, **kwargs)
        else:
            raise ValueError(f"Do not recognize argument type: {r}")

    def copy(self, tag=None):
        """
        A copy.

        Parameters
        ----------
        tag : str
            An optional new tag.

        Returns
        -------
            A copy of this potential.
        """
        if tag is None:
            tag = self.tag
        return self.__class__(self.get_all_parameters(), self.cutoff, self.kernels,
                              family=self.family, tag=tag, additional_inputs=self.additional_inputs)

    def __repr__(self):
        args = [f"{len(self.kernels):d} kernels", f"tag={self.tag}"]
        for k, v in sorted(self.get_all_parameters().items()):
            if isinstance(v, np.ndarray):
                if v.ndim <= 1:
                    rv = repr(v)
                else:
                    rv = f"<array shape={v.shape} dtype={v.dtype}>"
            elif isinstance(v, (float, int, complex, str)):
                rv = repr(v)
            else:
                rv = str(type(v))
            args.append(f"{k}={rv}")
        return f"{self.__class__.__name__ if self.family is None else self.family.tag}({', '.join(args)})"

    def state_dict(self):
        """State dict of the potential."""
        if self.family is None:
            raise ValueError("No family assigned to this potential")
        return self.family.get_state_dict(self)

    @staticmethod
    def from_state_dict(data):
        """Loads potential from the state dict."""
        return LocalPotentialFamily.instance_from_state_dict(data)


class ScaledLocalPotential(LocalPotential):
    def __init__(self, parameters, cutoff, kernels, family=None, tag=None, additional_inputs=None):
        """
        Potential with energy and length scale.

        Parameters
        ----------
        parameters : dict
            Potential parameters.
        cutoff : Callable
            Cutoff function.
        kernels : dict
            A dictionary with potential kernels.
        family : LocalPotentialFamily
            A family this potential belongs to.
        tag : str
            Optional tag.
        additional_inputs : list
            A list of additional fields required to compute potentials.
        """
        if "epsilon" not in parameters or "sigma" not in parameters:
            raise ValueError(f"Missing either 'epsilon' or 'sigma' from parameters: {parameters}")
        self.epsilon = parameters.pop("epsilon")
        self.sigma = parameters.pop("sigma")
        self.__out_scale__ = dict(
            kernel=self.epsilon,
            kernel_gradient=self.epsilon / self.sigma,
            kernel_numgrad=self.epsilon / self.sigma,
        )
        super().__init__(parameters, cutoff * self.sigma, kernels, family=family, tag=tag,
                         additional_inputs=additional_inputs)

    def get_all_parameters(self):
        """
        Retrieves a copy of a dict with all potential parameters.

        Returns
        -------
        parameters : dict
            A dict with parameters.
        """
        return {"epsilon": self.epsilon, "sigma": self.sigma, **super().get_all_parameters()}

    def fun_csr_split(self, kname, r_indptr, r_indices, r_data, cartesian_row, cartesian_col, out=None,
                      species_row=None, species_mask=None, **kwargs):
        """CSR-split function adapter."""
        out = super().fun_csr_split(kname, r_indptr, r_indices, r_data / self.sigma if r_data is not None else None,
                                    cartesian_row / self.sigma, cartesian_col / self.sigma, out, species_row,
                                    species_mask, **kwargs)
        out *= self.__out_scale__[kname]
        return out

    def copy(self, tag=None):
        """
        A copy.

        Parameters
        ----------
        tag : str
            An optional new tag.

        Returns
        -------
            A copy of this potential.
        """
        if tag is None:
            tag = self.tag
        return self.__class__(self.get_all_parameters(), self.cutoff / self.sigma,
                              self.kernels, family=self.family, tag=tag, additional_inputs=self.additional_inputs)

    def __eq__(self, other):
        if not isinstance(other, ScaledLocalPotential):
            return False
        return self.sigma == other.sigma and self.epsilon == other.epsilon and super().__eq__(other)


class NestedLocalPotential(LocalPotential):
    def __init__(self, parameters, cutoff, kernels, descriptors, **kwargs):
        """
        Potential requiring a list of other potentials to be computed.

        Parameters
        ----------
        parameters : dict
            Potential parameters.
        cutoff : Callable
            Cutoff function.
        kernels : dict
            A kernel lookup dictionary.
        descriptors : list, tuple
            A list of other potentials to be computed.
        kwargs
            Arguments to LocalPotential.
        """
        super().__init__(parameters, cutoff, kernels, **kwargs)
        self.descriptors = tuple(descriptors)

    def fun_csr_split(self, *args, **kwargs):
        """CSR-split function adapter."""
        return super().fun_csr_split(*args, descriptors=self.descriptors, **kwargs)

    def state_dict(self):
        """State dict of the potential."""
        result = super().state_dict()
        result["descriptors"] = result_wraps = []
        for i in self.descriptors:
            result_wraps.append(i.state_dict())
        return result

    def copy(self, tag=None):
        """
        A copy.

        Parameters
        ----------
        tag : str
            An optional new tag.

        Returns
        -------
            A copy of this potential.
        """
        if tag is None:
            tag = self.tag
        return self.__class__(self.get_all_parameters(), self.cutoff, self.kernels, self.descriptors,
                              family=self.family, tag=tag, additional_inputs=self.additional_inputs)


class PreComputeRFunction:
    def __init__(self, f, parameters_map=None):
        self.f = f
        f_args = getfullargspec(f)[0][1:]
        if parameters_map is None:
            parameters_map = dict()
        self.args = tuple(parameters_map.get(k, k) for k in f_args)

    def get_parameter_values(self, parameters):
        return tuple(parameters[k] for k in self.args)

    def __call__(self, r, parameters):
        return self.f(r, *self.get_parameter_values(parameters))

    def cache_key(self, parameters):
        return hash((id(self.f), self.get_parameter_values(parameters)))


class LocalPotentialFamily:
    default_proto = LocalPotential

    def __init__(self, parameters, cutoff, kernels, parameter_defaults=None,
                 tag=None, proto=None, pre_compute_r=None, additional_inputs=None, complement_accumulating=True,
                 complement_num_grad=True, doc=None):
        """
        Represents a local potential family with the same potential shape and
        arbitrary parameter values.

        Parameters
        ----------
        parameters : dict
            A dictionary with keys being potential parameters and values being parameter bounds.
        cutoff : float, str, Callable
            The cutoff value, parameter name or a function of parameters.
        kernels : list, tuple
            All kernels available for this potential.
        parameter_defaults : dict
            A dictionary with parameter default values.
        tag : str
            Optional tag
        proto : class
            A class wrapping constructed potentials.
        pre_compute_r : list
            A list of quantities depending on inter-atomic distance r
            that can be shared across several potentials of the same
            family.
        additional_inputs : list
            A list of additional fields required to compute potentials.
        complement_accumulating : bool
            If True, adds accumulating kernels based on resolved ones.
        complement_num_grad : bool
            If True, adds numerical gradients.
        doc : str
            Potential docstring.
        """
        kernels = tuple(kernels)
        if proto is None:
            proto = self.default_proto

        self.parameters = parameters
        self.parameter_defaults = parameter_defaults if parameter_defaults is not None else dict()
        self.__cutoff_handle__ = cutoff

        kernels = list(kernels)
        if complement_accumulating:
            kernels += list(i.accumulating() for i in kernels if i.is_resolving)
        self.tag = tag
        self.doc = doc
        self.proto = proto
        if pre_compute_r is not None:
            self.pre_compute_r = tuple(
                PreComputeRFunction(i) if not isinstance(i, PreComputeRFunction) else i
                for i in pre_compute_r
            )
        else:
            self.pre_compute_r = None
        if complement_num_grad:
            kernels += list(
                i.num_grad(pre_compute_r_functions=self.pre_compute_r)
                for i in kernels
                if i.name == "kernel"
            )
        self.kernels = kernel_dict(kernels)
        if additional_inputs is None:
            self.additional_inputs = tuple()
        elif isinstance(additional_inputs, str):
            self.additional_inputs = additional_inputs,
        else:
            self.additional_inputs = tuple(additional_inputs)

    def cutoff(self, kwargs):
        if isinstance(self.__cutoff_handle__, (float, int)):
            return self.__cutoff_handle__
        elif isinstance(self.__cutoff_handle__, str):
            return kwargs[self.__cutoff_handle__]
        elif callable(self.__cutoff_handle__):
            return self.__cutoff_handle__(kwargs)
        else:
            raise RuntimeError(f"Do not recognize the cutoff handle: {self.__cutoff_handle__}")

    def screen_parameters(self, **kwargs):
        """
        Check the validity of potential parameters.

        Parameters
        ----------
        kwargs
            Potential parameters.

        Returns
        -------
        result : dict
            Screened parameters.
        """
        parameters = self.parameter_defaults.copy()
        parameters.update({k: (np.array(v) if isinstance(v, (list, tuple)) else v) for k, v in kwargs.items()})
        for k, r in self.parameters.items():
            if k not in parameters:
                raise ValueError(f"Parameter '{k}' is missing from defined parameters")
            if r is not None:
                l, u = r
                p = parameters[k]
                if not np.all((l <= p) <= u):
                    raise ValueError(f"Parameter '{k}' is out of bounds: {l} <= {p} <= {u}")
        return parameters

    def instantiate(self, *, tag=None, empty=None, **kwargs):
        """
        Instantiate this potential.

        Parameters
        ----------
        tag : str
            An optional tag.
        empty : LocalPotential
            An optional empty object to use.
        kwargs
            Values of parameters.

        Returns
        -------
        result : LocalPotential
            The potential.
        """
        parameters = self.screen_parameters(**kwargs)
        return self.proto(parameters, self.cutoff(parameters), self.kernels, family=self, tag=tag,
                          additional_inputs=self.additional_inputs)

    def __call__(self, *args, **kwargs):
        return self.instantiate(*args, **kwargs)

    def get_state_dict(self, potential):
        """
        Retrieves a state dict.

        Parameters
        ----------
        potential : LocalPotential
            A potential to represent.

        Returns
        -------
        result : dict
            Potential parameters and other information.
        """
        if self.tag is None:
            raise ValueError("No tag set for potential family")
        return dict(
            tag=self.tag,
            parameters=potential.get_all_parameters(),
            ptag=potential.tag,
        )

    def instance_from_state_dict(self, data):
        """
        Restores a potential from its dict representation.

        Parameters
        ----------
        data : dict
            A dict with the data.

        Returns
        -------
        result : LocalPotential
            The restored potential.
        """
        parameters = data.pop("parameters")
        tag = data.pop("ptag")
        if len(data) > 0:
            raise ValueError(f"Unknown fields encountered: {set(data.keys())}")
        return self.instantiate(**parameters, tag=tag)


class NestedLocalPotentialFamily(LocalPotentialFamily):
    default_proto = NestedLocalPotential

    def instantiate(self, tag=None, **kwargs):
        """
        Instantiate this potential.

        Parameters
        ----------
        tag : str
            An optional tag.
        kwargs
            Values of parameters.

        Returns
        -------
        result : LocalPotential
            The potential.
        """
        if "descriptors" not in kwargs:
            raise ValueError("Missing descriptors for the nested potential")
        parameters = self.screen_parameters(**kwargs)
        descriptors = list(parameters.pop("descriptors"))
        for i in descriptors:
            assert isinstance(i, LocalPotential)
        return self.proto(parameters, max(self.cutoff(parameters), *tuple(i.cutoff for i in descriptors)),
                          self.kernels, descriptors, family=self, tag=tag, additional_inputs=self.additional_inputs)

    def get_state_dict(self, potential):
        """
        Retrieves a state dict.

        Parameters
        ----------
        potential : NestedLocalPotential
            A potential to represent.

        Returns
        -------
        result : dict
            Potential parameters and other information.
        """
        result = super().get_state_dict(potential)
        result["descriptors"] = list(i.state_dict() for i in potential.descriptors)
        return result

    def instance_from_state_dict(self, data):
        """
        Restores a potential from its dict representation.

        Parameters
        ----------
        data : dict
            A dict with the data.

        Returns
        -------
        result : LocalPotential
            The restored potential.
        """
        descriptors = data.pop("descriptors")
        data["parameters"]["descriptors"] = list(map(potential_from_state_dict, descriptors))
        return super().instance_from_state_dict(data)


def pre_compute_r(r, f_r, parameters):
    """
    Pre-computes r-dependent functions.

    Some potentials may partially share pre-computed functions to
    speed up computations. This function prepares a dense array
    of pre-computed distance-dependent functions.

    Parameters
    ----------
    r : np.ndarray
        A 1D array of distances.
    f_r : list
        A list of pairs of parameters and the corresponding functions.
    parameters : dict
        A dict with potential parameters.

    Returns
    -------
    result : np.ndarray
    """
    result = np.empty((len(r), len(f_r)), dtype=float)
    for i, fun in enumerate(f_r):
        result[:, i] = fun(r, parameters)
    return result


def _get_potentials(name, parallel=True, other=None):
    """
    Retrieves potentials functions from `_potentials` module according to the following convention:

    * `kernel_{name}` for potential;
    * `kernel_g_{name}` for potential gradients;
    * `pkernel_{name}` for parallel implementation of potential, optional;
    * `pkernel_g_{name}` for parallel implementation of potential gradients, optional;

    Parameters
    ----------
    name : str
        The name of the potential.
    parallel : bool
        If True, adds parallel routines to the output.
    other : dict
        Other kernel names to include.

    Returns
    -------
    result : list
        The resulting list of potentials.
    """
    fnames = ((f"kernel_{name}", "kernel", False), (f"kernel_g_{name}", "kernel_gradient", False))
    if other:
        fnames = fnames + tuple((src, dst, False) for dst, src in other.items())
    if parallel:
        fnames = fnames + tuple(("p" + src, dst, True) for src, dst, _ in fnames)
    result = []
    for fname, dst, p in fnames:
        pk = PotentialKernel(
            f=getattr(_potentials, fname),
            name=dst,
            out_shape=_potentials.out_shape[fname],
            coordination_number=_potentials.coordination[fname],
            is_parallel=p,
            is_resolving=_potentials.resolving[fname],
        )
        result.append(pk)
    return result


general_pair_potential_family = LocalPotentialFamily(
    parameters=dict(f=None, df_dr=None, a=(0, np.inf)),
    cutoff="a",
    tag='general pair',
    kernels=_get_potentials("general_2", parallel=False),
    doc="f(r)",
)
general_triple_potential_family = LocalPotentialFamily(
    parameters=dict(f=None, df_dr1=None, df_dr2=None, df_dt=None, a=(0, np.inf)),
    cutoff="a",
    tag='general triple',
    kernels=_get_potentials("general_3", parallel=False),
    doc="f(r1, r2, cos θ)",
)
on_site_potential_family = LocalPotentialFamily(
    parameters=dict(v0=(-np.inf, np.inf)),
    cutoff=0,
    kernels=[
        PotentialKernel(kernel_on_site, "kernel", "r", 1, False, True),
        PotentialKernel(kernel_g_on_site, "kernel_gradient", "rrd", 1, False, True),
    ],
    tag='on-site',
    doc="const",
)
harmonic_repulsion_potential_family = LocalPotentialFamily(
    parameters=dict(a=(0, np.inf), epsilon=(0, np.inf)),
    cutoff="a",
    tag="harmonic repulsion",
    kernels=_get_potentials("harmonic_repulsion"),
    doc="ε/2 (1 - r/a)^2",
)

atomic_ranges = dict(epsilon=(0, np.inf), sigma=(0, np.inf))

lj_potential_family = LocalPotentialFamily(
    parameters=dict(**atomic_ranges, a=(2. ** (1. / 6), np.inf)),
    cutoff="a",
    tag="Lennard-Jones",
    proto=ScaledLocalPotential,
    kernels=_get_potentials("lj"),
    doc="4 (1/r^12 - 1/r^6)",
)


class SW2PotentialFamily(LocalPotentialFamily):
    def instantiate(self, min_at=(2. ** (1. / 6), -1), tag=None, **kwargs):
        if not ("gauge_a" in kwargs and "gauge_b" in kwargs):
            sigma = kwargs.pop("sigma")
            epsilon = kwargs.pop("epsilon")
            min_x, min_y = min_at
            result = root_scalar(
                lambda x: self.__get_min__(dict(gauge_a=1, gauge_b=x, **kwargs)) - min_x,
                bracket=[1e-3, 3], method='bisect')
            gauge_b = result.root
            gauge_a = min_y / self.__scalar_target__(min_x, dict(gauge_a=1, gauge_b=gauge_b, **kwargs))
            kwargs = dict(gauge_a=gauge_a, gauge_b=gauge_b, **kwargs)
            kwargs["sigma"] = sigma
            kwargs["epsilon"] = epsilon
        return super().instantiate(tag=tag, **kwargs)

    def __scalar_target__(self, x, parameters, out=None):
        c = np.array([[0, 0, 0], [x, 0, 0]])
        d = np.array([[0, x], [0, 0]])
        if out is not None:
            out[:] = 0
        return self.kernels["kernel", False, True].csr(d, c, c, parameters, out)[0]

    def __get_min__(self, parameters):
        """
        Finds potential minimum.

        Parameters
        ----------
        parameters : dict
            Potential parameters.

        Returns
        -------
        r : float
            Radius where the potential takes the minimum.
        """
        bounds = self.__get_min_search_bounds__(parameters)
        if bounds[0] >= bounds[1]:
            return float("nan")

        out_buffer = np.zeros(2, dtype=float)
        result = minimize_scalar(partial(self.__scalar_target__, parameters=parameters, out=out_buffer), bounds=bounds,
                                 method="bounded", options=dict(xatol=1e-13))

        if not result.success:
            raise RuntimeError("Failed to find a minimum")

        return result.x

    def __get_min_search_bounds__(self, parameters):
        """
        Bounds for finding the potential minimum.

        Parameters
        ----------
        parameters : dict
            Potential parameters.

        Returns
        -------
        bounds : tuple
            Lower and upper bounds.
        """
        return parameters["gauge_b"] ** (1. / (parameters["p"] - parameters["q"])), self.cutoff(parameters)


sw2_potential_family = SW2PotentialFamily(
    parameters=dict(**atomic_ranges, gauge_a=(0, np.inf), gauge_b=(0, np.inf), a=(1, np.inf), p=(1, np.inf),
                    q=(-np.inf, np.inf)),
    cutoff="a",
    tag="Stillinger-Weber type 2",
    proto=ScaledLocalPotential,
    kernels=_get_potentials("sw_phi2"),
    doc="A ( B r^{-p} - r^{-q}) exp 1/(r-a)",
)
sw3_potential_family = LocalPotentialFamily(
    parameters=dict(**atomic_ranges, l=(0, np.inf), gamma=(0, np.inf), cos_theta0=(-1, 1), a=(1, np.inf)),
    cutoff="a",
    tag="Stillinger-Weber type 3",
    proto=ScaledLocalPotential,
    kernels=_get_potentials("sw_phi3"),
    doc="λ (cos θ - cos θ0)^2 exp (γ/(r1 - a) + γ/(r2 - a))",
)


def sine_cutoff_fn(r, a):
    return .5 + np.cos(np.pi * r / a) / 2


def sine_cutoff_fp(r, a):
    return - np.pi * np.sin(np.pi * r / a) / (a * 2)


def exp_fn(r, eta):
    return np.exp(- eta * r ** 2)


behler2_descriptor_family = LocalPotentialFamily(
    parameters=dict(a=(0, np.inf), eta=(0, np.inf), r_sphere=(0, np.inf)),
    cutoff="a",
    tag="Behler type 2",
    pre_compute_r=[sine_cutoff_fn, sine_cutoff_fp],
    kernels=_get_potentials("mlsf_g2"),
    doc="exp(- η (r-r0)^2) (cos(πr/a) + 1) / 2",
)
sigmoid_descriptor_family = LocalPotentialFamily(
    parameters=dict(a=(0, np.inf), dr=(0, np.inf), r0=(0, np.inf)),
    cutoff="a",
    tag="Sigmoid",
    kernels=_get_potentials("sigmoid"),
    doc="(cos(πr/a) + 1) / 2 / exp{(r-r0)/dr}",
)
behler5_descriptor_family = LocalPotentialFamily(
    parameters=dict(a=(0, np.inf), eta=(0, np.inf), l=(-1, 1), zeta=(0, np.inf)),
    parameter_defaults=dict(epsilon=1.0),
    cutoff="a",
    tag="Behler type 5",
    pre_compute_r=[sine_cutoff_fn, sine_cutoff_fp, exp_fn],
    kernels=_get_potentials("mlsf_g5"),
    doc="(1 + λ cos θ)^ζ 2^{1-ζ} ε exp(- η (r1^2 + r2^2)) (cos(πr1/a) + 1) (cos(πr2/a) + 1) / 4",
)
behler4_descriptor_family = LocalPotentialFamily(
    parameters=dict(a=(0, np.inf), eta=(0, np.inf), l=(-1, 1), zeta=(0, np.inf)),
    parameter_defaults=dict(epsilon=1.0),
    cutoff="a",
    tag="Behler type 4",
    pre_compute_r=[sine_cutoff_fn, sine_cutoff_fp, exp_fn],
    kernels=_get_potentials("mlsf_g4"),
    doc="(1 + λ cos θ)^ζ 2^{1-ζ} ε exp(- η (r1^2 + r2^2 + r3^2)) (cos(πr1/a) + 1) (cos(πr2/a) + 1) (cos(πr3/a) + 1) / 8",
)
behler5x_descriptor_family = LocalPotentialFamily(
    parameters=dict(a=(0, np.inf), eta1=(0, np.inf), eta2=(0, np.inf), cos_theta0=(-1, 1)),
    parameter_defaults=dict(epsilon=1.0),
    cutoff="a",
    tag="Behler type 5x",
    pre_compute_r=[
        sine_cutoff_fn, sine_cutoff_fp,
        PreComputeRFunction(exp_fn, parameters_map=dict(eta="eta1")),
        PreComputeRFunction(exp_fn, parameters_map=dict(eta="eta2")),
    ],
    kernels=_get_potentials("mlsf_g5x"),
    doc="ε/4 (cos θ - cos θ_0)^2 (f1(r1) f2(r2) + f2(r1) f1(r2)); fi(r) = (exp -η_i r^2) (cos(πr/a) + 1) / 2",
)
ewald_real_potential_family = LocalPotentialFamily(
    parameters=dict(a=(0, np.inf), eta=(0, np.inf)),
    cutoff="a",
    tag="Ewald-real",
    kernels=_get_potentials("ewald_real", other={"kernel_cgradient": "kernel_c_ewald_real"}),
    additional_inputs="charges",
    doc="erfc(ηr) q1 q2 / 2 / r ",
)
ewald_k_potential_family = LocalPotentialFamily(
    parameters=dict(eta=(0, np.inf)),
    cutoff=0,
    tag="Ewald-k",
    kernels=_get_potentials("ewald_k", other={"kernel_cgradient": "kernel_c_ewald_k"}),
    additional_inputs=("charges", "volume", "k_grid"),
)


def kernel_u_ewald_self(kind, r_indptr, r_indices, r_data, cartesian_row, cartesian_col, eta, charges, volume,
                        species_row, species_mask, out):
    """
    Ewald on-site potential energy kernel.

    Parameters
    ----------
    kind : {'fun', 'grad'}
        Indicates to return per-point energies or energy gradients.
    r_indptr : np.ndarray
    r_indices : np.ndarray
    r_data : np.ndarray
    cartesian_row : np.ndarray
    cartesian_col : np.ndarray
        Common arguments to descriptor kernels specifying coordinates and
        neighbor relations.
    eta : float
        Gaussian screening parameter.
    charges : np.ndarray
        Atomic charges.
    volume : float
        Lattice volume.
    species_row : np.ndarray
    species_mask : np.ndarray
    out : np.ndarray
    """
    assert kind in ("fun", "grad", "cgrad")
    a = - eta / (np.sqrt(np.pi))
    b = - 0.5 * np.pi / (eta ** 2 * volume)
    charges_sum = np.sum(charges)

    if kind == "fun":
        out[:] += (a * charges + b * charges_sum) * charges
    elif kind == "grad":
        pass
    elif kind == "cgrad":
        out[:] += np.diag(2 * a * charges + b * charges_sum) + b * charges[:, None]


kernel_ewald_self = partial(kernel_u_ewald_self, "fun")
kernel_g_ewald_self = partial(kernel_u_ewald_self, "grad")
kernel_c_ewald_self = partial(kernel_u_ewald_self, "cgrad")
ewald_self_potential_family = LocalPotentialFamily(
    parameters=dict(eta=(0, np.inf)),
    cutoff=0,
    tag="Ewald-self",
    kernels=[
        PotentialKernel(kernel_ewald_self, "kernel", "r", 1, False, True),
        PotentialKernel(kernel_g_ewald_self, "kernel_gradient", "rrd", 1, False, True),
        PotentialKernel(kernel_c_ewald_self, "kernel_cgradient", "rr", 1, False, True),
    ],
    additional_inputs=("charges", "volume"),
)


def kernel_u_ewald_total(components, r_indptr, r_indices, r_data, cartesian_row, cartesian_col, a, eta, charges, volume,
                         k_grid, scale, species_row, species_mask, out):
    """
    A kernel for Ewald potential sum.

    Parameters
    ----------
    components : list
        A list of potential kernel components: real, k, self.
    r_indptr : np.ndarray
    r_indices : np.ndarray
    r_data : np.ndarray
    cartesian_row : np.ndarray
    cartesian_col : np.ndarray
        Common arguments to descriptor kernels specifying coordinates and
        neighbor relations.
    a : float
        Cutoff of the real-space part.
    eta : float
    charges : np.ndarray
        An array with atomic charges.
    volume : float
        Unit cell volume.
    k_grid : np.ndarray
        Reciprocal summation grid.
    scale : float
        The scale: e^2 / 4 / π / ε0 = Hartree * aBohr
    species_row : np.ndarray
    species_mask : np.ndarray
    out : np.ndarray
    """
    # The real and self parts are resolving: allocate a bigger buffer
    if components[0] is _potentials.kernel_ewald_real:
        out_r = np.zeros(len(cartesian_row), dtype=out.dtype)
    else:
        out_r = np.zeros((len(cartesian_row),) + out.shape, dtype=out.dtype)
    components[0](r_indptr, r_indices, r_data, cartesian_row, cartesian_col, a, eta, charges, species_row, species_mask, out_r)  # R
    components[1](r_indptr, r_indices, r_data, cartesian_row, cartesian_col, eta, charges, volume, k_grid, species_row, species_mask, out)  # K
    components[2](r_indptr, r_indices, r_data, cartesian_row, cartesian_col, eta, charges, volume, species_row, species_mask, out_r)  # S
    out += out_r.sum(axis=0)
    out *= scale


kernel_ewald_total = partial(kernel_u_ewald_total, (_potentials.kernel_ewald_real, _potentials.kernel_ewald_k, kernel_ewald_self))
kernel_g_ewald_total = partial(kernel_u_ewald_total, (_potentials.kernel_g_ewald_real, _potentials.kernel_g_ewald_k, kernel_g_ewald_self))
kernel_c_ewald_total = partial(kernel_u_ewald_total, (_potentials.kernel_c_ewald_real, _potentials.kernel_c_ewald_k, kernel_c_ewald_self))


ewald_total_potential_family = LocalPotentialFamily(
    parameters=dict(a=(0, np.inf), eta=(0, np.inf), scale=None),
    cutoff=0,
    tag="Ewald-total",
    kernels=[
        PotentialKernel(kernel_ewald_total, "kernel", "", 2, False, False),
        PotentialKernel(kernel_g_ewald_total, "kernel_gradient", "rd", 2, False, False),
        PotentialKernel(kernel_c_ewald_total, "kernel_cgradient", "r", 2, False, False),
    ],
    additional_inputs=("charges", "volume", "k_grid"),
)


def kernel_u_ewald_charge_wrapper(kind, r_indptr, r_indices, r_data, cartesian_row, cartesian_col, descriptors,
                                  a, eta, charge_middleware, volume, k_grid, scale, species_row, species_mask, out):
    """
    A kernel combining charge descriptors into Ewald potentials.

    The workflow:
    1. Compute charges.
    2. Feed charges to Ewald potentials.

    Parameters
    ----------
    kind : str
        Ewald kernel to redirect to.
    r_indptr : np.ndarray
    r_indices : np.ndarray
    r_data : np.ndarray
    cartesian_row : np.ndarray
    cartesian_col : np.ndarray
        Common arguments to descriptor kernels specifying coordinates and
        neighbor relations.
    descriptors : list
        A dictionary with potentials determining atomic charges.
    a : float
    eta : float
    charge_middleware : {"subtract_mean", None}
        Charge post-processing.
    volume : float
    k_grid : np.ndarray
        Arguments to Ewald.
    scale : float
        The scale: e^2 / 4 / π / ε0 = Hartree * aBohr
    species_row : np.ndarray
    species_mask : np.ndarray
    out : np.ndarray
    """
    assert kind in ("fun", "grad")
    do_grad = kind == "grad"
    assert charge_middleware in (None, "subtract_mean")

    def _zeros(spec):
        return np.zeros(PotentialKernel.compute_shape(spec, *cartesian_row.shape), dtype=cartesian_row.dtype)

    # Compute all charges
    charges = _zeros("r")
    for charge_descriptor in descriptors:
        charge_descriptor.fun_csr_split(
            "kernel", r_indptr, r_indices, r_data, cartesian_row, cartesian_col, out=charges, species_row=species_row,
            species_mask=charge_descriptor.tag, prefer_parallel=True, resolving=True,
        )
    if charge_middleware == "subtract_mean":
        charges -= charges.mean()

    if do_grad:
        charges_g = _zeros("rrd")
        for charge_descriptor in descriptors:
            charge_descriptor.fun_csr_split(
                "kernel_gradient", r_indptr, r_indices, r_data, cartesian_row, cartesian_col, out=charges_g,
                species_row=species_row, species_mask=charge_descriptor.tag, prefer_parallel=True, resolving=True,
            )
        if charge_middleware == "subtract_mean":
            charges_g -= charges_g.mean(axis=0)[None, ...]

    # Compute energies/gradients
    _species_mask = np.zeros(2, dtype=np.int32)
    if do_grad:
        out_r = _zeros("rd")
        ewald_total_potential_family.kernels[kernel_kind(name="kernel_gradient", resolving=False, parallel=False)].f(
            r_indptr, r_indices, r_data, cartesian_row, cartesian_col, a, eta, charges, volume, k_grid, scale,
            species_row, _species_mask, out_r,
        )

        out_c = _zeros("r")
        ewald_total_potential_family.kernels[kernel_kind(name="kernel_cgradient", resolving=False, parallel=False)].f(
            r_indptr, r_indices, r_data, cartesian_row, cartesian_col, a, eta, charges, volume, k_grid, scale,
            species_row, _species_mask, out_c,
        )

        out += out_r + np.einsum("c,cik->ik", out_c, charges_g)
    else:
        ewald_total_potential_family.kernels[kernel_kind(name="kernel", resolving=False, parallel=False)].f(
            r_indptr, r_indices, r_data, cartesian_row, cartesian_col, a, eta, charges, volume, k_grid, scale,
            species_row, _species_mask, out,
        )


kernel_ewald_charge_wrapper = partial(kernel_u_ewald_charge_wrapper, "fun")
kernel_g_ewald_charge_wrapper = partial(kernel_u_ewald_charge_wrapper, "grad")


ewald_charge_wrapper_potential_family = NestedLocalPotentialFamily(
    parameters=dict(a=(0, np.inf), eta=(0, np.inf), charge_middleware=None),
    cutoff=0,
    kernels=[
        PotentialKernel(kernel_ewald_charge_wrapper, "kernel", "", 1, False, False),
        PotentialKernel(kernel_g_ewald_charge_wrapper, "kernel_gradient", "rd", 1, False, False),
    ],
    tag='Ewald charge wrapper potential',
    additional_inputs=("volume", "k_grid"),
    parameter_defaults=dict(charge_middleware="subtract_mean"),
)


known_families = {
    v.tag: v
    for v in locals().values()
    if isinstance(v, LocalPotentialFamily)
}


def potential_from_state_dict(data):
    """
    Restores a potential from its state dict.

    Parameters
    ----------
    data : dict
        A state dict.

    Returns
    -------
    result : LocalPotential
        The restored potential.
    """
    data = dict(data)
    family = known_families[data.pop("tag")]
    return family.instance_from_state_dict(data)


def behler2_p2(r, a, eta, r_sphere):
    """
    Second derivative of the two-point Behler descriptor.

    Parameters
    ----------
    r : float, np.ndarray
        Radial point(s).
    a : float
    eta : float
    r_sphere : float
        Behler type 2 function parameters.

    Returns
    -------
    result : float, np.ndarray
        The second derivative of the two-point descriptor.
    """
    cutoff_fn = (np.cos(r * np.pi / a) + 1) / 2
    cutoff_fn_1 = - np.sin(r * np.pi / a) * np.pi / a / 2
    cutoff_fn_2 = - np.cos(r * np.pi / a) * (np.pi / a) ** 2 / 2

    gaussian = np.exp(- eta * (r - r_sphere) ** 2)
    gaussian_1 = - gaussian * eta * 2 * (r - r_sphere)
    gaussian_2 = - gaussian_1 * eta * 2 * (r - r_sphere) - gaussian * eta * 2

    return cutoff_fn * gaussian_2 + 2 * cutoff_fn_1 * gaussian_1 + cutoff_fn_2 * gaussian


def behler_turning_point(a, eta, r_sphere):
    """
    Searches for the turning point of the two-point Behler descriptor.

    Parameters
    ----------
    a : float
    eta : float
    r_sphere : float
        Behler type 2 function parameters.

    Returns
    -------
    result : float
        The turning point.
    """
    eta = eta * a ** 2
    r_sphere = r_sphere / a
    if eta == 0:
        return a / 2
    rbound = min(.5, 1 / (2 * eta) ** .5)
    return root_scalar(behler2_p2, (1, eta, r_sphere), bracket=[0, rbound], method='bisect').root * a


def _pre_compute_r_quantities(distances, potentials):
    """
    Pre-computes r-dependent quantities for a given set of potentials.

    Parameters
    ----------
    distances : np.ndarray
        Pair distances.
    potentials : list, tuple
        Potentials to process.

    Returns
    -------
    pre_compute_r_data : np.ndarray
        A rectangular matrix `[len(distances), len(r_quantities)]` with floating point r-dependent function values.
    pre_compute_r_handles : list
        A list of integer numpy arrays with entries corresponding to columns in `pre_compute_r_data`.
    """
    signatures = []
    signature_offsets = [0]
    for p in potentials:
        p_f_r = p.pre_compute_r_functions
        if p_f_r is None:
            signature_offsets.append(0)
        else:
            signatures += list(
                i.cache_key(p.parameters)
                for i in p_f_r
            )
            signature_offsets.append(len(p_f_r))
    signatures = np.array(signatures)
    signature_offsets = np.cumsum(signature_offsets)
    if len(signatures) > 0:
        unique_signatures, signatures = np.unique(signatures, return_inverse=True)
        signatures = signatures.astype(np.int32)
        pre_compute_r_data = np.empty((len(distances), len(unique_signatures)), dtype=float)
        pre_compute_r_handles = list(
            signatures[fr:to]
            for fr, to in zip(signature_offsets[:-1], signature_offsets[1:])
        )
        computed = set()
        for p, i_fr, i_to in zip(potentials, signature_offsets[:-1], signature_offsets[1:]):
            p_f_r = p.pre_compute_r_functions
            if p_f_r is not None:
                _signatures = signatures[i_fr:i_to]
                for fun_entry, s in zip(p_f_r, _signatures):
                    if s not in computed:
                        computed.add(s)
                        pre_compute_r_data[:, s:s+1] = pre_compute_r(distances, [fun_entry], p.parameters)
        return pre_compute_r_data, pre_compute_r_handles


def eval_potentials(encoded_potentials, kname, sparse_pair_distances, cartesian_row, cartesian_col, spec_encoded_row,
                    pre_compute_r=False, additional_inputs=None, cutoff=None, out=None, **kwargs):
    """
    Calculates potentials: values, gradients and more.

    Parameters
    ----------
    encoded_potentials : list, LocalPotential
        A list of potentials or a single potential.
    kname : str, None
        Function to evaluate: 'kernel', 'kernel_gradient' or whatever
        other kernel function set for all potentials in the list.
    sparse_pair_distances : csr_matrix
        Pair distances.
    cartesian_row : np.ndarray
        Cartesian coordinates of atoms inside the cell.
    cartesian_col : np.ndarray
        Cartesian coordinates of surrounding atoms.
    spec_encoded_row : np.ndarray
        Species encoded as integers inside the unit cell.
    pre_compute_r : tuple
        Optional pre-computed r-dependent quantities for this set of potentials.
    additional_inputs : dict
        A dictionary with additional inputs which may be required to compute potentials.
    cutoff : float
        Optional cutoff to check potentials against.
    out : np.ndarray
        The output buffer `[n_potentials, n_atoms]` for
        kname == "kernel" and `[n_potentials, n_atoms, n_atoms, 3]`
        for kname == "kernel_gradient".
    kwargs
        Other common arguments to kernel functions.

    Returns
    -------
    result : np.ndarray
        The result of the potential computation given the cell data.
    """
    if cutoff is not None:
        for p in encoded_potentials:
            if p.cutoff > cutoff:
                raise ValueError(f"Potential cutoff exceeds the computed neighbors: {p.cutoff} > {cutoff}\n"
                                 f"Potential: {p}")

    if pre_compute_r is False:
        pre_compute_r = _pre_compute_r_quantities(sparse_pair_distances.data, encoded_potentials)

    if additional_inputs is None:
        additional_inputs = {}

    kwargs_get = {k: kwargs[k] for k in ("resolving", "prefer_parallel") if k in kwargs}

    # Check all kernels produce the output of the same shape
    shapes = set(i.get_kernel_by_name(kname, **kwargs_get).out_shape for i in encoded_potentials)
    if len(shapes) != 1:
        raise ValueError(f"The shape of the output across kernels is not the same: {shapes}")
    if out is None:
        out = np.zeros((len(encoded_potentials),) + PotentialKernel.compute_shape(shapes.pop(), len(cartesian_row)), dtype=float)

    for i, potential in enumerate(encoded_potentials):
        if not isinstance(potential, LocalPotential):
            raise ValueError(f'Not a LocalPotential: {repr(potential)}')
        if not isinstance(potential.tag, np.ndarray) and potential.tag is not None:
            raise ValueError(f'Expected array or None for potential.tag, found: {repr(potential.tag)}')

        _kwargs = kwargs.copy()
        # Insert pre-computed data
        if pre_compute_r is not None:
            pre_compute_r_data, pre_compute_r_handles = pre_compute_r
            if potential.pre_compute_r_functions is not None:
                _kwargs["pre_compute_r"] = pre_compute_r_data
                _kwargs["pre_compute_r_handles"] = pre_compute_r_handles[i]

        if potential.additional_inputs:
            for k in potential.additional_inputs:
                if k not in additional_inputs:
                    raise ValueError(f"Missing additional input '{k}' for potential {potential}")
                _kwargs[k] = additional_inputs.get(k, None)
        potential.fun_csr(kname, sparse_pair_distances, cartesian_row, cartesian_col, species_row=spec_encoded_row,
                          species_mask=potential.tag, out=out[i, ...], **_kwargs)
    return out
