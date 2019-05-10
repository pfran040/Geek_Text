\from django.shortcuts import redirect
from django.shortcuts import render, get_object_or_404
from users.models import Profile
from django.db.models import Avg
from .forms import ReviewForm
from .models import Author, Book, Review


# Create your views here.


#Author: Paul Franco
def add_review(request, book_name, slug):
    book = get_object_or_404(Book, book_name=book_name, slug=slug) #Obtain book info
    User = get_object_or_404(Profile, user=request.user)           #Obtain user info for comment

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            message     = form.cleaned_data['message']
            name        = request.POST.get('name_select')       #Get value of name_select from radio buttons
            rating      = request.POST.get('rating')            #Get rating from stars
            review      = form.save(commit=False)
            review.book = book                                  #Get book for which this review is being applied to
            if name == "Username":                              #Check what user selected from name_select radio buttons
                review.name = User.user
            elif name == "Nickname":
                review.name = User.nick_name
                if len(review.name) == 0:                       #If nickname is not filled, use username
                    review.name = User.user
            elif name == "Anonymous":
                review.name = "Anonymous"
            else:
                review.name = request.user                      #Use username if no option is selected
            review.rating = rating
            review.save()                                       #Need to save rating to update the avg_rating of book
            book.avg_rating = Review.objects.aggregate(Avg('rating')).get('rating__avg') #Get avg_rating of book
            book.save()
                                                                #Save form and then redirect back to book_info page for
                                                                #specific book
            return redirect('bookDetails:book_info', book_name=book.book_name, slug=book.slug)
    else:
        form = ReviewForm()
        return render(request, 'bookDetails/book/add_review.html', {'form':form})