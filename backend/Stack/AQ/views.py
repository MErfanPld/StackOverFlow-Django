from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import ListView, CreateView
from django.core.paginator import Paginator
from .forms import AnswerCreateForm, AnswerReplyForm
from .models import Question, Category, Answer, Vote, Sliders
from django.contrib.auth.mixins import LoginRequiredMixin
from account.models import User, Relation
from django.db.models import Q


# Create your views here.


class HomeView(ListView):
    template_name = 'AQ/home.html'
    queryset = Question.objects.all()
    paginate_by = 3

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['AllCategory'] = Category.objects.all()
        context['sliders'] = Sliders.objects.all()
        return context


class DetailView(View):
    form_class = AnswerCreateForm
    form_class_reply = AnswerReplyForm

    def setup(self, request, *args, **kwargs):
        self.question_instance = get_object_or_404(Question, pk=kwargs['q_id'], slug=kwargs['q_slug'])
        return super().setup(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        answers = self.question_instance.panswers.filter(is_reply=False)
        can_like = False
        if request.user.is_authenticated and self.question_instance.user_can_like(request.user):
            can_like = True
        return render(request, 'AQ/detail.html',
                      {'question': self.question_instance, 'answers': answers, 'form': self.form_class,
                       'reply_form': self.form_class_reply, 'can_like': can_like})

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            new_answer = form.save(commit=False)
            new_answer.user = request.user
            new_answer.question = self.question_instance
            new_answer.save()
            return redirect('home:detail', self.question_instance.id, self.question_instance.slug)


class CategoryList(ListView):
    paginate_by = 6
    template_name = 'AQ/category_list.html'
    model = Category

    def get_queryset(self):
        global category
        slug = self.kwargs.get('slug')
        category = get_object_or_404(Category.objects.all(), slug=slug)
        return category.questions.all()

    def get_context_data(self, **kwargs):
        context = super(CategoryList, self).get_context_data(**kwargs)
        context['AllCategory'] = Category.objects.all()
        return context


class AddReplyView(LoginRequiredMixin, View):
    form_class = AnswerReplyForm

    def post(self, request, q_id, answer_id):
        question = get_object_or_404(Question, id=q_id)
        answer = get_object_or_404(Answer, id=answer_id)
        form = self.form_class(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.user = request.user
            reply.question = question
            reply.reply = answer
            reply.is_reply = True
            reply.save()
        return redirect('home:detail', question.id, question.slug)


class UserList(LoginRequiredMixin, ListView):
    def get(self, request, pk):
        is_following = False
        user = get_object_or_404(User, pk=pk)
        questions = user.questions.all()
        relation = Relation.objects.filter(from_user=request.user, to_user=user)
        if relation.exists():
            is_following = True
        return render(request, 'AQ/user_list.html',
                      {'user': user, 'questions': questions, 'is_following': is_following})


class Like(LoginRequiredMixin, View):
    def get(self, request, question_id):
        question = get_object_or_404(Question, id=question_id)
        like = Vote.objects.filter(question=question, user=request.user)
        if like.exists():
            messages.error(request, 'you have already liked this question', 'danger')
        else:
            Vote.objects.create(question=question, user=request.user)
            messages.success(request, 'you liked this question', 'success')
        return redirect('home:detail', question.id, question.slug)


class SearchList(ListView):
    paginate_by = 5
    template_name = 'AQ/search_ist.html'

    def get_queryset(self):
        search = self.request.GET.get('q')
        return Question.objects.filter(Q(body__icontains=search) | Q(title__icontains=search))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search'] = self.request.GET.get('q')
        return context

# class SliderView(ListView):
#     template_name = 'AQ/include_sliders.html'
#     queryset = Sliders.objects.all()
#     context_object_name = 'sliders'

# def sliders(request):
#     slider_list = Sliders.objects.all()
#     context = {
#         "slider_list": slider_list
#     }
#     return render(request, 'AQ/home.html', context)
