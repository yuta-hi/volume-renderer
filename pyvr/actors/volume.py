from __future__ import absolute_import

import vtk
import numpy as np

from ..data.volume import (
    load_volume,
    sitkToVTK,
    centering,
    numpy_to_volume
    )
from ..actor import Actor
from ..utils.vtk.transforms import centered_transform
from ..preset import VolumePreset
import SimpleITK as sitk


class VolumeActor(Actor):
    """ Actor for volume raycasting """
    def __init__(self, volume, preset='muscle', centered=True, gpu=True):

        super().__init__()

        if isinstance(volume, str):
            volume = load_volume(volume)

        if isinstance(volume, np.ndarray):
            spacing, origin = [1,1,1], [0,0,0]
            volume = numpy_to_volume(volume, spacing, origin)

        if isinstance(volume, sitk.SimpleITK.Image):
            volume = sitkToVTK(volume)

        if centered:
            volume = centering(volume)

        preset = VolumePreset(preset)

        self._volume = volume
        self._preset = preset
        self._gpu = gpu

        self.update_mapper()
        self.update_property()


    def update_mapper(self):

        if self._gpu:
            mapper = vtk.vtkGPUVolumeRayCastMapper()
        else:
            mapper = vtk.vtkFixedPointVolumeRayCastMapper()

        mapper.SetInputData(self._volume)
        mapper.SetBlendModeToComposite()

        self._mapper = mapper


    def update_property(self):

        preset = self._preset

        color = vtk.vtkColorTransferFunction()
        for (v, r, g, b, mid, sharp) in preset.color_transfer:
            color.AddRGBPoint(v, r, g, b, mid, sharp)

        scalar_opacity = vtk.vtkPiecewiseFunction()
        for (v, a, mid, sharp) in preset.scalar_opacity:
            scalar_opacity.AddPoint(v, a, mid, sharp)

        gradient_opacity = None
        if preset.gradient_opacity is not None:
            gradient_opacity = vtk.vtkPiecewiseFunction()
            for (v, a, mid, sharp) in preset.gradient_opacity:
                gradient_opacity.AddPoint(v, a, mid, sharp)

        prop = vtk.vtkVolumeProperty()
        prop.SetIndependentComponents(True)
        prop.SetColor(color)
        prop.SetScalarOpacity(scalar_opacity)
        if gradient_opacity is not None:
            prop.SetGradientOpacity(gradient_opacity)

        if preset.interpolation:
            prop.SetInterpolationTypeToLinear()
        else:
            prop.SetInterpolationTypeToNearest()

        if preset.shade:
            prop.ShadeOn()
        else:
            prop.ShadeOff()

        prop.SetAmbient(preset.ambient)
        prop.SetDiffuse(preset.diffuse)
        prop.SetSpecular(preset.specular)
        prop.SetSpecularPower(preset.specular_power)

        unit_distance = min(self._volume.GetSpacing())
        prop.SetScalarOpacityUnitDistance(unit_distance)

        self._property = prop


    def build(self):

        actor = vtk.vtkVolume()

        actor.SetMapper(self._mapper)
        actor.SetProperty(self._property)

        if self._transform is not None:
            actor.SetUserTransform(self._transform)

        actor.Update()

        return actor
