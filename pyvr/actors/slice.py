from __future__ import absolute_import

import vtk
import numpy as np

from ..data.volume import load_volume
from ..data.volume import centering
from ..data.volume import numpy_to_volume
from ..actor import Actor

class SliceActor(Actor):
    """ Actor for volume slicing """
    def __init__(self, volume, origin=(0,0,0), normal=(0,1,0),
                clim=None, alpha=1., ambient=1., diffuse=1.,
                interp=False, centered=True):

        super().__init__()

        if isinstance(volume, str):
            volume = load_volume(volume)

        if isinstance(volume, np.ndarray):
            spacing, origin = [1,1,1], [0,0,0]
            volume = numpy_to_volume(volume, spacing, origin)

        if centered:
            volume = centering(volume)
            # TODO: it is better to shift the origin..

        self._volume = volume
        self._origin = origin
        self._normal = normal
        self._clim = clim
        self._alpha = alpha
        self._ambient = ambient
        self._diffuse = diffuse
        self._interp = interp

        self.update_mapper()
        self.update_property()


    def update_mapper(self):

        mapper = vtk.vtkImageResliceMapper()
        mapper.SetInputData(self._volume)
        mapper.SliceFacesCameraOff()
        mapper.SliceAtFocalPointOff()
        mapper.JumpToNearestSliceOn()
        mapper.SetImageSampleFactor(2)
        mapper.BorderOn()
        mapper.BackgroundOff()
        mapper.UpdateInformation()
        mapper.GetSlicePlane().SetOrigin(*self._origin)
        mapper.GetSlicePlane().SetNormal(*self._normal)
        mapper.GetSlicePlane().Modified()
        mapper.Modified()
        mapper.Update()

        self._mapper = mapper


    def update_property(self):

        prop = vtk.vtkImageProperty()

        if self._clim is not None:
            clim = self._clim
            window = max(clim) - min(clim)
            level = window / 2. + min(clim)

            prop.SetColorWindow(window)
            prop.SetColorLevel(level)

        prop.SetAmbient(self._ambient)
        prop.SetDiffuse(self._diffuse)
        prop.SetOpacity(self._alpha)

        if self._interp:
            prop.SetInterpolationTypeToLinear()
        else:
            prop.SetInterpolationTypeToNearest()

        self._property = prop


    def build(self):

        actor = vtk.vtkImageSlice()

        actor.SetMapper(self._mapper)
        actor.SetProperty(self._property)

        if self._transform is not None:
            actor.SetUserTransform(self._transform)

        actor.Update()

        return actor
