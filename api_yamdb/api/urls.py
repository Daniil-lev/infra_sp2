from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (CategoryViewSet, CommentsViewset, GenreViewSet,
                    ReviewsViewset, SignUpView, TitleViewSet, TokenView,
                    UsersViewSet)

app_name = 'api'
router = DefaultRouter()
router.register('users', UsersViewSet)
router.register('categories', CategoryViewSet)
router.register('genres', GenreViewSet)
router.register('titles', TitleViewSet)
router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewsViewset,
    basename='reviews')
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentsViewset,
    basename='comments')

urlpatterns = [
    path('v1/auth/signup/', SignUpView.as_view()),
    path('v1/auth/token/', TokenView.as_view()),
    path('v1/', include(router.urls)),
]
