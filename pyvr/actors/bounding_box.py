from __future__ import absolute_import

import vtk
import numpy as np

from ..actor import Actor

class BoundingBoxActor(Actor):
    """ Actor for a bounding box
    """
    def __init__(self, xyz_min, xyz_max,
                rgb=[0.,0.,1.], alpha=0.5,
                ambient=0.3, diffuse=0.6, specular=0.05, specular_power=1,
                interp='phong', shade=True):

        super().__init__()

        self._xyz_min = xyz_min
        self._xyz_max = xyz_max

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

        length = len(self._xyz_min) + len(self._xyz_max)
        bounds = [None] * length
        bounds[0::2] = self._xyz_min
        bounds[1::2] = self._xyz_max

        source = vtk.vtkCubeSource()
        source.SetBounds(bounds)

        mapper = vtk.vtkPolyDataMapper()
        if vtk.VTK_MAJOR_VERSION <= 5:
            mapper.SetInput(source.GetOutput())
        else:
            mapper.SetInputConnection(source.GetOutputPort())

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
