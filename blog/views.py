from django.urls import reverse_lazy, reverse
from django.shortcuts import render,redirect
from .models import Blog, Comment
from .forms import BlogForm, BlogChangeForm, CommentForm
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView




class CommentView(CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'add_comment.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        form.instance.article_id = self.kwargs['pk']
        return super().form_valid(form)



def detail(request, pk):
    blog = Blog.objects.get(id=pk)
    comments = blog.comments.all()
    context = {'blog': blog, "comments":comments}
    return render(request, 'post_detail.html', context)



def main(request):
    return render(request, 'main.html')




def index(request):
    blog = Blog.objects.all()
    context = {'blog': blog}
    return render(request, 'home.html', context)





@login_required(redirect_field_name='new_post/', login_url='register')
def add(request):
    blog = Blog.objects.all()
    form = BlogForm()

    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
        return redirect('home')

    context = {'blog':blog, 'form':form}
    return render(request, 'new_post.html', context)


def edit(request, pk):
    blog = Blog.objects.get(id=pk)
    form = BlogChangeForm(instance=blog)

    if request.method == 'POST':
        form = BlogChangeForm(request.POST, request.FILES, instance=blog)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {'form':form}
    return render(request, 'post_edit.html', context)


def delete(request, pk):
    blog = Blog.objects.get(id=pk)

    if request.method == 'POST':
        blog.delete()
        return redirect('home')

    context = {'blog':blog}
    return render(request, 'post_delete.html', context)


