from __future__ import absolute_import

import os
import json
import numpy as np
from abc import ABCMeta, abstractmethod

_cur_dir = os.path.dirname(os.path.abspath(__file__))

_default_preset_dir = {
    'volume': os.path.join(_cur_dir, 'presets/volume'),
    'label': os.path.join(_cur_dir, 'presets/label'),
}

class Preset(metaclass=ABCMeta):
    """ Base class of preset """

    preset_dir = None

    def __init__(self, name):

        _, ext = os.path.splitext(name)

        if ext in ['.json', '.JSON']:
            preset_path = name
        else:
            preset_path = os.path.join(self.preset_dir, name + '.json')

        with open(preset_path) as f:
            preset = json.load(f)

        self.preset = preset


class VolumePreset(Preset):

    preset_dir = _default_preset_dir['volume']

    @property
    def color_transfer(self):
        ret = np.asarray(self.preset['color_transfer'])
        assert ret.ndim == 2
        assert ret.shape[1] == 6
        return ret.astype(np.float)

    @property
    def scalar_opacity(self):
        ret = np.asarray(self.preset['scalar_opacity'])
        assert ret.ndim == 2
        assert ret.shape[1] == 4
        return ret.astype(np.float)

    @property
    def gradient_opacity(self):

        ret = self.preset['gradient_opacity']
        if ret is None:
            return None

        ret = np.asarray(ret)
        assert ret.ndim == 2
        assert ret.shape[1] == 4

        return ret.astype(np.float)

    @property
    def specular(self):
        return self.preset['specular']

    @property
    def specular_power(self):
        return self.preset['specular_power']

    @property
    def ambient(self):
        return self.preset['ambient']

    @property
    def diffuse(self):
        return self.preset['diffuse']

    @property
    def shade(self):
        return self.preset['shade']

    @property
    def interpolation(self):
        return self.preset['interpolation']


class LabelPreset(Preset):

    preset_dir = _default_preset_dir['label']

    @property
    def index(self):
        ret = np.asarray(self.preset['color'])
        assert ret.ndim == 2
        assert ret.shape[1] == 6
        ret = ret[:, 0]
        return ret.astype(np.int)

    @property
    def color(self):
        ret = np.asarray(self.preset['color'])
        assert ret.ndim == 2
        assert ret.shape[1] == 6
        ret = ret[:, 2:]
        return ret.astype(np.float)

    @property
    def colormap(self):
        index = self.index
        color = self.color

        max_index = np.max(index)
        ret = np.zeros((max_index, color.shape[1]), color.dtype)

        for i, c in zip(index, color):
            ret[i - 1, :] = c # NOTE: ignore background label

        return ret

    @property
    def legend(self):
        ret = np.asarray(self.preset['color'])
        assert ret.ndim == 2
        assert ret.shape[1] == 6
        ret = ret[:, 1]
        return ret

    @property
    def specular(self):
        return self.preset['specular']

    @property
    def specular_power(self):
        return self.preset['specular_power']

    @property
    def ambient(self):
        return self.preset['ambient']

    @property
    def diffuse(self):
        return self.preset['diffuse']

    @property
    def shade(self):
        return self.preset['shade']

    @property
    def interpolation(self):
        return self.preset['interpolation']
