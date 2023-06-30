import random
from pathlib import Path

import pytest

from django.core.files.uploadedfile import SimpleUploadedFile
from django.conf import settings


@pytest.fixture
def add_image_post_data(tag):
    dir = Path(__file__).resolve().parent
    with open(dir / 'test.jpg', 'rb') as img:
        return {
            'name': 'Test Image',
            'tags': tag.pk,
            'image': SimpleUploadedFile(
                name='test_image.jpg',
                content=img.read(),
                content_type='image/jpeg',
            ),
        }


@pytest.fixture
def paginated_by_get_data():
    return {'paginated_by': settings.PAGINATED_BY + 1}


@pytest.fixture
def image_update_post_data(tags, image):
    return {
        'name': 'New test name',
        'tags': [tag.pk for tag in tags],
        'private': not image.private,
    }


@pytest.fixture
def set_tag_form_post_data(images, categories):
    return {
        'category':categories[random.randint(0,len(categories) - 1)].pk,
        'name': 'New Tag Name',
        'choices': [images[random.randint(0, len(images) - 1)].pk
                    for _ in range(10)],
    }

