import datetime
from django.test import TestCase

from blog.models import BlogPost, BlogCategory, Comment
from register.models import User

class BlogPostModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        BlogPost.objects.create(name='Why being a boss not that cool', body='because you have to be')
        BlogCategory.objects.create(name='Art')
        blog = BlogPost.objects.get(id=1)
        category = BlogCategory.objects.get(id=1)
        blog.category = category
        blog.save()

    def test_name_label(self):
        blog = BlogPost.objects.get(id=1)
        field_label = blog._meta.get_field('name').verbose_name
        self.assertEqual(field_label, 'name')

    def test_expected_obj_name(self):
        blog = BlogPost.objects.get(id=1)
        if blog.author:
            self.assertEqual(f"{blog.name} by {blog.author}", str(blog))
        else:
            self.assertEqual(f"{blog.name} - NO Author", str(blog))

    def test_max_length_name(self):
        blog = BlogPost.objects.get(id=1)
        blog_max_length = blog._meta.get_field('name').max_length
        self.assertEqual(blog_max_length, 200)

    def test_abs_url(self):
        blog = BlogPost.objects.get(id=1)
        self.assertEqual(blog.get_absolute_url(), '/blog/1/')

    def test_list_blogs_with_cats(self):
        all_cats = set(BlogCategory.objects.all())
        blogs_with_cats = BlogPost.list_blogs_with_cats()
        all_cats_from_func = set([ blog.category for blog in blogs_with_cats ])
        self.assertEqual(all_cats, all_cats_from_func)
        self.assertNumQueries(1, lambda: list(BlogPost.list_blogs_with_cats()))


class BlogCategoryTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        BlogCategory.objects.create(name='Art')

    def test_verbose_names(self):
        category = BlogCategory.objects.get(id=1)
        self.assertEqual(category._meta.verbose_name, 'Blog category')
        self.assertEqual(category._meta.verbose_name_plural, 'Blog categories')

    def test_max_len_name_field(self):
        category = BlogCategory.objects.get(id=1)
        category_max_length = category._meta.get_field('name').max_length
        self.assertEqual(category_max_length, 200)


class CommentTest(TestCase):
    @classmethod
    def setUpTestData(cls):        
        blog = BlogPost.objects.create(name='Why being a boss not that cool', body='because you have to be')
        Comment.objects.create(to_blog=blog)

    def test_comment_pub_date(self):
        comment = Comment.objects.get(id=1)
        self.assertEqual(comment.pub_date, datetime.date.today())
