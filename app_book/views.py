
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Exists, OuterRef
from .models import Text, BuzzWord, Bookmarks, MediaFile

def heads(request):
    user = request.user
    has_bookmark = Exists(Bookmarks.objects.filter(bookmark=OuterRef('pk')))
    texts = Text.objects.annotate(first_page=has_bookmark).order_by('-first_page', 'pk')
    return render(request, 'chapters.html', {'texts': texts})

def chapter(request, pk):
    chapter_text = get_object_or_404(Text, pk=pk)
    chapter_buzzwords = BuzzWord.objects.filter(text=chapter_text)
    bookmark = Bookmarks.objects.filter(user=request.user).first()
    if_page_bookmark = chapter_text.has_bookmark

    if request.method == 'POST':
        if bookmark:
            if if_page_bookmark:
                bookmark.delete()
            else:
                bookmark.delete()
                Bookmarks.objects.create(user=request.user, bookmark=chapter_text)
        else:
            Bookmarks.objects.create(user=request.user, bookmark=chapter_text)
        return redirect('chapter', pk=pk)

    try:
        next_chapter=Text.objects.get(pk=(pk+1)).pk
    except Text.DoesNotExist:
        next_chapter = None
    try:
        prev_chapter=Text.objects.get(pk=(pk-1)).pk
    except Text.DoesNotExist:
        prev_chapter = None
    return render(request, 'single_chapter.html', {'text': chapter_text,
                                                   'chapter_buzzwords': chapter_buzzwords,
                                                   'next_chapter': next_chapter,
                                                   'prev_chapter': prev_chapter,
                                                   'bookmark': bookmark})

def greeting(request):
    return render(request, 'greetings.html')


def postcards(request):
    postcards = BuzzWord.objects.all()
    # postcards = MediaFile.objects.prefetch_related('buzzword_set__text').all
    return render(request, 'postcards.html', {'postcards': postcards})
