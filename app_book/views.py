
from django.shortcuts import render, get_object_or_404, redirect
from .models import Text, BuzzWord, Bookmarks

def heads(request):
    texts = Text.objects.all()
    return render(request, 'chapters.html', {'texts': texts})

def chapter(request, pk):
    chapter_text = get_object_or_404(Text, pk=pk)
    chapter_buzzwords = BuzzWord.objects.filter(text=chapter_text)
    bookmark = Bookmarks.objects.filter(user=request.user).first()
    if request.method == 'POST':
        if bookmark:
            bookmark.delete()
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
