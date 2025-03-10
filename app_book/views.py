
from django.shortcuts import render, get_object_or_404
from .models import Text

def heads(request):
    texts = Text.objects.all()
    return render(request, 'chapters.html', {'texts': texts})

def chapter(request, pk):
    text = get_object_or_404(Text, pk=pk)
    return render(request, 'single_chapter.html', {'text': text})

def greeting(request):
    
    return render(request, 'greetings.html')
