
import gtts
from pydub import AudioSegment
import moviepy.editor as mp
import speech_recognition 

import os

script_dir = os.path.dirname(os.path.abspath(__file__))
output_dir = os.path.join(script_dir, '..','..', 'assets', 'temp_files')

intro_dir = os.path.join(script_dir, '..','..', 'assets', 'pictures' ,'intro_empty.png')
head_sound = os.path.join(output_dir, 'head.mp3')
base_sound = os.path.join(output_dir, 'base.mp3')

minecraft = os.path.join(script_dir, '..','..', 'assets', 'random_videos', 'minecraftVideo1.mp4')


def create_sound_return_duration(text, output_path):
    tts = gtts.gTTS(text, lang='en', tld='us', slow=False)
    tts.save(output_path)
    audio = AudioSegment.from_mp3(output_path)
    faster_audio = audio.speedup(playback_speed=1.25)
    faster_audio.export(output_path, format='mp3')
    
    duration_in_ms = len(audio)  
    duration_in_seconds = duration_in_ms / 1000

    return duration_in_seconds


def create_sound(label, text, output_path):
    intro_time = create_sound_return_duration(label, output_path)
    full_time = create_sound_return_duration(text, output_path)
    return intro_time



def add_intro_and_sound(intro_time, intro_image, audio_file, video_source, output_mp4):

    video_clip = mp.VideoFileClip(video_source)
    audio_clip = mp.AudioFileClip(audio_file)
    
    intro_clip = mp.ImageClip(intro_image, duration=intro_time).set_fps(video_clip.fps)
    intro_clip = intro_clip.resize(height=400, width=500)
    
    intro_clip = intro_clip.set_position(('center', 'center'))

    final_clip = mp.CompositeVideoClip([video_clip, intro_clip.set_start(0)])

    duration = min(audio_clip.duration, final_clip.duration)
    final_clip = final_clip.subclip(0, duration).set_audio(audio_clip)

    final_clip.write_videofile(output_mp4, codec='libx264')

    return final_clip





# x = create_sound(label, (label+" "+source_text), head_sound)
# add_intro_and_sound(x[0], intro_dir, head_sound, minecraft, output_dir + r'\final.mp4')