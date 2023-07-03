from django.shortcuts import render, get_object_or_404
from .models import Post, BlogCategory, BlogSetup

from django.core.paginator import Paginator

from setup.models import ThemeSettings
try:
    theme_address = ThemeSettings.objects.get().name
except:
    theme_address = 'default'


# Create your views here.

def blog(request):
    blog_settings = BlogSetup.objects.get()
    
    page_number = request.GET.get('page')
    limit = request.GET.get('limit')
    
    max_post = Post.objects.filter(published=True)

    if limit:
        paginator = Paginator(max_post, *limit)
    else:
        paginator = Paginator(max_post, 6)



    posts = paginator.get_page(page_number)


    context = {
        
        'max_post': posts,
        'products': posts,
        'blog_categorys': BlogCategory.objects.all(),
        'blog_settings': blog_settings,
    }
    

    return render(request, 'blog/blog.html', context)



def blog_category_detail(request, slug):
    blog_category = get_object_or_404(BlogCategory, slug=slug)

    
    max_post = Post.objects.filter(published=True, parent_id=blog_category.id)
    context = {
        'blog_category': blog_category,
        'max_post': max_post,
        'blog_categorys': BlogCategory.objects.all(),
    }

    return render(request, 'blog/blog_catgory_detail.html', context)

def post_detail(request, slug):
    
    context = {
        'post': get_object_or_404(Post, slug=slug)
    }

    return render(request, 'blog/post_detail.html', context)
