import datetime

from django.test import TestCase
from django.urls import reverse

from blog.models import BlogCategory, BlogPost, Comment
from register.models import User


class BlogListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        for i in range(0, 21):
            BlogPost.objects.create(
                name="Random Name",
                body="This is a random text for a random Blog",
                pub_date=datetime.date.today() - datetime.timedelta(days=i)
            )

    def test_blog_list_url_location(self):
        response = self.client.get('/blog/blogs/')
        self.assertEqual(response.status_code, 200)

    def test_blog_list_url_by_name(self):
        response = self.client.get(reverse('blog:blogs'))
        self.assertEqual(response.status_code, 200)

    def test_blog_list_uses_correct_tempalte(self):
        response = self.client.get(reverse('blog:blogs'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/blogpost_list.html')

    def test_lists_all_blogs(self):
        response = self.client.get(reverse('blog:blogs'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.context['blogpost_list']) == 21)

    def test_blog_list_pagination(self):
        response = self.client.get(reverse('blog:blogs'))
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] == False)


class AuthorsListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        for i in range(0,5):
            user = User.objects.create_user(
                username=f'testuser{i}', 
                password='1X<ISRUkw+tuK', 
                is_author=True if i > 2 else False,
                email=f'user{i}@gmail.com'
            )
            user.save()

    def test_author_list_url_location(self):
        response = self.client.get('/blog/authors/')
        self.assertEqual(response.status_code, 200)

    def test_author_list_url_by_name(self):
        response = self.client.get(reverse('blog:authors'))
        self.assertEqual(response.status_code, 200)

    def test_author_list_uses_correct_tempalte(self):
        response = self.client.get(reverse('blog:authors'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/user_list.html')

    def test_lists_all_authors(self):
        response = self.client.get(reverse('blog:authors'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('user_list' in response.context)
        self.assertTrue(len(response.context['user_list']) == 2)


class CategoriesListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        for i in range(0, 5):
            BlogCategory.objects.create(
                name=f'Random Category {i}'
            )

    def test_category_list_url_location(self):
        response = self.client.get('/blog/categories/')
        self.assertEqual(response.status_code, 200)
        
    def test_category_list_url_by_name(self):
        response = self.client.get(reverse('blog:categories'))
        self.assertEqual(response.status_code, 200)

    def test_category_list_uses_correct_template(self):
        response = self.client.get(reverse('blog:categories'))
        self.assertEqual(response.status_code, 200)        
        self.assertTemplateUsed(response, 'blog/blogcategory_list.html')

    def test_category_lists_all(self):
        response = self.client.get(reverse('blog:categories'))
        self.assertTrue('blogcategory_list' in response.context)
        self.assertTrue(len(response.context['blogcategory_list']) == 5)


class BlogListByCategoryViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        for i in range(0, 5):
            cat = BlogCategory.objects.create(
                name=f'Random Category {i}'
            )
            for j in range(0, 5):
                BlogPost.objects.create(
                    name=f'blog {j}',
                    body=f'Random body',
                    category=cat
                )

    def test_blog_list_by_cat_url(self):
        cats = BlogCategory.objects.all()
        response = self.client.get(f'/blog/category/{cats[0].id}/')
        self.assertEqual(response.status_code, 200)
        response = self.client.get(f'/blog/category/{len(cats)+1}/')
        self.assertEqual(response.status_code, 404)

    def test_cat_list_by_brand_url_by_name(self):
        response = self.client.get(reverse('blog:blogs_of_category', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 200)


class AuthorDetailViewTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username=f'testuser', 
            password='1X<ISRUkw+tuK', 
            is_author=True,
            email=f'user_test@gmail.com'
        )
        self.user.save()

    def test_author_detail_url_location(self):
        response = self.client.get(f'/blog/author/{self.user.id}/')
        self.assertEqual(response.status_code, 200)

    def test_author_detail_url_by_name(self):
        response = self.client.get(reverse('blog:author', kwargs={'pk': self.user.id}))
        self.assertEqual(response.status_code, 200)

    def test_author_detail_context_data_name(self):
        response = self.client.get(reverse('blog:author', kwargs={'pk': self.user.id}))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('author' in response.context)
        self.assertTrue(response.context['author'] is not None)

    def test_author_detail_uses_correct_template(self):
        response = self.client.get(reverse('blog:author', kwargs={'pk': self.user.id}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/user_detail.html')


class BlogDetailViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cat = BlogCategory.objects.create(
            name='blog Category'
        )
        blog = BlogPost.objects.create(
            name='random post',
            body='Random blog Post text',
            category=cat
        )
        for i in range(0, 100):
            Comment.objects.create(
                description=f'autogenerated comment #{i}',
                to_blog=blog
            )

    def test_blog_detail_url_location(self):
        blog = BlogPost.objects.get(id=1)
        response = self.client.get(f'/blog/{blog.id}/')
        self.assertEqual(response.status_code, 200)

    def test_blog_detail_url_by_name(self):
        blog = BlogPost.objects.get(id=1)
        response = self.client.get(reverse('blog:blog', kwargs={'pk': blog.id}))
        self.assertEqual(response.status_code, 200)

    def test_blog_detail_uses_correct_tempalte(self):
        blog = BlogPost.objects.get(id=1)
        response = self.client.get(reverse('blog:blog', kwargs={'pk': blog.id}))
        self.assertTemplateUsed(response, 'blog/blogpost_detail.html')

    def test_number_of_comments(self):
        blog = BlogPost.objects.get(id=1)
        response = self.client.get(reverse('blog:blog', kwargs={'pk': blog.id}))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('comments_set' in response.context)
        self.assertTrue(len(response.context['comments_set']) == 100)


class BlogDetailViewWithCommentFormTest(TestCase):    
    def setUp(self):
        test_user1 = User.objects.create_user(
            username='testuser1', password='1X<ISRUkw+tuK',
            is_author=True,
            email='testuser1@g.com'
        )
        test_user2 = User.objects.create_user(
            username='testuser2', password='2HJ1vRV0Z&3iD',
            is_author=False,
            email='testuser2@g.com'
        )

        test_user1.save()
        test_user2.save()

        self.category = BlogCategory.objects.create(
            name='blog Category'
        )
        self.blog = BlogPost.objects.create(
            name='random post',
            body='Random blog Post text',
            category=self.category
        )
        self.comment1 = Comment.objects.create(
            description='random text',
            author=test_user1,
            to_blog=self.blog
        )
        self.comment2 = Comment.objects.create(
            description='random text',
            author=test_user2,
            to_blog=self.blog
        )

    def test_not_logged_user_cant_comment(self):
        response = self.client.get(reverse('blog:blog', kwargs={'pk': self.blog.id}))
        self.assertTrue(response.status_code, 200)
        self.assertTrue('form' not in response.context)

    def test_logged_user_sees_comment_form(self):
        login = self.client.login(username='testuser2', password='2HJ1vRV0Z&3iD')
        response = self.client.get(reverse('blog:blog', kwargs={'pk': self.blog.id}))
        self.assertTrue(response.status_code, 200)
        self.assertTrue('form' in response.context)
        self.assertEqual(response.context['form'].initial['to_blog'], self.blog)
        self.assertEqual(response.context['form'].initial['author'], response.context['user'])

    def test_cannot_edit_comments_not_logged_in(self):
        response = self.client.get(reverse('blog:edit-comment', kwargs={'pk': self.comment1.id}))
        self.assertTrue(response.status_code, 403)

    def test_cannot_delete_comments_not_logged_in(self):
        response = self.client.get(reverse('blog:delete-comment', kwargs={'pk': self.comment1.id}))
        self.assertTrue(response.status_code, 403)

    def test_cannot_edit_others_comments(self):
        login = self.client.login(username='testuser2', password='2HJ1vRV0Z&3iD')
        response = self.client.get(reverse('blog:edit-comment', kwargs={'pk': self.comment1.id}))
        self.assertTrue(response.status_code, 403)

    def test_cannot_delete_others_comments(self):
        login = self.client.login(username='testuser2', password='2HJ1vRV0Z&3iD')
        response = self.client.get(reverse('blog:delete-comment', kwargs={'pk': self.comment1.id}))
        self.assertTrue(response.status_code, 403)

    def test_can_edit_their_own_comments(self):
        login = self.client.login(username='testuser2', password='2HJ1vRV0Z&3iD')
        response = self.client.get(reverse('blog:edit-comment', kwargs={'pk': self.comment2.id}))
        self.assertTrue(response.status_code, 200)

    def test_can_delete_their_own_comments(self):
        login = self.client.login(username='testuser2', password='2HJ1vRV0Z&3iD')
        response = self.client.get(reverse('blog:delete-comment', kwargs={'pk': self.comment2.id}))
        self.assertTrue(response.status_code, 200)