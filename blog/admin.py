from django.contrib import admin
from .models import *
# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name','created_at')
    list_filter = ('name',)


class PostAdmin(admin.ModelAdmin):
    list_display = ('title','tags','posted_at')
    list_filter = ('tags',)


class CommentAdmin(admin.ModelAdmin):
    list_display = ('name','email','commented_at','is_resolved')
    list_filter = ('is_resolved','commented_at',)
    list_editable = ('is_resolved',)





admin.site.register(Category,CategoryAdmin)
admin.site.register(Post,PostAdmin)
admin.site.register(Comment,CommentAdmin)