
from django.shortcuts import render, get_object_or_404
from .models import Text, BuzzWord

def heads(request):
    texts = Text.objects.all()
    return render(request, 'chapters.html', {'texts': texts})

def chapter(request, pk):
    chapter_text = get_object_or_404(Text, pk=pk)
    chapter_buzzwords = BuzzWord.objects.filter(text=chapter_text)
    try:
        next_chapter=Text.objects.get(pk=(pk+1)).pk
    except Text.DoesNotExist:
        next_chapter = None
    return render(request, 'single_chapter.html', {'text': chapter_text,
                                                   'chapter_buzzwords': chapter_buzzwords,
                                                   'next_chapter': next_chapter})

def greeting(request):
    return render(request, 'greetings.html')
