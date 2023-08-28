import logging

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.db.utils import IntegrityError
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from pytils.translit import slugify

from comment.forms import CommentForm
from comment.models import Comment
from image.forms import ImageAddForm, ImageUpdateForm
from image.models import Image
from image.utils import hamming_distance
from tag_anything.models import Tag

from .forms import AssignTag

Users = get_user_model()

logger = logging.getLogger(__package__)


@login_required
def add_tag(request):
    """Добавление тега изображениям"""
    logger.debug("Добавляем теги изображениям")
    tag_form = AssignTag(request.POST)
    if tag_form.is_valid():
        try:
            tag = Tag.objects.get_or_create(
                name=tag_form.cleaned_data["name"].title().strip(),
                category=tag_form.cleaned_data["category"],
            )[0]
        except IntegrityError as error:
            logger.error(error, exc_info=True)
            tag_slug = slugify(tag_form.cleaned_data["name"].title().strip())
            tag = Tag.objects.get(slug=tag_slug)
        for image in tag_form.cleaned_data["choices"]:
            if image.author == request.user:
                image.tags.add(tag.pk)

    if next_page := request.POST.get("next"):
        return redirect(next_page)

    return redirect("gallery:index")


class BaseImageListView(ListView):
    """Базовый класс для галереи"""

    model = Image
    paginate_by = settings.PAGINATED_BY
    template_name = "gallery/gallery.html"
    allow_empty = False

    def get_queryset(self):
        logger.debug("Получаем базовый кверисет")
        return (
            self.model.objects.filter(private=False)
            .prefetch_related("tags", "tags__category")
            .select_related("author")
        )

    def get_context_data(self, *args, **kwargs):
        logger.debug("Получаем базовый контекст")
        context = super().get_context_data(*args, **kwargs)
        context["paginated_by"] = self.get_paginate_by(self.queryset)
        return context

    def get_paginate_by(self, queryset):
        logger.debug("Получаем пагинацию")
        if self.request.GET.get("paginated_by"):
            try:
                self.request.session["paginated_by"] = int(
                    self.request.GET.get("paginated_by")
                )
            except ValueError as error:
                logger.error(error, exc_info=True)
                self.request.session["paginated_by"] = settings.PAGINATED_BY

        return self.request.session.get("paginated_by", settings.PAGINATED_BY)


class SearchListView(BaseImageListView):
    """Страница поиска"""

    allow_empty = True

    def get_queryset(self):
        logger.debug("Получаем кверисет для поиска")
        search = Image.objects.all()
        if query := self.request.GET.get("q"):
            query = query.split(", ")
            for tag in query:
                search = search & Image.objects.filter(tags__name=tag.title())
        return search.prefetch_related(
            "tags", "tags__category"
        ).select_related("author")

    def get_context_data(self, *args, **kwargs):
        logger.debug("Получаем контекст поисковой страницы")
        context = super().get_context_data(*args, **kwargs)
        context["q"] = self.request.GET.get("q")
        context["title"] = f'Результаты поиска: "{self.request.GET.get("q")}"'
        return context


class IndexListView(BaseImageListView):
    """Главная страница"""

    allow_empty = True

    def get_context_data(self, *args, **kwargs):
        logger.debug("Получаем контекст главной страницы")
        context = super().get_context_data(*args, **kwargs)
        context["title"] = "Органайзер изображений"
        return context


class TagImageListView(BaseImageListView):
    """Просмотр тега"""

    def get_context_data(self, *args, **kwargs):
        tag_slug = self.kwargs.get("tag_slug")
        logger.debug(f"Получаем контекст страницы тега {tag_slug}")
        context = super().get_context_data(*args, **kwargs)
        tag = Tag.objects.get(slug=tag_slug)
        context["title"] = f"Просмотр тега {tag.name}"
        return context

    def get_queryset(self):
        tag_slug = self.kwargs.get("tag_slug")
        logger.debug(f"Получаем кверисет страницы тега {tag_slug}")
        return super().get_queryset().filter(tags__slug=tag_slug)


class UserImageListView(BaseImageListView):
    """Изображения пользователя"""

    allow_empty = True

    def get_queryset(self):
        logger.debug("Получаем кверисет страницы пользователя")
        if self.request.user.username == self.kwargs.get("username"):
            return (
                self.model.objects.filter(
                    author__username=self.kwargs.get("username")
                )
                .prefetch_related("tags", "tags__category")
                .select_related("author")
            )
        return (
            super()
            .get_queryset()
            .filter(author__username=self.kwargs.get("username"))
        )

    def get_context_data(self, *args, **kwargs):
        logger.debug("Получаем контекст страницы пользователя")
        context = super(UserImageListView, self).get_context_data(
            *args, **kwargs
        )
        context["user"] = get_object_or_404(
            Users, username=self.kwargs.get("username")
        )
        if context["user"] == self.request.user:
            context["tag_form"] = AssignTag()
        context[
            "title"
        ] = f'Галерея пользователя {self.kwargs.get("username")}'
        return context


