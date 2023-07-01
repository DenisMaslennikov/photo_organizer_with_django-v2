from http import HTTPStatus

import pytest
from pytest_lazyfixture import lazy_fixture

from django.urls import reverse

from conftest import (
    ANONYMOUS_ENDPOINTS,
    AUTH_USER_ENDPOINTS,
    LOGIN_REQURE_ENDPOINTS,
)

LOGIN_URL = reverse('users:login')


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
