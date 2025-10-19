from django.shortcuts import render, redirect, get_object_or_404
from .models import Movie, Review, Rating
from .forms import RatingForm
from django.contrib.auth.decorators import login_required

def index(request):
    search_term = request.GET.get('search')
    if search_term:
        movies = Movie.objects.filter(name__icontains=search_term)
    else:
        movies = Movie.objects.all()
    template_data = {}
    template_data['title'] = 'Movies'
    template_data['movies'] = movies

    return render(request, 'movies/index.html', {'template_data': template_data})

def show(request, id):
    movie = Movie.objects.get(id=id)
    reviews = Review.objects.filter(movie=movie)
    ratings = Rating.objects.filter(movie=movie)
    
    # Get user's existing rating if they're logged in
    user_rating = None
    if request.user.is_authenticated:
        try:
            user_rating = Rating.objects.get(movie=movie, user=request.user)
        except Rating.DoesNotExist:
            pass
    
    template_data = {}
    template_data['title'] = movie.name
    template_data['movie'] = movie
    template_data['reviews'] = reviews
    template_data['ratings'] = ratings
    template_data['user_rating'] = user_rating
    template_data['average_rating'] = movie.average_rating()
    template_data['rating_count'] = movie.rating_count()
    template_data['rating_form'] = RatingForm()
    
    return render(request, 'movies/show.html',
                  {'template_data': template_data})

@login_required
def create_review(request, id):
    if request.method == 'POST' and request.POST['comment'] != '':
        movie = Movie.objects.get(id=id)
        review = Review()
        review.comment = request.POST['comment']
        review.movie = movie
        review.user = request.user
        review.save()
        return redirect('movies.show', id=id)
    else:
        return redirect('movies.show', id=id)

@login_required
def edit_review(request, id, review_id):
    review = get_object_or_404(Review, id=review_id)
    if request.user != review.user:
        return redirect('movies.show', id=id)
    if request.method == 'GET':
        template_data = {}
        template_data['title'] = 'Edit Review'
        template_data['review'] = review
        return render(request, 'movies/edit_review.html', {'template_data': template_data})
    elif request.method == 'POST' and request.POST['comment'] != '':
        review = Review.objects.get(id=review_id)
        review.comment = request.POST['comment']
        review.save()
        return redirect('movies.show', id=id)
    else:
        return redirect('movies.show', id=id)

@login_required
def delete_review(request, id, review_id):
    review = get_object_or_404(Review, id=review_id,
        user=request.user)
    review.delete()
    return redirect('movies.show', id=id)

@login_required
def report_review(request, id, review_id):
    review = get_object_or_404(Review, id=review_id)
    review.delete()
    return redirect('movies.show', id=id)

@login_required
def submit_rating(request, id):
    movie = get_object_or_404(Movie, id=id)
    
    if request.method == 'POST':
        stars = request.POST.get('stars')
        if stars:
            # Get or create rating for this user and movie
            rating, created = Rating.objects.get_or_create(
                movie=movie,
                user=request.user,
                defaults={'stars': int(stars)}
            )
            if not created:
                # Update existing rating
                rating.stars = int(stars)
                rating.save()
    
    return redirect('movies.show', id=id)