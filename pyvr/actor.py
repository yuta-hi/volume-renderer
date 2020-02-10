from __future__ import absolute_import

import vtk
from abc import ABCMeta, abstractmethod

from .utils.vtk.transforms import euler_transform

_supported_actors = (
    vtk.vtkActor,
    vtk.vtkVolume,
    vtk.vtkImageSlice,
    vtk.vtkAxesActor
)

class Actor(metaclass=ABCMeta):
    """ Base class of Actor """
    def __init__(self):
        self._transform = None
        self._mapper = None
        self._property = None
        self._actor = None

    def set_transform(self, trans, rot):
        assert len(trans) == 3
        assert len(rot) == 3
        self._transform = euler_transform(trans, rot)

    @abstractmethod
    def update_mapper(self):
        raise NotImplementedError()

    @abstractmethod
    def update_property(self):
        raise NotImplementedError()

    @abstractmethod
    def build(self):
        raise NotImplementedError()

    def __call__(self):

        actor = self.build()
        assert isinstance(actor, _supported_actors)

        self._actor = actor
        return actor
