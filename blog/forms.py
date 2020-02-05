
from django import forms
from .models import Comment
from django.views.generic.detail import SingleObjectMixin
from django.contrib.auth.decorators import login_required


class CommentCreateForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ['description', 'to_blog', 'author']
        widgets = {
            'author': forms.HiddenInput(),
            'to_blog': forms.HiddenInput(),
        }

