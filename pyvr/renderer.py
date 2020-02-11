from __future__ import absolute_import

import numpy as np
import vtk
from vtk.util.numpy_support import vtk_to_numpy
from abc import ABCMeta, abstractmethod

from .actor import Actor
from .actor import _supported_actors
from .utils.vtk.camera import centered_camera

def _image_to_numpy(vtk_image):
    height, width, _ = vtk_image.GetDimensions()
    vtk_array = vtk_image.GetPointData().GetScalars()
    components = vtk_array.GetNumberOfComponents()
    np_array = vtk_to_numpy(vtk_array).reshape(width, height, components)
    return np.flip(np_array, 0)


_default_window_size = (500, 800)
_default_bg_color = (0.1, 0.1, 0.1)


class Renderer(metaclass=ABCMeta):
    """ Base class of renderer """
    def __init__(self):

        self._actors = []
        self._camera = None
        self._renderer = None
        self._window = None

        self.set_camera()

    @property
    def actors(self):
        return self._actors

    def add_actor(self, actor):
        if isinstance(actor, Actor):
            self._actors.append(actor())
        elif isinstance(actor, _supported_actors):
            self._actors.append(actor)
        else:
            raise ValueError

    def set_camera(self, pos=(0,-1000,0), fp=(0,0,0), up=(0,0,1), view=30, near=100, far=3000):
        self._camera = centered_camera(pos, fp, up, view, near, far)

    def _make_window(self, size, bg):

        ren = vtk.vtkRenderer()
        window = vtk.vtkRenderWindow()

        for actor in self._actors:
            ren.AddActor(actor)

        ren.SetBackground(bg[0], bg[1], bg[2])
        ren.SetActiveCamera(self._camera)
        ren.LightFollowCameraOn()
        ren.SetUseDepthPeeling(True)
        ren.SetMaximumNumberOfPeels(100)
        ren.SetOcclusionRatio(0.0)

        window.SetAlphaBitPlanes(True)
        window.SetMultiSamples(0)
        window.SetSize(size[0], size[1])
        window.AddRenderer(ren)

        self._renderer = ren
        self._window = window

    def interactor(self, size=_default_window_size, bg=_default_bg_color):

        self._make_window(size, bg)
        self._window.OffScreenRenderingOff()

        iren = vtk.vtkRenderWindowInteractor()
        iren.SetRenderWindow(self._window)
        iren.GetInteractorStyle().SetCurrentStyleToTrackballCamera()

        iren.Initialize()
        self._window.Render()
        iren.Start()

    def render(self, rotate_axis=2, rotate_angles=[0], size=_default_window_size, bg=_default_bg_color):

        self._make_window(size, bg)
        self._window.OffScreenRenderingOn()

        image_filter = vtk.vtkWindowToImageFilter()
        image_filter.SetInput(self._window)
        rendered_image = np.zeros((len(rotate_angles), size[1], size[0], 3), np.uint8)

        for i, angle in enumerate(rotate_angles):

            # forward rotation
            if rotate_axis == 0:
                self._camera.Elevation(angle)
            elif rotate_axis == 1:
                self._camera.Roll(angle)
            elif rotate_axis == 2:
                self._camera.Azimuth(angle)

            # render
            image_filter.Modified()
            image_filter.Update()
            self._window.Render()

            rendered_image[i,:] = _image_to_numpy(
                                        image_filter.GetOutput())

            # backward rotation
            if rotate_axis == 0:
                self._camera.Elevation(-angle)
            elif rotate_axis == 1:
                self._camera.Roll(-angle)
            elif rotate_axis == 2:
                self._camera.Azimuth(-angle)

        return rendered_image

    def __call__(self, *args, **kwargs):
        return self.render(*args, **kwargs)


class InteractiveRenderer(Renderer):

    def render(self, size=_default_window_size, bg=_default_bg_color):
        self.interactor(size=size, bg=bg)


class InteractiveMultiViewRenderer(InteractiveRenderer):

    def _make_window(self, size, bg):

        n_viewport = len(self._actors)
        x_grid = np.linspace(0.0, 1.0, n_viewport + 1)

        window = vtk.vtkRenderWindow()
        window.SetAlphaBitPlanes(True)
        window.SetMultiSamples(0)
        window.SetSize(size[0] * n_viewport, size[1])

        renderer = []

        for i, actor in enumerate(self._actors):

            ren = vtk.vtkRenderer()
            ren.SetViewport(x_grid[i], 0.0, x_grid[i+1], 1.0)
            ren.SetBackground(bg[0], bg[1], bg[2])
            ren.SetActiveCamera(self._camera)
            ren.LightFollowCameraOn()
            ren.SetUseDepthPeeling(True)
            ren.SetMaximumNumberOfPeels(100)
            ren.SetOcclusionRatio(0.0)
            ren.AddActor(actor)

            renderer.append(ren)
            window.AddRenderer(ren)

        self._renderer = renderer
        self._window = window
