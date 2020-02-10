from pyvr.renderer import Renderer
from pyvr.actors import LandmarkActor
from pyvr.utils.video import write_video

import vtk

if __name__ == '__main__':

    axes = vtk.vtkCubeAxesActor()
    axes.SetTotalLength(50, 50, 50)
    axes.AxisLabelsOff()

    renderer = Renderer()
    renderer.set_camera(pos=(0,-1200,0))
    renderer.add_actor(LandmarkActor((100,100,100), 10, rgb=(0,1,0)))
    renderer.add_actor(axes)
    proj = renderer.render(rotate_angles=list(range(0,360,1)), bg=(1,1,1))

    write_video(proj, 'test.mp4')
