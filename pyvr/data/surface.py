from __future__ import absolute_import

import numpy as np
import vtk
from vtk.util.numpy_support import numpy_to_vtk

from .volume import numpy_to_volume
from .volume import volume_to_numpy

def _marching_cubes(label, index=None, normal=True, gradient=True, force_close=True):

    if not isinstance(label, np.ndarray):
        label, spacing, origin = volume_to_numpy(label)
    else:
        spacing, origin = [1,1,1], [0,0,0]

    if force_close: # NOTE: make the closed surface
        _pad_width = 10
        label = np.pad(label, pad_width=_pad_width, mode='constant', constant_values=0)
    else:
        _pad_width = 0

    origin -= _pad_width * np.array(spacing)
    label = numpy_to_volume(label, spacing, origin)

    surface = vtk.vtkDiscreteMarchingCubes()
    surface.SetInputData(label)

    if index is None:
        n_label = int(label.GetScalarRange()[1]) + 1
        surface.GenerateValues(n_label, 1, n_label)
    else:
        surface.GenerateValues(1, index, index)

    if normal:
        surface.ComputeNormalsOn()
    else:
        surface.ComputeNormalsOff()

    if gradient:
        surface.ComputeGradientsOn()
    else:
        surface.ComputeGradientsOff()

    surface.Update()

    return surface.GetOutput()


def label_to_surface(volume, index=None, force_close=True):
    return _marching_cubes(label=volume, index=index, force_close=force_close)


def set_scalars(surface, scalars):

    assert isinstance(surface, vtk.vtkPolyData)

    if isinstance(scalars, np.ndarray):
        scalars = numpy_to_vtk(scalars, deep=1)

    surface.GetPointData().SetScalars(scalars)
