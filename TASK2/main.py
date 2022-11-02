import os
import sys
import argparse
import asyncio
import aiofiles
import aiohttp
import logging
import logging.config

log = logging.getLogger(__name__)

logging.basicConfig(filename='uploader.log', filemode='a',
                    level=logging.DEBUG, format='%(asctime)s %(message)s')

DEFAULT_DEST_URL = 'https://httpbin.org/post'
DEFAULT_IMAGE_DIR_PATH = '/var/www/images'
MAX_ASYNC_TASKS = 100


def get_files(image_dir_path):
    allowed_ext = ('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif')
    return [os.path.join(image_dir_path, file) for file in os.listdir(image_dir_path)
            if file.endswith(allowed_ext)]


async def upload_file(session, local_path):
    file_size = os.path.getsize(local_path)
    async with aiofiles.open(local_path, 'rb') as fp:
        file_content = await fp.read()
        try:
            response = await session.post(dest_url, data=file_content, raise_for_status=True)
            log.info("Status: {0} {1} size: {2} kb".format(response.status, local_path, file_size // 1024))
        except aiohttp.ClientConnectorError:
            log.error('Client connection error for {dest_url}'.format(dest_url))
        except Exception as e:
            log.error('Error: {0}'.format(e))


async def upload_files(paths):
    async with aiohttp.ClientSession() as session:
        tasks = []
        for path in paths:
            tasks.append(upload_file(session, path))

            if len(tasks) == MAX_ASYNC_TASKS:
                await asyncio.gather(*tasks)
                tasks = []
        await asyncio.gather(*tasks)


async def main(image_dir_path):
    image_file_list = get_files(image_dir_path)
    if image_file_list:
        log.info("{0} image files are found.".format(len(image_file_list)))
        await upload_files(image_file_list)
    else:
        log.info('Directory is empty'.format())

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--server", help="Provide a remote server address")
    parser.add_argument("--imgdir", help="Provide a local directory path")
    args = parser.parse_args()

    dest_url = args.server or DEFAULT_DEST_URL
    image_dir = args.imgdir or DEFAULT_IMAGE_DIR_PATH

    log.info('Script started. Uploading images to {0} server'.format(dest_url))
    if os.path.exists(image_dir):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(main(image_dir))
        log.info('Script is completed.')
    else:
        log.warning('Can''t find {0} path. Script is stopped.'.format(image_dir))
