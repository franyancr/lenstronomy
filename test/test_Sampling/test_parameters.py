__author__ = 'sibirrer'

import numpy as np
import numpy.testing as npt
import pytest

from lenstronomy.Sampling.parameters import Param
from lenstronomy.LensModel.lens_model import LensModel
from lenstronomy.LensModel.Solver.lens_equation_solver import LensEquationSolver


class TestParam(object):

    def setup(self):
        kwargs_model = {'lens_model_list': ['SPEP'], 'source_light_model_list': ['GAUSSIAN'],
                          'lens_light_model_list': ['SERSIC'], 'point_source_model_list': ['LENSED_POSITION']}
        kwargs_param = {'num_point_source_list': [2]}
        kwargs_fixed_lens = [{'gamma': 1.9}] #for SPEP lens
        kwargs_fixed_source = [{'sigma_x': 0.1, 'sigma_y': 0.1, 'center_x':0.2, 'center_y': 0.2}]
        kwargs_fixed_ps = [{'ra_image': [-1, 1], 'dec_image': [-1, 1]}]
        kwargs_fixed_lens_light = [{}]
        kwargs_fixed_cosmo = [{}]
        self.param_class = Param(kwargs_model, kwargs_fixed_lens=kwargs_fixed_lens,
                                 kwargs_fixed_source=kwargs_fixed_source,
                                 kwargs_fixed_lens_light=kwargs_fixed_lens_light, kwargs_fixed_ps=kwargs_fixed_ps,
                                 kwargs_fixed_special=kwargs_fixed_cosmo, **kwargs_param)
        self.param_class.print_setting()

    def test_num_param(self):
        num_param, list = self.param_class.num_param()
        assert list[0] == 'theta_E_lens0'
        assert num_param == 9

        kwargs_model = {'lens_model_list': ['SPEP'], 'source_light_model_list': ['GAUSSIAN'],
                        'lens_light_model_list': ['SERSIC'], 'point_source_model_list': ['LENSED_POSITION']}
        kwargs_param = {}
        kwargs_fixed_lens = [{'gamma': 1.9}]  # for SPEP lens
        kwargs_fixed_source = [{'sigma_x': 0.1, 'sigma_y': 0.1, 'center_x': 0.2, 'center_y': 0.2}]
        kwargs_fixed_ps = [{'ra_image': [-1, 1], 'dec_image': [-1, 1]}]
        kwargs_fixed_lens_light = [{}]
        kwargs_fixed_cosmo = [{}]
        param_class_linear = Param(kwargs_model, kwargs_fixed_lens, kwargs_fixed_source,
                                        kwargs_fixed_lens_light, kwargs_fixed_ps, kwargs_fixed_cosmo,
                                   linear_solver=True, **kwargs_param)
        num_param, list = param_class_linear.num_param()
        assert list[0] == 'theta_E_lens0'
        print(list)
        assert len(list) == num_param
        assert num_param == 9

    def test_num_param_linear(self):
        num_param = self.param_class.num_param_linear()
        assert num_param == 4

    def test_get_params(self):
        kwargs_true_lens = [{'theta_E': 1.,'gamma':1.9, 'e1':0.01, 'e2':-0.01, 'center_x':0., 'center_y':0.}] #for SPEP lens
        kwargs_true_source = [{'amp': 1*2*np.pi*0.1**2,'center_x':0.2, 'center_y':0.2, 'sigma_x': 0.1, 'sigma_y': 0.1}]
        kwargs_true_lens_light = [{'center_x': -0.06, 'center_y': 0.4, 'phi_G': 4.8,
                                  'q': 0.86, 'n_sersic': 1.7,
                                  'amp': 11.8, 'R_sersic': 0.697, 'phi_G_2': 0}]
        kwargs_true_ps = [{'point_amp': [1, 1], 'ra_image': [-1, 1], 'dec_image': [-1, 1]}]
        kwargs_cosmo = [{}]
        args = self.param_class.kwargs2args(kwargs_true_lens, kwargs_true_source, kwargs_lens_light=kwargs_true_lens_light, kwargs_ps=kwargs_true_ps, kwargs_special=kwargs_cosmo)
        kwargs_return = self.param_class.args2kwargs(args)
        lens_dict_list = kwargs_return['kwargs_lens']
        lens_light_dict_list = kwargs_return['kwargs_lens_light']
        lens_dict = lens_dict_list[0]
        assert lens_dict['theta_E'] == 1.
        assert lens_dict['gamma'] == 1.9
        assert lens_dict['e1'] == 0.01
        assert lens_dict['e2'] == -0.01
        assert lens_dict['center_x'] == 0.
        assert lens_dict['center_y'] == 0.
        assert lens_light_dict_list[0]['center_x'] == -0.06

    def test_get_cosmo(self):
        kwargs_model = {'lens_model_list': ['SPEP'], 'source_light_model_list': ['GAUSSIAN'],
                        'lens_light_model_list': ['SERSIC'], 'point_source_model_list': ['LENSED_POSITION'],
                        }
        kwargs_param = {'Ddt_sampling': True}
        kwargs_fixed_lens = [{'gamma': 1.9}]  # for SPEP lens
        kwargs_fixed_source = [{'sigma_x': 0.1, 'sigma_y': 0.1, 'center_x': 0.2, 'center_y': 0.2}]
        kwargs_fixed_ps = [{'ra_image': [-1, 1], 'dec_image': [-1, 1]}]
        kwargs_fixed_lens_light = [{}]
        kwargs_fixed_cosmo = {'D_dt': 1000}
        param_class = Param(kwargs_model, kwargs_fixed_lens=kwargs_fixed_lens, kwargs_fixed_source=kwargs_fixed_source,
                            kwargs_fixed_lens_light=kwargs_fixed_lens_light, kwargs_fixed_ps=kwargs_fixed_ps,
                            kwargs_fixed_special=kwargs_fixed_cosmo, **kwargs_param)

        kwargs_true_lens = [
            {'theta_E': 1., 'gamma': 1.9, 'e1':0.01, 'e2':-0.01, 'center_x': 0., 'center_y': 0.}]  # for SPEP lens
        kwargs_true_source = [
            {'amp': 1 * 2 * np.pi * 0.1 ** 2, 'center_x': 0.2, 'center_y': 0.2, 'sigma_x': 0.1, 'sigma_y': 0.1}]
        kwargs_true_lens_light = [{'center_x': -0.06, 'center_y': 0.4, 'phi_G': 4.8,
                                   'q': 0.86, 'n_sersic': 1.7,
                                   'amp': 11.8, 'R_sersic': 0.697, 'phi_G_2': 0}]
        kwargs_true_ps = [{'point_amp': [1, 1], 'ra_image': [-1, 1], 'dec_image': [-1, 1]}]
        args = param_class.kwargs2args(kwargs_true_lens, kwargs_true_source,
                                       kwargs_lens_light=kwargs_true_lens_light, kwargs_ps=kwargs_true_ps,
                                       kwargs_special={'D_dt': 1000})
        assert param_class.specialParams._D_dt_sampling is True

    def test_mass_scaling(self):
        kwargs_model = {'lens_model_list': ['SIS', 'NFW', 'NFW', 'SIS', 'SERSIC', 'HERNQUIST']}
        kwargs_constraints = {'mass_scaling_list': [False, 1, 1, 1, 1, 1]}
        kwargs_fixed_lens = [{}, {'alpha_Rs': 0.1}, {'alpha_Rs': 0.3}, {'theta_E': 0.1},
                             {'k_eff': 0.3}, {'sigma0': 1}]
        kwargs_fixed_cosmo = {}
        param_class = Param(kwargs_model, kwargs_fixed_lens=kwargs_fixed_lens, kwargs_fixed_special=kwargs_fixed_cosmo
                            , **kwargs_constraints)
        kwargs_lens = [{'theta_E': 1, 'center_x': 0, 'center_y': 0},
                       {'alpha_Rs': 0.1, 'Rs': 5, 'center_x': 1., 'center_y': 0},
                       {'alpha_Rs': 0.1, 'Rs': 5, 'center_x': 0, 'center_y': 1.},
                       {'theta_E': 0.1, 'center_x': 3, 'center_y': 1.},
                       {'k_eff': 0.3, 'R_sersic': 1, 'n_sersic': 2, 'center_x': 3, 'center_y': 1.},
                       {'sigma0': 1, 'Rs': 1, 'center_x': 3, 'center_y': 1.}]
        kwargs_source = []
        kwargs_lens_light = []
        kwargs_ps = []
        mass_scale = 2
        kwargs_cosmo = {'scale_factor': [mass_scale]}
        args = param_class.kwargs2args(kwargs_lens, kwargs_source, kwargs_lens_light, kwargs_ps, kwargs_special=kwargs_cosmo)
        assert args[-1] == mass_scale


        kwargs_return = param_class.args2kwargs(args)
        kwargs_lens = kwargs_return['kwargs_lens']
        print(kwargs_lens, 'test')
        assert kwargs_lens[0]['theta_E'] == 1
        assert kwargs_lens[1]['alpha_Rs'] == 0.1 * mass_scale
        assert kwargs_lens[2]['alpha_Rs'] == 0.3 * mass_scale
        assert kwargs_lens[3]['theta_E'] == 0.1 * mass_scale
        assert kwargs_lens[4]['k_eff'] == 0.3 * mass_scale
        assert kwargs_lens[5]['sigma0'] == 1 * mass_scale

        kwargs_return = param_class.args2kwargs(args, bijective=True)
        kwargs_lens = kwargs_return['kwargs_lens']
        assert kwargs_lens[0]['theta_E'] == 1
        assert kwargs_lens[1]['alpha_Rs'] == 0.1
        assert kwargs_lens[2]['alpha_Rs'] == 0.3

    def test_joint_lens_with_light(self):
        kwargs_model = {'lens_model_list': ['CHAMELEON'], 'lens_light_model_list': ['CHAMELEON']}
        i_light, k_lens = 0, 0
        kwargs_constraints = {'joint_lens_with_light': [[i_light, k_lens, ['w_t', 'w_c', 'center_x', 'center_y', 'e1', 'e2']]]}
        kwargs_lens = [{'alpha_1': 10}]
        kwargs_lens_light = [{'amp': 1, 'w_t': 0.5, 'w_c': 0.1, 'center_x': 0, 'center_y': 0.3, 'e1': 0.1, 'e2': -0.2}]
        param = Param(kwargs_model=kwargs_model, **kwargs_constraints)
        args = param.kwargs2args(kwargs_lens=kwargs_lens, kwargs_lens_light=kwargs_lens_light)
        kwargs_return = param.args2kwargs(args)
        kwargs_lens_out = kwargs_return['kwargs_lens_light']
        kwargs_lens_light_out = kwargs_return['kwargs_lens_light']
        assert kwargs_lens_out[0]['w_c'] == kwargs_lens_light[0]['w_c']
        assert kwargs_lens_light_out[0]['w_c'] == kwargs_lens_light[0]['w_c']

        kwargs_model = {'lens_model_list': ['SIS'], 'lens_light_model_list': ['SERSIC']}
        i_light, k_lens = 0, 0
        kwargs_constraints = {'joint_lens_with_light': [[i_light, k_lens, ['center_x',
                                                       'center_y']]]}  # list[[i_point_source, k_source, ['param_name1', 'param_name2', ...]], [
        kwargs_lens = [{'theta_E': 1, 'center_x': 0, 'center_y': 0}]
        kwargs_lens_light = [{'amp': 1, 'R_sersic': 0.5, 'n_sersic': 2, 'center_x': 1, 'center_y': 1}]
        param = Param(kwargs_model=kwargs_model, **kwargs_constraints)
        args = param.kwargs2args(kwargs_lens=kwargs_lens, kwargs_lens_light=kwargs_lens_light)
        #kwargs_lens_out, kwargs_source_out, _, kwargs_ps_out, _ = param.args2kwargs(args)
        kwargs_return = param.args2kwargs(args)
        kwargs_lens_out = kwargs_return['kwargs_lens']

        assert kwargs_lens_out[0]['theta_E'] == kwargs_lens[0]['theta_E']
        assert kwargs_lens_out[0]['center_x'] == kwargs_lens_light[0]['center_x']

    def test_joint_source_with_point_source(self):
        kwargs_model = {'lens_model_list': ['SIS'], 'source_light_model_list': ['SERSIC'], 'point_source_model_list': ['SOURCE_POSITION']}
        i_source, k_ps = 0, 0
        kwargs_constraints = {'joint_source_with_point_source': [[k_ps, i_source]]} # list[[i_point_source, k_source, ['param_name1', 'param_name2', ...]], [

        kwargs_lens = [{'theta_E': 1, 'center_x': 0, 'center_y': 0}]
        kwargs_source = [{'amp': 1, 'n_sersic': 2, 'R_sersic': 0.3, 'center_x': 1, 'center_y': 1}]
        kwargs_ps = [{'ra_source': 0.5, 'dec_source': 0.5}]
        param = Param(kwargs_model=kwargs_model, **kwargs_constraints)
        args = param.kwargs2args(kwargs_lens=kwargs_lens, kwargs_source=kwargs_source, kwargs_ps=kwargs_ps)
        kwargs_return = param.args2kwargs(args)
        kwargs_lens_out = kwargs_return['kwargs_lens']
        kwargs_source_out = kwargs_return['kwargs_source']
        #kwargs_lens_out, kwargs_source_out, _, kwargs_ps_out, _ = param.args2kwargs(args)
        assert kwargs_lens_out[0]['theta_E'] == kwargs_lens[0]['theta_E']
        assert kwargs_source_out[0]['center_x'] == kwargs_ps[0]['ra_source']

        kwargs_model = {'lens_model_list': ['SIS'], 'source_light_model_list': ['SERSIC'], 'point_source_model_list': ['LENSED_POSITION']}
        i_source, k_ps = 0, 0
        kwargs_constraints = {'joint_source_with_point_source': [[k_ps, i_source]]} # list[[i_point_source, k_source, ['param_name1', 'param_name2', ...]], [

        kwargs_lens = [{'theta_E': 1, 'center_x': 0, 'center_y': 0}]
        kwargs_source = [{'amp': 1, 'n_sersic': 2, 'R_sersic': 0.3, 'center_x': 1, 'center_y': 1}]
        kwargs_ps = [{'ra_image': [0.5], 'dec_image': [0.5]}]
        param = Param(kwargs_model=kwargs_model, **kwargs_constraints)
        args = param.kwargs2args(kwargs_lens=kwargs_lens, kwargs_source=kwargs_source, kwargs_ps=kwargs_ps)
        #kwargs_lens_out, kwargs_source_out, _, kwargs_ps_out, _ = param.args2kwargs(args)
        kwargs_return = param.args2kwargs(args)
        kwargs_lens_out = kwargs_return['kwargs_lens']
        kwargs_source_out = kwargs_return['kwargs_source']
        assert kwargs_lens_out[0]['theta_E'] == kwargs_lens[0]['theta_E']
        npt.assert_almost_equal(kwargs_source_out[0]['center_x'], -0.207, decimal=2)

    def test_joint_lens_light_with_point_source(self):
        kwargs_model = {'lens_model_list': ['SIS'], 'source_light_model_list': ['SERSIC'],
                        'point_source_model_list': ['LENSED_POSITION'],
                        'lens_light_model_list': ['SERSIC']}
        i_lens_light, k_ps = 0, 0
        kwargs_constraints = {'joint_lens_light_with_point_source': [
            [k_ps, i_lens_light]]}  # list[[i_point_source, k_source, ['param_name1', 'param_name2', ...]], [

        kwargs_lens = [{'theta_E': 1, 'center_x': 0, 'center_y': 0}]
        kwargs_source = [{'amp': 1, 'n_sersic': 2, 'R_sersic': 0.3, 'center_x': 1, 'center_y': 1}]
        kwargs_lens_light = [{'amp': 1, 'n_sersic': 2, 'R_sersic': 0.3, 'center_x': 0.2, 'center_y': 0.2}]
        kwargs_ps = [{'ra_image': [0.5], 'dec_image': [0.5]}]
        param = Param(kwargs_model=kwargs_model, **kwargs_constraints)
        args = param.kwargs2args(kwargs_lens=kwargs_lens, kwargs_source=kwargs_source, kwargs_lens_light=kwargs_lens_light, kwargs_ps=kwargs_ps)
        kwargs_return = param.args2kwargs(args)
        kwargs_lens_light_out = kwargs_return['kwargs_lens_light']
        kwargs_ps_out = kwargs_return['kwargs_ps']
        assert kwargs_lens_light_out[0]['center_x'] == kwargs_ps_out[0]['ra_image']

    def test_with_solver(self):
        kwargs_model = {'lens_model_list': ['SPEP'], 'source_light_model_list': ['SERSIC'],
                        'point_source_model_list': ['LENSED_POSITION']}
        i_lens_light, k_ps = 0, 0
        kwargs_constraints = {'solver_type': 'PROFILE', 'num_point_source_list': [4]}

        kwargs_lens = [{'theta_E': 1, 'gamma': 2, 'e1': 0.1, 'e2': 0.1, 'center_x': 0, 'center_y': 0}]
        kwargs_source = [{'amp': 1, 'n_sersic': 2, 'R_sersic': 0.3, 'center_x': 1, 'center_y': 1}]
        kwargs_lens_light = [{'amp': 1, 'n_sersic': 2, 'R_sersic': 0.3, 'center_x': 0.2, 'center_y': 0.2}]
        lensModel = LensModel(lens_model_list=['SPEP'])
        lensEquationSlover = LensEquationSolver(lensModel=lensModel)
        x_image, y_image = lensEquationSlover.image_position_from_source(sourcePos_x=0.0, sourcePos_y=0.01, kwargs_lens=kwargs_lens)
        print(x_image, y_image, 'test')
        kwargs_ps = [{'ra_image': x_image, 'dec_image': y_image}]
        param = Param(kwargs_model=kwargs_model, kwargs_lens_init=kwargs_lens, **kwargs_constraints)
        args = param.kwargs2args(kwargs_lens=kwargs_lens, kwargs_source=kwargs_source,
                                 kwargs_lens_light=kwargs_lens_light, kwargs_ps=kwargs_ps)
        #kwargs_lens_out, kwargs_source_out, kwargs_lens_light_out, kwargs_ps_out, _ = param.args2kwargs(args)
        kwargs_return = param.args2kwargs(args)
        kwargs_lens_out = kwargs_return['kwargs_lens']
        kwargs_ps_out = kwargs_return['kwargs_ps']
        dist = param.check_solver(kwargs_lens=kwargs_lens_out, kwargs_ps=kwargs_ps_out)
        npt.assert_almost_equal(dist, 0, decimal=10)


if __name__ == '__main__':
    pytest.main()
