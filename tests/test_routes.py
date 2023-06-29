from http import HTTPStatus

import pytest
from pytest_lazyfixture import lazy_fixture

from django.urls import reverse

LOGIN_URL = reverse('users:login')

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
    lazy_fixture('get_tag_url'),
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
    lazy_fixture('get_tag_url'),
]

LOGIN_REQURE_ENDPOINTS = [
    # Эндпоинты приложения users
    reverse('users:password_change'),
    reverse('users:password_change_done'),
    # Эндпоинты приложения gallery
    reverse('gallery:add_image'),
    reverse('gallery:add_tag'),
    lazy_fixture('get_add_comment_url'),
    lazy_fixture('get_image_update_url'),
]

@pytest.mark.django_db
@pytest.mark.parametrize(
    'endpoint', ANONYMOUS_ENDPOINTS
)
def test_anonymous_endpoint(endpoint, unlogged_client, image):
    """Проверяем доступность страниц для анонимного пользователя"""
    response = unlogged_client.get(endpoint)
    assert response.status_code == HTTPStatus.OK, (
        f'Проверьте доступность {endpoint} для анонимного пользователя'
    )


@pytest.mark.django_db
@pytest.mark.parametrize(
    'endpoint', AUTH_USER_ENDPOINTS
)
def test_auth_user_endpoint(endpoint, user_client, image):
    """Проверяем доступность страниц для авторизированного пользователя"""
    response = user_client.get(endpoint)
    assert response.status_code == HTTPStatus.OK, (
        f'Проверьте доступность {endpoint} для авторизованного пользователя'
    )


@pytest.mark.django_db
@pytest.mark.parametrize(
    'endpoint', LOGIN_REQURE_ENDPOINTS
)
def test_login_requre_endpoint(endpoint, unlogged_client):
    """Проверяем переадресацию на страницы авторизации со страниц где она
    необходима"""
    response = unlogged_client.get(endpoint)
    expected_url = f'{LOGIN_URL}?next={endpoint}'
    assert response.url == expected_url,(
        f'Проверьте что анонимного пользователя со страницы {endpoint} '
        f'перенаправляет на страницу авторизации {expected_url}'
    )
