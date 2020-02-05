from django import forms
from django.shortcuts import render, get_list_or_404
from django.http import HttpResponse, HttpResponseForbidden, Http404
from django.urls import reverse, reverse_lazy
from django.views.generic.list import ListView
from django.views.generic.detail import  DetailView
from django.views.generic.edit import  FormMixin, UpdateView, DeleteView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.exceptions import PermissionDenied
from .models import BlogPost, Comment, BlogCategory
from .forms import CommentCreateForm
from register.models import User

# Create your views here.
def index(request):
    return render(request, 'blog/index.html')


class BlogListView(ListView):
    model = BlogPost
    queryset = BlogPost.list_blogs_with_cats()


class AuthorsListView(ListView):
    model = User
    template_name = 'blog/user_list.html'    

    def get_queryset(self):
        return User.objects.filter(is_author=True)


class CategoriesListView(ListView):
    model = BlogCategory


class BlogListByCategoryView(ListView):
    """Generic class-based view listing blogs for a given category."""

    model = BlogPost
    template_name ='blog/blogposts_by_category.html'
    
    def get_queryset(self):
        queryset = BlogPost.objects.filter(category=self.kwargs['pk']).order_by('-pub_date')
        if queryset:
            return queryset
        raise Http404()


class AuthorDetailView(DetailView):
    model = User
    template_name = 'blog/user_detail.html'
    context_object_name = 'author'


class BlogDetailView(FormMixin, DetailView):
    model = BlogPost
    form_class = CommentCreateForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments_set'] = self.get_object().get_comments()        
        if 'form' in context:
            del context['form']
        if self.request.user.is_authenticated:
            context['form'] = CommentCreateForm(
                initial={
                        'to_blog': self.object,
                        'author': self.request.user
                    })
        return context

    def get_success_url(self):
        return reverse('blog:blog', kwargs={'pk': self.object.id})

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden()
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class CommentEditView(UpdateView, LoginRequiredMixin):
    model = Comment
    fields = ['description']

    def get_object(self, *args, **kwargs):
        obj = super().get_object(*args, **kwargs)
        if not obj.author == self.request.user:
            raise PermissionDenied
        return obj

    def get_success_url(self):
        return reverse('blog:blog', kwargs={'pk': self.object.to_blog.id})


class CommentDeleteView(DeleteView, LoginRequiredMixin):
    model = Comment
    template_name_suffix = '_delete'

    def get_object(self, *args, **kwargs):
        obj = super().get_object(*args, **kwargs)
        if not obj.author == self.request.user:
            raise PermissionDenied
        return obj

    def get_success_url(self):
        return reverse('blog:blog', kwargs={'pk': self.object.to_blog.id})


class BlogPostCreateView(PermissionRequiredMixin, CreateView):
    model = BlogPost
    fields = ['category', 'name', 'body', 'author']
    permission_required = 'blog.can_add_posts'

    def get_initial(self):
        return {
            'author': self.request.user
        }

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['author'].widget = forms.HiddenInput()
        return form
