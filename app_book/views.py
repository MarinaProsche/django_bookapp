
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Exists, OuterRef
from .models import Text, BuzzWord, Bookmarks, MediaFile, Favorites

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
    favorites = Favorites.objects.filter(user=request.user).values_list('favorites_id', flat=True)

    return render(request, 'postcards.html', {
        'postcards': postcards,
        'favorites': favorites
    })

def add_to_favorite(request, id):
    fav_picture = get_object_or_404(MediaFile, id=id)
    print(fav_picture,11111)
    add_to_fav, if_exist = Favorites.objects.get_or_create(user=request.user, favorites=fav_picture)
    if not if_exist:
        add_to_fav.delete() 
    return redirect('postcards')

def favorites(request):
    favorites = Favorites.objects.select_related('favorites').prefetch_related('favorites__buzzword_set__text').all()
    return render(request, 'favorites.html', {'favorites': favorites})
