import requests
import os
import random
from vk_api_error import handle_vk_error

from dotenv import load_dotenv


def download_random_comic():
    response = requests.get('https://xkcd.com/info.0.json')
    response.raise_for_status()
    max_comic_id = response.json()['num']
    image_number = random.randint(1, int(max_comic_id))

    url = f'https://xkcd.com/{image_number}/info.0.json'

    response = requests.get(url)
    response.raise_for_status()

    response_unpacked = response.json()
    image_link = response_unpacked['img']
    comment = response_unpacked['alt']
    extension = os.path.splitext(image_link)[1]
    filename = f'{image_number}{extension}'

    response = requests.get(image_link)
    response.raise_for_status()

    with open(filename, 'wb') as file:
        file.write(response.content)

    return filename, comment


def get_vk_upload_url(group_id, token, api_version):
    params = {
        'group_id': group_id,
        'access_token': token,
        'v': api_version,
    }
    endpoint = 'https://api.vk.com/method/photos.getWallUploadServer'

    response = requests.get(endpoint, params)
    response.raise_for_status()
    handle_vk_error(response)

    return response.json()['response']['upload_url']


def upload_photo_to_vk(filename, upload_url, group_id, token, api_version):
    params = {
        'group_id': group_id,
        'access_token': token,
        'v': api_version,
    }
    with open(filename, 'rb') as file:
        files = {
            'photo': file,
        }
        response = requests.post(upload_url, params=params, files=files)
    response.raise_for_status()
    response_unpacked = response.json()
    handle_vk_error(response)

    return response_unpacked['server'], response_unpacked['photo'], response_unpacked['hash']


def save_to_album(server, photo, _hash, group_id, token, api_version):
    endpoint = 'https://api.vk.com/method/photos.saveWallPhoto'
    params = {
        'group_id': group_id,
        'access_token': token,
        'v': api_version,
        'server': server,
        'photo': photo,
        'hash': _hash,
    }

    response = requests.post(endpoint, params)
    response.raise_for_status()
    response_unpacked = response.json()['response'][0]
    handle_vk_error(response_unpacked)

    media_id = response_unpacked['id']
    owner_id = response_unpacked['owner_id']

    return media_id, owner_id


def post_to_group(group_id, token, api_version, owner_id, media_id, comment):
    endpoint = 'https://api.vk.com/method/wall.post'
    params = {
        'owner_id': f'-{group_id}',
        'access_token': token,
        'v': api_version,
        'from_group': 1,
        'attachments': f'photo{owner_id}_{media_id}',
        'message': comment,
    }

    response = requests.post(endpoint, params)
    response.raise_for_status()
    handle_vk_error(response.json())


if __name__ == '__main__':
    load_dotenv()
    token = os.environ['VK_ACCESS_TOKEN']
    api_version = os.environ['VK_API_VERSION']
    group_id = os.environ['VK_GROUP_ID']

    filename, comment = download_random_comic()
    try:
        upload_url = get_vk_upload_url(group_id, token, api_version)

        server, photo, _hash = upload_photo_to_vk(filename, upload_url, group_id, token, api_version)

        media_id, owner_id = save_to_album(server, photo, _hash, group_id, token, api_version)

        post_to_group(group_id, token, api_version, owner_id, media_id, comment)
    finally:
        os.remove(filename)
