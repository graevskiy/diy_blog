from datetime import date
from django.db import models
from django.urls import reverse
from django.conf import settings


# Create your models here.

class BlogCategory(models.Model):
    name = models.CharField(max_length=200, help_text='Category of a Blog', unique=True)

    class Meta:
        verbose_name = 'Blog category'
        verbose_name_plural = 'Blog categories'

    def __str__(self):
        """String for representing the Model object."""
        return self.name

    def get_absolute_url(self):
        return reverse('blog:blogs_of_category', args=[str(self.id)])


class BlogPost(models.Model):
    name = models.CharField(max_length=200, help_text='Blog Post Header')
    body = models.TextField(help_text='Blog Post Body')
    pub_date = models.DateField(default=date.today, help_text='Date When Post Was Created')    

    # even though we should not delete authors from DB set on_delete option to Null to keep post
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)

    category = models.ForeignKey(BlogCategory, on_delete=models.SET_NULL, null=True)

    class Meta:
        ordering = ['-pub_date', 'category']
        permissions = [('can_add_posts', 'Can add Posts')]

    def __str__(self):
        """String for representing the Model object."""
        auth_ins = f'by {self.author}' if self.author else '- NO Author'
        return f"{self.name} {auth_ins}"

    def get_absolute_url(self):
        return reverse('blog:blog', args=[str(self.id)])

    def get_comments(self):
        return self.comment_set.all()

    @classmethod
    def list_blogs_with_cats(cls):
        return cls.objects.select_related('category', 'author').all()


class Comment(models.Model):
    description = models.TextField()
    pub_date = models.DateField(default=date.today, help_text='Date When Comment Was Added')

    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)

    to_blog = models.ForeignKey(BlogPost, on_delete=models.CASCADE)

    def __str__(self):
        """String for representing the Model object."""
        return f"Comment of {self.author} - \"{self.description}\""