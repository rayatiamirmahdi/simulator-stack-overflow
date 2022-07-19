from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .models import Post, Comment
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import UpdateCreatPostFrom, CommentCreateForm, ReplyForm
from django.utils.text import slugify

class ShowPost(View):
    def get(self,request):
        posts = Post.objects.all()
        return render(request, "home/index.html", {"posts": posts})


class DetailPost(View):
    form_class = CommentCreateForm
    form_reply = ReplyForm
    def setup(self, request, *args, **kwargs):
        self.post_instance = get_object_or_404(Post, id=kwargs["post_id"], slug=kwargs["slug_post"])
        return super().setup(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        comments = self.post_instance.post_co.filter(is_reply=False)
        return render(request, "home/detail.html", {"post": self.post_instance, "comments": comments,"form":self.form_class, "reply": self.form_reply},)

    def post(self,request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.user = request.user
            new_comment.post = self.post_instance
            new_comment.save()
            messages.success(request, "your comment sended")
            return redirect("home:detail_url", self.post_instance.id, self.post_instance.slug)

class ReplyComment(LoginRequiredMixin,View):
    form_class = ReplyForm

    def post(self,request, *args, **kwargs):
        form = self.form_class(request.POST)
        post = get_object_or_404(Post, id=kwargs["post_id"])
        comment = get_object_or_404(Comment,id=kwargs["comment_id"])
        if form.is_valid():
            reply_co = form.save(commit=False)
            reply_co.user = request.user
            reply_co.post = post
            reply_co.reply = comment
            reply_co.is_reply = True
            reply_co.save()
            messages.success(request, "your comment send")
        return redirect("home:detail_url", post.id, post.slug)
class DeletePost(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        post = get_object_or_404(Post, pk=kwargs["post_id"])
        if post.user.pk == request.user.pk:
            post.delete()
            messages.success(request,"ba mvfght pak shd")
            return redirect("home:showindex_url")
        else:
            messages.error(request,"You do not have access")
            return redirect("home:showindex_url")

class UpdatePost(LoginRequiredMixin,View):
    form_class = UpdateCreatPostFrom

    def setup(self, request, *args, **kwargs):
        self.post_instance = Post.objects.get(pk=kwargs["post_id"])
        return super().setup( request, *args, **kwargs)



    def dispatch(self, request, *args, **kwargs):
        post = self.post_instance
        if post.user.pk != request.user.pk:
            messages.error(request, "You do not have access")
            return redirect("home:showindex_url")
        return super().dispatch(request, *args, **kwargs)

    def get(self,request, **kwargs):
        post = self.post_instance
        form = self.form_class(instance=post)
        return render(request, "home/updtform.html", {"form": form})

    def post(self,request, **kwargs):
        post = self.post_instance
        form = self.form_class(request.POST, instance=post)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.slug = slugify(form.cleaned_data["body"][:20])
            new_post.save()
            messages.success(request, "Updated")
            return redirect("home:detail_url", post.pk, post.slug)


class CreatePost(LoginRequiredMixin,View):
    form_class = UpdateCreatPostFrom
    def get(self,request,*args, **kwargs):
        form = self.form_class
        return render(request, "home/create.html", {"form":form})

    def post(self,request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.slug = slugify(form.cleaned_data["body"][:20])
            new_post.user = request.user
            new_post.save()
            messages.success(request, "Created the post")
            return redirect("account:profile_url", new_post.user.id)























