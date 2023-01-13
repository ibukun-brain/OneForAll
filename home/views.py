
from django.contrib import messages
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.views import logout_then_login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import (
    TemplateView, UpdateView, View,
    ListView
)
from django.urls import reverse_lazy

from home.models import CustomUser
from home.forms import UpdateProfileForm
from friends.models import FriendList, FriendRequest
from location.models import Country

from ofa.utils.friends_system import (
    check_friend_request, FriendRequestStatus
)


# Create your views here.
class IndexView(LoginRequiredMixin, TemplateView):
    template_name = "home/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user"] = self.request.user
        return context

class SearchView(LoginRequiredMixin, ListView):
    pass

class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = "home/profile.html"

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     slug = kwargs.get("slug")
    #     user= get_object_or_404(CustomUser, slug=slug)
        
    #     friends_list, _ = FriendList.objects.select_related('user').prefetch_related('friends').get_or_create(user=user)
    #     friends = friends_list.friends.all()
    #     first_4_friends = friends[:4]

    #     # is_self = True
    #     current_user = self.request.user
    #     is_friend = friends_list.is_friend(current_user)
    #     request_sent = FriendRequestStatus.NO_REQUEST_SENT
    #     friend_requests = FriendRequest.objects.select_related('sender','receiver').filter(receiver=user, is_active=True)
    #     first_4_friend_requests = friend_requests[:4]
    #     if current_user != user:
    #         request_sent, pending_friend_request_id  = check_friend_request(user, current_user)
    #         if pending_friend_request_id:
    #             context.update({
    #                 "pending_friend_request_id":pending_friend_request_id
    #             })


    #     context.update({
    #         "user":user,
    #         "is_friend":is_friend,
    #         "friend_requests":friend_requests,
    #         "request_sent":request_sent,
    #         "friends":friends,
    #         "first_4_friends":first_4_friends,
    #         "first_4_friend_requests":first_4_friend_requests,

    #     })
    #     return context
    
class ProfileAboutView(LoginRequiredMixin, TemplateView):
    template_name = "home/profile-about.html"

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     slug = kwargs.get("slug")
    #     user= get_object_or_404(CustomUser, slug=slug)

    #     context ={
    #         "user":user
    #     }

    #     return context

class ConnectionsView(LoginRequiredMixin, TemplateView):
    template_name = "home/connections.html"

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     current_user = self.request.user
    #     slug = kwargs.get("slug")
    #     user = get_object_or_404(CustomUser, slug=slug)
    #     friend_lists, _ = FriendList.objects.select_related('user').prefetch_related('friends').get_or_create(user=user)

    #     friend_list_tuple = []
    #     current_user_friend_list = FriendList.objects.select_related("user").prefetch_related("friends").get(user=current_user)
    #     for friend in friend_lists.friends.all():
    #         friend_list_tuple.append((friend, current_user_friend_list.is_friend(friend)))

    #     context.update({
    #         "friend_list_tuple": friend_list_tuple,
    #         "user":user
    #     })

    #     return context


class MediaView(LoginRequiredMixin, TemplateView):
    template_name = "home/about.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        slug = kwargs.get("slug")
        user = CustomUser.objects.select_related("country").prefetch_related().get(slug=slug)
        context.update({
            "user":user,
        })
        return context

class EventView(LoginRequiredMixin, TemplateView):
    template_name = "home/about.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        slug = kwargs.get("slug")
        user = CustomUser.objects.select_related("country").prefetch_related().get(slug=slug)
        context.update({
            "user":user,
        })
        return context

class ActivityView(LoginRequiredMixin, TemplateView):
    template_name = "home/about.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        slug = kwargs.get("slug")
        user = CustomUser.objects.select_related("country").prefetch_related().get(slug=slug)
        context.update({
            "user":user,
        })
        return context

class UpdateAccountSettingsView(LoginRequiredMixin, UpdateView):
    form_class = UpdateProfileForm
    template_name = "account/edit-profile.html"

    def get_object(self):
        return self.request.user

    def get_success_url(self):
        messages.success(self.request, "Account Updated Successfully")
        return reverse_lazy("home:update-account")

    def form_valid(self, form):
        form = form.save(commit=False)
        print(self.request.POST)
        form.country = Country.objects.get(name=self.request.user.country)
        form.save()
        return redirect(reverse_lazy("home:update-account"))



    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        country = Country.objects.get(name=self.request.user.country)
        iso_code = country.iso_code

        context.update({
            "password_change_form": PasswordChangeForm(user=self.request.user),
            "iso_code":iso_code
            }
        ) # type: ignore

        return context

class CustomPasswordChangeView(View):
    # form_class = PasswordChangeForm

    def get_success_url(self):
        messages.success(self.request, "Your Password has been changed succesfully")
        return reverse_lazy("home:update-account")

    def get(self, request, **kwargs):
        context = {
            "password_change_form":PasswordChangeForm(user=request.user),
            "form":UpdateProfileForm(instance=request.user),
        }
        return render(request, "account/edit-profile.html", context)

    def post(self, request, **kwargs):
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            # return self.form_valid(form)


            messages.success(self.request, "Your Password has been changed succesfully")
            return logout_then_login(request, 'account_login')
            # return redirect("home:update-account")

        else:
            # return self.form_invalid(form)
            # messages.error(self.request, form.error_messages)
            # return redirect("home:update-account")
            context = {
                "password_change_form":PasswordChangeForm(user=request.user, data=request.POST),
                "form":UpdateProfileForm(instance=request.user),
            }
            return render(request, "account/edit-profile.html", context)