import numpy as np
import numericalunits as nu
import json
import torch
import warnings


def init_default_atomic_units():
    """Initializes atomic units in numericalunits."""
    nu.m = 1e10  # angstrom
    nu.s = 1e12  # pico-seconds
    nu.kg = 1. / 1.602176634e-23  # ??
    nu.C = 1. / 1.602176634e-19  # Coulomb in proton charges
    nu.K = 1
    nu.set_derived_units_and_constants()


class UnknownUnitsWarning(RuntimeWarning):
    pass


def check_units_known(logger=None, tolerance=1e-6):
    if abs(nu.angstrom - 1) > tolerance and abs(nu.eV - 1) > tolerance:
        if logger is not None:
            logger.warning(f"Non-standard units detected: nu.angstrom={nu.angstrom}, nu.eV={nu.eV}")
        warnings.warn("Non-standard units detected. Make sure that the units are not random and can be restored",
                      UnknownUnitsWarning)


def serialize_nu():
    """
    Retrieves the current state of `numericalunits` package and saves it into dict.

    Returns
    -------
    units : dict
        A dictionary with units.
    """
    return {k: v for k, v in nu.__dict__.items() if isinstance(v, float) and not k.startswith("_")}


def load_nu(data):
    """
    Loads previously saved `numericalunits` values.

    Parameters
    ----------
    data : dict
        A dictionary with the serialized data.
    """
    nu.__dict__.update(data)


class UnitsContext:
    def __init__(self, seed=None):
        self.seed = seed
        self.state = None

    def __enter__(self):
        self.state = serialize_nu()

    def __exit__(self, exc_type, exc_val, exc_tb):
        load_nu(self.state)
        self.state = None


new_units_context = UnitsContext


class UnitsDict(dict):
    def get_uv(self, key, default=1):
        """
        Retrieves a unit value assigned to the key.

        Parameters
        ----------
        key
            A valid dictionary key.
        default : float
            Default value.

        Returns
        -------
        result : float
            The unit value.
        """
        if key not in self:
            return default
        return nu.nu_eval(self[key])

    def apply(self, parameters):
        """
        Applies units to parameters.

        Parameters
        ----------
        parameters : dict
            A dict of potential parameters where units have to be applied.

        Returns
        -------
        result : dict
            A dict of potential parameters with units applied.
        """
        def _apply(_v, _u):
            if _v is None:
                return None
            elif isinstance(_v, (list, tuple)):
                return tuple(_apply(_i, _u) for _i in _v)
            else:
                return _v / _u
        return {k: _apply(v, self.get_uv(k)) for k, v in parameters.items()}

    def lift(self, parameters):
        """
        Lift units from parameters (inverse to `self.apply_units`).

        Parameters
        ----------
        parameters : dict
            A dict of potential parameters where units have to be lifted.

        Returns
        -------
        result : dict
            A dict of potential parameters with units lifted.
        """
        def _apply(_v, _u):
            if _v is None:
                return None
            elif isinstance(_v, (list, tuple)):
                return tuple(_apply(_i, _u) for _i in _v)
            else:
                return _v * _u
        return {k: _apply(v, self.get_uv(k)) for k, v in parameters.items()}

    def repr1(self, value, k, fmt="{:.3e}", spacer=" "):
        """
        Represents a single value with units.

        Parameters
        ----------
        value : float
            The value to represent.
        k : str
            The key to lookup units.
        fmt : str
            Floating-point format.
        spacer : str
            Spacer between value and units.

        Returns
        -------
        result : str
            The resulting string.
        """
        if k in self:
            value /= self.get_uv(k)
            value_s = fmt.format(value)
            return value_s + spacer + self[k]
        else:
            return fmt.format(value)

    def repr(self, parameters):
        """
        Represents parameters with the units specified.

        Parameters
        ----------
        parameters : dict
            Parameters to represent.

        Returns
        -------
        result : str
            The string representation.
        """
        parameters = self.apply(parameters)
        result = []

        for k in sorted(parameters):
            v = parameters[k]
            if k in self:
                result.append(f'{k}={v:.3e}*{self[k]}')
            else:
                result.append(f'{k}={v:.3e}')
        return f"dict({', '.join(result)})"


def array_from_json(d):
    data = dict(d)
    assert data.pop("_type") == "numpy"

    a = np.asarray(data.pop("data"))
    is_complex = data.pop("complex")
    units = data.pop("units")
    assert len(data) == 0
    if is_complex:
        a = a[..., 0] + 1j * a[..., 1]
    if units is not None:
        a *= nu.nu_eval(units)
    return a


def array_to_json(a, units=None):
    if units is not None:
        a = a / nu.nu_eval(units)
    is_complex = np.iscomplexobj(a)
    if is_complex:
        a = np.concatenate((a.real[..., None], a.imag[..., None]), axis=-1)
    return dict(
        _type="numpy",
        data=a.tolist(),
        complex=is_complex,
        units=units,
    )


class JSONEncoderWithArray(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, np.ndarray):
            return array_to_json(o)
        elif isinstance(o, torch.Tensor):
            result = array_to_json(o.detach().numpy())
            result["_type"] = "numpy:torch"
            return result
        else:
            return super(JSONEncoderWithArray, self).default(o)


def units_object_hook(d):
    if "_type" in d:
        t = d["_type"]
        if t == "numpy":
            return array_from_json(d)
        elif t == "numpy:torch":
            d["_type"] = "numpy"
            return torch.tensor(array_from_json(d))
        else:
            raise json.JSONDecodeError(f"Unknown type {t}")
    else:
        return d


# Shortcuts for dumping/loading jsons with arrays
def dump(*args, **kwargs):
    defaults = dict(cls=JSONEncoderWithArray)
    defaults.update(kwargs)
    return json.dump(*args, **defaults)


def dumps(*args, **kwargs):
    defaults = dict(cls=JSONEncoderWithArray)
    defaults.update(kwargs)
    return json.dumps(*args, **defaults)


def load(*args, **kwargs):
    defaults = dict(object_hook=units_object_hook)
    defaults.update(kwargs)
    return json.load(*args, **defaults)


def loads(*args, **kwargs):
    defaults = dict(object_hook=units_object_hook)
    defaults.update(kwargs)
    return json.loads(*args, **defaults)
