from __future__ import absolute_import

import vtk

def euler_transform(trans=[0,0,0], rot=[0,0,0]):

    assert len(trans) == 3
    assert len(rot) == 3

    transform = vtk.vtkTransform()
    transform.PostMultiply()
    transform.Identity()
    transform.Translate(trans[0], trans[1], trans[2])
    transform.RotateX(rot[0])
    transform.RotateY(rot[1])
    transform.RotateZ(rot[2])
    transform.Update()

    return transform


def centered_transform(image):

    assert isinstance(image, vtk.vtkImageData)

    center = [0]*3
    bounds = image.GetBounds()
    for i in range(len(center)):
        center[i] = (bounds[i*2 + 1] - bounds[i*2]) / 2.0
    transform = vtk.vtkTransform()
    transform.Translate(-center[0], -center[1], -center[2])
    transform.Update()

    return transform
