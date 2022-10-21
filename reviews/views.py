from django.shortcuts import render
from django.shortcuts import render, redirect
from .models import Review
from .forms import ReviewForm
from django.contrib.auth.decorators import login_required
# Create your views here.

def index(request):
  review = Review.objects.all().order_by('-pk')
  context = {
    'review': review,
  }
  return render(request, 'reviews/index.html', context)

@login_required
def create(request):
  if request.user.is_authenticated:
    if request.method == 'POST':
      review_form = ReviewForm(request.POST, request.FILES)
      if review_form.is_valid():
          review = review_form.save(commit=False)
          review.user = request.user
          review.save()
          return redirect('reviews:index')
    else:
      review_form = ReviewForm()
    context = {
      'review_form': review_form,
    }
    return render(request, 'reviews/create.html', context=context)
  else:
    return redirect('accounts:login')



