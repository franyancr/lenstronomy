__author__ = 'sibirrer'

from lenstronomy.Workflow.update_manager import UpdateManager
import copy


class MultiBandUpdateManager(UpdateManager):
    """
    specific Manager to deal with multiple images with disjoint lens model parameterization. The class inherits the
    FittingSequence() class and adds functionalities to hold and relieve fixed all lens model parameters of a specific
    frame/image for more convenient use of the FittingSequence.
    """
    def __init__(self, kwargs_model, kwargs_constraints, kwargs_likelihood, kwargs_params, num_bands=0):
        super(MultiBandUpdateManager, self).__init__(kwargs_model, kwargs_constraints, kwargs_likelihood, kwargs_params)
        kwargs_lens_fixed_init, _, _, _, _, _ = self._fixed_kwargs
        self._kwargs_lens_fixed_init = copy.deepcopy(kwargs_lens_fixed_init)

        self._index_lens_model_list = kwargs_model.get('index_lens_model_list', [None for i in range(num_bands)])
        self._index_source_list = kwargs_model.get('index_source_light_model_list',
                                             [None for i in range(num_bands)])
        self._index_lens_light_list = kwargs_model.get('index_lens_light_model_list',
                                                 [None for i in range(num_bands)])
        self._num_bands = num_bands

    def keep_frame_fixed(self, frame_list_fixed):
        """

        :param frame_list_fixed: list of indexes of frames whose lens models to be fixed
        :return: updated fixed lens model parameter in the FittingSequence()
        """
        for j in frame_list_fixed:
            if self._index_lens_model_list[j] is not None:
                for i in self._index_lens_model_list[j]:
                    self._lens_fixed[i] = self._kwargs_temp['kwargs_lens'][i]

    def undo_frame_fixed(self, frame_list):
        """

        :param frame_list: list of frame indexes to be set back to the parameters being fixed in the initial fix
        parameters in the class creation
        :return: updated fixed lens model parameter in the FittingSequence()
        """
        for j in frame_list:
            if self._index_lens_model_list[j] is not None:
                for i in self._index_lens_model_list[j]:
                    self._lens_fixed[i] = copy.deepcopy(self._kwargs_lens_fixed_init[i])

    def fix_not_computed(self, free_bands):
        """
        fix all the lens models that are part of a imaging band that is not set to be computed. Free those that are
        modeled.
        #TODO check for overlapping models for more automated fixing of parameters

        :param free_bands: boolean list of length of the imaging bands, True indicates that the lens model is being fitted for
        :return:
        """
        undo_frame_list = []
        fix_frame_list = []
        for i in range(len(free_bands)):
            if free_bands[i] is True:
                undo_frame_list.append(i)
            else:
                fix_frame_list.append(i)
        self.undo_frame_fixed(undo_frame_list)
        self.keep_frame_fixed(fix_frame_list)