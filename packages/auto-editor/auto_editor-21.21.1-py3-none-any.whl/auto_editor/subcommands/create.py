'''subcommands/create.py'''

import os
import time

def create_options(parser):
    parser.add_argument('--frame_rate', '-fps', '-r', type=float, default=30.0,
        help='set the framerate for the output video.')
    parser.add_argument('--duration', '-d', type=int, default=10,
        help='set the length of the video (in seconds).')
    parser.add_argument('--width', type=int, default=1280,
        help='set the pixel width of the video.')
    parser.add_argument('--height', type=int, default=720,
        help='set the pixel height of the video.')
    parser.add_argument('--output_file', '--output', '-o', type=str,
        default='testsrc.mp4')
    parser.add_argument('--my_ffmpeg', action='store_true',
        help='use your ffmpeg and other binaries instead of the ones packaged.')
    parser.add_argument('(input)', nargs='*',
        help='the template')
    return parser

def create(ffmpeg, theme, output, fps, duration, width, height, log):

    if(theme == []):
        log.error('You must put a theme!')

    if(len(theme) > 1):
        log.error('Only one theme at a time.')

    theme = theme[0]

    try:
        os.remove(output)
    except FileNotFoundError:
        pass

    if(theme == 'test'):
        # Create sine wav.
        ffmpeg.run(['-f', 'lavfi', '-i', 'sine=frequency=1000:duration=0.2', 'short.wav'])
        ffmpeg.run(['-i', 'short.wav', '-af', 'apad', '-t', '1', 'beep.wav']) # Pad audio.

        # Generate video with no audio.
        ffmpeg.run(['-f', 'lavfi', '-i',
            f'testsrc=duration={duration}:size={width}x{height}:rate={fps}', '-pix_fmt',
            'yuv420p', output])

        # Add empty audio channel to video.
        ffmpeg.run(['-f', 'lavfi', '-i', 'anullsrc=channel_layout=stereo:sample_rate=44100',
            '-i', output, '-c:v', 'copy', '-c:a', 'aac', '-shortest', 'pre' + output])

        # Mux Video with repeating audio.
        ffmpeg.run(['-i', 'pre' + output, '-filter_complex',
            'amovie=beep.wav:loop=0,asetpts=N/SR/TB[aud];[0:a][aud]amix[a]',
            '-map', '0:v', '-map', '[a]', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '256k',
            '-shortest', output])

        time.sleep(1)
        os.remove('short.wav')
        os.remove('beep.wav')
        os.remove('pre' + output)

    if(theme in ['white', 'black']):
        ffmpeg.run(['-f', 'lavfi', '-i',
            f'color=size={width}x{height}:rate={fps}:color={theme}', '-t', str(duration),
                output])

