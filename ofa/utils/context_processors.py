from django.shortcuts import get_object_or_404

from friends.models import FriendList, FriendRequest
from home.models import CustomUser
from ofa.utils.friends_system import (
    check_friend_request, FriendRequestStatus
)

def friend_system_check(request, *args, **kwargs):
    # namespace = request.resolver_match.namespace

    # slug = None
    # try:
    if request.path == '/':
        slug = ''
    else:
        slug = request.path.split('/')[2]
    # except IndexError as e:
    #     pass
    context = {}

    if slug:
        try:
            user= CustomUser.objects.get(slug=slug)
            friends_list, _ = FriendList.objects.select_related('user').prefetch_related('friends').get_or_create(user=user)
            friends = friends_list.friends.all()
            first_4_friends = friends[:4]

            # is_self = True
            current_user = request.user
            is_friend = friends_list.is_friend(current_user)
            request_sent = FriendRequestStatus.NO_REQUEST_SENT
            friend_requests = FriendRequest.objects.select_related('sender','receiver').filter(receiver=user, is_active=True)
            first_4_friend_requests = friend_requests[:4]
            if current_user != user:
                request_sent, pending_friend_request_id  = check_friend_request(user, current_user)
                if pending_friend_request_id:
                    context = {
                        "pending_friend_request_id":pending_friend_request_id
                    }
            # else:
            #     request_sent, pending_friend_request_id  = check_friend_request(current_user, user)
            #     if pending_friend_request_id:
            #         context.update({
            #             "pending_friend_request_id":pending_friend_request_id
                    # })
            
            friend_list_tuple = []
            current_user_friend_list = FriendList.objects.get(user=current_user)
            for friend in friends_list.friends.all():
                friend_list_tuple.append((friend, current_user_friend_list.is_friend(friend)))  


            context.update({
                "friend_list_tuple": friend_list_tuple,
                "user":user,
                "is_friend":is_friend,
                "friend_requests":friend_requests,
                "request_sent":request_sent,
                "friends":friends,
                "first_4_friends":first_4_friends,
                "first_4_friend_requests":first_4_friend_requests,
            })
        
        except CustomUser.DoesNotExist:
            pass
       

    return context