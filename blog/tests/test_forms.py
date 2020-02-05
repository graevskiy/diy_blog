import datetime
from django.test import TestCase
from django import forms
from register.models import User
from blog.models import BlogPost
from blog.forms import CommentCreateForm

class CommentCreateFormTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(
            username='testuser1', password='1X<ISRUkw+tuK',
            is_author=True,
            email='testuser1@g.com'
        )
        self.user1.save()

        self.blog = BlogPost.objects.create(
            name='random post',
            body='Random blog Post text'
        )

    def test_comment_create_form_description_label(self):
        form = CommentCreateForm()
        self.assertTrue(form.fields["description"].label == None or form.fields["description"].label == "Description")

    def test_comment_create_form_help_text(self):
        form = CommentCreateForm()
        self.assertTrue(form.fields["description"].help_text == "")

    def test_comment_form_invalid_if_no_user(self):
        form = CommentCreateForm(data={
            'description': 'test comment'
        })
        self.assertFalse(form.is_valid())

    def test_comment_form_invalid_if_no_blog(self):
        form = CommentCreateForm(data={
            'description': 'test comment',
            'author': self.user1
        })
        self.assertFalse(form.is_valid())

    def test_comment_form_valid(self):
        form = CommentCreateForm(data={
            'description': 'test comment',
            'author': self.user1,
            'to_blog': self.blog
        })
        self.assertFalse(form.is_valid())