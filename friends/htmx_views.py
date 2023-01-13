from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import  redirect, render, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.urls import reverse_lazy
from django.views.generic import View, TemplateView

from django_htmx.http import HttpResponseClientRefresh

from home.models import CustomUser
from friends.models import FriendRequest, FriendList

from ofa.utils.friends_system import FriendRequestStatus


class SendFriendRequestView(LoginRequiredMixin, View):
    
    def post(self, request, *args, **kwargs):

        if request.htmx:
           
            current_user = request.user
            payload = {}
            user_receiver = request.POST.get('user_receiver')
            request_sent = FriendRequestStatus.YOU_SENT_TO_THEM.value
            if user_receiver:
                receiver = CustomUser.objects.get(slug=user_receiver)

                friend_request, created = FriendRequest.objects.get_or_create(sender=current_user, receiver=receiver, is_active=True)

                if created:
                    payload['response'] = "Friend Request sent"
                else:
                    # payload['response'] = "You already sent a friend request"
                    return HttpResponse("<html><body><script>alert(you already sent a friend request)</script></body></html>")
            else:
                payload['response'] = "Unable to send a friend request"
            context =  {
                'request_sent':request_sent,
                "user": friend_request.receiver,
            }
            template_name = "friends/partials/_cancel_friend_request.html" 
            return render(request, template_name=template_name, context=context)
      

class AcceptFriendRequestView(LoginRequiredMixin, View):


    def post(self, request, *args, **kwargs):

        if request.htmx:
            # friend_requests_url = request.build_absolute_uri(f'/friends/friend-requests/{request.user}/')
            profile_url = request.build_absolute_uri(f'/profile/{request.POST.get("sender__user")}/')
            connection_url = request.build_absolute_uri(f'/connections/{request.POST.get("sender__user")}/')

            # print("htmx current url", request.htmx.current_url)
            current_user = request.user
            payload = {}
            pending_friend_request_id = request.POST.get('pending_friend_request_id')
            # print(pending_friend_request_id)
            if pending_friend_request_id:
                friend_request = FriendRequest.objects.get(pk=pending_friend_request_id)
                if friend_request:
                    friend_request.accept
                else:
                    return HttpResponse('Something went wrong')
            else:
                return HttpResponse("unable to accept friend request")

            friend_request.delete()
            # return redirect('friends:friend-requests', request.user)
            # return HttpResponse('')
           
            if request.htmx.current_url == profile_url:
                template_name = "friends/partials/_friend_profile_update.html" 
                user_slug = request.POST.get("sender__user")
                user = get_object_or_404(CustomUser, username=user_slug)
                friends_list, _ = FriendList.objects.get_or_create(user=user)
                
                friends = friends_list.friends.all()
                number_of_friends = friends.all().count()
                is_friend = False
                current_user = self.request.user

                if current_user in friends:
                    is_friend = True
                else:
                    is_friend = False
                
                
                context = {
                    "user":user,
                    "is_friend":is_friend,
                    'friends':friends,
                    'number_of_friends':number_of_friends,
                }
                return render(request, template_name=template_name, context=context)
            elif request.htmx.current_url == connection_url:
                return HttpResponseClientRefresh()
            else:
                template_name = "friends/partials/_friend_request_list.html" 
                friends_list, _ = FriendList.objects.select_related('user').prefetch_related('friends').get_or_create(user=current_user)
                friends = friends_list.friends.all()
                friend_requests = FriendRequest.objects.filter(receiver=current_user, is_active=True).select_related('sender','receiver')
                context = {
                    "friend_requests":friend_requests,
                    "friends":friends,
                }
                return render(request, template_name=template_name, context=context)
        
