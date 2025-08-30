from fractions import Fraction

import numpy as np
import av

from av.container import input as av_input
from matplotlib import pyplot as plt

import logging


logging.getLogger("matplotlib").setLevel(logging.WARNING)
logging.basicConfig(level=logging.DEBUG)

avifile = "test1/rawvideo_pal8.avi"

# import ffmpegio as ff

# ff.transcode(
#     "testsrc=duration=5.3:size=qcif:rate=10",
#     avifile,
#     f_in="lavfi",
#     vcodec="rawvideo",
#     pix_fmt="pal8",
#     g=1,
#     overwrite=True,
# )
# print(ff.probe.video_streams_basic(avifile))

seek_first = False
with av.open(avifile) as fmt:
    vst = fmt.streams.video[0]
    if seek_first:
        fmt.seek(0, stream=vst, backward=True, any_frame=False)
    
    iterpackets = fmt.demux()

    for pkt  in iterpackets:
        print(pkt.pts,pkt.dts)
        print(pkt.palette())
    # iterframes = fmt.decode(video=0)
    # frame = next(iterframes)

    # frame.data

        exit()
    # for frame in iterframes:
    #     data = frame.to_ndarray(format="rgb24")

    #     print(frame.pts, np.any(data!=0)) # errors out only if seek_first=True



# seek_first = True
# with av.open(avifile) as fmt:
#     print(hex(fmt.flags))
#     vst = fmt.streams.video[0]
#     # if seek_first:
#     #     fmt.seek(0, stream=vst, backward=True, any_frame=False)
#     for i, pkt in zip(range(10), fmt.decode(video=0)):
#         ...
#     frame = next(fmt.decode(video=0))
#     data = frame.to_ndarray(format="gray")
#     assert np.any(data != 0)


plt.imshow(data)
plt.show()
