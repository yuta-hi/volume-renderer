from pyvr import volume_render
from pyvr.utils.video import write_video

if __name__ == '__main__':

    volume = 'original-image.mhd'
    preset = 'skelton'

    proj = volume_render(volume, preset, pos=(0,-1200,0), bg=(0,0,0))
    write_video(proj, 'test.mp4')
