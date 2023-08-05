from . import ml_util
from .ml import Normalization, PotentialExtrapolationWarning
from .potentials import behler2_descriptor_family as behler2, behler4_descriptor_family as behler4, NestedLocalPotential,\
    lj_potential_family
from .units import UnknownUnitsWarning

from .test_ml import assert_datasets_equal, assert_allclose
from .test_samples import runner_input_sample, lammps_nnp_sample, amorphous_bise_json_sample

from unittest import TestCase
from pathlib import Path
from numericalunits import aBohr, angstrom, eV
from collections import Counter
import numpy as np
from numpy import testing
import torch
from tempfile import NamedTemporaryFile
import io
import warnings


class RunnerParserTest(TestCase):
    def test_file(self):
        d_parsed = ml_util.parse_runner_input(io.StringIO(runner_input_sample))

        # Descriptors excluded from the long list
        d_blacklisted = [
            # Both two-point descriptors eta=0.3 targeting Te
            behler2(eta=0.3 / aBohr ** 2, r_sphere=0., a=12.0 * aBohr, tag=f"Ge-Te"),
            behler2(eta=0.3 / aBohr ** 2, r_sphere=0., a=12.0 * aBohr, tag=f"Te-Te"),
            # A single one for eta=0.2, zeta=4, l=-1
            behler4(eta=0.2 / aBohr ** 2, l=-1., zeta=4.0, a=12 * aBohr, tag=f"Te-Te-Te"),
            # A block at eta=0.2, zeta=16, l=-1 (except Te-Te-Ge)
            behler4(eta=0.2 / aBohr ** 2, l=-1., zeta=16.0, a=12 * aBohr, tag=f"Ge-Ge-Ge"),
            behler4(eta=0.2 / aBohr ** 2, l=-1., zeta=16.0, a=12 * aBohr, tag=f"Ge-Te-Ge"),
            behler4(eta=0.2 / aBohr ** 2, l=-1., zeta=16.0, a=12 * aBohr, tag=f"Ge-Te-Te"),
            behler4(eta=0.2 / aBohr ** 2, l=-1., zeta=16.0, a=12 * aBohr, tag=f"Te-Ge-Ge"),
            behler4(eta=0.2 / aBohr ** 2, l=-1., zeta=16.0, a=12 * aBohr, tag=f"Te-Te-Te"),
            # Two "Te" descriptors eta=0.001, zeta=16, l=1
            behler4(eta=0.001 / aBohr ** 2, l=1., zeta=16.0, a=13 * aBohr, tag=f"Te-Ge-Ge"),
            behler4(eta=0.001 / aBohr ** 2, l=1., zeta=16.0, a=13 * aBohr, tag=f"Te-Te-Te"),
            # All eta=0.3, zeta=4, l=-1 descriptors in the last block
            behler4(eta=0.3 / aBohr ** 2, l=-1., zeta=4.0, a=12 * aBohr, tag=f"Ge-Ge-Ge"),
            behler4(eta=0.3 / aBohr ** 2, l=-1., zeta=4.0, a=12 * aBohr, tag=f"Te-Ge-Ge"),
        ]

        d_full = []
        # 2-point
        # =======
        # cutoff=12
        for eta in 0.3, 0.2, 0.07, 0.03, 0.01, 0.001:
            for a1 in "Ge", "Te":
                for a2 in "Ge", "Te":
                    d_full.append(behler2(eta=eta / aBohr ** 2, r_sphere=0., a=12.0 * aBohr, tag=f"{a1}-{a2}"))

        # cutoff=13 eta=0.001
        for a1 in "Ge", "Te":
            for a2 in "Ge", "Te":
                d_full.append(behler2(eta=0.001 / aBohr ** 2, r_sphere=0., a=13.0 * aBohr, tag=f"{a1}-{a2}"))

        # 3-point
        # =======
        # primary block, cutoff=12 eta!=0.3
        for eta in 0.2, 0.07, 0.03, 0.01, 0.001:
            for zeta in 1., 4., 2., 16.:
                for l in 1., -1.:
                    for a1 in "Ge", "Te":
                        for a23 in "Ge-Ge", "Te-Ge", "Te-Te":
                            d_full.append(behler4(eta=eta / aBohr ** 2, l=l, zeta=zeta, a=12 * aBohr, tag=f"{a1}-{a23}"))

        # cutoff=13 eta=0.001
        for zeta in 1., 4., 2., 16.:
            for l in 1., -1.:
                for a1 in "Ge", "Te":
                    for a23 in "Ge-Ge", "Te-Ge", "Te-Te":
                        d_full.append(behler4(eta=0.001 / aBohr ** 2, l=l, zeta=zeta, a=13 * aBohr, tag=f"{a1}-{a23}"))

        # eta=0.3 cutoff=12 *-Ge-Ge
        for zeta in 1., 4., 2.:
            for l in 1., -1.:
                for a1 in "Ge", "Te":
                    d_full.append(behler4(eta=0.3 / aBohr ** 2, l=l, zeta=zeta, a=12 * aBohr, tag=f"{a1}-Ge-Ge"))

        # remove blacklisted
        id_parsed = tuple(map(repr, (i.state_dict() for i in d_parsed)))
        id_blacklisted = tuple(map(repr, (i.state_dict() for i in d_blacklisted)))
        id_full = tuple(map(repr, (i.state_dict() for i in d_full)))

        self.assertEqual(set(id_full), set(id_parsed) | set(id_blacklisted))


