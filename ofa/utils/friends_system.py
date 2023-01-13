from friends.models import FriendRequest, FriendList
from django.db import models
class FriendRequestStatus(models.IntegerChoices):
    NO_REQUEST_SENT = -1 #We are not friends yet and no friend request has been sent and you are look at their profile
    THEM_SENT_TO_YOU = 0 #We are not friends yet and a friend request was sent to you and you are looking at their profile
    YOU_SENT_TO_THEM = 1 #We are not friends yet and you sent a friend request to them and you are looking at their profile


def get_friend_request_or_false(sender, receiver):
    try:
        return FriendRequest.objects.select_related('sender','receiver').get(sender=sender, receiver=receiver, is_active=True)
    except FriendRequest.DoesNotExist:
        return False

def check_friend_request(user, current_user):
       
    """
    CASE1: Request has been sent to you
    FriendRequestStatus.THEM_SENT_TO_YOU
    """

    context = {}
    request_sent = FriendRequestStatus.NO_REQUEST_SENT.value
    # my_friend_request = FriendRequest.objects.select_related('sender','receiver').get(sender=user, receiver=current_user)

    if get_friend_request_or_false(sender=user, receiver=current_user):
        request_sent = FriendRequestStatus.THEM_SENT_TO_YOU.value
        pending_friend_request_id = get_friend_request_or_false(sender=user, receiver=current_user).pk  # type: ignore

        # return request_sent, context
        return request_sent, pending_friend_request_id


    elif get_friend_request_or_false(sender=current_user, receiver=user):
        """
        CASE2: Request has been sent from you to them
        FriendRequestStatus.YOU_SENT_TO_THEM
        """
        request_sent = FriendRequestStatus.YOU_SENT_TO_THEM.value
    
      
        return request_sent, None

    """
    CASE3: No request has been sent
    FriendRequestStatus.NO_REQUEST_SENT
    """
    # request_sent = FriendRequestStatus.NO_REQUEST_SENT.value
    return request_sent, None

      