from django.urls import path
from friends.htmx_views import (SendFriendRequestView, AcceptFriendRequestView,
                                RemoveFriendView, DeclineFriendRequestView,
                                CancelFriendRequestView
                                )
from friends.views import FriendRequestListView, FriendListView

app_name = 'friends'

urlpatterns = [
    path('send-friend-request/', SendFriendRequestView.as_view(), name='send-friend-request'),
    path('remove-friend-request/', RemoveFriendView.as_view(), name='remove-friend'),
    path('accept-friend-request/', AcceptFriendRequestView.as_view(), name='accept-friend-request'),
    path('decline-friend-request/', DeclineFriendRequestView.as_view(), name='decline-friend-request'),
    path('cancel-friend-request/', CancelFriendRequestView.as_view(), name='cancel-friend-request'),
    path('<slug:slug>/requests/', FriendRequestListView.as_view(), name='friend-requests'),
    path('<slug:slug>/', FriendListView.as_view(), name="friend-lists")

]