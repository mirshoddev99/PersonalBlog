from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.urls import reverse
from django.shortcuts import render,redirect
from django.views import View
from members.models import CustomUser
from .models import Blog, Comment
from .forms import BlogForm, BlogChangeForm, CommentForm
from django.contrib.auth.decorators import login_required



def main(request):
    return render(request, 'main.html')



def index(request):
    blog = Blog.objects.all().order_by('-id')
    superuser = CustomUser.objects.get(is_superuser=True)

    # pagination section
    page_size = request.GET.get("page_size", 2)
    paginator = Paginator(blog, page_size)
    page_num = request.GET.get("page", 1)
    page_obj = paginator.get_page(page_num)

    context = {'page_obj': page_obj, "superuser":superuser}
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



class BlogDetailView(View):
    def get(self, request, id):
        blog = Blog.objects.get(id=id)
        comment_form = CommentForm()
        superuser = CustomUser.objects.get(is_superuser=True)
        context = {'blog': blog, "superuser": superuser, "comment_form": comment_form}
        return render(request, 'post_detail.html', context)



class CommentView(View, LoginRequiredMixin):
    def post(self, request, id):
        blog = Blog.objects.get(id=id)
        comment_form = CommentForm(data=request.POST)

        if comment_form.is_valid():
            Comment.objects.create(
                article = blog,
                body = comment_form.cleaned_data['body'],
                subscriber = request.user
            )
            return redirect(reverse("post_detail", kwargs={"id":blog.id}))

        return render(request, "post_detail.html", {"comment_form":comment_form, "blog":blog})



