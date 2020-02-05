from django.contrib import admin
from django.db.models import Count

from .models import BlogCategory, BlogPost, Comment

# Register your models here.
admin.site.register(BlogCategory)
admin.site.register(Comment)



class BlogPostListFilter(admin.SimpleListFilter):
    title = 'number of comments'
    parameter_name = 'num_comments'

    def lookups(self, request, model_admin):
        return (
                ('0', '0'),
                ('1_more', '1+'),
                ('10_more', '10+'),
                ('100_more', '100+')
            )

    def queryset(self, request, queryset):
        qs = queryset.annotate(num_comments=Count('comment'))
        if self.value() == '0':
            return qs.filter(num_comments=0)
        elif self.value() == '1_more':            
            return qs.filter(num_comments__gte=1)
        elif self.value() == '10_more':
            return qs.filter(num_comments__gte=10)
        elif self.value() == '100_more':            
            return qs.filter(num_comments__gte=100)
        return queryset

class BlogPostInlineAdmin(admin.TabularInline):
    model = BlogCategory
    extra = 0

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):

    readonly_fields = ('pub_date',)
    
    list_display = ('id', '__str__', 'pub_date', 'category')
    list_display_links = ('__str__',)
    
    list_filter = ('pub_date', 'category', BlogPostListFilter)

    inline = [BlogPostInlineAdmin]

