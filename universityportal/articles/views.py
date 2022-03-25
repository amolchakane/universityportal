from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from rest_framework.viewsets import ModelViewSet

from .forms import NewUserForm, ArticleForm, CommentForm
from .models import Articles, UserRoles
# Create your views here.
from .serializers import ArticleSerializer


@login_required
def index(request):
    # ToDo:Check role of the user logged in and based on that fetch articles
    user_role = UserRoles.objects.filter(user=request.user)
    if user_role[0].role == 'student':
        articles = Articles.objects.filter(user=request.user).order_by('-created_at')[:10]
    else:
        articles = Articles.objects.filter(reviewer=request.user).order_by('-created_at')[:10]
    context = {
        'articles': articles,
        'user_role': user_role[0].role
    }
    return render(request, 'index.html', context)


@login_required()
def article_details(request, id):
    try:
        article = Articles.objects.get(id=id)
        if article.user != request.user and article.reviewer != request.user:
            return render(request, '403.html')
        context = {
            'article': article
        }
        return render(request, 'article_details.html', context)
    except ObjectDoesNotExist:
        return render(request, '404.html')


@login_required
def article_new(request):
    if request.method == "POST":
        form = ArticleForm(request.POST)
        if form.is_valid():
            article = form.save(commit=False)
            article.user = request.user
            # Get the random professor to assign as reviewer
            random_professor_role = UserRoles.objects.filter(role='professor').order_by('?')[:1]
            print(random_professor_role)
            print(random_professor_role[0].user)
            article.reviewer = random_professor_role[0].user
            article.save()
            return redirect('details', article.pk)
    else:
        form = ArticleForm()

    form = ArticleForm()
    return render(request, 'article_edit.html', {'form': form})


@login_required
def article_edit(request, pk):
    try:
        article = Articles.objects.get(pk=pk)
    except ObjectDoesNotExist:
        return render(request, '404.html')
    if article.user != request.user:
        return render(request, '403.html')
    if request.method == "POST":
        form = ArticleForm(request.POST, instance=article)
        if form.is_valid():
            article = form.save(commit=False)
            article.save()
            return redirect('details', article.pk)
    else:
        form = ArticleForm(instance=article)
    return render(request, 'article_edit.html', {'form': form})


def register(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            usertype = request.POST.get('usertype')
            user_role = UserRoles(role=usertype, user=user)
            user_role.save()
            messages.success(request, f"New account created: {username}")
            login(request, user)
            return redirect("homepage")
        else:
            for msg in form.error_messages:
                messages.error(request, f"{msg}:{form.error_messages[msg]}")

    form = NewUserForm
    return render(
        request,
        "register.html",
        {"form": form}
    )


@login_required()
def article_approve(request, id):
    Articles.objects.filter(id=id).update(status='approved')
    return redirect('homepage')


@login_required()
def add_comment_to_post(request, pk):
    article = get_object_or_404(Articles, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.article = article
            comment.author = request.user
            comment.save()
            return redirect('details', article.pk)
    else:
        form = CommentForm()
    return render(request, 'add_comment_to_article.html', {'form': form})


class ArticleViewSet(ModelViewSet):
    serializer_class = ArticleSerializer
    queryset = Articles.objects.all().order_by('-created_at')
