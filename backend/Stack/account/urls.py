from django.contrib.auth import views
from django.urls import path
from .views import Dashboard, QuestionCreate, QuestionUpdate, QuestionDelete, Profile, Login, UserFollowView, \
    UserUnfollowView, UserRegisterView, PasswordChange

app_name = 'account'

urlpatterns = [
    path('login/', Login.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('password_change/', PasswordChange.as_view(), name='password_change'),
    # path('password_reset/', views.PasswordResetView.as_view(), name='password_reset'),
    # path('password_reset/done/', views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    # path('reset/<uidb64>/<token>/', views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    # path('reset/done/', views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]

urlpatterns += [
    path('', Dashboard.as_view(), name="dashboard"),
    path('question/create', QuestionCreate.as_view(), name="create"),
    path('question/update/<int:pk>', QuestionUpdate.as_view(), name="update"),
    path('question/delete/<int:pk>', QuestionDelete.as_view(), name="delete"),
    path('profile/', Profile.as_view(), name="profile"),
    path('follow/<int:pk>/', UserFollowView.as_view(), name='user_follow'),
    path('unfollow/<int:pk>/', UserUnfollowView.as_view(), name='user_unfollow'),
    path('register/', UserRegisterView.as_view(), name='user_register'),
]
