from pyvr import surface_distance_render
from pyvr.utils.video import write_video

if __name__ == '__main__':

    source = 'original-mask.mhd'
    target = 'original-mask.mhd'

    source_index = 5
    target_index = 6

    clim = (0, 10)

    proj = surface_distance_render(source, target, source_index, target_index, clim=clim, pos=(0,-1200,0))
    write_video(proj, 'test.mp4')
