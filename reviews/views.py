from django.shortcuts import render
from django.shortcuts import render, redirect
from .models import Review
from .forms import ReviewForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
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

def detail(request, pk):
  # 특정 글을 가져온다.
  review = Review.objects.get(pk=pk)
  context = {
    'review': review,   
  }
  return render(request, 'reviews/detail.html', context)

@login_required
def update(request, pk):
    review = Review.objects.get(pk=pk)
    if request.user == review.user:
      if request.method == 'POST':
          # POST : input 값 가져와서, 검증하고, DB에 저장
          review_form = ReviewForm(request.POST, request.FILES, instance=review)
          if review_form.is_valid():
              # 유효성 검사 통과하면 저장하고, 상세보기 페이지로
              review_form.save()
              messages.success(request, '글이 수정되었습니다.')
              return redirect('reviews:detail', review.pk)
          # 유효성 검사 통과하지 않으면 => context 부터해서 오류메시지 담긴 review_form을 랜더링
      else:
          # GET : Form을 제공
          review_form = ReviewForm(instance=review)
      context = {
          'review_form': review_form
      }
      return render(request, 'reviews/update.html', context)
    else:
      messages.warning(request, '작성자만 수정할 수 있습니다.')
      return redirect('reviews.detail', review.pk)

def delete(request, pk):
    Review.objects.get(id=pk).delete()
    return redirect("reviews:index")