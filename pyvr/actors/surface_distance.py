from __future__ import absolute_import

import vtk
import numpy as np
import matplotlib.cm as cm

from ..data.volume import load_volume
from ..data.volume import centering
from ..data.volume import numpy_to_volume
from ..data.surface import label_to_surface
from ..data.surface import set_scalars
from ..actor import Actor
from ..utils.vtk.transforms import centered_transform

def _isosurface(label, index, centered):

    if isinstance(label, str):
        label = load_volume(label)

    if isinstance(label, np.ndarray):
        spacing, origin = [1,1,1], [0,0,0]
        label = numpy_to_volume(label, spacing, origin)

    if centered:
        label = centering(label)

    surface = label_to_surface(label, index)

    return surface


def _absolute_surface_distance(source, target):

    assert(isinstance(source, vtk.vtkPolyData))
    assert(isinstance(target, vtk.vtkPolyData))

    distances = []

    implicitPolyDataDistance = vtk.vtkImplicitPolyDataDistance()
    implicitPolyDataDistance.SetInput(target)

    # evaluate the signed distance function
    for pointId in range(source.GetNumberOfPoints()):
        p = source.GetPoint(pointId)
        signedDistance = implicitPolyDataDistance.EvaluateFunction(p)
        distances.append(signedDistance)

    return np.abs(distances)


class SurfaceDistanceActor(Actor):
    """ Actor for surface distance rendering """
    def __init__(self, source, target, source_index=1, target_index=1,
                 centered=True, cmap='jet', clim=None):

        super().__init__()

        source = _isosurface(source, source_index, centered)
        target = _isosurface(target, target_index, centered)

        distance = _absolute_surface_distance(source, target)
        set_scalars(source, distance)

        self._source = source
        self._target = target
        self._source_index = source_index
        self._target_index = target_index
        self._cmap = cmap
        self._clim = clim

        self.update_mapper()
        self.update_property()


    def update_mapper(self):

        surface = self._source
        cmap = cm.get_cmap(self._cmap)
        clim = self._clim

        lut = vtk.vtkLookupTable()
        lut.SetNumberOfTableValues(255)
        for i in range(255):
            r, g, b, a = cmap(float(i)/255.)
            lut.SetTableValue(i, r, g, b, a)
        lut.Build()

        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputData(surface)
        if clim is None:
            scalar_range = surface.GetScalarRange()
            mapper.SetScalarRange(scalar_range[0], scalar_range[1])
        else:
            mapper.SetScalarRange(float(clim[0]), float(clim[1]))
        mapper.SetLookupTable(lut)
        mapper.Update()

        self._mapper = mapper


    def update_property(self):
        prop = vtk.vtkProperty()
        self._property = prop


    def build(self):

        actor = vtk.vtkActor()

        actor.SetMapper(self._mapper)
        actor.SetProperty(self._property)

        if self._transform is not None:
            actor.SetUserTransform(self._transform)

        return actor
