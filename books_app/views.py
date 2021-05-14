from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
from django.db.models import Q

# Create your views here.
def logout(request):
    request.session.clear()
    return redirect('/')

def books(request):
    if not "userid" in request.session:
        return redirect('/')
    if request.session['userid'] == 0:
        context = {
            "reviews" : Review.objects.all().order_by("-created_at")[:5],
            "books" : Book.objects.all(),
            }
        return render(request, "books.html", context)
    context = {
        "user" : User.objects.get(id = request.session['userid']),
        "reviews" : Review.objects.all().order_by("-created_at")[:5],
        "books" : Book.objects.all(),
        }
    return render(request,'books.html', context)

def addbook(request):
    context = {
        "user" : User.objects.get(id = request.session['userid']),
        "authors" : Author.objects.all(),
        }
    return render(request, "addbook.html", context)

def add(request):
    if request.method == "GET":
        return redirect('/books/addbook')
    errors = Book.objects.validator(request.POST)
    if errors:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/books/addbook')
    if request.POST['new_author']:
        author = Author.objects.create(name = request.POST['new_author'])
    else:
        author = Author.objects.create(name = request.POST['author'])
    user = User.objects.get(id = request.session['userid'])
    new_book = Book.objects.create(
        title= request.POST['title'], 
        desc = request.POST['desc'],
        author = author,
        added_by = user
        )
    Review.objects.create(
        content = request.POST['review'],
        rating = request.POST['rating'],
        book = new_book,
        user = user
        )
    return redirect(f'/books/{new_book.id}')

def delete_review(request, review_id):
    review_to_delete = Review.objects.get(id = review_id)
    book_id = review_to_delete.book.id
    review_to_delete.delete()
    return redirect(f'/books/{book_id}')

def post_review(request, book_id):
    if request.method == "GET":
        return redirect(f"/books/{book_id}")
    book = Book.objects.get(id = book_id)
    user = User.objects.get(id = request.session['userid'])
    Review.objects.create(
        content=request.POST['review'], 
        rating=request.POST['rating'],
        book=book,
        user=user
    )
    context = {
        "book" : book,
        "user" : user,
    }
    return render(request, "review-partial.html", context)
        
def display_book(request, book_id):
    if request.session['userid'] == 0:
        context = {
            "book" : Book.objects.get(id = book_id)
            }
        return render(request, "reviews.html", context)
    book = Book.objects.get(id = book_id)
    user = User.objects.get(id = request.session['userid'])
    context = {
        "user" : user,
        "book" : book,
    }
    return render(request, "reviews.html", context)

def favorite_book(request, book_id):
    user = User.objects.get(id = request.session['userid'])
    book = Book.objects.get(id = book_id)
    user.favorites.add(book)
    return redirect(f'/books/{book_id}')

def unfavorite_book(request, book_id):
    user = User.objects.get(id = request.session['userid'])
    book = Book.objects.get(id = book_id)
    user.favorites.remove(book)
    return redirect(f'/books/{book_id}')

def delete_book(request, book_id):
    book = Book.objects.get(id = book_id)
    if request.session['userid'] == book.added_by.id:
        book.delete()
        return redirect('/books/')
    return redirect(f'/books/{book_id}')
    
def display_profile(request, profile_id):
    profile = User.objects.get(id=profile_id)
    if request.session['userid'] == 0:
        context = {
            "profile" : profile,
        }
        return render(request, "user.html", context)
    context = {
        "profile" : profile,
        "user" : User.objects.get(id=request.session['userid']),
    }
    return render(request, "user.html", context)

def delete_profile(request, profile_id):
    user_to_delete = User.objects.get(id = profile_id)
    user_to_delete.delete()
    return redirect('/books/admin')

def admin(request):
    context = {
        "user" : User.objects.get(id = request.session['userid']),
        "profiles" : User.objects.all(),
    }
    return render(request, "admin.html", context)

# def likes(request, review_id):
#     user = User.objects.get(id = request.session['userid'])
#     review = Review.objects.get(id = review_id)
#     if review.likes.filter(user = user):
#         like = Like.objects.filter(Q(review = review), Q(user = user))
#         like.delete()
#         return redirect(f'/books/{review.book.id}')
#     else:
#         Like.objects.create(review = review, user = user)
#     context = {
#         "book" : Book.objects.get(id = review.book.id),
#         "user" : user,
#     }
#     return render(request, "review-partial.html", context)