class RemoveFriendView(LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):
        print(kwargs)

        if request.htmx:
            profile_url = request.build_absolute_uri(f'/profile/{request.POST.get("remover_friend")}/')
            connection_url = request.build_absolute_uri(f'/connections/{request.POST.get("remover_friend")}/')
            # print(profile_url)
            # print(request.htmx.current_url)
          
            current_user = request.user
            payload = {}
            remover_friend = request.POST.get('remover_friend')
            user = get_object_or_404(CustomUser, slug=remover_friend)
            if remover_friend:
                removee = CustomUser.objects.get(slug=remover_friend)
                friend_list = FriendList.objects.get(user=current_user)
                friend_list.unfriend(removee)
                # return HttpResponse(f"<html><body><scr>alert('{remover_friend} was successfully removed as your friend')</scr></body></html>")
                if request.htmx.current_url == profile_url:            
                    template_name = "friends/partials/_friend_profile_update.html" 
                    # friends_list, _ = FriendList.objects.select_related('user').prefetch_related('friends').get_or_create(user=user)
                    
                    friends = friend_list.friends.all()
                    number_of_friends = friends.all().count()
                    is_friend = False
                    request_sent = FriendRequestStatus.NO_REQUEST_SENT.value
                    context = {
                        "user":user,
                        "request_sent":request_sent,
                        "is_friend":is_friend,
                        'friends':friends,
                        'number_of_friends':number_of_friends,
                    }
                    return render(request, template_name=template_name, context=context)

                elif request.htmx.current_url == connection_url:
                    return HttpResponseClientRefresh()
                
                else:
                    template_name = "friends/partials/_friend_list.html" 
                    # user = get_object_or_404(CustomUser, username=user_slug)
                    # friends_list, _ = FriendList.objects.select_related('user').prefetch_related('friends').get_or_create(user=user)
                    friends = friend_list.friends.all()
                    number_of_friends = friends.all().count()
                    is_friend = False
                    request_sent = FriendRequestStatus.NO_REQUEST_SENT.value
                    friend_requests = FriendRequest.objects.filter(receiver=current_user, is_active=True).select_related('sender','receiver')
                    context = {
                        "friend_requests":friend_requests,
                        "friends":friends,
                        'number_of_friends':number_of_friends,
                    }
                    return render(request, template_name=template_name, context=context)
               
            else:
                return HttpResponse("<html><body><script>alert('There was an error, unable to remove friend request')</script></body></html>")

            # return redirect('friends:friend-requests', request.user)
            # return HttpResponse('')
           
 
            

class DeclineFriendRequestView(LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):
        if request.htmx:
            # friend_requests_url = request.build_absolute_uri(f'/friends/friend-requests/{request.user}/')
            profile_url = request.build_absolute_uri(f'/profile/{request.POST.get("sender__user")}/')

            current_user = request.user
            pending_friend_request_id = request.POST.get('pending_friend_request_id')
            if pending_friend_request_id:
                friend_request = FriendRequest.objects.get(pk=pending_friend_request_id)
    
                if friend_request.receiver == current_user:
                    friend_request.decline

                else:
                    return HttpResponse('Something went wrong!, this is not friend request to decline')
            else:
                return HttpResponse("unable to decline friend request")

            friend_request.delete()

            # return redirect('friends:friend-requests', request.user)
            # return HttpResponse('')
            
            if request.htmx.current_url == profile_url:
                template_name = "friends/partials/_friend_profile_update.html" 
                user_slug = request.POST.get("sender__user")
                user = get_object_or_404(CustomUser, slug=user_slug)
                friends_list, _ = FriendList.objects.get_or_create(user=user)
                
                friends = friends_list.friends.all()
                is_friend = False
                is_self = False
                current_user = self.request.user
                request_sent = FriendRequestStatus.NO_REQUEST_SENT.value
                if current_user in friends:
                    is_friend = True
                else:
                    is_friend = False
                
                
                context = {
                    "user":user,
                    "is_friend":is_friend,
                    "is_self":is_self,
                    'friends':friends,
                    'request_sent':request_sent
                }
                return render(request, template_name=template_name, context=context)
            else:
                template_name = "friends/partials/_friend_request_list.html" 
                # user = get_object_or_404(CustomUser, username=user_slug)
                friends_list, _ = FriendList.objects.select_related('user').prefetch_related('friends').get_or_create(user=current_user)
                friends = friends_list.friends.all()
                friend_requests = FriendRequest.objects.filter(receiver=current_user, is_active=True).select_related('sender','receiver')
                context = {
                    "friend_requests":friend_requests,
                    "friends":friends,
                }
                return render(request, template_name=template_name, context=context)

class CancelFriendRequestView(LoginRequiredMixin, View):
    
    def post(self, request, *args, **kwargs):
        user_fullname = kwargs.get("slug")

        if request.htmx:
           
            current_user = request.user
            payload = {}
            user_receiver = request.POST.get('user_receiver')
            # print(user_receiver)
            request_sent = FriendRequestStatus.NO_REQUEST_SENT.value
            if user_receiver:
                receiver = CustomUser.objects.get(slug=user_receiver)
                friend_request = FriendRequest.objects.get(sender=current_user, receiver=receiver, is_active=True)
                if friend_request:
                    friend_request.cancel
                    friend_request.delete()
                    payload['response'] = "Friend Request cancelled"
                else:
                    payload['response'] = "Nothing to cancel. Friend request does not exist"

            context =  {
                'request_sent':request_sent,
                "user":friend_request.receiver,
            }
            template_name = "friends/partials/_send_friend_request.html" 
            return render(request, template_name=template_name, context=context)