from django.shortcuts import render
from django.views.generic import TemplateView


def page_not_found(request, exception):
    """Страница 404 ошибки"""
    template_name = "pages/404.html"
    return render(request, template_name, status=404)


def forbidden(request, exception):
    """Страница 403 ошибки"""
    template_name = "pages/403.html"
    return render(request, template_name, status=403)


def csrf_failure(request, reson=""):
    """Страница ошибки csfr токена"""
    template_name = "pages/403csrf.html"
    return render(request, template_name, status=403)


def server_error(request):
    """Страница 500 ошибки"""
    template_name = "pages/500.html"
    return render(request, template_name, status=500)


def bad_request(request, exception):
    template_name = "pages/400.html"
    return render(request, template_name, status=400)


class AboutTemplateView(TemplateView):
    """Страница 'о проекте'"""

    template_name = "pages/about.html"
