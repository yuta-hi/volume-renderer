from __future__ import absolute_import

import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

import numpy as np
import vtk
from vtk.util.numpy_support import numpy_to_vtk
from vtk.util.numpy_support import vtk_to_numpy
import SimpleITK as sitk

def load_volume(path):
    reader = vtk.vtkNIFTIImageReader()
    reader.SetFileName(path)
    reader.Update()
    volume = reader.GetOutput()
    return volume


def sitkToVTK(img_sitk):
    """ convert an sitk image to a vtk object
    """
    data = sitk.GetArrayFromImage(img_sitk)
    data_type = vtk.VTK_FLOAT
    flat_data_array = data.flatten()
    vtk_data = numpy_to_vtk(num_array=flat_data_array, deep=True, array_type=data_type)
    shape = data.shape
    img = vtk.vtkImageData()
    img.GetPointData().SetScalars(vtk_data)
    img.SetDimensions(shape[2], shape[1], shape[0])
    img.SetSpacing = img.GetSpacing
    return img


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
