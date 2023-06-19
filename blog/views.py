from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator
from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from members.models import CustomUser
from .models import Blog, Comment, PostViews
from .forms import BlogForm, BlogChangeForm, CommentForm
from django.contrib.auth.decorators import login_required


class MainView(View):
    def get(self, request):
        return render(request, 'main.html')


def index(request):
    blog = Blog.objects.all().order_by('-id')
    superuser = CustomUser.objects.get(username='admin99')

    # pagination section
    page_size = request.GET.get("page_size", 2)
    paginator = Paginator(blog, page_size)
    page_num = request.GET.get("page", 1)
    page_obj = paginator.get_page(page_num)

    context = {'page_obj': page_obj, "superuser": superuser}
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

    context = {'blog': blog, 'form': form}
    return render(request, 'new_post.html', context)


def edit(request, pk):
    blog = Blog.objects.get(id=pk)
    form = BlogChangeForm(instance=blog)

    if request.method == 'POST':
        form = BlogChangeForm(request.POST, request.FILES, instance=blog)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {'form': form}
    return render(request, 'post_edit.html', context)


def delete(request, pk):
    blog = Blog.objects.get(id=pk)
    if request.method == 'POST':
        blog.delete()
        return redirect('home')

    context = {'blog': blog}
    return render(request, 'post_delete.html', context)


class CustomUserMixin:
    def dispatch(self, request, *args, **kwargs):
        user = request.user
        print(f"user: {user}")
        print("dispatch method called")
        if not user.is_authenticated:
            # Here, A user will be redirected to the (login) View if user is not instance of CustomUser
            return redirect('members:login')
        """
         Here, the Dispatch method redirects the user according to the appropriate HTTP methods of a particular View. 
         for example, we have a LoginView to log in users into our blog. LoginView inherits from this View(CustomUserMixin). 
         The dispatch method of CustomUserMixin checks if a user is an instance of the CustomUser model if it is, the GET or PUT methods of our LoginView are executed normally. 
         Otherwise, Dispatch method of CustomUserMixin redirects user to (main)View and Other methods(GET, POST) of LoginView are not executed.
        """
        return super().dispatch(request, *args, **kwargs)


class BlogDetailView(View):
    def get(self, request, id):
        blog = get_object_or_404(Blog, id=id)
        comment_form = CommentForm()
        superuser = CustomUser.objects.get(username='admin99')

        # counting the viewed posts
        # get the user's IP address
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
            print(f"IP ADDRESS: {ip}")
        else:
            ip = request.META.get('REMOTE_ADDR')
            print(f"IP ADDRESS: {ip}")

        PostViews.objects.get_or_create(IPAddres=ip, post=blog)

        context = {'blog': blog, "superuser": superuser, "comment_form": comment_form, "counter": blog.views_count}
        return render(request, 'post_detail.html', context)


class CommentView(CustomUserMixin, View):
    def post(self, request, id):
        blog = Blog.objects.get(id=id)
        comment_form = CommentForm(data=request.POST)

        if comment_form.is_valid():
            Comment.objects.create(article=blog, body=comment_form.cleaned_data['body'], subscriber=request.user)

            return redirect(reverse("post_detail", kwargs={"id": blog.id}))
        return render(request, "post_detail.html", {"comment_form": comment_form, "blog": blog})
