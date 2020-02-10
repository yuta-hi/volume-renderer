from pyvr.renderer import Renderer
from pyvr.actors import VolumeActor
from pyvr.actors import LandmarkActor
from pyvr.utils.video import write_video

if __name__ == '__main__':

    volume = 'original-image.mhd'

    renderer = Renderer()
    renderer.set_camera(pos=(0,-1200,0))
    renderer.add_actor(VolumeActor(volume, 'bone'))
    renderer.add_actor(LandmarkActor((99.658,-53.036,-195.258), 10, rgb=(1,0,0)))
    renderer.add_actor(LandmarkActor((-105.237,-57.957,-188.071), 10, rgb=(0,1,0)))
    renderer.add_actor(LandmarkActor((0.753,-52.335,-105.167), 10, rgb=(0,0,1)))
    proj = renderer.render(rotate_angles=list(range(0,360,1)), bg=(1,1,1))

    write_video(proj, 'test.mp4')
