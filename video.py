import shutil
import os
import moviepy.video.io.ImageSequenceClip
from PIL import Image
from helper import add_audio

def make_video(audio_filename,video_name = 'my_video.MP4'):
    image_folder = os.path.join(os.getcwd(),"tmp")

    fps = 30
    print("fps:"+ str(fps))


    image_files = [os.path.join(image_folder,img)
                for img in os.listdir(image_folder)
                if img.endswith(".png")]


    image_files.pop() # occcasionally prevents bugs
    image_files.pop() #matplotlib generates an extra frame so we have to remove it
    print("Immage count= "+ str(len(image_files)))

    image_files.sort()
    clip = moviepy.video.io.ImageSequenceClip.ImageSequenceClip(image_files, fps=fps)
    clip.write_videofile(video_name)
    add_audio(fps1=fps,audio_path=audio_filename)

def del_img():
    dir = os.path.join(os.getcwd(),"tmp")
    if os.path.exists(dir):
        shutil.rmtree(dir)
    os.makedirs(dir)

if __name__ == '__main__':
    song_name = "Crosstal.wav"
    path = os.path.join(os.getcwd(),"Sound_Proj\Proj",song_name)
    print("The Path is: " + path)
    make_video(path)