class LAMMPSParserTest(TestCase):
    def test_file(self):
        potentials = ml_util.parse_lammps_input(io.StringIO(lammps_nnp_sample), simplify=False)

        self.assertEqual(len(potentials), 2)

        potential_sample = potentials[0]
        self.assertIsInstance(potential_sample, NestedLocalPotential)
        self.assertEqual(potential_sample.tag, "O")
        self.assertEqual(len(potential_sample.descriptors), 70)

        descriptor_sample = potential_sample.descriptors[4]
        self.assertIs(descriptor_sample.family, behler2)
        testing.assert_equal(descriptor_sample.parameters["eta"], 0.214264 / angstrom ** 2)
        testing.assert_equal(descriptor_sample.parameters["a"], 6 * angstrom)
        testing.assert_equal(descriptor_sample.parameters["r_sphere"], 0)
        testing.assert_equal(descriptor_sample.tag, "O-Si")

        descriptor_sample = potential_sample.descriptors[37]
        self.assertIs(descriptor_sample.family, behler4)
        testing.assert_equal(descriptor_sample.parameters["eta"], 0.000357 / angstrom ** 2)
        testing.assert_equal(descriptor_sample.parameters["a"], 6 * angstrom)
        testing.assert_equal(descriptor_sample.parameters["zeta"], 2)
        testing.assert_equal(descriptor_sample.parameters["l"], -1)
        testing.assert_equal(descriptor_sample.tag, "O-Si-O")

        potential_sample = potentials[1]
        self.assertIsInstance(potential_sample, NestedLocalPotential)
        self.assertEqual(potential_sample.tag, "Si")
        self.assertEqual(len(potential_sample.descriptors), 70)

        descriptor_sample = potential_sample.descriptors[10]
        self.assertIs(descriptor_sample.family, behler2)
        testing.assert_equal(descriptor_sample.parameters["eta"], 0.071421 / angstrom ** 2)
        testing.assert_equal(descriptor_sample.parameters["a"], 6 * angstrom)
        testing.assert_equal(descriptor_sample.parameters["r_sphere"], 0)
        testing.assert_equal(descriptor_sample.tag, "Si-O")

        descriptor_sample = potential_sample.descriptors[42]
        self.assertIs(descriptor_sample.family, behler4)
        testing.assert_equal(descriptor_sample.parameters["eta"], 0.089277 / angstrom ** 2)
        testing.assert_equal(descriptor_sample.parameters["a"], 6 * angstrom)
        testing.assert_equal(descriptor_sample.parameters["zeta"], 4)
        testing.assert_equal(descriptor_sample.parameters["l"], -1)
        testing.assert_equal(descriptor_sample.tag, "Si-Si-O")

        assert len(potentials) == 2
        for p, (w_ref, b_ref, _slice) in zip(potentials, [
            (
                [0.690412761572473, 0.33830388432626607, 0.08148770379598626, 5.344496403824106, 2.9638922703877952],
                [0.9544249661796863, 0.45117268520701787, 0.10237238535366817, 12.587994927233154, 6.748988405785591],
                slice(40, 45),
            ), (
                [0.7019746179904176, 0.530114971386907, 0.40562997229952297, 0.2792499782562679, 0.16943875861884494],
                [2.9579656875347435, 2.010843911436129, 1.3495712305969263, 0.7817472414666415, 0.3489072530470396],
                slice(0, 5),
            )
        ]):
            outer_sequential = p.parameters["nn"]
            norm_descriptors, inner_sequential, norm_energy = outer_sequential
            testing.assert_allclose(norm_energy.weight.item(), eV)
            testing.assert_equal(norm_energy.bias.item(), 0)

            w = norm_descriptors.weight.data.numpy()
            b = norm_descriptors.bias.data.numpy()

            w_ref = np.array(w_ref)
            b_ref = np.array(b_ref)
            w_ref = 1./w_ref
            b_ref = - b_ref * w_ref
            testing.assert_allclose(w[_slice, _slice], np.diag(w_ref))
            testing.assert_allclose(b[_slice], b_ref)

        nn_sample = potentials[0].parameters["nn"][1]
        self.assertEqual(len(nn_sample), 5)
        for i in range(0, 5, 2):
            layer = nn_sample[i]
            self.assertIsInstance(layer, torch.nn.Linear, msg=f"#{i:d}")
            self.assertIs(layer.weight.dtype, torch.float64, msg=f"#{i:d}")
            self.assertIs(layer.bias.dtype, torch.float64, msg=f"#{i:d}")
        for i in range(1, 5, 2):
            self.assertIsInstance(nn_sample[i], torch.nn.Sigmoid, msg=f"#{i:d}")

        linear_sample = nn_sample[2]
        testing.assert_equal(linear_sample.weight.detach().numpy()[2, 3:6], [0.5721273035047503, 0.10739355013492079,
                                                                             0.5264601494420822])
        testing.assert_equal(linear_sample.bias.detach().numpy()[4:6], [-0.194013890882, -0.691780401616])

        nn_sample = potentials[1].parameters["nn"][1]
        linear_sample = nn_sample[4]
        testing.assert_equal(linear_sample.weight.detach().numpy()[0, 5:7], [-0.1973799972276568, 0.4005192115707977])
        testing.assert_equal(linear_sample.bias.detach().item(), 0.132187475486)


