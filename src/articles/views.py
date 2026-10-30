from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from .models import Article


def archive(request):
    return render(request, 'archive.html', {'posts': Article.objects.all()})


def get_article(request, article_id):
    post = get_object_or_404(Article, id=article_id)
    return render(request, 'article.html', {'post': post})


def create_post(request):
    if not request.user.is_authenticated:
        raise Http404

    form = {'title': '', 'text': '', 'errors': ''}
    if request.method == 'POST':
        form['title'] = request.POST.get('title', '').strip()
        form['text'] = request.POST.get('text', '').strip()
        if not form['title'] or not form['text']:
            form['errors'] = 'Не все поля заполнены'
        elif len(form['title']) > 200:
            form['errors'] = 'Название не должно быть длиннее 200 символов'
        elif any(title.casefold() == form['title'].casefold()
                 for title in Article.objects.values_list('title', flat=True)):
            form['errors'] = 'Статья с таким названием уже существует'
        else:
            post = Article.objects.create(
                title=form['title'], text=form['text'], author=request.user
            )
            return redirect('get_article', article_id=post.id)
    return render(request, 'create_post.html', {'form': form})
