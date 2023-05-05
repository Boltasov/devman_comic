import requests
import os
import random

from dotenv import load_dotenv


'''
Get token
https://oauth.vk.com/authorize?client_id=51633822&redirect_uri=https://oauth.vk.com/blank.html&scope=photos,groups,wall&response_type=token
https://oauth.vk.com/blank.html#access_token=&expires_in=86400&user_id=275658820
'''


def get_comic(max_comic_id):
    image_number = random.randint(1, int(max_comic_id))
    url = f'https://xkcd.com/{image_number}/info.0.json'

    response = requests.get(url)
    response.raise_for_status()

    image_link = response.json()['img']
    image = requests.get(image_link)
    image.raise_for_status()

    comment = response.json()['alt']

    extension = os.path.splitext(image_link)[1]
    filename = f'{image_number}{extension}'

    with open(filename, 'wb') as file:
        file.write(image.content)

    print(comment)
    return filename, comment


def get_upload_url(vk_base_url, params):
    method_name = 'photos.getWallUploadServer'
    url = f'{vk_base_url}/{method_name}'

    response = requests.get(url, params)
    response.raise_for_status()
    print(response.json())
    return response.json()['response']['upload_url']


def send_photo(file, upload_url, params):
    files = {
        'photo': file,
    }

    response = requests.post(upload_url, params=params, files=files)
    response.raise_for_status()
    return response.json()


def save_to_album(vk_base_url, photo_response, params):
    method_name = 'photos.saveWallPhoto'
    url = f'{vk_base_url}/{method_name}'
    params['photo'] = photo_response['photo']
    params['server'] = photo_response['server']
    params['hash'] = photo_response['hash']

    response = requests.post(url, params)
    response.raise_for_status()
    return response.json()


def post_to_group(vk_base_url, params):
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
    max_comic_id = os.environ['CURRENT_COMIC_NUMBER']
    vk_url = 'https://api.vk.com/method'
    params = {
        'group_id': group_id,
        'access_token': token,
        'v': api_version,
    }

    # 0. Download comic from xkcd.com
    filename, comment = get_comic(max_comic_id)

    # 1. Get upload url for the image
    upload_url = get_upload_url(vk_url, params)

    # 2. Send image to VK
    with open(filename, 'rb') as file:
        photo_response = send_photo(file, upload_url, params)

    # 3. Save image to the group album
    response = save_to_album(vk_url, photo_response, params)
    media_id = response['response'][0]['id']
    owner_id = response['response'][0]['owner_id']

    # 4. Publish to the group
    publish_params = {
        'owner_id': f'-{group_id}',  # id группы должно быть с минусом
        'access_token': token,
        'v': api_version,
        'from_group': 1,
        'attachments': f'photo{owner_id}_{media_id}',
        'message': comment,
    }
    response = post_to_group(vk_url, publish_params)

    # 5. Delete the file
    os.remove(filename)
