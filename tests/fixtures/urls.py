import random

from django.urls import reverse

import pytest


@pytest.fixture
def get_image_url(image) -> str:
    return reverse("gallery:image", args=(image.pk,))


@pytest.fixture
def get_user_profile_url(user) -> str:
    return reverse("gallery:user_profile", args=(user.username,))


@pytest.fixture
def get_photo_by_url(image) -> str:
    return reverse("gallery:photo_by", args=(image.camera_model,))


@pytest.fixture
def get_tag_url(tagged_images, tags):
    return reverse(
        "gallery:tag_view", args=(tags[random.randint(0, len(tags) - 1)].slug,)
    )


@pytest.fixture
def get_add_comment_url(image) -> str:
    return reverse("gallery:add_comment", args=(image.pk,))


@pytest.fixture
def get_image_update_url(image) -> str:
    return reverse("gallery:update_image", args=(image.pk,))


@pytest.fixture
def get_image_update_url(image) -> str:
    return reverse("gallery:update_image", args=(image.pk,))
