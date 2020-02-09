from __future__ import absolute_import

import vtk

def centered_camera(pos=[0,-1000,0], fp=[0,0,0], up=[0,0,-1], view=30, near=100, far=3000):

    assert len(pos) == 3
    assert len(fp) == 3
    assert len(up) == 3

    camera = vtk.vtkCamera()
    camera.SetViewUp(up[0], up[1], up[2])
    camera.SetPosition(pos[0], pos[1], pos[2])
    camera.SetFocalPoint(fp[0], fp[1], fp[2])
    camera.ComputeViewPlaneNormal()
    camera.SetViewAngle(view)
    camera.ParallelProjectionOff()
    camera.SetClippingRange(near, far)

    return camera
