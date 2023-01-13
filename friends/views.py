from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, ListView

from friends.models import FriendRequest, FriendList
from ofa.utils.mixins import IsSelf
from home.models import CustomUser

class FriendRequestListView(IsSelf, LoginRequiredMixin, ListView):
    template_name = "friends/friend_request_lists.html"
    model = FriendRequest
    context_object_name = "friend_requests"

    def get_queryset(self):
        user = self.request.user

        queryset = super().get_queryset()
        queryset = FriendRequest.objects.filter(
            receiver=user, is_active=True
        ).select_related("sender","receiver")

        return queryset

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     user = self.request.user
    #     friend_lists = FriendList.objects.select_related("user") \
    #                     .prefetch_related("friends").get(user=user)
    #     friends = friend_lists.friends.all()

    #     context.update({
    #        "friends":friends,

    #     })
    #     return context
    


# class FriendListView(LoginRequiredMixin, View):
class FriendListView(IsSelf, LoginRequiredMixin, ListView):
    template_name = "friends/friend_lists.html"
    context_object_name = "friend_lists"
    model = FriendList

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     user = self.request.user
    #     friend_lists = FriendList.objects.select_related("user") \
    #                     .prefetch_related("friends").get(user=user)
    #     friends = friend_lists.friends.all()

    #     friend_requests = FriendRequest.objects.filter(
    #         receiver=user, is_active=True
    #     ).select_related("sender","receiver")

    #     context.update({
    #         "friend_requests":friend_requests,
    #         "friends":friends,

    #     })
    #     return context
    

    # def get(self, request, *args, **kwargs):
    
        # context = {}
        # current_user = request.user
        # slug = kwargs.get("slug")
        # if slug:
        #     this_user = get_object_or_404(CustomUser, slug=slug)
        #     context["this_user"] = this_user
        #     friend_list = get_object_or_404(FriendList, user=this_user)

        #     friends = []
        #     current_user_friend_list = FriendList.objects.select_related("user").prefetch_related("friends").get(user=current_user)
        #     for friend in friend_list.friends.all():
        #         friends.append((friend, current_user_friend_list.is_friend(friend)))

        #     context.update({
        #         "friends": friends,
        #     })

        
        # # return render(request, "friends/friend_lists.html", context=context)

    