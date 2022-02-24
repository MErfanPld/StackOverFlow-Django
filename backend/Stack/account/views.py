from django.contrib import messages
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.text import slugify
from django.views.generic import ListView, UpdateView, DeleteView, View
from AQ.models import Question, Category
from .mixins import UserAccessMixin
from django.urls import reverse_lazy
from .forms import CreateUpdateForm, UserRegistrationForm
from .models import User, Relation


# Create your views here.

class Dashboard(LoginRequiredMixin, ListView):
    template_name = 'registration/dashboard.html'

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Question.objects.all()
        else:
            return Question.objects.filter(user=self.request.user)


class QuestionCreate(LoginRequiredMixin, View):
    form_class = CreateUpdateForm

    def get(self, request, *args, **kwargs):
        form = self.form_class
        return render(request, 'registration/create_update.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            new_question = form.save(commit=False)
            new_question.slug = slugify(form.cleaned_data['title'][:30])
            new_question.user = request.user
            new_question.save()
            return redirect('home:detail', new_question.id, new_question.slug)


# class QuestionCreate(LoginRequiredMixin, CreateView):
#     model = Question
#     fields = ['title', 'user', 'slug', 'category', 'body', 'image']
#     template_name = 'registration/create_update.html'


class QuestionUpdate(LoginRequiredMixin, UserAccessMixin, UpdateView):
    form_class = CreateUpdateForm

    def setup(self, request, *args, **kwargs):
        self.post_instance = get_object_or_404(Question, pk=kwargs['pk'])
        return super().setup(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        post = self.post_instance
        if not post.user.id == request.user.id:
            return redirect('home:home')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        post = self.post_instance
        form = self.form_class(instance=post)
        return render(request, 'registration/create_update.html', {'form': form})

    def post(self, request, *args, **kwargs):
        post = self.post_instance
        form = self.form_class(request.POST, request.FILES, instance=post)
        if form.is_valid():
            new_question = form.save(commit=False)
            new_question.slug = slugify(form.cleaned_data['title'][:30])
            new_question.user = request.user
            new_question.save()
            return redirect('home:detail', post.id, post.slug)


# class QuestionUpdate(LoginRequiredMixin, UserAccessMixin, UpdateView):
#     model = Question
#     fields = ['title', 'user', 'slug', 'category', 'body', 'image']
#     template_name = 'registration/create_update.html'


class QuestionDelete(UserAccessMixin, DeleteView):
    model = Question
    success_url = reverse_lazy('account:dashboard')


class Profile(LoginRequiredMixin, UpdateView):
    model = User
    fields = ['username', 'email', 'first_name', 'last_name', 'image', 'city', 'label_job', 'bio']
    template_name = 'registration/profile.html'
    success_url = reverse_lazy('account:profile')

    def get_object(self):
        return User.objects.get(pk=self.request.user.pk)


class Login(LoginView):
    def get_success_url(self):
        user = self.request.user

        if user.is_superuser:
            return reverse_lazy("account:dashboard")
        else:
            return reverse_lazy("account:profile")


class UserRegisterView(View):
    form_class = UserRegistrationForm
    template_name = 'registration/register.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home:home')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            User.objects.create_user(cd['username'], cd['email'], cd['password1'])
            messages.success(request, 'you registered successfully', 'success')
            return redirect('account:login')
        return render(request, self.template_name, {'form': form})


class UserFollowView(LoginRequiredMixin, View):
    def get(self, request, pk):
        user = User.objects.get(id=pk)
        relation = Relation.objects.filter(from_user=request.user, to_user=user)
        if relation.exists():
            messages.error(request, 'you are already following this user', 'danger')
        else:
            Relation(from_user=request.user, to_user=user).save()
            messages.success(request, 'you followed this user', 'success')
        return redirect('home:user_profile', user.pk)


class UserUnfollowView(LoginRequiredMixin, View):
    def get(self, request, pk):
        user = User.objects.get(id=pk)
        relation = Relation.objects.filter(from_user=request.user, to_user=user)
        if relation.exists():
            relation.delete()
            messages.success(request, 'you unfollowed this user', 'success')
        else:
            messages.error(request, 'you are not following this user', 'danger')
        return redirect('home:user_profile', user.pk)


class PasswordChange(PasswordChangeView):
    success_url = reverse_lazy('account:profile')
