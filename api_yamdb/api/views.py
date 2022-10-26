from random import randint
from django.core.mail import send_mail
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters import rest_framework as filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import (AllowAny, IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from reviews.models import Category, Comment, Genre, Review, Title
from users.models import ROLE_USER, User

from .filters import TitlesFilter
from .permissions import (IsAdminOrSuperuser, IsAuthorAdminModeratorPermission,
                          IsOwner, ReadOnly)
from .serializers import (CategorySerializer, CommentSerializer,
                          GenreSerializer, ReviewSerializer,
                          TitlePostSerializer, TitleReadSerializer,
                          UserSerializer, UserSerializerSignUp,
                          UserSerializerToken)


class SignUpView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            user = User.objects.get(
                username=request.data.get('username'),
                email=request.data.get('email')
            )
        except User.DoesNotExist:
            serializer = UserSerializerSignUp(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = User()
            user.username = serializer.validated_data.get('username')
            user.email = serializer.validated_data.get('email')
        except Exception as e:
            raise e('Не удается зарегистрировать пользователя!')

        confirmation_code = randint(10000, 99999)
        user.confirmation_code = confirmation_code
        user.save()
        send_mail(
            subject='YaMDB confirmation code',
            message=f'Your confirmation code is: {confirmation_code}',
            from_email='noreplay@yamdb.fake',
            recipient_list=[user.email],
            fail_silently=False
        )
        return Response(request.data, status=status.HTTP_200_OK)


class TokenView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserSerializerToken(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data.get('username')
            user = get_object_or_404(User, username=username)
            token = str(RefreshToken.for_user(user).access_token)
            return Response({'token': token},
                            status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UsersViewSet(viewsets.ModelViewSet):
    lookup_field = 'username'
    permission_classes = [IsAdminOrSuperuser]
    queryset = User.objects.all()
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    serializer_class = UserSerializer

    @action(detail=False, methods=['get', 'patch'],
            permission_classes=[IsAuthenticated, IsOwner])
    def me(self, request):
        user = request.user
        data = request.data.copy()
        data['username'] = user.username
        data['email'] = request.data.get('email') or user.email
        serializer = UserSerializer(user, data=data)
        if serializer.is_valid():
            if user.is_user:
                serializer.validated_data['role'] = user.role
            serializer.save()
            return Response(serializer.data,
                            status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def perform_update(self, serializer):
        if self.request.user.is_user:
            serializer.validated_data['role'] = ROLE_USER
        return super().perform_update(serializer)


class ListCreateDestroyViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    pass


class CategoryViewSet(ListCreateDestroyViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [ReadOnly | IsAdminOrSuperuser]
    filter_backends = (filters.SearchFilter,)
    lookup_field = 'slug'
    search_fields = ('name',)


class GenreViewSet(ListCreateDestroyViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [ReadOnly | IsAdminOrSuperuser]
    filter_backends = (filters.SearchFilter,)
    lookup_field = 'slug'
    search_fields = ('name',)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.annotate(
        rating=Avg('reviews__score'))
    serializer_class = TitleReadSerializer
    permission_classes = [ReadOnly | IsAdminOrSuperuser]
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    filterset_class = TitlesFilter
    ordering_fields = ('name',)
    ordering = ('name',)

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return TitleReadSerializer
        return TitlePostSerializer


class ReviewsViewset(viewsets.ModelViewSet):

    permission_classes = [
        IsAuthenticatedOrReadOnly, IsAuthorAdminModeratorPermission
    ]
    serializer_class = ReviewSerializer
    pagination_class = LimitOffsetPagination

    def get_title(self):
        return get_object_or_404(Title, pk=self.kwargs.get("title_id"))

    def get_queryset(self):
        queryset = Review.objects.filter(title=self.get_title())
        return queryset

    def perform_update(self, serializer):
        serializer.save(
            author=self.request.user,
            title=self.get_title())

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            title=self.get_title())


class CommentsViewset(viewsets.ModelViewSet):

    permission_classes = [
        IsAuthenticatedOrReadOnly, IsAuthorAdminModeratorPermission
    ]
    serializer_class = CommentSerializer
    pagination_class = LimitOffsetPagination

    def get_title(self):
        return get_object_or_404(Title, pk=self.kwargs['title_id'])

    def get_review(self):
        return get_object_or_404(Review, pk=self.kwargs['review_id'])

    def perform_create(self, serializer):
        serializer.save(review=self.get_review(),
                        author=self.request.user
                        )

    def get_queryset(self):
        queryset = Comment.objects.filter(
            review__title=self.get_title(),
            review=self.get_review()
        )
        return queryset
