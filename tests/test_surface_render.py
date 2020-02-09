from pyvr import surface_render
from pyvr.utils.video import write_video

if __name__ == '__main__':

    volume = 'original-mask.mhd'
    preset = 'muscle'

    proj = surface_render(volume, preset, pos=(0,-1200,0))
    write_video(proj, 'test.mp4')
