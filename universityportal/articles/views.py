from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect
from .models import Articles, UserRoles, User
from .forms import NewUserForm, ArticleForm
from django.contrib import messages
from django.contrib.auth import login
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required


# Create your views here.
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


def article_details(request, id):
    articles = Articles.objects.get(id=id)
    context = {
        'article': articles
    }
    return render(request, 'article_details.html', context)


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
    article = get_object_or_404(Articles, pk=pk)
    if article.user != request.user:
        raise Http404  # or similar
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


def article_approve(request, id):
    Articles.objects.filter(id=id).update(status='approved')
    return redirect('homepage')
