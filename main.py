import requests
import os
import random

from dotenv import load_dotenv


def upload_random_comic():
    max_comic_id = requests.get('https://xkcd.com/info.0.json').json()['num']
    image_number = random.randint(1, int(max_comic_id))
    url = f'https://xkcd.com/{image_number}/info.0.json'

    response = requests.get(url)
    response.raise_for_status()

    image_json = response.json()
    image_link = image_json['img']
    comment = image_json['alt']
    extension = os.path.splitext(image_link)[1]
    filename = f'{image_number}{extension}'

    image = requests.get(image_link)
    image.raise_for_status()

    with open(filename, 'wb') as file:
        file.write(image.content)

    return filename, comment


def get_upload_url(params):
    vk_base_url = 'https://api.vk.com/method'
    method_name = 'photos.getWallUploadServer'
    url = f'{vk_base_url}/{method_name}'

    response = requests.get(url, params)
    response.raise_for_status()
    return response.json()['response']['upload_url']


def send_photo(file, upload_url, params):
    files = {
        'photo': file,
    }

    response = requests.post(upload_url, params=params, files=files)
    response.raise_for_status()
    return response.json()


def save_to_album(photo_response, params):
    vk_base_url = 'https://api.vk.com/method'
    method_name = 'photos.saveWallPhoto'
    params.update(photo_response)
    url = f'{vk_base_url}/{method_name}'

    response = requests.post(url, params)
    response.raise_for_status()

    return response.json()


def post_to_group(params):
    vk_base_url = 'https://api.vk.com/method'
    method_name = 'wall.post'
    url = f'{vk_base_url}/{method_name}'

    response = requests.post(url, params)
    response.raise_for_status()

    return response.json()


if __name__ == '__main__':
    load_dotenv()
    token = os.environ['VK_ACCESS_TOKEN']
    api_version = os.environ['VK_API_VERSION']
    group_id = os.environ['VK_GROUP_ID']
    params = {
        'group_id': group_id,
        'access_token': token,
        'v': api_version,
    }

    # 0. Download comic from xkcd.com
    filename, comment = upload_random_comic()

    # 1. Get upload url for the image
    upload_url = get_upload_url(params)

    # 2. Send image to VK
    with open(filename, 'rb') as file:
        photo_response = send_photo(file, upload_url, params)

    # 3. Save image to the group album
    save_response = save_to_album(photo_response, params)
    media_id = save_response['response'][0]['id']
    owner_id = save_response['response'][0]['owner_id']

    # 4. Publish to the group
    publish_params = {
        'owner_id': f'-{group_id}',  # id группы должно быть с минусом
        'access_token': token,
        'v': api_version,
        'from_group': 1,
        'attachments': f'photo{owner_id}_{media_id}',
        'message': comment,
    }
    response = post_to_group(publish_params)

    # 5. Delete the file
    os.remove(filename)
