import os
import random
import time
from datetime import timedelta
from typing import Type

from django.conf import settings
from django.contrib.auth import get_user_model
from django.db.models import Model
from django.test.client import Client
from django.urls import reverse

import pytest
from mixer.backend.django import mixer as _mixer
from pytest_lazyfixture import lazy_fixture

ANONYMOUS_ENDPOINTS = [
    # Эндпоинты приложения users
    reverse("users:logout"),
    reverse("users:login"),
    reverse("users:registration"),
    reverse("users:password_reset"),
    reverse("users:password_reset_complete"),
    reverse("users:password_reset_done"),
    # Эндпоинты приложения pages
    reverse("pages:about"),
    # Эндпоинты приложения  gallery
    reverse("gallery:index"),
    lazy_fixture("get_image_url"),
    reverse("gallery:search"),
    lazy_fixture("get_user_profile_url"),
    lazy_fixture("get_photo_by_url"),
    lazy_fixture("get_tag_url"),
]
AUTH_USER_ENDPOINTS = [
    # Эндпоинты приложения users
    reverse("users:edit_profile"),
    reverse("users:password_change"),
    reverse("users:password_change_done"),
    # Эндпоинты приложения gallery
    reverse("gallery:index"),
    lazy_fixture("get_image_url"),
    reverse("gallery:search"),
    lazy_fixture("get_user_profile_url"),
    lazy_fixture("get_photo_by_url"),
    reverse("gallery:add_image"),
    lazy_fixture("get_tag_url"),
]
LOGIN_REQURE_ENDPOINTS = [
    # Эндпоинты приложения users
    reverse("users:password_change"),
    reverse("users:password_change_done"),
    # Эндпоинты приложения gallery
    reverse("gallery:add_image"),
    reverse("gallery:add_tag"),
    lazy_fixture("get_add_comment_url"),
]
LIST_VIEW_ENDPOINTS = [
    reverse("gallery:index"),
    reverse("gallery:search"),
    lazy_fixture("get_user_profile_url"),
    lazy_fixture("get_photo_by_url"),
    lazy_fixture("get_tag_url"),
]
IMAGE_DETAIL_ENDPOINT = [
    lazy_fixture("get_image_url"),
]
USER_PROFILE_ENDPOINT = [
    lazy_fixture("get_user_profile_url"),
]
ADD_IMAGE_ENDPOINT = [
    reverse("gallery:add_image"),
]
UPDATE_IMAGE_ENDPOINT = [
    lazy_fixture("get_image_update_url"),
]
ADD_TAG = [
    reverse("gallery:add_tag"),
]

IMAGES_AMOUNT = settings.PAGINATED_BY * 10
TAGS_AMOUNT = 3
CATEGORY_AMOUNT = 2
TAGS_PER_IMAGE = 2
CAMERA_MODEL = "Canon 5d mark iv"
COMMENT_AMOUNT = 10


pytest_plugins = ["tests.fixtures.urls", "tests.fixtures.request_data"]


@pytest.fixture
def mixer():
    return _mixer


@pytest.fixture
def user_model() -> Type[Model]:
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
        raise AssertionError("Ошибка импорта файла image/models.py")
    return Image


@pytest.fixture
def tag_model() -> Type[Model]:
    try:
        from tag_anything.models import Tag
    except ImportError:
        raise AssertionError("Ошибка импорта файла tag_anything/models.py")
    return Tag


@pytest.fixture
def tag_category_model() -> Type[Model]:
    try:
        from tag_anything.models import TagCategory
    except ImportError:
        raise AssertionError("Ошибка импорта файла tag_anything/models.py")
    return TagCategory


@pytest.fixture
def comment_model() -> Type[Model]:
    try:
        from comment.models import Comment
    except ImportError:
        raise AssertionError("Ошибка импорта файла comment/models.py")
    return Comment


@pytest.fixture
def image(mixer, image_model, user):
    image = mixer.blend(image_model, author=user, camera_model=CAMERA_MODEL)
    return image


@pytest.fixture
def comments(mixer, comment_model, image):
    comments = mixer.cycle(COMMENT_AMOUNT).blend(comment_model, image=image)
    for index, comment in enumerate(comments):
        comment.created = comment.created - timedelta(days=index)
        comment.save()
    return comments


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
def images(mixer, image_model, user):
    images = mixer.cycle(IMAGES_AMOUNT).blend(
        image_model, camera_model=CAMERA_MODEL, author=user
    )
    for index, image in enumerate(images):
        image.created = image.created - timedelta(days=index)
    return images


@pytest.fixture
def categories(mixer, tag_category_model):
    categories = mixer.cycle(CATEGORY_AMOUNT).blend(tag_category_model)
    return categories


@pytest.fixture
def tags(mixer, tag_model, categories):
    tags = mixer.cycle(TAGS_AMOUNT).blend(
        tag_model, category=categories[random.randint(0, len(categories)) - 1]
    )
    return tags


@pytest.fixture
def tagged_images(images, tags):
    for image in images:
        for _ in range(TAGS_PER_IMAGE):
            image.tags.add(tags[random.randint(0, len(tags) - 1)])
    return images


@pytest.fixture(scope="session", autouse=True)
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
