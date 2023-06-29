import pytest

from django.conf import settings
from django.urls import reverse
from pytest_lazyfixture import lazy_fixture


LIST_VIEW_ENDPOINTS = [
    reverse('gallery:index'),
    reverse('gallery:search'),
    lazy_fixture('get_user_profile_url'),
    lazy_fixture('get_photo_by_url'),
    lazy_fixture('get_tag_url'),
]

IMAGE_DETAIL_ENDPOINT = lazy_fixture('get_image_url')


@pytest.mark.django_db
@pytest.mark.parametrize(
    'endpoint', LIST_VIEW_ENDPOINTS

)
def test_pagination(endpoint, tagged_images, unlogged_client):
    """Проверяем работу пагинации"""
    response = unlogged_client.get(endpoint)
    assert len(response.context.get('page_obj')) == settings.PAGINATED_BY, (
        f'Проверьте что по адресу {endpoint} количество изображений '
        f'соответствует настройкам пагинации'
    )


@pytest.mark.django_db
@pytest.mark.parametrize(
    'active_client, form', [
        (lazy_fixture('unlogged_client'), False),
        (lazy_fixture('user_client'), True),
    ]
)
@pytest.mark.parametrize(
    'endpoint', LIST_VIEW_ENDPOINTS
)
def test_tag_form(active_client, form, endpoint):
    """Проверяем наличие/отсутствие формы тегов в контексте"""
    response = active_client.get(endpoint)
    assert ('tag_form' in response.context) == form, (
        f'Проверьте что на странице {endpoint} {"не" if not form else ""} '
        f'выводится форма тегов'
    )


@pytest.mark.django_db
@pytest.mark.parametrize(
    "active_client, form", [
        (lazy_fixture('unlogged_client'), False),
        (lazy_fixture('user_client'), True),
        (lazy_fixture('another_user_client'), False),
    ]
)
@pytest.mark.parametrize(
    'endpoint', [IMAGE_DETAIL_ENDPOINT, ]
)
def test_image_update_form_on_image_page(active_client, form, endpoint):
    response = active_client.get(endpoint)
    assert ('image_update_form' in response.context) == form, (
        f'Проверьте что форма редактирования {"не" if not form else ""} '
        f'выводится для {"анонимного/не автора" if not form else "владельца"} '
        f'изображения'
    )


@pytest.mark.django_db
@pytest.mark.parametrize(
    "active_client, form", [
        (lazy_fixture('unlogged_client'), False),
        (lazy_fixture('user_client'), True),
    ]
)
@pytest.mark.parametrize(
    'endpoint', [IMAGE_DETAIL_ENDPOINT, ]
)
def test_comment_form_visibly(endpoint, active_client, form):
    response = active_client.get(endpoint)
    assert ('comment_form' in response.context) == form, (
        f'Проверьте что форма комментариев {"не" if not form else ""} '
        f'выводится для '
        f'{"анонимного" if not form else "зарегистрированного"} '
        f'пользователя'
    )
