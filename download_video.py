import os
import traceback
import logging.config
import requests
import numpy as np

logger = logging.getLogger(__name__)

video_type_dict = {
    'video/mp4': 'mp4',
    'video/x-m4v': 'm4v'
}

def Download(video_id, url):
    try:
        r = requests.head(url, timeout=10)
        video_type = r.headers['Content-Type']
        video_type = video_type_dict[video_type]
    except:
        video_type = "mp4"
    try:
        logger.info("begin download video {} {}".format(video_id, url))
        video_path = os.path.abspath(video_id + ".{}".format(video_type))
        r = requests.get(url, stream=True)
        with open(video_path, "wb") as file:
            for chunk in r.iter_content(chunk_size=2048):
                if chunk:
                    file.write(chunk)
        logger.info("download video success {} {}, path is {}".format(video_id, url, video_path))
        return 0, video_path
    except Exception as e:
        s = traceback.format_exc()
        logger.error(s)
        logger.error(e)
        logger.info("{} {} 视频url下载失败，可能存在异常".format(video_id, url))
        return 1, None
