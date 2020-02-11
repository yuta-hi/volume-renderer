from pyvr.renderer import InteractiveRenderer
from pyvr.renderer import InteractiveMultiViewRenderer
from pyvr.actors import VolumeActor

def test(renderer):

    volume = 'original-image.mhd'

    renderer.set_camera(pos=(0,-1200,0))
    renderer.add_actor(VolumeActor(volume, 'bone'))
    renderer.add_actor(VolumeActor(volume, 'muscle'))
    renderer.render(bg=(1,1,1))

if __name__ == '__main__':

    test(InteractiveRenderer())
    test(InteractiveMultiViewRenderer())

