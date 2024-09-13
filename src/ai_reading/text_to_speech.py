import math
import ffmpeg
import gtts
from pydub import AudioSegment
import moviepy.editor as mp
import speech_recognition as sr
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import os
from faster_whisper import WhisperModel
# Create TTS audio and speed it up

source_text = """
I wrote a list of things I suspected my new boss was lying about and she saw it. This happened a year ago but it still plagues me and I need to get it off my chest.
"""
script_dir = os.path.dirname(os.path.abspath(__file__))
output_dir = os.path.join(script_dir, '..','..', 'assets', 'temp_files')
base_sound = os.path.join(output_dir, 'base.mp3')
base_video = os.path.join(output_dir, 'white.mp4')


    
tts = gtts.gTTS(source_text, lang='en', tld='us', slow=False)
tts.save(base_sound)

audio = AudioSegment.from_mp3(base_sound)
faster_audio = audio.speedup(playback_speed=1.25)
faster_audio.export(base_sound, format='mp3')

# Create Wav audio 
def extract_audio(input_video_name, output_wav_name):
    extracted_audio = f"{output_wav_name}\pureSounds.wav"
    stream = ffmpeg.input(input_video_name)
    stream = ffmpeg.output(stream, extracted_audio)
    ffmpeg.run(stream, overwrite_output=True)
    return extracted_audio

# Create a white screen video and add the audio
def create_white_video_with_audio(audio_file, output_mp4):
    audio_clip = mp.AudioFileClip(audio_file)
    duration = audio_clip.duration
    vertical_clip = mp.ColorClip(size=(1920, 1080), color=(100, 100, 100), duration=duration)
    final_video = vertical_clip.set_audio(audio_clip)
    final_video.write_videofile(output_mp4, fps=24)

def transcribe(audio):
    model = WhisperModel("small",device="cpu")
    segments, info = model.transcribe(audio)
    language = info[0]
    segments = list(segments)
    for segment in segments:
        # print(segment)
        print("[%.2fs -> %.2fs] %s" %
              (segment.start, segment.end, segment.text))
    
    return segments

def format_time(seconds):

    hours = math.floor(seconds / 3600)
    seconds %= 3600
    minutes = math.floor(seconds / 60)
    seconds %= 60
    milliseconds = round((seconds - math.floor(seconds)) * 1000)
    seconds = math.floor(seconds)
    formatted_time = f"{hours:02d}:{minutes:02d}:{seconds:01d},{milliseconds:03d}"

    return formatted_time

def generate_subtitle_file(output_dir, segments):

    subtitle_file = f"{output_dir}\subtitle.srt"
    text = ""
    for index, segment in enumerate(segments):
        segment_start = format_time(segment.start)
        segment_end = format_time(segment.end)
        text += f"{str(index+1)} \n"
        text += f"{segment_start} --> {segment_end} \n"
        text += f"{segment.text} \n"
        text += "\n"
        
    f = open(subtitle_file, "w")
    f.write(text)
    f.close()

    return subtitle_file


import ffmpeg

import ffmpeg

import ffmpeg
import os

def add_subtitle_to_video(soft_subtitle, subtitle_file, subtitle_language, output_dir, input_video):
    # Construct the paths

    video_input_stream = ffmpeg.input(input_video)
    subtitle_input_stream = ffmpeg.input(subtitle_file)
    output_vid = fr"{output_dir}\result.mp4"
    subtitle_track_title = subtitle_file.replace(".srt", "")

    # Add the subtitle track
    if soft_subtitle:
        stream = ffmpeg.output(
            video_input_stream, subtitle_input_stream, output_vid, **{"c": "copy", "c:s": "mov_text"},
            **{"metadata:s:s:0": f"language={subtitle_language}",
            "metadata:s:s:0": f"title={subtitle_track_title}"}
            
        )
        ffmpeg.run(stream, overwrite_output=True)
    else:
        stream = ffmpeg.output(video_input_stream, output_vid,

        vf=f"subtitles={subtitle_file}")

        ffmpeg.run(stream, overwrite_output=True)


subtitleFile = generate_subtitle_file(output_dir, transcribe(base_sound))
print(f'{subtitleFile} ---------------------------------')
create_white_video_with_audio(base_sound, base_video)
add_subtitle_to_video(True, subtitleFile, 'eng', output_dir, base_video)

