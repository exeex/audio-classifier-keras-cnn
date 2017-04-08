from __future__ import unicode_literals
import youtube_dl
import os


filenames = []

class MyLogger(object):
    def debug(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        print(msg)



def my_hook(d):
    if d['status'] == 'finished':
        print('Done downloading, now converting ...')

        name = d['filename']

        r = name.split('-')[-1].split('.')[0]+'.mp3'


        namesplit = name.split('-')
        namesplit[-1]= r

        newname = "-".join(namesplit)

        filenames.append(newname)


ydl_opts = {
    'format': 'bestaudio/best',
    'noplaylist': 'True',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
    ''
    'logger': MyLogger(),
    'progress_hooks': [my_hook],
}





def ydownload(filelist,songname):
    filenames.clear()
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download(filelist)
    for idx,file in enumerate(filenames):
        os.rename(filenames[idx],str(idx+1)+songname[idx]+'.mp3')