
from django.shortcuts import render, get_object_or_404
from .models import Text, BuzzWord

def heads(request):
    texts = Text.objects.all()
    return render(request, 'chapters.html', {'texts': texts})

def chapter(request, pk):
    chapter_text = get_object_or_404(Text, pk=pk)
    chapter_buzzwords = BuzzWord.objects.filter(text=chapter_text)
    return render(request, 'single_chapter.html', {'text': chapter_text, 'chapter_buzzwords': chapter_buzzwords})

def greeting(request):
    
    return render(request, 'greetings.html')
