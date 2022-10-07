from django.contrib import admin

from .models import Listing, Comment, Bid, WatchlistItem, User

# Register your models here.
admin.site.register(Listing)
admin.site.register(Comment)
admin.site.register(Bid)
admin.site.register(WatchlistItem)
admin.site.register(User)