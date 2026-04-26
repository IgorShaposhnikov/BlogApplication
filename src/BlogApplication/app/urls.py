from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views
from rest_framework.routers import DefaultRouter
from django.views.decorators.cache import cache_page

router = DefaultRouter()
router.register(r'posts', views.PostViewSet, basename='post')

urlpatterns = [
    # 1. Главная страница
    path('', cache_page(600)(views.PostList.as_view()), name='home'),

    # 2. Аутентификация (Вход, Выход, Регистрация)
    path('register/', views.register_request, name="register"),
    path('login/', views.login_request, name="login"),
    path('logout/', views.logout_request, name="logout"),

    path('testcookie/', views.cookie_session, name='cookie_session'),
    path('deletecookie/', views.cookie_delete, name='cookie_delete'),
    path('create/', views.create_session, name='create_session_url'),
    path('access/', views.access_session, name='access_session'),
    path('delete/', views.delete_session, name='delete_session'),

    # 3. Сброс пароля
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='app/password_reset.html'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='app/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='app/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='app/password_reset_complete.html'), name='password_reset_complete'),

    # 4. API
    path('api/v1/', include(router.urls)),

    # 5. Детали поста (используем функцию views.post_detail БЕЗ .as_view())
    path('<slug:slug>/', views.post_detail, name='post_detail')
]