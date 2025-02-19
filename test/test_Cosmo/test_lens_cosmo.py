__author__ = 'sibirrer'

import numpy as np
import numpy.testing as npt
import pytest

from lenstronomy.Cosmo.lens_cosmo import LensCosmo, LCDM


class TestLensCosmo(object):
    """
    tests the UnitManager class routines
    """
    def setup(self):
        z_L = 0.8
        z_S = 3.0
        from astropy.cosmology import FlatLambdaCDM
        cosmo = FlatLambdaCDM(H0=70, Om0=0.3, Ob0=0.05)
        self.lensCosmo = LensCosmo(z_L, z_S, cosmo=cosmo)

    def test_ang_dist(self):
        npt.assert_almost_equal(self.lensCosmo.D_s, 1588.9213590743666, decimal=8)
        npt.assert_almost_equal(self.lensCosmo.D_d, 1548.7055203661785, decimal=8)
        npt.assert_almost_equal(self.lensCosmo.D_ds, 892.0038749095863, decimal=8)

    def test_epsilon_crit(self):
        npt.assert_almost_equal(self.lensCosmo.epsilon_crit/1.9121e+15, 1, decimal=3)

    def test_arcsec2phys(self):
        arcsec = np.array([1, 2]) # pixel coordinate from center
        physcoord = self.lensCosmo.arcsec2phys_lens(arcsec)
        npt.assert_almost_equal(physcoord[0], 0.0075083362428338641, decimal=8)
        npt.assert_almost_equal(physcoord[1], 0.015016672485667728, decimal=8)

        physcoord = self.lensCosmo.arcsec2phys_source(arcsec)
        npt.assert_almost_equal(physcoord[0], 0.007703308130864105, decimal=8)
        npt.assert_almost_equal(physcoord[1], 0.01540661626172821, decimal=8)

    def test_phys2arcsec_lens(self):
        phys = 1.
        arc_sec = self.lensCosmo.phys2arcsec_lens(phys)
        phys_new = self.lensCosmo.arcsec2phys_lens(arc_sec)
        npt.assert_almost_equal(phys_new, phys, decimal=8)

    def test_mass_in_phi_E(self):
        phi_E = 1.5
        mass = self.lensCosmo.mass_in_theta_E(phi_E)
        npt.assert_almost_equal(mass, 761967261292.6725, decimal=2)

    def test_kappa2proj_mass(self):
        kappa = 0.5
        mass = self.lensCosmo.kappa2proj_mass(kappa)
        npt.assert_almost_equal(mass, kappa * self.lensCosmo.epsilon_crit, decimal=3)

    def test_mass_in_coin(self):
        theta_E = 1.
        m_coin = self.lensCosmo.mass_in_coin(theta_E)
        npt.assert_almost_equal(m_coin, 165279526936.52194, decimal=0)

    def test_D_dt_model(self):
        D_dt = self.lensCosmo.D_dt
        npt.assert_almost_equal(D_dt, 4965.660384441859, decimal=8)

    def test_nfw_angle2physical(self):
        Rs_angle = 6.
        alpha_Rs = 1.
        rho0, Rs, c, r200, M200 = self.lensCosmo.nfw_angle2physical(Rs_angle, alpha_Rs)
        assert Rs * c == r200

    def test_nfw_physical2angle(self):
        M = 10.**13.5
        c = 4
        Rs_angle, alpha_Rs = self.lensCosmo.nfw_physical2angle(M, c)
        rho0, Rs, c_out, r200, M200 = self.lensCosmo.nfw_angle2physical(Rs_angle, alpha_Rs)
        npt.assert_almost_equal(c_out, c, decimal=3)
        npt.assert_almost_equal(np.log10(M200), np.log10(M), decimal=4)

    def test_sis_theta_E2sigma_v(self):
        theta_E = 2.
        sigma_v = self.lensCosmo.sis_theta_E2sigma_v(theta_E)
        theta_E_out = self.lensCosmo.sis_sigma_v2theta_E(sigma_v)
        npt.assert_almost_equal(theta_E_out, theta_E, decimal=5)

    def test_fermat2delays(self):

        fermat_pot = 0.5
        dt_days = self.lensCosmo.time_delay_units(fermat_pot)
        fermat_pot_out = self.lensCosmo.time_delay2fermat_pot(dt_days)
        npt.assert_almost_equal(fermat_pot, fermat_pot_out, decimal=10)


class TestFlatLCDM(object):
    def setup(self):
        self.cosmo = LCDM(z_lens=0.5, z_source=1.5, flat=True)
        self.cosmo_k = LCDM(z_lens=0.5, z_source=1.5, flat=False)

    def test_D_d(self):
        D_d = self.cosmo.D_d(H_0=70, Om0=0.3)
        npt.assert_almost_equal(D_d, 1259.0835972889377, decimal=8)

        D_d_k = self.cosmo_k.D_d(H_0=70, Om0=0.3, Ode0=0.7)
        npt.assert_almost_equal(D_d, D_d_k, decimal=8)

    def test_D_s(self):
        D_s = self.cosmo.D_s(H_0=70, Om0=0.3)
        npt.assert_almost_equal(D_s, 1745.5423064934419, decimal=8)
        D_s_k = self.cosmo_k.D_s(H_0=70, Om0=0.3, Ode0=0.7)
        npt.assert_almost_equal(D_s, D_s_k, decimal=8)

    def test_D_ds(self):
        D_ds = self.cosmo.D_ds(H_0=70, Om0=0.3)
        npt.assert_almost_equal(D_ds, 990.0921481200791, decimal=8)
        D_ds_k = self.cosmo_k.D_ds(H_0=70, Om0=0.3, Ode0=0.7)
        npt.assert_almost_equal(D_ds, D_ds_k, decimal=8)

    def test_D_dt(self):
        D_dt = self.cosmo.D_dt(H_0=70, Om0=0.3)
        npt.assert_almost_equal(D_dt, 3329.665360925441, decimal=8)
        D_dt_k = self.cosmo_k.D_dt(H_0=70, Om0=0.3, Ode0=0.7)
        npt.assert_almost_equal(D_dt, D_dt_k, decimal=8)


if __name__ == '__main__':
    pytest.main()
