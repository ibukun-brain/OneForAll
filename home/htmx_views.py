from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import View

from home.models import CustomUser


class AboutHTMXView(LoginRequiredMixin, View):
    # template_name = "home/about.html"

    def get(self, request, *args, **kwargs):
        slug = kwargs.get("slug")
        if request.htmx:
            user = CustomUser.objects.select_related("country").prefetch_related().get(slug=slug)
            context = {
                "user":user,
            }

            return render(request, 'home/partials/_about.html', context)
        
            """
                if htmx request fails render normal request
            """
        else:
            slug = kwargs.get("slug")
            user = CustomUser.objects.select_related("country").prefetch_related().get(slug=slug)
            context = {
                "user":user,
            }

            return render(request, 'home/about.html', context)

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     user = CustomUser.objects.select_related("country").prefetch_related().get(slug=slug)
    #     context.update({
    #         "user":user,
    #     })
    #     return context
