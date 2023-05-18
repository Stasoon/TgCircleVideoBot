import os
from dotenv import load_dotenv, find_dotenv


load_dotenv(find_dotenv())


# для utils/misc/messages.py
max_video_size_mb = 8
max_sides_len_px = 640
max_video_duration_sec = 60


# для utils/convert.py
watermark_duration = 2.5
videos_dir = 'user_videos'
watermark_image_name = 'watermark.png'


# class Config:
try:
    TOKEN = str(os.getenv('BOT_TOKEN'))
    ADMIN_IDS = [int(i) for i in os.getenv('BOT_ADMIN_IDS').split(',')]

    PAYMASTER_TOKEN = str(os.getenv('PAYMASTER_TOKEN'))
except (ValueError, TypeError) as e:
    print(e)
