from django.shortcuts import  render, redirect
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView
from .models import CustomUser, Post, PostImage, Tag
from django.views.generic import DetailView, ListView
from .forms import CustomUserCreationForm, CustomUserChangeForm, PostCreationForm
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.contrib.auth import views as auth_views
from django.contrib.auth.hashers import check_password
from django.http import HttpResponseNotFound, HttpResponseRedirect
from django.contrib.auth.forms import PasswordChangeForm
from django.utils import timezone


class PostList(UserPassesTestMixin, ListView):
    queryset = Post.objects.filter(status=1).order_by('-publish_date')
    template_name = 'post_list.html'

    def test_func(self):
        return self.request.user.is_authenticated 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post_list'] = self.queryset
        context['Tag'] = Tag.objects.all()
        return context




class MyPostList(UserPassesTestMixin, ListView):
    queryset = Post.objects.all()
    template_name = 'my_post_list.html'

    def test_func(self):
        return self.request.user.is_authenticated 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post_list'] = Post.objects.filter(author=self.request.user.id)
        return context



class PostDetail(DetailView):
    model = Post
    template_name = 'post_detail.html'

    
class PostEditView(UserPassesTestMixin, UpdateView):
    model = Post
    fields = "__all__"
    success_url = reverse_lazy('my_post_list')
    template_name = 'my_post_edit.html'

    def test_func(self):
        au = Post.objects.get(slug=self.kwargs['slug'])
        return self.request.user.is_authenticated and au.author == self.request.user 




class PostCreationView(UserPassesTestMixin, CreateView):
    model = PostImage
    fields = ("images", )
    success_url = reverse_lazy('post_list')
    template_name = 'post_creation.html'


    def test_func(self):
        return self.request.user.is_authenticated
    


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tags'] = Tag.objects.all()

        if self.request.POST:
            print(self.request.POST)
            context['post_form'] = PostCreationForm(self.request.POST)
        else:
            context['post_form'] = PostCreationForm()
        return context

    def post(self, request, *args, **kwargs):
        post = Post(title=self.request.POST['title'], subtitle=self.request.POST['subtitle'], body=self.request.POST['body'], meta_description=self.request.POST['meta_description'], author=self.request.user)
        saved = post.save()
        if self.request.POST['tags']:
            for t in ' '.join(self.request.POST['tags'].split(",")).split():
                if Tag.objects.get(name=t.strip()):
                    post.tags.add(Tag.objects.get(name=t.strip()))
                else:
                    Tag.objects.create(name=t.strip())
                    post.tags.add(Tag.objects.get(name=t.strip()))

        PostImage.objects.create(post=post, images=self.request.FILES['images'])
        return HttpResponseRedirect('/posts')



class SignUpView(UserPassesTestMixin, CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'
    permission_denied_message = ("You are already registered!")

    def test_func(self):
        return self.request.user.is_anonymous

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        f = open(r"C:\\Users\\alik2\\Desktop\\upproject\\main\\hobbies.txt", "r")
        context['languages'] = f.read().split(",")
        print(context)
        return context

class ChangeView(UserPassesTestMixin, UpdateView):
    form_class = CustomUserChangeForm
    success_url = reverse_lazy('index')
    template_name = 'change.html'
    queryset = CustomUser.objects.all()

    def test_func(self):
        return self.request.user.is_authenticated 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        f = open(r"C:\\Users\\alik2\\Desktop\\upproject\\main\\hobbies.txt", "r")
        context['languages'] = f.read().split(",")
        context['img'] = self.queryset.get(pk=self.request.user.id).profile_image.url
        print(context)
        return context

    def get_object(self):
        return CustomUser.objects.get(pk=self.request.user.id)


class PasswordsChangeView(auth_views.PasswordChangeView):
    form_class = PasswordChangeForm
    success_url = reverse_lazy('index')
    template_name = 'password_change.html'


class ProfileView(UserPassesTestMixin, DetailView):
    model = CustomUser
    template_name = 'profile.html'


    def test_func(self):
        return self.request.user.is_authenticated 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['resume'] = self.request.user.resume
        context['age'] = {'year': timezone.now().year - self.request.user.age.year, 'days': timezone.now().day - self.request.user.age.day}
        context['img_path'] = self.request.user.profile_image.path
        context['country'] = self.request.user.country 
        context['interest'] = self.request.user.interest
        context['username'] = self.request.user
        context['created_at'] = {'year': timezone.now().year - self.request.user.created_at.year, 'days': timezone.now().day - self.request.user.created_at.day}
        print(context)
        return context

    def get_object(self):
        return CustomUser.objects.get(pk=self.request.user.id)




def index(request):
    return render(request, 'index.html')
  