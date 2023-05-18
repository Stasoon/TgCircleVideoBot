import os
from aiogram import types
from moviepy.editor import VideoFileClip, ImageClip, CompositeVideoClip
from src.config import watermark_duration, videos_dir, watermark_image_name


async def send_video_as_note(video_msg: types.Message, add_watermark: bool = True) -> types.Message:
    # Скачиваем видео
    video_file_path = f'{videos_dir}/{video_msg.from_id}.mp4'
    await video_msg.answer_chat_action(action='record_video_note')
    (await video_msg.video.download(destination_file=video_file_path)).close()
    await video_msg.answer_chat_action(action='record_video_note')
    # Добавляем водяной знак
    if add_watermark:
        # Создаём
        video = VideoFileClip(video_file_path)
        watermark = (ImageClip(watermark_image_name)
                     .set_duration(watermark_duration if watermark_duration < video.duration else video.duration)
                     .set_pos(('center', 'center'))
                     .resize(height=video.h))

        final_clip = CompositeVideoClip([video, watermark])
        final_clip.write_videofile(f'{videos_dir}/res_{video_msg.from_id}.mp4', audio=True)

        os.remove(video_file_path)
        video_file_path = f'{videos_dir}/res_{video_msg.from_id}.mp4'

    await video_msg.answer_chat_action(action='upload_video_note')
    with open(video_file_path, 'rb') as video_note:
        note_message = await video_msg.answer_video_note(video_note=video_note)

    os.remove(video_file_path)
    return note_message
