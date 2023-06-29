import os
import time
from typing import Type

import pytest

from mixer.backend.django import mixer as _mixer
from django.test.client import Client

from django.db.models import Model
from django.contrib.auth import get_user_model
from django.urls import reverse


@pytest.fixture
def mixer():
    return _mixer


@pytest.fixture
def user_model():
    return get_user_model()


@pytest.fixture
def user(mixer, user_model):
    user = mixer.blend(user_model)
    return user


@pytest.fixture
def another_user(mixer, user_model):
    user = mixer.blend(user_model)
    return user


@pytest.fixture
def user_client(user) -> Client:
    client = Client()
    client.force_login(user)
    return client


@pytest.fixture
def another_user_client(another_user) -> Client:
    client = Client()
    client.force_login(another_user)
    return client


@pytest.fixture
def unlogged_client(client) -> Client:
    return client


@pytest.fixture
def image_model() -> Type[Model]:
    try:
        from image.models import Image
    except ImportError:
        raise AssertionError('Ошибка импорта файла image/models.py')
    return Image


@pytest.fixture
def tag_model() -> Type[Model]:
    try:
        from tag_anything.models import Tag
    except ImportError:
        raise AssertionError('Ошибка импорта файла tag_anything/models.py')
    return Tag


@pytest.fixture
def tag_category_model() -> Type[Model]:
    try:
        from tag_anything.models import TagCategory
    except ImportError:
        raise AssertionError('Ошибка импорта файла tag_anything/models.py')
    return TagCategory


@pytest.fixture
def comment_model() -> Type[Model]:
    try:
        from comment.models import Comment
    except ImportError:
        raise AssertionError('Ошибка импорта файла comment/models.py')
    return Comment


@pytest.fixture
def image(mixer, image_model, user):
    image = mixer.blend(image_model, author=user)
    return image


@pytest.fixture
def comment(mixer, comment_model):
    comment = mixer.blend(comment_model)
    return comment


@pytest.fixture
def tag_category(mixer, tag_category_model):
    category = mixer.blend(tag_category_model)
    return category


@pytest.fixture
def tag(mixer, tag_model):
    tag = mixer.blend(tag_model)
    return tag


@pytest.fixture
def tagged_image(image, tag):
    image.tags.add(tag)
    return image


@pytest.fixture
def get_image_url(image):
    return reverse('gallery:image', args=(image.pk,))


@pytest.fixture
def get_user_profile_url(user):
    return reverse('gallery:user_profile', args=(user.username, ))


@pytest.fixture
def get_photo_by_url(image):
    return reverse('gallery:photo_by', args=(image.camera_model, ))


@pytest.fixture(scope='session', autouse=True)
def cleanup(request):
    start_time = time.time()
    yield

    from play_with_image import settings

    image_dir = settings.MEDIA_ROOT
    for root, dirs, files in os.walk(image_dir):
        for filename in files:
            if (
                filename.endswith(".jpg")
                or filename.endswith(".gif")
                or filename.endswith(".png")
            ):
                file_path = os.path.join(root, filename)
                if os.path.getmtime(file_path) >= start_time:
                    os.remove(file_path)
