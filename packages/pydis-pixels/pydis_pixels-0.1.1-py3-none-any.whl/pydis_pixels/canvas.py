from time import sleep
from typing import Tuple

from loguru import logger
from PIL import Image
from requests import get, post


class Canvas:
    """The canvas and an interface to its API"""

    def __init__(
        self, token: str, base_url: str = 'https://pixels.pythondiscord.com'
    ):
        self.token = token
        self.base_url = base_url

        self.headers = {'Authorization': f'Bearer {self.token}'}

    @property
    def size(self) -> Tuple[int, int]:
        """The canvas size"""

        response = get(f'{self.base_url}/get_size')

        if response.ok:
            size = response.json()
            logger.debug(f'Retrieved size ({size["width"]}, {size["height"]})')
        else:
            logger.critical(str(response.status_code))
            exit()

        return (size['width'], size['height'])

    @property
    def image(self) -> Image:
        response = get(f'{self.base_url}/get_pixels', headers=self.headers)

        if response.ok:
            logger.debug('Retrieved pixel data')
        else:
            logger.critical(str(response.status_code))
            exit()

        image = Image.frombytes('RGB', self.size, response.content)
        logger.debug('Initialized image')
        return image

    def set_pixel(self, x: int, y: int, rgb: str, wait_cooldown: bool = True):
        response = post(
            f'{self.base_url}/set_pixel',
            headers=self.headers,
            json={'x': x, 'y': y, 'rgb': rgb},
        )

        if response.ok:
            logger.info(f'Set {x}, {y} to {rgb}')
            logger.debug(response.json()['message'])
        elif response.status_code == 429:
            logger.debug(
                f'Trying again in {response.headers["Cooldown-Reset"]} seconds'
            )
            sleep(int(response.headers['Cooldown-Reset']) + 0.1)
            return self.set_pixel(x, y, rgb)
        else:
            logger.critical(str(response.status_code))
            exit()

        remaining = int(response.headers['Requests-Remaining'])
        reset = int(response.headers['Requests-Reset'])

        logger.debug(f'{remaining} requests remaining')

        if remaining == 0 and wait_cooldown:
            logger.debug(f'Sleeping for {reset} seconds')
            sleep(reset + 0.1)

        return response.json()
