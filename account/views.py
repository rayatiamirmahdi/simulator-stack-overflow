from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .forms import UserRegisterForm, UserLoginForm
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from home.models import Post
from .models import Relations
from django.contrib import messages

class RegisterForm(View):
    form_class = UserRegisterForm

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("home:showindex_url")
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        form = self.form_class()
        return render(request, "account/register.html", {"form":form})

    def post(self,request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            User.objects.create_user(cd["username"], cd["email"], cd["password1"])
            return redirect("home:showindex_url")
            messages.success(request, "welcome")

        return render(request,"account/register.html", {"form":form})


class LoginForm(View):
    form_class = UserLoginForm

    def setup(self, request, *args, **kwargs):
        self.next = request.GET.get("next")
        return super().setup(request, *args, **kwargs)


    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("home:index_url")
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        form = self.form_class()
        return render(request, "account/login.html", {"form": form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd["username"], password=cd["password"])
            if user is not None:
                login(request, user)
                messages.success(request, "you Entered")
                if self.next:
                    return redirect(self.next)
                return redirect("home:showindex_url")
            messages.error(request, "username or password not correct")
        return render(request, "account/login.html", {"form": form})


class LogoutUser(LoginRequiredMixin, View):

    def get(self, request):
        logout(request)
        messages.success(request, "Got out")
        return redirect("home:showindex_url")


class ProfileUser(LoginRequiredMixin, View):
    def get(self, request, user_id):
        is_following = False
        user = get_object_or_404(User, pk=user_id)
        posts = Post.objects.filter(user=user)
        relation = Relations.objects.filter(from_follow=request.user, to_follow=user)
        if relation.exists():
            is_following = True
        return render(request, "account/profile.html", {"user": user, "posts": posts, "is_following": is_following})


class UserFollowView(LoginRequiredMixin,View):
    def get(self,request, *args, **kwargs):
        user = get_object_or_404(User, id=kwargs["user_id"])
        relation = Relations.objects.filter(from_follow=request.user, to_follow=user)
        if relation.exists():
            messages.error(request, " already followed")

        else:
            Relations(from_follow=request.user, to_follow=user).save()
            messages.success(request, "you are following user")

        return redirect("account:profile_url", user.id)

class UserUnfollowView(LoginRequiredMixin,View):
    def get(self,request, *args, **kwargs):
        user = get_object_or_404(User, id=kwargs["user_id"])
        relation = Relations.objects.filter(from_follow=request.user, to_follow=user)
        if relation.exists():
            relation.delete()
            messages.success(request,"unfollowed")
        else:
            messages.error(request,"already not followed")

        return redirect("account:profile_url", user.id)











