

from __future__ import absolute_import

import vtk
import numpy as np
import matplotlib.cm as cm
from vtk.util import numpy_support

from ..data.volume import load_volume
from ..data.volume import centering
from ..data.volume import numpy_to_volume
from ..data.surface import label_to_surface
from ..data.surface import set_scalars
from ..actor import Actor
from ..utils.vtk.transforms import centered_transform


def _geodesic_distances(surface, query_point):

    assert(isinstance(surface, vtk.vtkPolyData))

    locator = vtk.vtkPointLocator()
    locator.SetDataSet(surface)
    locator.BuildLocator()

    closest_point_idx = locator.FindClosestPoint(query_point)

    dijkstra = vtk.vtkDijkstraGraphGeodesicPath()
    dijkstra.SetInputData(surface)
    dijkstra.SetStartVertex(closest_point_idx)
    dijkstra.SetEndVertex(0) # NOTE: dummy value
    dijkstra.Update()

    weights = vtk.vtkDoubleArray()
    dijkstra.GetCumulativeWeights(weights)

    distances = numpy_support.vtk_to_numpy(weights)
    distances = np.where(distances >= vtk.VTK_DOUBLE_MAX/10., \
                         -1.0, distances)
    return distances


class GeodesicDistanceActor(Actor):
    """ Actor for geodesic distance rendering """
    def __init__(self, label, query_point, label_index=1,
                 centered=True, cmap='jet', clim_max=None):
        super().__init__()

        if isinstance(label, str):
            label = load_volume(label)

        if isinstance(label, np.ndarray):
            spacing, origin = [1,1,1], [0,0,0]
            label = numpy_to_volume(label, spacing, origin)

        if centered:
            label = centering(label)

        surface = label_to_surface(label, label_index)

        distances = _geodesic_distances(surface, query_point)
        set_scalars(surface, distances)

        self._surface = surface
        self._query_point = query_point
        self._label_index = label_index
        self._cmap = cmap
        self._clim_max = clim_max

        self.update_mapper()
        self.update_property()


    def update_mapper(self):

        surface = self._surface
        clim_max = self._clim_max

        scalar_range = surface.GetScalarRange()
        n_tables = int(np.ceil(scalar_range[1]))

        cmap = cm.get_cmap(self._cmap, n_tables)

        lut = vtk.vtkLookupTable()
        lut.SetNumberOfTableValues(n_tables + 1)
        lut.SetTableValue(0, 1.0, 1.0, 1.0, 1.0)
        for i in range(n_tables):
            r, g, b, a = cmap(float(i)/255.)
            lut.SetTableValue(i + 1, r, g, b, a)
        lut.Build()

        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputData(surface)
        if clim_max is None:
            mapper.SetScalarRange(-1.0, scalar_range[1])
        else:
            mapper.SetScalarRange(-1.0, float(clim_max))
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
