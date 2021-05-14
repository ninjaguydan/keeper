from django.db import models
from login_app.models import *

#Validators
class BookManager(models.Manager):
    def validator(self, postData):
        errors = {}
        if len(postData['title']) < 1:
            errors['title'] = "Must enter a book title"
        if len(postData['new_author']) and len(postData['new_author']) < 4:
            errors['author'] = "Author name must be more than 4 characters"
        if len(postData['desc']) < 10:
            errors['desc'] = "Description must be more than 10 characters"
        if len(postData['review']) < 10:
            errors['review'] = "Review must be longer than 10 characters"
        return errors

class ReviewManager(models.Manager):
    def validator(self, postData):
        errors = {}
        if len(postData['review']) < 10:
            errors['review'] = "Review must be longer than 10 characters"
        return errors


# Create your models here.
class Author(models.Model):
    name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    #books

class Book(models.Model):
    title = models.CharField(max_length=200)
    desc = models.TextField()
    author = models.ForeignKey(Author, related_name = "books", on_delete = models.CASCADE)
    added_by = models.ForeignKey(User, related_name = "books_added", on_delete = models.CASCADE)
    favorited_by = models.ManyToManyField(User, related_name="favorites", blank=True)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    #reviews
    objects = BookManager()

class Review(models.Model):
    content = models.TextField()
    rating = models.IntegerField()
    book = models.ForeignKey(Book, related_name = "reviews", on_delete = models.CASCADE)
    user = models.ForeignKey(User, related_name = "reviews", on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    #likes
    objects = ReviewManager()

class Like(models.Model):
    review = models.ForeignKey(Review, related_name = "likes", on_delete = models.CASCADE)
    user = models.ForeignKey(User, related_name = "likes", on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
