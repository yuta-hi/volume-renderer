from pyvr.renderer import Renderer
from pyvr.actors import LandmarkActor
from pyvr.actors import BoundingBoxActor
from pyvr.utils.video import write_video

if __name__ == '__main__':

    renderer = Renderer()
    renderer.set_camera(pos=(0,-1200,0))
    renderer.add_actor(LandmarkActor((100,100,100), 50, rgb=(1,0,0)))
    renderer.add_actor(BoundingBoxActor((50,50,50), (150,150,150), rgb=(0,1,0)))
    proj = renderer.render(rotate_angles=list(range(0,360,1)), bg=(1,1,1))

    write_video(proj, 'test.mp4')
