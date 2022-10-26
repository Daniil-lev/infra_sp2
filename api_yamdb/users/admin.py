from django.contrib import admin
from django.contrib.auth import get_user_model
from reviews.models import Category, Comment, Genre, Review, Title

User = get_user_model()

admin.site.register(User)
admin.site.register(Title)
admin.site.register(Genre)
admin.site.register(Category)
admin.site.register(Review)
admin.site.register(Comment)
