import logging
from logging.handlers import RotatingFileHandler

import imagehash
from exif import Image

from django.conf import settings

"""EXIF_CAMERA_MODEL = 'Exif.Image.Model'
EXIF_LENS_MODEL = 'Exif.Photo.LensModel'
EXIF_ISO = 'Exif.Photo.ISOSpeedRatings'
EXIF_FOCAL_LENGTH = 'Exif.Photo.FocalLength'
EXIF_FLASH = 'Exif.Photo.Flash'
EXIF_F_NUMBER = 'Exif.Photo.FNumber'
EXIF_EXPOSURE_TIME = 'Exif.Photo.ExposureTime'"""

EXIF_CAMERA_MODEL = 'model'
EXIF_LENS_MODEL = 'lens_model'
EXIF_ISO = 'photographic_sensitivity'
EXIF_FOCAL_LENGTH = 'focal_length'
EXIF_FLASH = 'flash'
EXIF_F_NUMBER = 'f_number'
EXIF_EXPOSURE_TIME = 'exposure_time'
EXIF_MAKE = 'make'

logger = logging.getLogger(__package__)
logger.setLevel(settings.LOG_LEVEL)
file_handler = RotatingFileHandler(
    settings.LOG_DIR / f'{__package__}.log',
    maxBytes=settings.LOG_MAX_SIZE,
    backupCount=settings.LOG_BACKUP_COUNT,
)
stream_handler = logging.StreamHandler()
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(filename)s - %(levelname)s - %(funcName)s - '
    '%(lineno)d - %(message)s'
)
file_handler.setFormatter(formatter)
stream_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(stream_handler)


def get_average_image_hash(path_to_image: str) -> imagehash.ImageHash:
    """Средний хеш изображения"""
    return imagehash.average_hash(imagehash.Image.open(path_to_image))


def get_phash_image_hash(path_to_image: str) -> imagehash.ImageHash:
    """Phash изображения"""
    return imagehash.phash(imagehash.Image.open(path_to_image))


def hamming_distance(hash1: int, hash2: int) -> int:
    """Расстояние Хемминга"""
    result = str(bin(hash1 ^ hash2)).count('1')
    return result


def get_exif(path_to_image: str):
    """Читаем и возвращаем EXIF изображения"""
    with open(path_to_image, 'rb') as image:
        return Image(image)


def get_camera_model(exif):
    """Извлекаем из EXIF модель камеры"""
    if (exif.get(EXIF_MAKE) in exif.get(EXIF_CAMERA_MODEL)
        and  len(exif.get(EXIF_MAKE).split()) == 1
    ):
        return exif.get(EXIF_CAMERA_MODEL)
    return f'{exif.get(EXIF_MAKE)} {exif.get(EXIF_CAMERA_MODEL)}'


def get_lens_model(exif):
    """Извлекаем из EXIF модель объектива"""
    return exif.get(EXIF_LENS_MODEL)


def get_iso(exif):
    """Извлекаем из EXIF ISO"""
    return exif.get(EXIF_ISO)


def get_focal_length(exif):
    """Извлекаем из EXIF фокусное расстояние"""
    return exif.get(EXIF_FOCAL_LENGTH)


def get_flash(exif):
    """Извлекаем из EXIF информацию о вспышке"""
    return exif.get(EXIF_FLASH).flash_fired


def get_f_number(exif):
    """Извлекаем из EXIF значение диафрагмы"""
    return exif.get(EXIF_F_NUMBER)


def get_exposure_time(exif):
    """Извлекаем из EXIF время выдержки"""
    exposure_time = exif.get(EXIF_EXPOSURE_TIME)
    if exposure_time < 1:
        exposure_time = 1 / exposure_time
        exposure_time = f'1/{int(exposure_time)}'
    else:
        exposure_time = str(exposure_time)
    return exposure_time


def ms_to_degrees(cords: tuple):
    """Конвертируем градусы минуты, секунды в десятичные градусы"""
    convert_ratio = 1
    degrees = 0
    for cord in cords:
        degrees += cord / convert_ratio
        convert_ratio *= 60
    return degrees

def get_longitude(exif):
    gps_longitude = exif.get('gps_longitude')
    gps_longitude_ref = exif.get('gps_longitude_ref')
    if not gps_longitude is None:
        if isinstance(gps_longitude, tuple):
            return f'{ms_to_degrees(gps_longitude):10.8}{gps_longitude_ref}'
        return f'{gps_longitude:10.8}{gps_longitude_ref}'


def get_latitude(exif):
    gps_latitude = exif.get('gps_latitude')
    gps_latitude_ref = exif.get('gps_latitude_ref')
    if not gps_latitude is None:
        if isinstance(gps_latitude, tuple):
            return f'{ms_to_degrees(gps_latitude):10.8}{gps_latitude_ref}'
        return f'{gps_latitude:10.8}{gps_latitude_ref}'




