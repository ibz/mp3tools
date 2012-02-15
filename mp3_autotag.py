#!/usr/bin/env python

__doc__ = """Usage: %s directory [compilation]""" % __file__

import os
import re
import sys

import tagger

file_re = re.compile(r"^(\d{2}). (.*).mp3$")

def new_text_frame(id3v2, id, text):
    frame = id3v2.new_frame(id)
    frame.set_text(text)
    return frame

def main(directory, compilation):
    filenames = [f for f in os.listdir(directory) if file_re.match(f)]
    fileinfos = [file_re.match(f).groups() for f in filenames]
    if not compilation:
        artist = os.path.basename(os.path.abspath(os.path.join(directory, os.path.pardir)))
    album = os.path.basename(os.path.abspath(directory))
    track_count = len(filenames)
    for filename, fileinfo in zip(filenames, fileinfos):
        filename = os.path.join(directory, filename)
        track, title = fileinfo
        if compilation:
            artist, title = title.split(" - ", 1)
        tagger.ID3v1(filename).remove_and_commit()
        id3v2 = tagger.ID3v2(filename)
        id3v2.frames = [new_text_frame(id3v2, "TPE1", artist),
                        new_text_frame(id3v2, "TALB", album),
                        new_text_frame(id3v2, "TIT2", title),
                        new_text_frame(id3v2, "TRCK", "%s/%02d" % (track, track_count)),
                        new_text_frame(id3v2, "TPOS", "01/01")]
        id3v2.commit()
        print "artist: '%s', album: '%s', title: '%s', track: '%s'" % (artist, album, title, "%s/%02d" % (track, track_count))

if __name__ == '__main__':
    if len(sys.argv) not in [2, 3]:
        print __doc__
    else:
        directory = sys.argv[1]
        compilation = len(sys.argv) == 3 and sys.argv[2] == 'compilation'
        main(directory, compilation)
