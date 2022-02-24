from django.urls import path
from .views import DetailView, HomeView, CategoryList, AddReplyView, UserList, Like, SearchList

app_name = "home"

urlpatterns = [
    path('', HomeView.as_view(), name="home"),
    path('question/<int:q_id>/<slug:q_slug>/', DetailView.as_view(), name="detail"),
    path('question/category/<slug:slug>/', CategoryList.as_view(), name="category"),
    path('reply/<int:q_id>/<int:answer_id>/', AddReplyView.as_view(), name="reply"),
    path('user/<int:pk>/', UserList.as_view(), name="user_profile"),
    path('search/', SearchList.as_view(), name="search"),
    path('like/<int:question_id>', Like.as_view(), name="like"),
]

