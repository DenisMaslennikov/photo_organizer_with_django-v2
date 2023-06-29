from http import HTTPStatus

import pytest
from pytest_lazyfixture import lazy_fixture

from django.urls import reverse

ANONYMOUS_ENDPOINTS = [
    # Эндпоинты приложения users
    reverse('users:logout'),
    reverse('users:login'),
    reverse('users:registration'),
    reverse('users:password_reset'),
    reverse('users:password_reset_complete'),
    reverse('users:password_reset_done'),
    # Эндпоинты приложения pages
    reverse('pages:about'),
    # Эндпоинты приложения  gallery
    reverse('gallery:index'),
    lazy_fixture('get_image_url'),
    reverse('gallery:search'),
    lazy_fixture('get_user_profile_url'),
    lazy_fixture('get_photo_by_url'),
]

AUTH_USER_ENDPOINTS = [
    # Эндпоинты приложения users
    reverse('users:edit_profile'),
    reverse('users:password_change'),
    reverse('users:password_change_done'),
    # Эндпоинты приложения gallery
    reverse('gallery:index'),
    lazy_fixture('get_image_url'),
    reverse('gallery:search'),
    lazy_fixture('get_user_profile_url'),
    lazy_fixture('get_photo_by_url'),
    reverse('gallery:add_image'),
]

@pytest.mark.django_db
@pytest.mark.parametrize(
    'endpoint', ANONYMOUS_ENDPOINTS
)
def test_anonymous_endpoint(endpoint, unlogged_client, image):
    response = unlogged_client.get(endpoint)
    assert response.status_code == HTTPStatus.OK, (
        f'Проверьте доступность {endpoint} для анонимного пользователя'
    )


@pytest.mark.django_db
@pytest.mark.parametrize(
    'endpoint', AUTH_USER_ENDPOINTS
)
def test_auth_user_endpoint(endpoint, user_client, image):
    response = user_client.get(endpoint)
    assert response.status_code == HTTPStatus.OK, (
        f'Проверьте доступность {endpoint} для авторизованного пользователя'
    )
