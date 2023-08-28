import pytest
from conftest import (
    ADD_IMAGE_ENDPOINT,
    ADD_TAG,
    LIST_VIEW_ENDPOINTS,
    UPDATE_IMAGE_ENDPOINT
)
from pytest_lazyfixture import lazy_fixture


@pytest.mark.django_db
@pytest.mark.parametrize(
    "active_client, result",
    [
        (lazy_fixture("user_client"), True),
        (lazy_fixture("unlogged_client"), False),
    ],
)
@pytest.mark.parametrize("endpoint", ADD_IMAGE_ENDPOINT)
def test_add_image(
    image_model, active_client, result, add_image_post_data, endpoint
):
    """Проверяем добавление изображения"""
    count_before = image_model.objects.count()
    active_client.post(endpoint, data=add_image_post_data)
    count_after = image_model.objects.count()
    assert (count_after > count_before) == result, (
        f'Проверьте, что {"авторизированный" if result else "анонимный"} '
        f'пользователь {"не" if not result else ""} может добавить изображение'
    )


@pytest.mark.django_db
@pytest.mark.parametrize("endpoint", LIST_VIEW_ENDPOINTS)
def test_paginated_by_form(
    endpoint, unlogged_client, images, paginated_by_get_data
):
    """Проверяем настройку пагинации"""
    response = unlogged_client.get(endpoint, data=paginated_by_get_data)
    paginated_by = paginated_by_get_data["paginated_by"]
    assert len(response.context.get("page_obj")) == paginated_by, (
        f"Проверьте что по адресу {endpoint} настройка пагинации работает "
        f"корректно"
    )
    response = unlogged_client.get(endpoint)
    assert (
        len(response.context.get("page_obj")) == paginated_by
    ), f"Проверьте что настройки пагинации сохраняются для адреса {endpoint}"


@pytest.mark.django_db
@pytest.mark.parametrize(
    "active_client, result",
    [
        (
            lazy_fixture("unlogged_client"),
            False,
        ),
        (
            lazy_fixture("another_user_client"),
            False,
        ),
        (
            lazy_fixture("user_client"),
            True,
        ),
    ],
)
@pytest.mark.parametrize("endpoint", UPDATE_IMAGE_ENDPOINT)
def test_image_update_form(
    endpoint,
    active_client,
    result,
    image,
    image_update_post_data,
):
    active_client.post(endpoint, data=image_update_post_data)
    image.refresh_from_db()
    assert (image.name == image_update_post_data["name"]) == result, (
        f'Проверьте что {"аноним/не владелец" if not result else "владелец"} '
        f'{"не" if not result else ""} может редактировать информацию об '
        f"изображении"
    )
    assert (image.private == image_update_post_data["private"]) == result, (
        f'Проверьте что {"аноним/не владелец" if not result else "владелец"} '
        f'{"не" if not result else ""} может редактировать информацию об '
        f"изображении"
    )
    for tag in image.tags.filter():
        assert (tag.pk in image_update_post_data["tags"]) == result, (
            f"Проверьте что "
            f'{"аноним/не владелец" if not result else "владелец"} '
            f'{"не" if not result else ""} может редактировать информацию об '
            f"изображении"
        )


@pytest.mark.django_db
@pytest.mark.parametrize("endpoint", ADD_TAG)
@pytest.mark.parametrize(
    "active_client, result",
    [
        (lazy_fixture("unlogged_client"), False),
        (lazy_fixture("another_user_client"), False),
        (lazy_fixture("user_client"), True),
    ],
)
def test_tag_form(
    active_client, result, endpoint, set_tag_form_post_data, image_model
):
    active_client.post(endpoint, set_tag_form_post_data)
    for pk in set_tag_form_post_data["choices"]:
        image = image_model.objects.get(pk=pk)
        assert (
            len(image.tags.filter(name=set_tag_form_post_data["name"])) > 0
        ) == result, (
            f'Проверьте что {"анонимный" if result else "зарегистрированный"} '
            f'пользователь {"не" if not result else ""} может добавлять теги '
            f"изображениям"
        )
