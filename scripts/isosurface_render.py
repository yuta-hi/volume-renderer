#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import argparse

from pyvr import isosurface_render
from pyvr.utils.video import write_video

def main():

    parser = argparse.ArgumentParser(description='Isosurface render',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--volume', '-v', type=str, help='path to volume file (.mhd)', required=True)
    parser.add_argument('--index', '-i', type=int, help='the isosurface value', required=True)
    parser.add_argument('--out', '-o', type=str, help='path to output video file (.mp4)', required=True)
    parser.add_argument('--rgb', type=float, nargs=3, default=[0,0,1], help='color for the isosurface')
    parser.add_argument('--alpha', type=float, default=1., help='opacity for the isosurface')
    parser.add_argument('--ambient', type=float, default=0.3, help='ambient lighting coefficient')
    parser.add_argument('--diffuse', type=float, default=0.6, help='diffuse lighting coefficient')
    parser.add_argument('--specular', type=float, default=0.05, help='specular lighting coefficient')
    parser.add_argument('--specular_power', type=float, default=1., help='specular power')
    parser.add_argument('--interp', type=str, default='phong', help='shading method')
    parser.add_argument('--no_shade', '-ns', action='store_false', help='disable the shading')
    parser.add_argument('--no_centered', '-nc', action='store_false', help='disable the centering of volume')
    parser.add_argument('--pos', type=float, nargs=3, default=[0,-1000,0], help='position for the camera')
    parser.add_argument('--fp', type=float, nargs=3, default=[0,0,0], help='focal point for the camera')
    parser.add_argument('--up', type=float, nargs=3, default=[0,0,1], help='view up direction for the camera')
    parser.add_argument('--view', type=float, default=30, help='view angle for the camera')
    parser.add_argument('--near', type=float, default=100., help='near clipping plane for the camera')
    parser.add_argument('--far', type=float, default=3000., help='far clipping plane for the camera')
    parser.add_argument('--rotate_axis', '-axis', type=int, default=2., metavar='AXIS', help='rotation axis for the camera')
    parser.add_argument('--rotate_angles', '-angle', type=int, nargs=3, metavar='ANGLE', default=[0,360,1], help='rotation angles for the camera')
    parser.add_argument('--size', '-sz', type=float, nargs=2, default=[500,800], help='window size')
    parser.add_argument('--bg', type=float, nargs=3, default=[1.,1.,1.], help='background color')
    parser.add_argument('--rate', '-r', type=str, default='30/1', help='frame rate for the video')
    parser.add_argument('--vcodec', type=str, default='libx264', help='codec for the video')
    parser.add_argument('--pix_fmt', type=str, default='yuv420p', help='pixel format for the video')
    args = parser.parse_args()

    proj = isosurface_render(args.volume, args.index, rgb=args.rgb, alpha=args.alpha,
                    ambient=args.ambient, diffuse=args.diffuse, specular=args.specular, specular_power=args.specular_power,
                    interp=args.interp, shade=args.no_shade, centered=args.no_centered,
                    pos=args.pos, fp=args.fp, up=args.up,
                    view=args.view, near=args.near, far=args.far,
                    rotate_axis=args.rotate_axis, rotate_angles=list(range(*args.rotate_angles)),
                    size=args.size, bg=args.bg)

    out_dir = os.path.dirname(args.out)

    if out_dir != '':
        os.makedirs(out_dir, exist_ok=True)

    write_video(proj, args.out, args.rate, args.vcodec, args.pix_fmt)


if __name__ == '__main__':
    sys.exit(main())
