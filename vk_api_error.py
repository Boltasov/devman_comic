import requests


class VkApiError(Exception):
    pass


def handle_vk_error(response_unpacked):
    if 'error' in response_unpacked.keys():
        output = {
            'code': response_unpacked['error']['error_code'],
            'message': response_unpacked['error']['error_msg'],
        }
        raise VkApiError(output)
