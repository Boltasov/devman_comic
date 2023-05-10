import requests


class VkApiError(Exception):
    pass


def handle_vk_error(response):
    response = response.json()
    if 'error' in response.keys():
        output = {
            'code': response['error']['error_code'],
            'message': response['error']['error_msg'],
        }
        raise VkApiError(output)
