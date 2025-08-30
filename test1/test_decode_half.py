from typing import cast
import av
from av.container import input as av_input
from common import fate_suite
from fractions import Fraction

from matplotlib import pyplot as plt
import ffmpegio as ff
from pprint import pprint

# static char buffer[20];

# static const char *ret_str(int v)
# {
#     switch (v) {
#     case AVERROR_EOF:     return "-EOF";
#     case AVERROR(EIO):    return "-EIO";
#     case AVERROR(ENOMEM): return "-ENOMEM";
#     case AVERROR(EINVAL): return "-EINVAL";
#     default:
#         snprintf(buffer, sizeof(buffer), "%2d", v);
#         return buffer;
#     }
# }

# static void ts_str(char buffer[60], int64_t ts, AVRational base)
# {
#     if (ts == AV_NOPTS_VALUE) {
#         strcpy(buffer, " NOPTS   ");
#         return;
#     }
#     ts= av_rescale_q(ts, base, (AVRational){1, 1000000});
#     snprintf(buffer, 60, "%c%"PRId64".%06"PRId64"", ts<0 ? '-' : ' ', FFABS(ts)/1000000, FFABS(ts)%1000000);
# }

# filename = fate_suite("h264/interlaced_crop.mp4")
filename = "test1/rawvideo_pal8.avi"
seekforw = None
seekback = None
seekfirstf = 0.5
firstback = True

pprint(ff.probe.full_details(filename))

nframes = 126
stfps = 25
sttb = Fraction(1, 25)

with av.open(filename) as fmt:  # AVFormatContext
    ic = cast(av_input.InputContainer, fmt)

    seekfirst = round(seekfirstf * cast(int, ic.duration))
    print(seekfirst, av.time_base, Fraction(seekfirst, av.time_base))

    # int i, ret, stream_id;
    # int j;
    # int64_t timestamp;
    # AVDictionary *format_opts = NULL;
    # int64_t seekfirst = AV_NOPTS_VALUE;
    # int firstback=0;
    # int frame_count = 1;
    # int duration = 4;

    #     } else if(!strcmp(argv[i], "-frames")){
    #         frame_count = atoi(argv[i+1]);
    #     } else if(!strcmp(argv[i], "-duration")){
    #         duration = atoi(argv[i+1]);
    #     } else if(!strcmp(argv[i], "-fastseek")) {
    #         if (atoi(argv[i+1])) {
    #             ic->flags |= AVFMT_FLAG_FAST_SEEK;
    #         }
    #     } else if(argv[i][0] == '-' && argv[i+1]) {
    #         av_dict_set(&format_opts, argv[i] + 1, argv[i+1], 0);
    #     } else {
    #         argc = 1;
    #     }
    # }

    # av_dict_set(&format_opts, "ch_layout", "mono", 0);
    # av_dict_set(&format_opts, "sample_rate", "22050", 0);

    # ret = avformat_open_input(&ic, filename, NULL, &format_opts);
    # ret = avformat_find_stream_info(ic, NULL);

    ic.seek(seekfirst)
    # if seekfirst:
    #     print(seekfirst)
    #     if firstback:
    #         ic.seek2(seekfirst, max_ts=seekfirst)
    #     else:
    #         ic.seek2(seekfirst, min_ts=seekfirst)

    for pkt in ic.demux():

        # AVPacket pkt = { 0 };
        # AVStream *av_uninit(st);

        # for (j=0; j<frame_count; j++) {
        # ret= av_read_frame(ic, &pkt);

        # st = pkt.stream
        # tb = pkt.time_base.denominator

        frms = pkt.decode()
        # print(
        #     f"st:{pkt.stream_index} dts:{pkt.dts}/{tb} pts:{pkt.pts}/{tb} pos:{pkt.pos} size:{pkt.size}, frames: {len(frms)}"
        # )
        # print(frms)
        for frm in frms:
            print(f"   frame pts: {frm.pts}")

            plt.imshow(frm.to_ndarray(format="rgb24"))
            plt.show()
        #     exit()

    # if(i>25) break;

    # stream_id= (i>>1)%(ic->nb_streams+1) - 1;
    # timestamp= (i*19362894167LL) % (duration*AV_TIME_BASE) - AV_TIME_BASE;
    # if(stream_id>=0){
    #     st= ic->streams[stream_id];
    #     timestamp= av_rescale_q(timestamp, AV_TIME_BASE_Q, st->time_base);
    # }
    # //FIXME fully test the new seek API
    # if(i&1) ret = avformat_seek_file(ic, stream_id, INT64_MIN, timestamp, timestamp, 0);
    # else    ret = avformat_seek_file(ic, stream_id, timestamp, timestamp, INT64_MAX, 0);
    # ts_str(ts_buf, timestamp, stream_id < 0 ? AV_TIME_BASE_Q : st->time_base);
    # printf("ret:%-10s st:%2d flags:%d  ts:%s\n", ret_str(ret), stream_id, i&1, ts_buf);

    ic.seek(seekfirst)
    # if seekfirst:
    #     print(seekfirst)
    #     if firstback:
    #         ic.seek2(seekfirst, max_ts=seekfirst)
    #     else:
    #         ic.seek2(seekfirst, min_ts=seekfirst)

    st = ic.streams.video[0]
    for frm in ic.decode():

        tb = frm.time_base.denominator

        print(f"st:{st.index} dts:{frm.dts}/{tb} pts:{frm.pts}/{tb}")
