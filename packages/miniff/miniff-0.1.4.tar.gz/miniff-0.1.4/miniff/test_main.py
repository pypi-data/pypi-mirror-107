from unittest import TestCase
from tempfile import NamedTemporaryFile
import sys
import os
from pathlib import Path
import warnings

from .test_samples import yaml_main_sample, amorphous_bise_json_sample
from .ml_util import load_potentials
from .ml import ml_potential_family, PotentialExtrapolationWarning
from . import __version__


class patch_argv:
    def __init__(self, new_argv):
        self.prev_argv = None
        self.new_argv = list(new_argv)

    def __enter__(self):
        self.prev_argv = sys.argv
        sys.argv = self.new_argv

    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.argv = self.prev_argv


class MainTest(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.cells_file = f = NamedTemporaryFile('w+')
        f.write(amorphous_bise_json_sample)
        f.flush()
        cls.cells_path = Path(f.name)

        cls.potential_file = f = NamedTemporaryFile()
        cls.potential_path = Path(f.name)

        cls.yaml_file = f = NamedTemporaryFile('w+')
        f.write(yaml_main_sample.format(
            fn_cells=cls.cells_path.name,
            fn_cells_root=cls.cells_path.parent,
            potential=cls.potential_path,
        ))
        f.flush()

    def test_main(self):
        """Emulates ``python -m miniff``"""
        with patch_argv([os.path.realpath("__main__.py"), self.yaml_file.name]):
            with warnings.catch_warnings():
                warnings.filterwarnings(action="ignore", category=PotentialExtrapolationWarning)
                from . import __main__
        potentials = load_potentials(self.potential_path)
        assert len(potentials) == 2
        for i in potentials:
            self.assertIs(i.family, ml_potential_family)

    def test_version(self):
        self.assertIsInstance(__version__, str)
