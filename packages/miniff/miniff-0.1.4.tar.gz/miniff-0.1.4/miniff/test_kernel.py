from . import kernel, potentials, util, units

import numpy as np
from numpy import testing
from scipy.integrate import quad

import numericalunits as nu
from unittest import TestCase
from pathlib import Path
from functools import partial
from io import StringIO


def f_dummy(r, row, col, a):
    return a * r ** 2


def g_dummy(r, row, col, a):
    return 2 * a * r


class TestCell(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.c = kernel.Cell(
            vectors=np.array([[1, 0, 0], [2, 3, 0], [0, 0, 4]]),
            coordinates=[(.5, .5, 0), (.5, .5, .5)],
            values=["a", "b"],
            meta=dict(
                scalar=3.4,
                str="abc",
                array=np.array((9, 8, 7)),
                list=["1", 1],
                array_w_u=np.array([3, 6, 8]),
            )
        )

    def __assert_cells_same__(self, c, r):
        testing.assert_allclose(c.vectors, r.vectors)
        testing.assert_equal(c.coordinates, r.coordinates)
        testing.assert_equal(c.values, r.values)
        cm = dict(c.meta)
        rm = dict(r.meta)
        for k in "scalar", "str", "list", "array", "array_w_u":
            testing.assert_equal(cm.pop(k), rm.pop(k), err_msg=k)
        self.assertEqual(len(cm), 0)
        self.assertEqual(len(rm), 0)

    def test_state(self):
        r = kernel.Cell.from_state_dict(self.c.state_dict())
        self.__assert_cells_same__(self.c, r)

    def test_save_load(self):
        buffer = StringIO()
        kernel.Cell.save(self.c, buffer)
        buffer.seek(0)
        r = kernel.Cell.load(buffer)
        self.__assert_cells_same__(self.c, r)


class TestNW(TestCase):
    @classmethod
    def setUpClass(cls):
        cell = kernel.Cell([
            (3. ** .5 / 2, .5, 0),
            (3. ** .5 / 2, -.5, 0),
            (0, 0, 5),
        ], [(1. / 3, 1. / 3, .5), (2. / 3, 2. / 3, .5)], ("a", "b"))
        cls.bond_length = a = 1. / 3. ** .5
        cls.nw = kernel.NeighborWrapper(cell, cutoff=cls.bond_length * 1.4)

        cls.delta = 1e-1
        cell_distorted = cell.copy()
        cell_distorted.coordinates[0] += [cls.delta, cls.delta, 0]
        cls.nw_distorted = kernel.NeighborWrapper(cell_distorted, cutoff=cls.bond_length * 1.5)

        cls.bond_length_small = cls.bond_length - cls.delta * 3. ** .5
        cls.bond_length_large = ((.5 / 3. ** .5 + cls.delta * 3. ** .5) ** 2 + .25) ** .5

        cls.potentials_s = [
            potentials.on_site_potential_family(v0=3.14, tag="a"),
            potentials.on_site_potential_family(v0=1.59, tag="b"),
        ]
        cls.potentials_p = [
            potentials.sw2_potential_family(p=4, q=0, a=1.3, epsilon=3, sigma=a / 2. ** (1. / 6), tag="a-a"),
            potentials.sw2_potential_family(p=4, q=0, a=1.3, epsilon=7, sigma=a / 2. ** (1. / 6), tag="a-b"),
            potentials.sw2_potential_family(p=4, q=0, a=1.3, epsilon=7, sigma=a / 2. ** (1. / 6), tag="b-a"),
            potentials.sw2_potential_family(p=4, q=0, a=1.3, epsilon=11, sigma=a / 2. ** (1. / 6), tag="b-b"),
        ]
        cls.potentials_sp = cls.potentials_s + cls.potentials_p

        cls.potentials_dummy_p = [
            potentials.general_pair_potential_family(a=a * 1.3, f=partial(f_dummy, a=3), df_dr=partial(g_dummy, a=3), tag="a-a"),
            potentials.general_pair_potential_family(a=a * 1.3, f=partial(f_dummy, a=7), df_dr=partial(g_dummy, a=7), tag="a-b"),
            potentials.general_pair_potential_family(a=a * 1.3, f=partial(f_dummy, a=7), df_dr=partial(g_dummy, a=7), tag="b-a"),
            potentials.general_pair_potential_family(a=a * 1.3, f=partial(f_dummy, a=11), df_dr=partial(g_dummy, a=11), tag="b-b"),
        ]
        cls.potentials_dummy_sp = cls.potentials_s + cls.potentials_dummy_p

        cls.pyscf_ewald_reference = -2.671202914430402

    def test_nw_fields_simple(self):
        a = self.bond_length
        nw = self.nw

        self.assertIsNotNone(nw.cell)
        testing.assert_equal(self.nw.cutoff, a * 1.4)
        testing.assert_equal(self.nw.species, ["a", "b"])
        testing.assert_equal(self.nw.spec_encoded_row, [0, 1])
        self.assertEqual(self.nw.spec_encoded_row.dtype, np.int32)

    def test_nw_fields_pairs(self):
        a = self.bond_length
        v1, v2, v3 = self.nw.cell.vectors
        p1 = np.array([a, 0., 0.]) + v3 / 2
        p2 = np.array([2 * a, 0., 0.]) + v3 / 2
        pairs_self_ref = np.array([p1, p1, p1, p2, p2, p2])
        pairs_other_ref = np.array([p2 - v2, p2 - v1, p2, p1, p1 + v1, p1 + v2])

        _s, _o = self.nw.sparse_pair_distances.nonzero()
        order = np.lexsort((_o, _s))
        _s = _s[order]
        _o = _o[order]
        pairs_self = self.nw.cartesian_row[_s, :]
        pairs_other = self.nw.cartesian_col[_o, :]

        testing.assert_allclose(pairs_self, pairs_self_ref, atol=1e-12)
        testing.assert_allclose(pairs_other, pairs_other_ref, atol=1e-12)

        values = list(self.nw.sparse_pair_distances[i] for i in zip(_s, _o))
        testing.assert_allclose(values, [a] * 6)

    def test_nw_fields_pairs_distorted(self):
        _s, _o = self.nw_distorted.sparse_pair_distances.nonzero()
        order = np.lexsort((_o, _s))
        _s = _s[order]
        _o = _o[order]

        values = list(self.nw_distorted.sparse_pair_distances[i] for i in zip(_s, _o))
        testing.assert_allclose(values, 2 * [self.bond_length_large] + 2 * [self.bond_length_small] + 2 * [self.bond_length_large])

    def test_eval_s(self):
        out_ref = np.array(((self.potentials_s[0].parameters["v0"], 0), (0, self.potentials_s[1].parameters["v0"])))
        testing.assert_allclose(self.nw.eval(self.potentials_s, "kernel"), out_ref)
        out = np.zeros((2, 2), dtype=float)
        out_ = self.nw.eval(self.potentials_s, "kernel", out=out)
        self.assertIs(out, out_)
        testing.assert_allclose(out, out_ref)

    def test_energy_s(self):
        testing.assert_allclose(self.nw.total(self.potentials_s), self.potentials_s[0].parameters["v0"] + self.potentials_s[1].parameters["v0"])

    def test_energy_sp(self):
        testing.assert_allclose(
            self.nw.total(self.potentials_p), - self.potentials_p[1].epsilon * 6, atol=1e-5)
        testing.assert_allclose(
            self.nw.total(self.potentials_sp),
            - self.potentials_p[1].epsilon * 6 + self.potentials_s[0].parameters["v0"] + self.potentials_s[1].parameters["v0"], atol=1e-5)

    def test_gradient_sp(self):
        testing.assert_allclose(self.nw.grad(self.potentials_sp), 0, atol=1e-10)

    def test_dummy_energy_sp(self):
        a = self.bond_length
        testing.assert_allclose(self.nw.total(self.potentials_dummy_sp),
                                self.potentials_dummy_p[1].parameters["f"].keywords["a"] * 6 * a ** 2 +  # double-counting
                                self.potentials_s[0].parameters["v0"] +
                                self.potentials_s[1].parameters["v0"])

    def test_dummy_gradient_sp(self):
        testing.assert_allclose(self.nw.grad(self.potentials_dummy_sp), 0, atol=1e-12)

    def test_dummy_energy_sp_distorted(self):
        testing.assert_allclose(self.nw_distorted.total(self.potentials_dummy_sp),
                                self.potentials_dummy_p[1].parameters["f"].keywords["a"] * 2 * (self.bond_length_small ** 2 + 2 * self.bond_length_large ** 2) +
                                self.potentials_s[0].parameters["v0"] +
                                self.potentials_s[1].parameters["v0"])

    def test_dummy_gradient_sp_distorted(self):
        def f(coords):
            cell = self.nw_distorted.cell.copy()
            cell.coordinates = cell.transform_from_cartesian(coords)
            nw = kernel.NeighborWrapper(cell)
            nw.shift_vectors = self.nw_distorted.shift_vectors
            nw.compute_distances(self.nw_distorted.cutoff)
            assert nw.sparse_pair_distances.nnz == 6
            return nw.total(self.potentials_dummy_sp)
        testing.assert_allclose(self.nw_distorted.grad(self.potentials_dummy_sp), util.num_grad(f, self.nw_distorted.cell.cartesian()), atol=1e-10)

    def test_relax(self):
        relaxed = self.nw_distorted.relax(self.potentials_p)
        d = relaxed.distances()
        testing.assert_allclose(d, [[0, self.bond_length], [self.bond_length, 0]])
        testing.assert_allclose(relaxed.meta["forces"], 0, atol=1e-5)
        testing.assert_allclose(relaxed.meta["total-energy"], - self.potentials_p[1].epsilon * 6, atol=1e-5)

    def test_relax2(self):

        def f(r, row, col, dmin, dmax):
            return (dmin - r) ** 2 * (r < dmin) + (dmax - r) ** 2 * (r > dmax)

        def g(r, row, col, dmin, dmax):
            return 2 * (r - dmin) * (r < dmin) + 2 * (r - dmax) * (r > dmax)

        box_size = 1.442
        dummy_potential = potentials.general_pair_potential_family(
            a=2 * box_size,
            f=partial(f, dmin=0.8, dmax=1.2),
            df_dr=partial(g, dmin=0.8, dmax=1.2),
        )
        cell = kernel.Cell(np.eye(3) * box_size, np.array([
            [0.55301837, 1.1418651,  0.76279847],
            [0.81926202, 1.33494135, 0.10245172],
            [0.1256622,  0.02915998, 1.20084561]]) / box_size, ("x",) * 3)
        nw = kernel.NeighborWrapper(cell, cutoff=2 * box_size, pbc=False)
        relaxed = nw.relax(dummy_potential.copy(tag="x-x"), rtn_history=True)
        testing.assert_allclose(relaxed[-1].meta["total-energy"], 0)
        testing.assert_equal(np.logical_or(0.8 > relaxed[-1].distances(), 1.2 < relaxed[-1].distances()).sum(), 3)

    def test_rdf(self):
        sigma = 0.1
        nat = quad(lambda x: self.nw.rdf(x, 0.1)["a-b"] * 4 * np.pi * x ** 2, self.bond_length - 3 * sigma, self.bond_length + 3 * sigma)
        testing.assert_allclose(nat[0], 3, atol=1e-2)

    def test_batch_rdf(self):
        r = np.linspace(0.1, 1)
        rdf = self.nw.rdf(r, 0.1)
        rdfb = kernel.batch_rdf([self.nw], r, 0.1)
        testing.assert_equal(rdf, rdfb)


class CoulombTest(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cell = kernel.Cell(
            [[0.5, 0.5, 0], [0.5, 0.0, 0.5], [0.0, 0.5, 0.5]],
            [[0, 0, 0], [0.52, 0.52, 0.48]],
            ("na", "cl"),
            meta={"charges": [11, 17]},
        )
        cls.nw = kernel.NeighborWrapper(cell, cutoff=3, reciprocal_cutoff=30)
        cls.eta, cls.r_cut, cls.k_cut = 3, 3, 30
        cls.reference_e = -1143.0469293384504  # pyscf

        cls.potentials = potentials.ewald_total_potential_family(eta=cls.eta, a=cls.r_cut, scale=1)

    def __test_pyscf__(self):  # This is for the reference
        from .util import pyscf_coulomb_ewald
        testing.assert_allclose(
            pyscf_coulomb_ewald(self.nw.cell, eta=self.eta, r_cut=self.r_cut, k_cut=self.k_cut),
            self.reference_e,
        )

    def test_value(self):
        testing.assert_allclose(
            self.nw.total(self.potentials),
            self.reference_e,
        )


class IntegrationTests(TestCase):
    """Various weird bugs are collected here."""
    def test_supercell_match(self):
        """
        I figured out that total energy of 2D and 3D supercells do not match
        a multiple of the total energy of a unit cell.
        """
        c1 = kernel.Cell(np.diag([1, 1, 10]), [[.5, .5, .5]], ['x'])
        c2 = c1.repeated(2, 2, 1)
        lj = potentials.lj_potential_family(epsilon=1, sigma=1, a=1.9)

        c1w = kernel.NeighborWrapper(c1, cutoff=lj.cutoff + 0.05)

        c2w = kernel.NeighborWrapper(c2, cutoff=lj.cutoff + 0.05)

        testing.assert_equal(
            len(c1w.sparse_pair_distances.nonzero()[0]) * 4,
            len(c2w.sparse_pair_distances.nonzero()[0])
        )
        testing.assert_allclose(c1w.total(lj.copy(tag="x-x")) * 4, c2w.total(lj.copy(tag="x-x")))

    def test_relax(self):
        """Relaxation is too slow: this test is for profiling and benchmarking the issue."""
        potential_pre = potentials.harmonic_repulsion_potential_family(a=1, epsilon=1)
        potential = potentials.lj_potential_family(epsilon=1, sigma=1, a=20)
        coords = [
            [
                [0.5488135039273248, 0.7151893663724195, 0.6027633760716439],
                [0.5448831829968969, 0.4236547993389047, 0.6458941130666561],
                [0.4375872112626925, 0.8917730007820798, 0.9636627605010293]
            ], [
                [0.3834415188257777, 0.7917250380826646, 0.5288949197529045],
                [0.5680445610939323, 0.925596638292661, 0.07103605819788694],
                [0.08712929970154071, 0.02021839744032572, 0.832619845547938]
            ], [
                [0.7781567509498505, 0.8700121482468192, 0.978618342232764],
                [0.7991585642167236, 0.46147936225293185, 0.7805291762864555],
                [0.11827442586893322, 0.6399210213275238, 0.1433532874090464]
            ], [
                [0.9446689170495839, 0.5218483217500717, 0.4146619399905236],
                [0.26455561210462697, 0.7742336894342167, 0.45615033221654855],
                [0.5684339488686485, 0.018789800436355142, 0.6176354970758771]
            ], [
                [0.6120957227224214, 0.6169339968747569, 0.9437480785146242],
                [0.6818202991034834, 0.359507900573786, 0.43703195379934145],
                [0.6976311959272649, 0.06022547162926983, 0.6667667154456677]
            ], [
                [0.6706378696181594, 0.2103825610738409, 0.1289262976548533],
                [0.31542835092418386, 0.3637107709426226, 0.5701967704178796],
                [0.43860151346232035, 0.9883738380592262, 0.10204481074802807]
            ], [
                [0.2088767560948347, 0.16130951788499626, 0.6531083254653984],
                [0.2532916025397821, 0.4663107728563063, 0.24442559200160274],
                [0.15896958364551972, 0.11037514116430513, 0.6563295894652734]
            ], [
                [0.1381829513486138, 0.1965823616800535, 0.3687251706609641],
                [0.8209932298479351, 0.09710127579306127, 0.8379449074988039],
                [0.09609840789396307, 0.9764594650133958, 0.4686512016477016]
            ], [
                [0.9767610881903371, 0.604845519745046, 0.7392635793983017],
                [0.039187792254320675, 0.2828069625764096, 0.1201965612131689],
                [0.29614019752214493, 0.11872771895424405, 0.317983179393976]
            ], [
                [0.41426299451466997, 0.06414749634878436, 0.6924721193700198],
                [0.5666014542065752, 0.2653894909394454, 0.5232480534666997],
                [0.09394051075844168, 0.5759464955561793, 0.9292961975762141]
            ]
        ]
        cells = list(kernel.Cell(np.diag([9, 10, 10]), c, ['x', 'x', 'x']) for c in coords)
        for i_c, c in enumerate(cells):
            nw = kernel.NeighborWrapper(c, cutoff=potential.cutoff, pbc=False)
            # Pre-relax with harmonic repulsion
            cell = nw.relax(potential_pre.copy(tag="x-x"), method="CG")
            nw.set_cell(cell)
            nw.compute_distances(potential.cutoff)
            # Actual relax
            cell_r = nw.relax(potential.copy(tag="x-x"), method="CG")
            testing.assert_allclose(cell_r.meta["forces"], 0, atol=1e-5, err_msg=f"#{i_c}")

    def test_relax_lj(self):
        """Unphysical relaxation with LJ potential"""
        potential = potentials.lj_potential_family(epsilon=1, sigma=1, a=2.9)
        c = kernel.Cell(
            np.eye(3),
            [[0.65098689, 0.99427277, 0.22621891], [0.58800034, -0.22191917, 0.5648664], [0.29229667, 1.25826357, 1.42123495]],
            ("x",) * 3,
        )
        nw = kernel.NeighborWrapper(c, normalize=False, cutoff=potential.cutoff, pbc=False)
        relaxed = nw.relax(potential.copy(tag="x-x"), normalize=False)
        testing.assert_allclose(relaxed.distances()[(0, 1, 2), (1, 2, 0)], 2.**(1./6))

    def test_forces_bise(self):
        """Unphysical interatomic distances after relaxation with HarmonicRepulsion. Tests units integration as well."""
        with units.new_units_context():
            units.init_default_atomic_units()
            c = kernel.Cell(
                np.array([
                    [18.56360405994572, -0.03675281063824605, -0.17909313429020757],
                    [-0.03675281063824605, 18.15389548261195, -0.058158866059653695],
                    [-0.17909313429020757, -0.058158866059653695, 18.544192830120462]
                ]) * nu.angstrom,
                [
                    [0.7151893663724194, 0.6027633760716439, 0.5448831829968968],
                    [0.42365479933890465, 0.6458941130666561, 0.4375872112626924],
                    [0.8917730007820798, 0.9636627605010293, 0.38344151882577765],
                    [0.7917250380826646, 0.5288949197529045, 0.5680445610939322],
                    [0.925596638292661, 0.07103605819788694, 0.0871292997015407],
                    [0.02021839744032572, 0.832619845547938, 0.7781567509498504],
                    [0.8700121482468192, 0.9786183422327639, 0.7991585642167235],
                    [0.4614793622529318, 0.7805291762864556, 0.11827442586893322],
                    [0.6399210213275238, 0.14335328740904638, 0.9446689170495837],
                    [0.5218483217500717, 0.4146619399905236, 0.2645556121046269],
                    [0.7742336894342167, 0.45615033221654855, 0.5684339488686484],
                    [0.018789800436355142, 0.6176354970758772, 0.6120957227224213],
                    [0.6169339968747568, 0.9437480785146243, 0.6818202991034834],
                    [0.35950790057378595, 0.43703195379934145, 0.6976311959272647],
                    [0.06022547162926982, 0.6667667154456677, 0.6706378696181593],
                    [0.21038256107384085, 0.12892629765485333, 0.31542835092418386],
                    [0.3637107709426226, 0.5701967704178796, 0.43860151346232035],
                    [0.9883738380592261, 0.10204481074802808, 0.20887675609483466],
                    [0.16130951788499623, 0.6531083254653984, 0.25329160253978206],
                    [0.4663107728563062, 0.24442559200160277, 0.1589695836455197],
                    [0.11037514116430512, 0.6563295894652734, 0.13818295134861378],
                    [0.1965823616800535, 0.3687251706609641, 0.820993229847935],
                    [0.09710127579306126, 0.8379449074988039, 0.09609840789396305],
                    [0.9764594650133959, 0.4686512016477015, 0.976761088190337],
                    [0.604845519745046, 0.7392635793983017, 0.03918779225432067],
                    [0.2828069625764096, 0.1201965612131689, 0.2961401975221449],
                    [0.11872771895424407, 0.317983179393976, 0.4142629945146699],
                    [0.06414749634878436, 0.6924721193700198, 0.5666014542065752],
                    [0.2653894909394454, 0.5232480534666997, 0.09394051075844166],
                    [0.5759464955561793, 0.9292961975762142, 0.3185689524513236],
                    [0.6674103799636816, 0.13179786240439217, 0.7163272041185655],
                    [0.28940609294720115, 0.18319136200711686, 0.586512934810083],
                    [0.02010754618749355, 0.8289400292173631, 0.004695476192547065],
                    [0.6778165367962301, 0.27000797319216485, 0.7351940221225948],
                    [0.9621885451174382, 0.24875314351995803, 0.5761573344178368],
                    [0.592041931271839, 0.5722519057908734, 0.22308163264061828],
                    [0.9527490115169849, 0.4471253786176273, 0.8464086724711277],
                    [0.6994792753175043, 0.29743695085513366, 0.8137978197024771],
                    [0.39650574084698464, 0.8811031971111616, 0.5812728726358586],
                    [0.8817353618548527, 0.692531590077766, 0.7252542798196404],
                    [0.5013243819267023, 0.956083634723224, 0.6439901992296373],
                    [0.4238550485581797, 0.6063932141279244, 0.019193198309333522],
                    [0.30157481667454933, 0.660173537492685, 0.29007760721044407],
                    [0.6180154289988414, 0.4287687009457662, 0.1354740642224502],
                    [0.29828232595603077, 0.5699649107012649, 0.5908727612481731],
                    [0.5743252488495787, 0.6532008198571336, 0.6521032700016888],
                    [0.43141843543397396, 0.896546595851063, 0.3675618700478965],
                    [0.43586492526562676, 0.8919233550156721, 0.8061939890460856],
                    [0.7038885835403663, 0.10022688731230112, 0.9194826137446735],
                    [0.7142412995491114, 0.9988470065678666, 0.14944830465799375],
                    [0.8681260573682141, 0.16249293467637482, 0.6155595642838441],
                    [0.12381998284944151, 0.8480082293222343, 0.8073189587250106],
                    [0.5691007386145931, 0.40718329722599966, 0.06916699545513803],
                    [0.6974287731445636, 0.45354268267806885, 0.7220555994703478],
                    [0.8663823259286293, 0.9755215050028858, 0.8558033423926109],
                    [0.01171408418500197, 0.35997806447836395, 0.7299905624240579],
                    [0.17162967726144052, 0.5210366062041293, 0.05433798833925362],
                    [0.19999652489640005, 0.018521794460613975, 0.7936977033574205],
                    [0.2239246880603801, 0.34535168069690264, 0.9280812934655908],
                    [0.7044144019235327, 0.031838929531307854, 0.16469415649791275],
                    [0.6214784014997635, 0.5772285886041675, 0.2378928213745086],
                    [0.9342139979247936, 0.6139659559658959, 0.5356328030249582],
                    [0.5899099763545711, 0.7301220295167697, 0.3119449954796018],
                    [0.39822106221609194, 0.20984374897512217, 0.18619300588033616],
                    [0.9443723899839335, 0.7395507950492876, 0.4904588086175671],
                    [0.22741462797332324, 0.25435648177039294, 0.05802916032387561],
                    [0.4344166255581208, 0.3117958819941026, 0.6963434888154594],
                    [0.3777518392924809, 0.17960367755963483, 0.024678728391331225],
                    [0.06724963146324857, 0.6793927734985673, 0.45369684455604525],
                    [0.5365792111087222, 0.8966712930403421, 0.9903389473967043],
                    [0.2168969843984739, 0.6630782031001008, 0.2633223767371506],
                    [0.02065099946572868, 0.7583786538361413, 0.3200171508224678],
                    [0.38346389417189797, 0.5883171135536057, 0.8310484552361903],
                    [0.6289818435911486, 0.8726506554473953, 0.2735420348156357],
                    [0.7980468339125636, 0.1856359443059522, 0.9527916569719446],
                    [0.6874882763878153, 0.21550767711355845, 0.947370590488924],
                    [0.7308558067701578, 0.25394164259502583, 0.21331197736748195],
                    [0.5182007139306634, 0.025662718054531575, 0.20747007544110938],
                    [0.42468546875150626, 0.37416998033422555, 0.4635754243648106],
                    [0.2776287062947319, 0.5867843464581689, 0.8638556059232313],
                    [0.11753185596203308, 0.5173791071541141, 0.1320681063451533],
                    [0.7168596811925937, 0.39605970280729375, 0.565421311858509],
                    [0.18327983621407862, 0.14484775934337724, 0.48805628064895457],
                    [0.35561273784995556, 0.940431945252813, 0.7653252538069651],
                    [0.7486636198505473, 0.9037197397459337, 0.08342243544201854],
                    [0.5521924699224064, 0.5844760689557689, 0.9619363785472287],
                    [0.2921475267925488, 0.24082877991544685, 0.1002939422654978],
                    [0.016429629591474204, 0.9295293167921904, 0.6699165465909099],
                    [0.7851529120231378, 0.2817301057539491, 0.5864101661863266],
                    [0.06395526612098112, 0.4856275959346229, 0.9774951397444466],
                    [0.8765052453165907, 0.33815895183684563, 0.9615701545414983],
                    [0.23170162647120449, 0.9493188224156814, 0.9413777047064986],
                    [0.7992025873523917, 0.6304479368667912, 0.8742879666249468],
                    [0.2930202845077967, 0.8489435553129182, 0.6178766919175237],
                    [0.01323685775889949, 0.34723351793221957, 0.148140860948165],
                    [0.9818293898182531, 0.47837030703998806, 0.49739136549866264],
                    [0.6394725163987236, 0.3685846061296175, 0.13690027168559893],
                    [0.8221177331942455, 0.189847911902758, 0.5113189825464559],
                    [0.22431702897473926, 0.09784448449403405, 0.8621915174216832],
                    [0.9729194890231304, 0.9608346580630003, 0.9065554992211787],
                    [0.7740473326986388, 0.3331451520286419, 0.08110138998799675],
                    [0.4072411714138073, 0.2322341421709427, 0.13248763475798297],
                    [0.05342718178682527, 0.7255943642105788, 0.011427458625031027],
                    [0.7705807485027762, 0.14694664540037508, 0.07952208258675574],
                    [0.08960303423860538, 0.6720478073539145, 0.24536720985284474],
                    [0.42053946668009845, 0.5573687913239169, 0.8605511738287936],
                    [0.7270442627113282, 0.27032790523871464, 0.13148279929112758],
                    [0.055374320421197935, 0.30159863448094254, 0.26211814923967824],
                    [0.4561405668004796, 0.6832813355476806, 0.6956254456388572],
                    [0.2835188465821666, 0.3799269559001205, 0.181150961736903],
                    [0.7885455123065186, 0.056848076433240295, 0.6969972417249872],
                    [0.7786953959411034, 0.7774075618487531, 0.2594225643453549],
                    [0.3738131379325614, 0.587599635196389, 0.27282190242446697],
                    [0.3708527992178887, 0.19705428018563964, 0.45985588375600733],
                    [0.04461230125411408, 0.799795884570618, 0.07695644698663273],
                    [0.5188351488315259, 0.3068100995451961, 0.5775429488313754],
                    [0.9594333408334254, 0.6455702444560039, 0.03536243575549091],
                    [0.43040243950806123, 0.5100168523182502, 0.5361774947034519],
                    [0.6813925106038379, 0.2775960977317661, 0.1288605654663202],
                    [0.39267567654709434, 0.9564057227959488, 0.1871308917508447],
                    [0.903983954928237, 0.5438059500773263, 0.4569114216457657],
                    [0.8820414102298897, 0.45860396176858587, 0.7241676366115432],
                    [0.39902532170310195, 0.9040443929009576, 0.6900250201912272],
                    [0.6996220542505167, 0.32772040155711896, 0.7567786427368891],
                    [0.6360610554471413, 0.24002027337970955, 0.16053882248525642],
                    [0.7963914745173317, 0.9591666030352225, 0.4581388272600428],
                    [0.5909841653236848, 0.8577226441935546, 0.457223453353857],
                    [0.9518744768327362, 0.5757511620448724, 0.8207671207013149],
                    [0.9088437184127383, 0.815523818768569, 0.1594144634489559],
                    [0.6288984390617004, 0.39843425861967713, 0.06271295202334569],
                    [0.4240322518898419, 0.25868406688940776, 0.8490383084285107],
                    [0.0333046265466962, 0.9589827218634736, 0.35536884847192957],
                    [0.35670689040254283, 0.016328502683707894, 0.1852323252361839],
                    [0.4012595008036087, 0.9292914173027139, 0.09961493022127131],
                    [0.9453015334790796, 0.8694885305466322, 0.4541623969075517]
                ],
                ["se", "se", "bi", "bi", "se", "se", "bi", "bi", "se", "se", "bi", "se", "bi", "se", "se", "se",
                 "se", "bi", "bi", "se", "se", "bi", "bi", "se", "se", "bi", "se", "bi", "se", "se", "se", "se",
                 "bi", "bi", "se", "se", "bi", "bi", "se", "se", "bi", "se", "bi", "se", "se", "se", "se", "bi",
                 "bi", "se", "se", "bi", "bi", "se", "se", "bi", "se", "bi", "se", "se", "se", "se", "bi", "bi",
                 "se", "se", "bi", "bi", "se", "se", "bi", "se", "bi", "se", "se", "se", "se", "bi", "bi", "se",
                 "se", "bi", "bi", "se", "se", "bi", "se", "bi", "se", "se", "se", "se", "bi", "bi", "se", "se",
                 "bi", "bi", "se", "se", "bi", "se", "bi", "se", "se", "se", "se", "bi", "bi", "se", "se", "bi",
                 "bi", "se", "se", "bi", "se", "bi", "se", "se", "se", "se", "bi", "bi", "se", "se", "bi", "bi",
                 "se", "se", "bi", "se", "bi", "se", "se"]
            )
            cutoff = 2 * nu.angstrom
            wrapped = kernel.NeighborWrapper(c, cutoff=cutoff)
            p = potentials.harmonic_repulsion_potential_family(a=cutoff, epsilon=nu.Ry)
            pots = [p.copy(tag="bi-bi"), p.copy(tag="se-bi"), p.copy(tag="bi-se"), p.copy(tag="se-se")]

            relaxed = wrapped.relax(pots)
            wrapped_relaxed = kernel.NeighborWrapper(relaxed, cutoff=2 * p.cutoff)
            testing.assert_allclose(relaxed.meta["forces"] / (nu.Ry / nu.angstrom), 0, atol=1e-5)
            testing.assert_array_less(1.99, wrapped_relaxed.sparse_pair_distances.data.min() / nu.angstrom)