class UtilTest(TestCase):
    def test_default_behler_choice(self):
        descriptors = ml_util.default_behler_descriptors({"a-a": 2, "a-b": 3, "b-b": 4}, 6, 12)
        self.assertEqual(len(descriptors), 2)

        self.assertEqual(Counter(i.tag for i in descriptors['a']), {"a-a": 6, "a-b": 6})
        self.assertEqual(Counter(i.tag for i in descriptors['b']), {"b-a": 6, "b-b": 6})

    def test_default_behler_choice_3(self):
        descriptors = ml_util.default_behler_descriptors_3(("a", "b"), 12)
        self.assertEqual(len(descriptors), 2)

        self.assertEqual(Counter(i.tag for i in descriptors['a']), {"a-a-a": 8, "a-a-b": 8, "a-b-b": 8})
        self.assertEqual(Counter(i.tag for i in descriptors['b']), {"b-a-a": 8, "b-a-b": 8, "b-b-b": 8})


class WorkflowTest(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.dataset_file = f = NamedTemporaryFile('w+')
        f.write(amorphous_bise_json_sample)
        f.seek(0)
        cls.dataset_file_path = Path(f.name)

    @classmethod
    def tearDownClass(cls) -> None:
        cls.dataset_file.close()

    def test_units_warning(self):
        with warnings.catch_warnings():
            warnings.filterwarnings('error')
            with self.assertRaises(UnknownUnitsWarning):
                ml_util.Workflow()

    def test_default(self):
        workflow = ml_util.FitWorkflow(units_are_known=True)
        workflow.prepare(
            fn_cells=[self.dataset_file_path.name],
            fn_cells_root=self.dataset_file_path.parent,
            cells_order=None,
            test_set=0.1,
        )
        workflow.run(n_epochs=1)

        self.assertEqual(len(workflow.cells), 10)
        self.assertEqual(len(workflow.descriptors), 2)
        for k, v in workflow.descriptors.items():
            self.assertEqual(len(v), 36, msg=k)
        testing.assert_allclose(workflow.cutoff, 12 * aBohr)
        self.assertEqual(len(workflow.cells_nw), 10)
        self.assertIsInstance(workflow.datasets, dict)
        self.assertIsInstance(workflow.normalization, Normalization)
        self.assertIsInstance(workflow.__diag_scale__, list)
        self.assertEqual(workflow.datasets["learn"].per_cell_dataset.n_samples, 9)
        self.assertEqual(workflow.datasets["test"].per_cell_dataset.n_samples, 1)
        self.assertEqual(len(workflow.datasets["learn"].per_point_datasets), 2)
        for i in workflow.datasets["learn"].per_point_datasets:
            self.assertEqual(i.n_samples, 9)
            self.assertIn(i.n_species, (26, 27, 38, 39))
            self.assertEqual(i.n_features, 36)
        self.assertEqual(len(workflow.nn), 2)
        for i in workflow.nn:
            self.assertIsInstance(i, torch.nn.Sequential)
        self.assertIsInstance(workflow.closure, ml_util.SimpleClosure)
        self.assertIsInstance(workflow.closure.last_loss.loss_value.detach().item(), float)
        self.assertIs(workflow.nn_potentials, None)

        parallel_workflow = ml_util.FitWorkflow(units_are_known=True)
        parallel_workflow.prepare(
            fn_cells=[self.dataset_file_path.name],
            fn_cells_root=self.dataset_file_path.parent,
            cells_order=None,
            parallel=True,
            test_set=0.1,
        )
        parallel_workflow.run(n_epochs=1)

        for k, v in workflow.datasets.items():
            assert_datasets_equal(parallel_workflow.datasets[k], v, err_msg=k)

        direct_test_workflow = ml_util.OneShotWorkflow(units_are_known=True)
        direct_test_workflow.prepare(
            fn_cells=[self.dataset_file_path.name],
            fn_cells_root=self.dataset_file_path.parent,
            cells_order=None,
            potentials=parallel_workflow.build_potentials(),
        )
        with warnings.catch_warnings():
            warnings.filterwarnings('error')
            with self.assertRaises(PotentialExtrapolationWarning):
                direct_test_workflow.run()

    def test_forces(self):
        workflow = ml_util.FitWorkflow(units_are_known=True)
        workflow.prepare(
            fn_cells=[self.dataset_file_path.name],
            fn_cells_root=self.dataset_file_path.parent,
            cells_subset=10,
            learn_cauldron_kwargs=dict(grad=True),
            closure_kwargs=dict(w_gradients=0.1),
            test_set=0.1,
        )
        workflow.run(n_epochs=1)
        workflow.build_potentials()

    def test_pca(self):
        workflow = ml_util.FitWorkflow(units_are_known=True)
        workflow.prepare(
            fn_cells=[self.dataset_file_path.name],
            fn_cells_root=self.dataset_file_path.parent,
            cells_subset=10,
            learn_cauldron_kwargs=dict(grad=True),
            closure_kwargs=dict(w_gradients=0.1),
            normalization_kwargs=dict(pca_features=5),
            test_set=0.1,
        )
        workflow.run(n_epochs=1)
        workflow.build_potentials()

    def test_filter(self):
        workflow = ml_util.FitWorkflow(units_are_known=True)
        workflow.prepare(
            fn_cells=[self.dataset_file_path.name],
            fn_cells_root=self.dataset_file_path.parent,
            cells_subset=10,
            filter_descriptors=True,
            filter_descriptors_kwargs=dict(min_spread=1),
            test_set=0.1,
        )
        workflow.run(n_epochs=1)
        workflow.build_potentials()
        self.assertEqual(len(workflow.descriptors['bi']), 26)
        self.assertEqual(len(workflow.descriptors['se']), 25)
        self.assertEqual(len(workflow.datasets), 2)
        for k, v in workflow.datasets.items():
            self.assertEqual(v.per_point_datasets[0].n_features, 26)
            self.assertEqual(v.per_point_datasets[1].n_features, 25)

    def test_charges(self):
        workflow = ml_util.ChargeFitWorkflow(units_are_known=True)
        workflow.prepare(
            fn_cells=[self.dataset_file_path.name],
            fn_cells_root=self.dataset_file_path.parent,
            cells_subset=10,
            test_set=0.1,
        )
        dst = NamedTemporaryFile()
        workflow.run(n_epochs=1, save=True, save_fn=dst.name)
        workflow.build_potentials()

        workflow_r = ml_util.ChargeFitWorkflow(units_are_known=True)
        workflow_r.prepare(
            fn_cells=[self.dataset_file_path.name],
            fn_cells_root=self.dataset_file_path.parent,
            cells_subset=10,
            test_set=0.1,
            load=dst.name,
        )
        workflow_r.run(n_epochs=1)

    def test_resume(self):
        workflow = ml_util.FitWorkflow(units_are_known=True)
        workflow.prepare(
            fn_cells=[self.dataset_file_path.name],
            fn_cells_root=self.dataset_file_path.parent,
            cells_order=None,
            cells_subset=100,
            test_set=0.1,
        )
        dst = NamedTemporaryFile()
        workflow.run(n_epochs=1, save=True, save_fn=dst.name)

        workflow_r = ml_util.FitWorkflow(units_are_known=True)
        workflow_r.prepare(
            fn_cells=[self.dataset_file_path.name],
            fn_cells_root=self.dataset_file_path.parent,
            cells_order=None,
            cells_subset=100,
            test_set=0.1,
            load=dst.name,
        )

        old_losses = workflow.losses
        new_losses = workflow_r.losses
        for k in set(old_losses) | set(new_losses):
            l1, l2 = old_losses[k], new_losses[k]
            assert_allclose(l1.reference, l2.reference, err_msg=k)
            assert_allclose(l1.prediction, l2.prediction, err_msg=k)
        workflow_r.run(n_epochs=1)

    def test_relax(self):
        workflow = ml_util.SDWorkflow(units_are_known=True)
        prepare_kwargs = dict(
            fn_cells=[self.dataset_file_path.name],
            fn_cells_root=self.dataset_file_path.parent,
            potentials=[
                lj_potential_family(epsilon=1 * eV, sigma=2.5 * angstrom, a=5, tag="bi-bi"),
                lj_potential_family(epsilon=1 * eV, sigma=2.5 * angstrom, a=5, tag="bi-se"),
                lj_potential_family(epsilon=1 * eV, sigma=3 * angstrom, a=5, tag="se-se"),
            ],
            cells_order=None,
            cells_subset=4,
        )
        workflow.prepare(**prepare_kwargs)
        m_kwargs = dict(options=dict(maxiter=2), inplace=False)
        workflow.run(**m_kwargs)
        serial_result = workflow.cells_result

        workflow.prepare(**prepare_kwargs)
        workflow.run(**m_kwargs, parallel=True)
        for x, (i, j) in enumerate(zip(serial_result, workflow.cells_result)):
            testing.assert_equal(i.vectors, j.vectors, err_msg=str(x))
            testing.assert_allclose(i.coordinates, j.coordinates, err_msg=str(x))
            testing.assert_equal(i.values, j.values, err_msg=str(x))
