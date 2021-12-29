from django.http.response import HttpResponseRedirect
from django.shortcuts import render, reverse, redirect, get_object_or_404
from django.views import generic
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, request
import json
from .forms import EditProfileForm, UserForm
from django.contrib.auth import login
from django.contrib import messages
from .forms import NewUserForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import PasswordChangeView
from .models import Article, Profile
from .forms import CommentForm, ProfilePageForm
from .models import Comment
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post
from .forms import PostForm, EditForm, PasswordChangingForm

def index(request):
    form = '<tr><th><label for="id_name">Name:</label></th><td><input type="text" name="name" required id="id_name" /></td></tr><tr><th><label for="id_age">Age:</label></th><td><input type="number" name="age" required id="id_age" /></td></tr>'
    if request.method == "POST":
        name = request.POST.get("name")
        age = request.POST.get("age")     # получение значения поля age
        return HttpResponse("<h2>Привет, {0}, возрастом {1}</h2>".format(name,age))
    else:
        userform = UserForm()
        return render(request, "test.html", {"form": userform})

def about(request):
    posts = Article.objects.all()
    print(posts)
    return render(request, 'about.html',{'posts':posts})


@csrf_exempt
def test_get(request):
    num = request.GET['num']
    deg = request.GET['deg']
    r = int(num)** int(deg)
    print(r)
    return HttpResponse(r)

@csrf_exempt
def test_post(request):
    body = json.loads(request.body)
    r = body['num']**body['deg']
    array = [body['num'], body['deg']]
    min_num = array[0]
    for i in array:
        if min_num > i:
            min_num = i
    return HttpResponse(min_num)

@csrf_exempt
def admin(request):
    with open('templates/test.html', 'r') as file:
        return HttpResponse(file.read())

@csrf_exempt
def testo(request):
    with open('templates/fff.html', 'r') as file:
        return HttpResponse(file.read())

@csrf_exempt
def script(request):
    with open('templates/script.js', 'r') as file:
        return HttpResponse(file.read(), content_type="text/javascript")


def register_request(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect("home")
        messages.error(request, "Вы испоьзуете некорректную информацию.")  
    form = NewUserForm()
    return render (request=request, template_name="register.html", context={"register_form":form}) 
# Create your views here.

def contact(request):
    return render(request, "contact.html")

def create(request):
    error = ''
    comments = Comment.objects.order_by('-id')
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('com')
        else:
            error = 'Форма неверна'
    form = CommentForm()

    context = {
        "form":form,
        "error":error,
        "comments":comments
    }
    return render(request, "create.html", context)

def comment(request):
    comments = Comment.objects.order_by('-id')
    print(comments)
    return render(request, 'comms.html',{'comments':comments})

def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request,user)
                messages.info(request, f"You are logged in as {username}.")
                return redirect("home")
            else:
                messages.error(request, "Неверное имя пользователя или пароль.")
        else:
            messages.error(request, "Неверное имя пользователя или пароль.")
    form = AuthenticationForm()
    return render(request=request, template_name="login.html", context={"login_form":form})


class HomeView(ListView):
    model = Post
    template_name = 'post.html'
    ordering = ['-id']


class PostHomeView(DetailView):
    model = Post
    template_name = 'post_detail.html'

    def get_context_data(self, **kwargs):
        context = super(PostHomeView, self).get_context_data(**kwargs)
        stuff = get_object_or_404(Post, id=self.kwargs['pk'])
        total_likes = stuff.total_likes()
        liked = False
        if stuff.likes.filter(id=self.request.user.id).exists():
            liked = True
        context['total_likes'] = total_likes
        context['liked'] = liked
        return context

class AddPostView(CreateView):
    model = Post
    form_class = PostForm
    template_name = 'add_post.html'

class UpdatePostView(UpdateView):
    model = Post
    form_class = EditForm
    template_name = 'update_post.html'

class DeletePostView(DeleteView):
    model = Post
    template_name = 'delete_post.html'
    success_url = reverse_lazy('posts')

    
class UserEditView(generic.UpdateView):
    form_class = EditProfileForm
    template_name = 'edit_profile.html'
    success_url = reverse_lazy('home')

    def get_object(self):
        return self.request.user

class PasswordChangeView(PasswordChangeView):
    form_class = PasswordChangingForm
    success_url = reverse_lazy('password_success')

def password_success(request):
    return render(request, 'password_success.html', {})

def likeView(request, pk):
    post = get_object_or_404(Post, id=request.POST.get('post_id'))
    liked = False
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
        liked = False
    else:
        post.likes.add(request.user)
        liked = True
    return HttpResponseRedirect(reverse('post-detail', args=[str(pk)]))

class ShowProfilePageView(DetailView):
    model = Profile
    template_name = 'user_profile.html'

    def get_context_data(self, *args ,  **kwargs):
        context = super(ShowProfilePageView, self).get_context_data(*args, **kwargs)

        page_user = get_object_or_404(Profile, id=self.kwargs['pk'])
        context["page_user"] = page_user
        return context

class CreateProfilePageView(CreateView):
    model = Profile
    form_class = ProfilePageForm
    template_name = 'create_user_profile.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class EditProfilePageView(UpdateView):
    model = Profile
    template_name = 'edit_user_profile.html'
    fields = ['bio', 'profile_pic', 'website_url', 'facebook_url', 'instagram_url']

    success_url = reverse_lazy('home')