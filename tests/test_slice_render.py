from pyvr.renderer import Renderer
from pyvr.actors import VolumeActor
from pyvr.actors import SliceActor
from pyvr.data.volume import load_volume
from pyvr.utils.video import write_video

if __name__ == '__main__':

    volume_file = 'original-image.mhd'

    volume = load_volume(volume_file)
    clim = (-150, 350)

    renderer = Renderer()
    renderer.set_camera(pos=(0,-1200,0))
    renderer.add_actor(VolumeActor(volume, 'bone'))
    renderer.add_actor(SliceActor(volume, normal=(1,0,0), clim=clim))
    renderer.add_actor(SliceActor(volume, normal=(0,1,0), clim=clim))
    renderer.add_actor(SliceActor(volume, normal=(0,0,1), clim=clim))
    proj = renderer.render(rotate_angles=list(range(0,360,1)), bg=(1,1,1))

    write_video(proj, 'test.mp4')
