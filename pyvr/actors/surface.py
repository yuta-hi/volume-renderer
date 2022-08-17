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
from ..preset import LabelPreset
import SimpleITK as sitk


class SurfaceActor(Actor):
    """ Actor for surface rendering

    Note that background index should be zero.
    """
    def __init__(self, label, preset='muscle', centered=True, alpha_scale=1.):

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

        preset = LabelPreset(preset)

        surface = label_to_surface(label)

        self._label = label
        self._surface = surface
        self._preset = preset
        self._alpha_scale = alpha_scale

        self.update_mapper()
        self.update_property()


    def update_mapper(self):

        colormap = self._preset.colormap
        n_label = len(colormap)

        colorLookupTable = vtk.vtkLookupTable()
        colorLookupTable.SetNumberOfTableValues(n_label)
        colorLookupTable.Build()
        for i, (r, g, b, a)  in enumerate(colormap):
            a = min(max(a * self._alpha_scale, 0.), 1.)
            colorLookupTable.SetTableValue(i, r, g, b, a)

        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputData(self._surface)
        mapper.ScalarVisibilityOn()
        mapper.SetLookupTable(colorLookupTable)
        mapper.SetScalarRange(1, n_label)
        mapper.Update()

        self._mapper = mapper

    def update_property(self):

        preset = self._preset

        prop = vtk.vtkProperty()
        prop.SetAmbient(preset.ambient)
        prop.SetDiffuse(preset.diffuse)
        prop.SetSpecular(preset.specular)
        prop.SetSpecularPower(preset.specular_power)

        if preset.interpolation == 'phong':
            prop.SetInterpolationToPhong()
        elif preset.interpolation == 'flat':
            prop.SetInterpolationToFlat()
        elif preset.interpolation == 'gouraud':
            prop.SetInterpolationToGouraud()
        else:
            raise KeyError

        if preset.shade:
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
