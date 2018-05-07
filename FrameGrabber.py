import subprocess as sp
import numpy
import cv2
import re

FFMPEG_BIN = "ffmpeg"


class FrameGrabber():
    def __init__(self, fp, verbose=False):
        self.fp = fp

        self.infos = ffmpeg_parse_info(fp, fps_source='fps')

        if verbose:
            print(self.infos)

        self.command = [
            FFMPEG_BIN, '-i', fp, '-f', 'image2pipe', '-pix_fmt', 'rgb24',
            '-vcodec', 'rawvideo', '-'
        ]

        self.pipe = sp.Popen(
            self.command, stderr=sp.PIPE, stdout=sp.PIPE, bufsize=10**8)

        self.position = 0

    def next(self):
        # read w*h*3 bytes (= 1 frame)
        nbytes = self.get_size()[0] * self.get_size()[1] * 3
        raw_image = self.pipe.stdout.read(nbytes)
        if len(raw_image) != nbytes:

            # either the pipe was empty or the file was corrupted
            return None

        # transform the byte read into a numpy array
        image = numpy.fromstring(raw_image, dtype='uint8')
        image = image.reshape((self.get_size()[1], self.get_size()[0], 3))
        # throw away the data in the pipe's buffer.
        self.pipe.stdout.flush()

        self.position += 1

        return image

    def previous(self, framestoskip=0):
        if self.position > (framestoskip + 1):
            self.set_position(self.position - (1 + framestoskip))
            return self.next()
        else:
            self.set_position(0)
            return self.next()

    def skip_frames(self, n=1):
        nbytes = self.get_size()[0] * self.get_size()[1] * 3

        for i in range(n):
            self.pipe.stdout.read(nbytes)

        # throw away the data in the pipe's buffer.
        self.pipe.stdout.flush()
        self.position += n

    def get_frame(self, idx):

        self.set_position(idx)
        return self.next()

    def set_position(self, position):
        if position <= 0:
            self.reset()
        elif position < self.position:
            # you can't go back in the pipe, so must reset and start from beginning
            self.reset()
            self.skip_frames(position-1)

        else:
            # skip until the given position
            self.skip_frames(position - self.position)

    def get_position(self):
        return self.position

    def set_time(self, time):
        position = self.get_fps() * time

        self.set_position(position)

    def reset(self):
        self.terminate()

        self.pipe = sp.Popen(
            self.command, stderr=sp.PIPE, stdout=sp.PIPE, bufsize=10**8)
        self.position = 0

    def terminate(self):
        self.pipe.terminate()
        self.pipe.stdout.close()
        self.pipe.stderr.close()
        self.pipe.wait()
        self.pipe = None

    def get_duration(self):
        return self.infos['duration']

    def get_fps(self):
        return self.infos['video_fps']

    def get_nframes(self):
        return self.infos['video_nframes']

    def get_size(self):
        return self.infos['video_size']


def ffmpeg_parse_info(fp, check_duration=True, fps_source='tbr'):
    command = [
        FFMPEG_BIN, '-i', fp
    ]  # ffmpeg will give an error that you need to provide an output file, but that's not necessary here. The info is still there.
    pipe = sp.Popen(command, stderr=sp.PIPE, stdout=sp.PIPE)
    pipe.stdout.readline()
    pipe.terminate()
    infos = pipe.stderr.read()

    lines = infos.splitlines()
    if b'No such file or directory' in lines[-1]:
        raise IOError(("The file %s could not be found!\n"
                       "Please check that you entered the correct "
                       "path.") % fp)

    result = dict()

    # get duration (in seconds)
    result['duration'] = None

    if check_duration:
        try:
            keyword = b'Duration: '
            index = 0
            line = [l for l in lines if keyword in l][index]
            match = re.findall(b'([0-9][0-9]:[0-9][0-9]:[0-9][0-9].[0-9][0-9])',
                               line)[0]
            ftr = [3600, 60, 1]

            result['duration'] = sum(
                [a * b for a, b in zip(ftr, map(float, match.split(b':')))])
        except:
            raise IOError(
                ("MoviePy error: failed to read the duration of file %s.\n"
                 "Here are the file infos returned by ffmpeg:\n\n%s") %
                (fp, infos))

    # get the output line that speaks about video
    lines_video = [
        l for l in lines if b' Video: ' in l and re.search(b'\d+x\d+', l)
    ]

    result['video_found'] = (lines_video != [])

    if result['video_found']:
        try:
            line = lines_video[0]

            # get the size, of the form 460x320 (w x h)
            match = re.search(b'[0-9]*x[0-9]*(,| )', line)
            s = list(map(int, line[match.start():match.end() - 1].split(b'x')))
            result['video_size'] = s
        except:
            raise IOError(
                ("Failed to read video dimensions in file %s.\n"
                 "Here are the file infos returned by ffmpeg:\n\n%s") %
                (fp, infos))

        # Get the frame rate. Sometimes it's 'tbr', sometimes 'fps', sometimes
        # tbc, and sometimes tbc/2...
        # Current policy: Trust tbr first, then fps unless fps_source is
        # specified as 'fps' in which case try fps then tbr

        # If result is near from x*1000/1001 where x is 23,24,25,50,
        # replace by x*1000/1001 (very common case for the fps).

        def get_tbr():
            match = re.search(b'( [0-9]*.| )[0-9]* tbr', line)

            # Sometimes comes as e.g. 12k. We need to replace that with 12000.
            s_tbr = line[match.start():match.end()].split(b' ')[1]
            if b'k' in s_tbr:
                tbr = float(s_tbr.replace(b'k', b'')) * 1000
            else:
                tbr = float(s_tbr)
            return tbr

        def get_fps():
            match = re.search(b'( [0-9]*.| )[0-9]* fps', line)
            fps = float(line[match.start():match.end()].split(' ')[1])
            return fps

        if fps_source == 'tbr':
            try:
                result['video_fps'] = get_tbr()
            except:
                result['video_fps'] = get_fps()

        elif fps_source == 'fps':
            try:
                result['video_fps'] = get_fps()
            except:
                result['video_fps'] = get_tbr()

        # It is known that a fps of 24 is often written as 24000/1001
        # but then ffmpeg nicely rounds it to 23.98, which we hate.
        coef = 1000.0 / 1001.0
        fps = result['video_fps']
        for x in [23, 24, 25, 30, 50]:
            if (fps != x) and abs(fps - x * coef) < .01:
                result['video_fps'] = x * coef

        if check_duration:
            result['video_nframes'] = int(
                result['duration'] * result['video_fps']) + 1
            result['video_duration'] = result['duration']
        else:
            result['video_nframes'] = 1
            result['video_duration'] = None

    return result
