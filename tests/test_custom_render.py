from pyvr.renderer import Renderer
from pyvr.actors import IsosurfaceActor
from pyvr.actors import SurfaceDistanceActor
from pyvr.utils.video import write_video


def _surface_distance_render(source, target, source_index, target_index, clim=[0,10], rotate_angles=list(range(0, 360, 1)), bg=[1.,1.,1.]):
    renderer = Renderer()
    renderer.set_camera(pos=(0,-1200,0))
    renderer.add_actor(IsosurfaceActor(source, index=1, rgb=[1.,1.,1.], alpha=0.3))
    renderer.add_actor(IsosurfaceActor(source, index=2, rgb=[1.,1.,1.], alpha=0.3))
    renderer.add_actor(IsosurfaceActor(source, index=22, rgb=[0.5,0.5,0.5], alpha=0.3))
    renderer.add_actor(SurfaceDistanceActor(source, target, source_index, target_index, clim=clim))
    proj = renderer.render(rotate_angles=rotate_angles, bg=bg)
    return proj


if __name__ == '__main__':

    source = 'original-mask.mhd'
    target = 'original-mask.mhd'

    source_index = 5
    target_index = 6

    proj = _surface_distance_render(source, target, source_index, target_index)
    write_video(proj, 'test.mp4')
