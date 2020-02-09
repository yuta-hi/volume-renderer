from pyvr import isosurface_render
from pyvr.utils.video import write_video

if __name__ == '__main__':

    volume = 'original-mask.mhd'
    index = 1

    proj = isosurface_render(volume, index, pos=(0,-1200,0))
    write_video(proj, 'test.mp4')
