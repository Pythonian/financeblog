from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
# from django.shortcuts import render, get_object_or_404
from django.views.generic import (
    CreateView, DetailView, DeleteView, ListView, UpdateView)

from .models import Blog


# def blog_list(request):
#     blogs = Blog.objects.all()
#     return render(request, 'blog/list.html', {'blogs': blogs})


# def blog_detail(request, pk):
#     blog = get_object_or_404(Blog, pk=pk)
#     return render(request, 'blog/detail.html', {'blog': blog})


class BlogListView(ListView):
    model = Blog
    paginate_by = 3


class BlogDetailView(DetailView):
    model = Blog


class BlogCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Blog
    fields = ['title', 'content']
    success_message = "Blog Created Successfully!"

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class BlogUpdateView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, UpdateView):
    model = Blog
    fields = ['title', 'content']
    success_message = "Blog Updated Successfully!"

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        """
        This method puts the conditional pass for the
        UserPassesTestMixin to only allow access to this view
        if the currently logged-in user is the author of the Post
        """
        blog = self.get_object()
        if self.request.user == blog.author:
            return True
        else:
            return False


class BlogDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Blog
    success_message = "Blog Deleted Successfully!"
    success_url = "/"

    def test_func(self):
        blog = self.get_object()
        if self.request.user == blog.author:
            return True
        else:
            return False

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super().delete(request, *args, **kwargs)
