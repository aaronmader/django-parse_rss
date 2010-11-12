from django.contrib import admin
from parse_rss.models import *

class ArticleAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'feed','pubDate', 'created',)
    
admin.site.register(Feed)
admin.site.register(Article, ArticleAdmin)

