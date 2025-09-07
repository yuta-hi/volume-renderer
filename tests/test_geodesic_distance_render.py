from pyvr.renderer import Renderer
from pyvr.actors import VolumeActor
from pyvr.actors import GeodesicDistanceActor
from pyvr.actors import LandmarkActor
from pyvr.utils.video import write_video

if __name__ == '__main__':

    volume = 'original-mask.mhd'
    query_point = (99.658,-53.036,-195.258)

    renderer = Renderer()
    renderer.set_camera(pos=(0,-1200,0))
    renderer.add_actor(GeodesicDistanceActor(volume, query_point,  1))
    renderer.add_actor(LandmarkActor(query_point, 10, rgb=(1,0,0)))
    proj = renderer.render(rotate_angles=list(range(0,360,1)), bg=(1,1,1))

    write_video(proj, 'test.mp4')
