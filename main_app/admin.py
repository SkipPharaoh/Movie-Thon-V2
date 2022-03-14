from django.contrib import admin
from .models import Comment, UserProfile, CommentSection, Watchlist

admin.site.register(Comment)
admin.site.register(UserProfile)
admin.site.register(CommentSection)
admin.site.register(Watchlist)
