import re

from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator, UniqueValidator
from reviews.models import Category, Comment, Genre, Review, Title
from users.models import User


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        max_length=254,
        validators=[UniqueValidator(queryset=User.objects.all())])

    class Meta:
        model = User

        fields = ('username', 'first_name', 'last_name', 'email',
                  'bio', 'role')


class UserSerializerSignUp(serializers.Serializer):
    email = serializers.EmailField(
        max_length=254,
        validators=[UniqueValidator(queryset=User.objects.all())])
    username = serializers.CharField(
        max_length=150,
        validators=[UniqueValidator(queryset=User.objects.all())])

    def validate_username(self, username):
        if username == 'me':
            raise serializers.ValidationError(
                'Нельзя создать пользователя с именем "me"')
        m = re.search(r'^[\w.@+-]+$', username)
        if not m:
            raise serializers.ValidationError(
                'Допустимы буквы, цифры и символы: @/./+/-/_.')
        return username


class UserSerializerToken(serializers.Serializer):
    username = serializers.CharField(max_length=150, required=True)
    confirmation_code = serializers.CharField(max_length=24, required=True)

    def validate_confirmation_code(self, confirmation_code):
        username = self.initial_data.get('username')
        user = User.objects.filter(username=username).first()
        if user and str(confirmation_code) != str(user.confirmation_code):
            raise serializers.ValidationError('Неверный код подтверждения')
        return confirmation_code


class CategorySerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=256)

    class Meta:
        exclude = ['id']
        model = Category


class GenreSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=256)

    class Meta:
        exclude = ['id']
        model = Genre


class TitlePostSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=256)
    genre = serializers.SlugRelatedField(
        slug_field='slug', many=True, queryset=Genre.objects.all()
    )
    category = serializers.SlugRelatedField(
        slug_field='slug', queryset=Category.objects.all()
    )

    class Meta:
        fields = (
            'id', 'name', 'year', 'description', 'genre', 'category'
        )
        model = Title


class TitleReadSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(read_only=True, many=True)
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        fields = '__all__'
        model = Title


class CurrentTitleDefault:
    requires_context = True

    def __call__(self, serializer_field):
        return serializer_field.context.get('view').kwargs.get('title_id')


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=serializers.CurrentUserDefault()
    )
    title = serializers.HiddenField(
        default=CurrentTitleDefault()
    )

    class Meta:
        fields = ('__all__')
        model = Review
        validators = [
            UniqueTogetherValidator(
                queryset=Review.objects.all(),
                fields=['title', 'author']
            )

        ]


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )
    review = serializers.PrimaryKeyRelatedField(
        read_only=True,
    )

    class Meta:
        fields = '__all__'
        model = Comment
