from __future__ import absolute_import

import skvideo
import skvideo.io

def write_video(images, out, rate='30/1', vcodec='libx264', pix_fmt='yuv420p'):

    writer = skvideo.io.FFmpegWriter(
        out,
        inputdict={
        '-r': rate,
        },
        outputdict={
        '-vcodec': vcodec,
        '-pix_fmt': pix_fmt,
        '-r': rate,
    })

    for image in images:
        writer.writeFrame(image)

    writer.close()
