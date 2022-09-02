from django.views.generic import (
    ListView, DetailView, UpdateView, DeleteView
)
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.models import Group
from django.core.cache import cache

from .models import Post
from .forms import PostForm, CommentForm


class PostList(ListView):
    model = Post
    ordering = 'title'
    template_name = 'list.html'
    context_object_name = 'post'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_subs'] = not self.request.user.groups.filter(name='subscribers').exists()
        return context


class PostDetail(DetailView):
    model = Post
    comment_class = CommentForm
    template_name = 'post.html'
    context_object_name = 'post'

    def get_object(self, *args, **kwargs):
        obj = cache.get(f'product-{self.kwargs["pk"]}',
                        None)
        if not obj:
            obj = super().get_object(queryset=self.queryset)
            cache.set(f'product-{self.kwargs["pk"]}', obj)

        return obj


@login_required
@permission_required('post.add_post', raise_exception=True)
def create_post(request):
    form = PostForm()

    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            form.save()

            return HttpResponseRedirect('/post/add')
    return render(request, 'post_add.html', {'form': form})


class PostEdit(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'
    permission_required = 'post.change_post'


class PostDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('post_list')
    permission_required = 'post.delete_post'


@login_required
def subscribe(request):
    user = request.user
    subs = Group.objects.get(name='subscribers')
    if not request.user.groups.filter(name='subscribers').exists():
        subs.user_set.add(user)

    return redirect('http://127.0.0.1:8000/post/')
