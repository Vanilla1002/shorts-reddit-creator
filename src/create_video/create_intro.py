
import textwrap
from PIL import Image, ImageDraw, ImageFont

import os



script_dir = os.path.dirname(os.path.abspath(__file__))
output_dir = os.path.join(script_dir, '..','..', 'assets', 'temp_files')
input_dir = os.path.join(script_dir, '..','..', 'assets', 'pictures' ,'intro_empty.png')
font_label = ImageFont.truetype('arialbd.ttf', 65) 
font_text =  ImageFont.truetype('arialbd.ttf', 40)



def create_start_image(reddit_r, label, output_dir=output_dir): 
    img = Image.open(input_dir)
    I1 = ImageDraw.Draw(img)
    I1.text((155, 0), "r/" + reddit_r ,font=font_label, fill=(0, 0, 0))
    wrapped_text = textwrap.fill(label, width=30)  
    I1.text((50, 125), wrapped_text,font=font_text, fill=(0, 0, 0))
    img.save(f'{output_dir}/intro.png')
    return f'{output_dir}/intro.png'

# create_start_image('shorts', 'hi noobs.')
