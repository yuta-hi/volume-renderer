from __future__ import absolute_import

from . import renderer
from . import preset
from . import actors
from . import utils

def volume_render(volume, preset, centered=True, gpu=True,
        pos=[0,-1000,0], fp=[0,0,0], up=[0,0,1],
        view=30, near=100, far=3000,
        rotate_axis=2, rotate_angles=list(range(0, 360, 1)),
        size=(500,800), bg=(1.,1.,1.)):

    ren = renderer.Renderer()
    ren.add_actor(actors.VolumeActor(volume, preset=preset, centered=centered, gpu=gpu))
    ren.set_camera(pos=pos, fp=fp, up=up, view=view, near=near, far=far)
    proj = ren.render(rotate_axis=rotate_axis, rotate_angles=rotate_angles, size=size, bg=bg)

    return proj


def surface_render(label, preset, centered=True, alpha_scale=1.,
        pos=[0,-1000,0], fp=[0,0,0], up=[0,0,1],
        view=30, near=100, far=3000,
        rotate_axis=2, rotate_angles=list(range(0, 360, 1)),
        size=(500,800), bg=(1.,1.,1.)):

    ren = renderer.Renderer()
    ren.add_actor(actors.SurfaceActor(label, preset=preset, centered=centered, alpha_scale=alpha_scale))
    ren.set_camera(pos=pos, fp=fp, up=up, view=view, near=near, far=far)
    proj = ren.render(rotate_axis=rotate_axis, rotate_angles=rotate_angles, size=size, bg=bg)

    return proj


def isosurface_render(label, index=1, rgb=[0.,0.,1.], alpha=1.,
        ambient=0.3, diffuse=0.6, specular=0.05, specular_power=1,
        interp='phong', shade=True, centered=True,
        pos=[0,-1000,0], fp=[0,0,0], up=[0,0,1],
        view=30, near=100, far=3000,
        rotate_axis=2, rotate_angles=list(range(0, 360, 1)),
        size=(500,800), bg=(1.,1.,1.)):

    ren = renderer.Renderer()
    ren.add_actor(actors.IsosurfaceActor(label, index, rgb, alpha,
                            ambient, diffuse, specular, specular_power,
                            interp, shade, centered))
    ren.set_camera(pos=pos, fp=fp, up=up, view=view, near=near, far=far)
    proj = ren.render(rotate_axis=rotate_axis, rotate_angles=rotate_angles, size=size, bg=bg)

    return proj


def surface_distance_render(source, target, source_index=1, target_index=1,
        centered=True, cmap='jet', clim=None,
        pos=[0,-1000,0], fp=[0,0,0], up=[0,0,1],
        view=30, near=100, far=3000,
        rotate_axis=2, rotate_angles=list(range(0, 360, 1)),
        size=(500,800), bg=(1.,1.,1.)):

    ren = renderer.Renderer()
    ren.add_actor(actors.SurfaceDistanceActor(source, target,
                            source_index, target_index,
                            centered, cmap, clim))
    ren.set_camera(pos=pos, fp=fp, up=up, view=view, near=near, far=far)
    proj = ren.render(rotate_axis=rotate_axis, rotate_angles=rotate_angles, size=size, bg=bg)

    return proj




