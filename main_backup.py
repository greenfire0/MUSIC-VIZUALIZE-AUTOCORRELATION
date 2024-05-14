import matplotlib
matplotlib.use('TkAgg')
from audio import test_moviepy
from video import make_video,del_img
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
from scipy.fftpack import fft
import wave
from scipy import signal
import statsmodels.api as sm
import sys
from helper import *

if __name__ == '__main__':
    
    commands = sys.argv[1:]

    if len(commands) == 0:
        print("Invalid arguments type help in arguments to learn more")
        quit()
    # ------------ HELP MENU ---------------
    if "help" in commands:
        print("\n\nThe formatting to run the program is as follows:")
        print("The first arg should be a path to the audio file! Make sure that it is the full path")
        print("\n-------------FLAGS-------------\n")

        print("You can also specify if you would like smoothing on the FFT graph") 
        print("You can do this by putting a -S in the command line") 
        quit()

    if ".mp3" in commands[0] or ".MP3" in commands[0]:
        print("Converting MP3 to wav")
        convert(commands[0])
        commands[0] = "test.wav"
    if "-S" in commands or "-s" in commands:
        SMOOTH = True
    else:
        SMOOTH = False


    try:
        print(commands[0].replace("\\","\\\\"))
        wave.open(commands[0], 'rb')
        filename = [commands[0]]

    except:
        print("Invalid File name try again or use type help in the arguments")
        quit()
    


# ------------ Audio Setup ---------------
wf = wave.open(filename[0], 'rb')

FPS_static = 30
SPS = wf.getframerate()  # samples per second
CHUNK = wf.getframerate()//FPS_static         
lags = 100
count = [0]


#wz = wave.open(filename[0], 'rb')
#with wave.open(filename[0]) as mywav:
#    duration_seconds = mywav.getnframes() // mywav.getframerate()

#file_data = np.fromstring(wz.readframes(wf.getframerate()*duration_seconds), dtype=np.int16)
#print(len(file_data))
#(0+count[0]*chunk):(sps*2*chunk)


# ------------ Plot Setup ---------------
fig, (a,b,c) = plt.subplots(3, figsize=(15, 7))


x = np.arange(0, 2 * CHUNK, 2)       # samples (waveform)
xf = np.linspace(0, SPS, CHUNK//2)     # frequencies (spectrum)
xa = np.arange(0, lags*2, 2)       # samples (waveform)


##setup for amplitude
r = 2**16/2 # Signal range is -32k to 32k
a.set_ylim([-r, r])
a.set_xlabel('time [s]')
a.set_ylabel('sample value [-]')
line, = a.plot(x, np.random.rand(CHUNK), '-', lw=2)


b.set_xscale('log') ##setup for fft
b.set_ylim([0,5000000])
b.set_xlabel('frequency [Hz]')
b.set_ylabel('|amplitude|')
line2, = b.plot(xf, np.random.rand(CHUNK//2), '-', lw=2)


c.set_ylim([-1, 1]) ##setup for acor
a.set_xlabel('time [s]')
a.set_ylabel('Correlation')
line3, = c.plot(xa, '-', lw=2)


def ticks(x,c):
    out = []
    out.append(0)
    for a in range(x):
       out.append(round(((1/FPS_static)*(a+(c*x))/x),3))
    return out


def animate(i):
            count[0] += 1
            da = np.fromstring(wf.readframes(CHUNK), dtype=np.int16)
            if len(da) ==(2*CHUNK):
                left= da[0::2]
                
                lf = abs(np.fft.rfft(left))
                plt.figure(1)

                #(0.03333333333/7)*0, ,2,3,4,5,6,7 calc for x tick labelse for seconds
                a.set_xticklabels((ticks(7,count[0])))
                #a.set_xticklabels(("", (((0+count[0]) * CHUNK))//7,(((2+count[0]) * CHUNK))//7,(((4+count[0]) * CHUNK))//7,(((6+count[0]) * CHUNK))//7,(((7+count[0]) * CHUNK))//7,(((10+count[0]) * CHUNK))//7,(((12+count[0]) * CHUNK))//7,(((14+count[0]) * CHUNK))//7))        
                ###adjust plot 1 x label so that it lines up with whrere it is in audio file just basically do + chunk every tiume
                line.set_ydata(left) ##amplitude
                if SMOOTH:
                    lf = signal.savgol_filter(lf, window_length=9, polyorder=3, mode="nearest")

                c.set_xticklabels((ticks(10,count[0])))
                line2.set_ydata(lf[1:]) ##fft
                line3.set_ydata(quick_acor(left,lags=lags))
                #plt.plot(lf)
                plt.savefig('C:\\Users\\Miles\\Desktop\\Proj\\enhanced-visualizer\\tmp\\plt__'+str(1000+count[0])+'.png')
                
            elif (len(da) ==0):
                  close()

def start_graph():
    
    anim = animation.FuncAnimation(fig, animate, blit=False, interval=1)
    fig.canvas.mpl_connect('close_event', on_close) ### triggers when you close the graph
    plt.show()

def on_close(event):
    ##when program gets manually closed
    print('\n\nClosed Figure!\n\n')
    del_img()
    quit()
def close():

    
    print('stream stopped')

    make_video(audio_filename=filename[0])
    del_img()

    quit()

start_graph()