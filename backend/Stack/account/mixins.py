from django.http import Http404
from django.shortcuts import get_object_or_404, redirect
from AQ.models import Question


class FieldsMixin():
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_superuser:
            self.fields = ['title', 'user', 'slug', 'category', 'body', 'image']
        elif not request.user.is_superuser:
            self.fields = ['title', 'slug', 'category', 'body', 'image']
        else:
            raise Http404("You cant see this page")
        return super().dispatch(request, *args, **kwargs)


class UserAccessMixin():
    def dispatch(self, request, pk, *args, **kwargs):
        question = get_object_or_404(Question, pk=pk)
        if question.user == request.user or request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        else:
            raise Http404("You cant see this page")
