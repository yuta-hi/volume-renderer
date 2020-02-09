from __future__ import absolute_import

import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

import numpy as np
import vtk
from vtk.util.numpy_support import numpy_to_vtk
from vtk.util.numpy_support import vtk_to_numpy


def load_volume(path):

    reader = vtk.vtkMetaImageReader()
    reader.SetFileName(path)
    reader.Update()

    volume = reader.GetOutput()

    return volume


def centering(volume):

    assert isinstance(volume, vtk.vtkImageData)

    shape = np.asarray(volume.GetDimensions())
    spacing = np.asarray(volume.GetSpacing())
    origin = - shape * spacing / 2.
    volume.SetOrigin(origin)

    return volume


def volume_to_numpy(volume, order='xyz'):

    assert isinstance(volume, vtk.vtkImageData)

    spacing = volume.GetSpacing()
    origin = volume.GetOrigin()
    shape = volume.GetDimensions()

    array = vtk_to_numpy(volume.GetPointData().GetScalars())
    array = array.reshape(shape, order='F')

    if order == 'xyz':
        pass
    elif order == 'zyx':
        array = np.transpose(array, (2, 1, 0))
        spacing = spacing[::-1]
        origin = origin[::-1]
    else:
        raise ValueError('unexpected axis order')

    return array, spacing, origin


def numpy_to_volume(array, spacing, origin, order='xyz'):

    assert isinstance(array, np.ndarray)

    if order == 'xyz':
        pass
    elif order == 'zyx':
        array = np.transpose(array, (2, 1, 0))
        spacing = spacing[::-1]
        origin = origin[::-1]
    else:
        raise ValueError('unexpected axis order')

    volume = vtk.vtkImageData()
    volume.SetDimensions(array.shape)
    volume.SetSpacing(spacing)
    volume.SetOrigin(origin)
    volume.GetPointData().SetScalars(
        numpy_to_vtk(array.reshape(-1, order='F'), deep=True))

    return volume
