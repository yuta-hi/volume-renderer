from __future__ import absolute_import

import vtk
import numpy as np

from ..data.volume import (
    load_volume,
    sitkToVTK,
    centering,
    numpy_to_volume
    )
from ..data.surface import label_to_surface
from ..actor import Actor
from ..utils.vtk.transforms import centered_transform
import SimpleITK as sitk


class IsosurfaceActor(Actor):
    """ Actor for isosurface rendering """

    def __init__(self, label, index=1, rgb=[0.,0.,1.], alpha=1.,
                ambient=0.3, diffuse=0.6, specular=0.05, specular_power=1,
                interp='phong', shade=True, centered=True):

        super().__init__()

        if isinstance(label, str):
            label = load_volume(label)

        if isinstance(label, np.ndarray):
            spacing, origin = [1,1,1], [0,0,0]
            label = numpy_to_volume(label, spacing, origin)

        if isinstance(label, sitk.SimpleITK.Image):
            label = sitkToVTK(label)

        if centered:
            label = centering(label)

        surface = label_to_surface(label, index)

        self._label = label
        self._surface = surface

        self._rgb = rgb
        self._alpha = alpha
        self._ambient = ambient
        self._diffuse = diffuse
        self._specular = specular
        self._specular_power = specular_power
        self._interp = interp
        self._shade = shade

        self.update_mapper()
        self.update_property()

    def update_mapper(self):

        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputData(self._surface)
        mapper.ScalarVisibilityOff()
        mapper.Update()

        self._mapper = mapper

    def update_property(self):

        prop = vtk.vtkProperty()
        prop.SetColor(*self._rgb)
        prop.SetOpacity(self._alpha)

        prop.SetAmbient(self._ambient)
        prop.SetDiffuse(self._diffuse)
        prop.SetSpecular(self._specular)
        prop.SetSpecularPower(self._specular_power)

        if self._interp == 'phong':
            prop.SetInterpolationToPhong()
        elif self._interp == 'flat':
            prop.SetInterpolationToFlat()
        elif self._interp == 'gouraud':
            prop.SetInterpolationToGouraud()
        else:
            raise KeyError

        if self._shade:
            prop.ShadingOn()
        else:
            prop.ShadingOff()

        prop.BackfaceCullingOn()

        self._property = prop


    def build(self):

        actor = vtk.vtkActor()

        actor.SetMapper(self._mapper)
        actor.SetProperty(self._property)

        if self._transform is not None:
            actor.SetUserTransform(self._transform)

        return actor

