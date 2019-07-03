from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Post
"""
posts = [
    {
        'author':'Shubham',
        'title': 'What is life',
        'content': 'Some pretentious shit',
        'date_posted': '13 Feb 2019'
    },
    {
        'author': 'Dummy',
        'title': 'What is knife',
        'content': 'Some pretentious hit',
        'date_posted': '14 Feb 2019'
    }
]

"""


def home(request):
    context = {
        'posts': Post.objects.all()
    }
    #return HttpResponse("<h1>Hello world</h1>
    return render(request, 'blog/home.html', context)


class PostListView(ListView):
    model = Post
    template_name = "blog/home.html"
    context_object_name = 'posts'
    ordering = ['-date_posted']  #### ['-date_posted'] for newest to oldest
    #blog/post_list.html
    # <app_name>/<model_name>_<view_type>.html


class PostDetailView(DetailView):
    model = Post


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = "/"

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})

