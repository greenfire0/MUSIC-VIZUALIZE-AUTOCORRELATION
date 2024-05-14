import statsmodels.api as sm
from os import path
from pydub import AudioSegment
def acor(data,lags):
    lags = range(lags)

    acorr = len(lags) * [0]

    # Mean
    mean = sum(data) / len(data) 

    # Variance
    var = sum([(x - mean)**2 for x in data]) / len(data) 

    # Normalized data
    ndata = [x - mean for x in data]


    # Go through lag components one-by-one
    for l in lags:
        c = 1 # Self correlation
        
        if (l > 0):
            tmp = [ndata[l:][i] * ndata[:-l][i] 
                for i in range(len(data) - l)]
            
            c = sum(tmp) / len(data) / var
            
        acorr[l] = c

    return acorr
def quick_acor(data,lags):
        return sm.tsa.acf(data, nlags = (lags))[1:]
def convert(path):                                           
    src = path
    dst = "test.wav"                                                         
    sound = AudioSegment.from_mp3(src)
    sound.export(dst, format="wav")
def add_audio(fps1, audio_path, video_path = 'MY_video.mp4', output_path='output-moviepy1.mp4'):
    import moviepy.editor as mpe
    print('--- moviepy ---')
    print("fps:"+ str(fps1))
    video = mpe.VideoFileClip(video_path)
    video = video.set_audio(mpe.AudioFileClip(audio_path))
    video.write_videofile(output_path, fps=fps1)