class PhotoByListView(BaseImageListView):
    """Изображения сделанные на камеру или объективом"""

    def get_queryset(self):
        logger.debug("Получаем кверисет страницы камеры/объектива")
        return (
            super()
            .get_queryset()
            .filter(
                Q(camera_model=self.kwargs.get("model"))
                | Q(lens_model=self.kwargs.get("model"))
            )
        )

    def get_context_data(self, *args, **kwargs):
        logger.debug("Получаем контекст страницы камеры/объектива")
        context = super(PhotoByListView, self).get_context_data(
            *args, **kwargs
        )
        context["title"] = f'Снимки сделанные {self.kwargs.get("model")}'
        return context


class ImageDetailView(DetailView):
    """Просмотр изображения"""

    model = Image
    template_name = "gallery/detail.html"

    def get_object(self, queryset=None):
        logger.debug("Получаем изображение для страницы изображения")
        return get_object_or_404(
            Image,
            Q(private=False) | Q(author__username=self.request.user.username),
            pk=self.kwargs.get("pk"),
        )

    def get_context_data(self, *args, **kwargs):
        logger.debug("Получаем контекст страницы изображения")
        context = super().get_context_data(**kwargs)
        # Добавляем в контекст похожие изображения
        logger.debug("Выбираем похожие изображения")
        related = (
            Image.objects.filter(
                Q(image_hash_part1=self.object.image_hash_part1)
                | Q(image_hash_part2=self.object.image_hash_part2)
                | Q(image_hash_part3=self.object.image_hash_part3)
                | Q(image_hash_part4=self.object.image_hash_part4)
            )
            .exclude(Q(pk=self.object.pk) | Q(private=True))
            .prefetch_related("tags", "tags__category")
            .select_related("author")
        )
        # Считаем расстояние Хемминга между изображениями
        for image in related:
            hamming = hamming_distance(
                image.image_hash_part1, self.object.image_hash_part1
            )
            hamming += hamming_distance(
                image.image_hash_part2, self.object.image_hash_part2
            )
            hamming += hamming_distance(
                image.image_hash_part3, self.object.image_hash_part3
            )
            hamming += hamming_distance(
                image.image_hash_part4, self.object.image_hash_part4
            )
            if hamming > settings.MAX_HEMMING_DISTANCE:
                related = related.exclude(pk=image.pk)

        context["related"] = related[: settings.RELATED_IMAGES]
        form = ImageUpdateForm(instance=self.object)
        if self.request.user == self.object.author:
            context["image_update_form"] = form
        comment_form = CommentForm()
        if self.request.user.is_authenticated:
            context["comment_form"] = comment_form
        context["comments"] = Comment.objects.filter(
            image=self.kwargs["pk"]
        ).select_related("author")
        return context


class ImageCreateView(LoginRequiredMixin, CreateView):
    """Добавление изображения"""

    template_name = "gallery/add_image.html"
    form_class = ImageAddForm

    def form_valid(self, form):
        logger.debug("Добавление изображения, форма валидна")
        form.instance.author = self.request.user
        return super().form_valid(form)


class ImageUpdateView(LoginRequiredMixin, UpdateView):
    """Редактирование информации об изображении"""

    model = Image
    form_class = ImageUpdateForm

    def dispatch(self, request, *args, **kwargs):
        image = get_object_or_404(Image, pk=self.kwargs.get("pk"))
        if self.request.user == image.author:
            return super().dispatch(request, *args, **kwargs)
        return redirect("gallery:image", pk=self.kwargs.get("pk"))


class AddCommentCreateView(LoginRequiredMixin, CreateView):
    """Добавление комментария"""

    model = Comment
    form_class = CommentForm

    def form_valid(self, form):
        logger.debug("Добавление комментария форма валидна")
        form.instance.author = self.request.user
        form.instance.image = Image.objects.get(pk=self.kwargs["pk"])
        return super().form_valid(form)

    def get_success_url(self):
        url = reverse("gallery:image", kwargs={"pk": self.kwargs["pk"]})
        logger.debug(
            f"Перенаправление пользователя на страницу {url} после добавления "
            f"комментария"
        )
        return url
