import os
from src.scraping import reddit_scraper 
from src.create_video import create_intro, create

script_dir = os.path.dirname(os.path.abspath(__file__))
temp_dir = os.path.join(script_dir, 'assets', 'temp_files')
output_dir = os.path.join(script_dir, 'assets', 'output_files')
minecraft_dir = os.path.join(script_dir, 'assets', 'random_videos', 'minecraftVideo1.mp4') #need to change


def get_logs():
    with open ('log.txt', 'r') as f: 
        data = f.read()
        return data.splitlines()
        
def update_log(list_of_new_logs: list):
    with open ('log.txt', 'a') as f:
        f.write('\n')
        f.write('\n'.join(list_of_new_logs))

url = 'https://www.reddit.com/r/confession/top/'
min_of_upvotes = 10

def main():
    articles = reddit_scraper.use_driver(url)
    info_of_articles = reddit_scraper.information_of_articles(articles, min_of_upvotes)
    for article in info_of_articles:
        text = article.label + " " + reddit_scraper.text_of_articles(article.link)
        intro_image = create_intro.create_start_image('confession', article.label)
        intro_time = create.create_sound(article.label, text, temp_dir + r'\sound.mp3')
        create.add_intro_and_sound(intro_time, intro_image, temp_dir + r'\sound.mp3',minecraft_dir , output_dir + r'\final.mp4')




        


    