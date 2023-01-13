from django.contrib import admin
from friends.models import FriendRequest, FriendList

from ofa.utils.cache import CachingPaginator

# Register your models here.
@admin.register(FriendList)
class FriendListAdmin(admin.ModelAdmin):
    list_display = ['user']
    list_filter = ['created_at']
    filter_horizontal = ['friends']
    search_fields = ['user__username', 'user__email']
    autocomplete_fields = ["user"]
    paginator = CachingPaginator


@admin.register(FriendRequest)
class FriendRequestAdmin(admin.ModelAdmin):
    list_select_related = ['sender', 'receiver']
    list_display = ['sender', 'receiver', 'is_active', 'created_at']
    search_fields = ['sender__username', 'sender__email', 'receiver__email','receiver__username']
    autocomplete_fields = ['sender', 'receiver']
    paginator = CachingPaginator
