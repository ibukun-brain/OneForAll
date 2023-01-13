import auto_prefetch
from django.db import models

from ofa.utils.models import TimeBasedModel

# Create your models here.
class FriendList(TimeBasedModel):
    user = auto_prefetch.OneToOneField("home.CustomUser", on_delete=models.CASCADE)
    friends = models.ManyToManyField("home.CustomUser", blank=True, related_name="friends", verbose_name="Friends List")

    class Meta:
        ordering = ['-created_at', '-pk']

    def __str__(self):
        return self.user.username

    def add_friend(self, user):
        """
        Add a new friend
        """
        if not user in self.friends.all():
            self.friends.add(user)


    def remove_friend(self, user):
        """
        Remove a friend
        """
        if user in self.friends.all():
            self.friends.remove(user)

    def unfriend(self, removee):
        """
        Initiate the action of unfriending someone
        """
        remover_friends_list = self #person terminating the friendship

        # Remove friend from remover friend list
        remover_friends_list.remove_friend(removee)

        # Remove friend from removee friend list
        removee_friends_list = FriendList.objects.get(user=removee)
        # friends_list.remove_friend(remover_friends_list.user)
        removee_friends_list.remove_friend(self.user)

    def is_friend(self, friend):
        """
        Is this a mutual friend?
        """
        is_friend = False
        if friend in self.friends.all():
            is_friend = True
            return is_friend 
        return is_friend


class FriendRequest(TimeBasedModel):
    """
    A friend request consists of two main part
        1. SENDER:
            - Person sending/Intiating the friend request
        2. RECEIVER:
            - Person recieiving the friend request

    """

    sender = auto_prefetch.ForeignKey("home.CustomUser", on_delete=models.CASCADE, related_name="sender")
    receiver = auto_prefetch.ForeignKey("home.CustomUser", on_delete=models.CASCADE, related_name="receiver")
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = ('sender', 'receiver')
        ordering = ['-created_at', '-pk']

    def __str__(self):
        return f"{self.sender.username} sent {self.receiver.username} a friend request"

    @property
    def accept(self):
        """
        Accept a friend request
        Update both SENDER and RECIEVER friends list
        """
        receiver_friend_list, _created = FriendList.objects.get_or_create(user=self.receiver)
        if receiver_friend_list:
            receiver_friend_list.add_friend(self.sender)

            sender_friend_list, _created = FriendList.objects.get_or_create(user=self.sender)
            if sender_friend_list:
                sender_friend_list.add_friend(self.receiver)
                self.is_active = False
                self.save()

    @property
    def decline(self):
        """
        When a reciever decline a friend request.
        it is "declined" by setting the is_active field to False
        """
        self.is_active = False
        self.save()

    @property
    def cancel(self):
        """
        When a sender cancels a friend request.
        it is "canceled" by setting the is_active field to False
        This is only different with respect to "declining" through the notification that is generated.
        """

        self.is_active = False
        self.save()
