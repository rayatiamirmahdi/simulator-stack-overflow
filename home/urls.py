from django.urls import path
from . import views
app_name = "home"
urlpatterns = [
    path("", views.ShowPost.as_view(), name="showindex_url"),
    path("post/<int:post_id>/<slug:slug_post>/", views.DetailPost.as_view(), name="detail_url"),
    path("post/delete/<int:post_id>/", views.DeletePost.as_view(), name="delete_url"),
    path("post/update/<int:post_id>/", views.UpdatePost.as_view(), name="update_url"),
    path("post/create", views.CreatePost.as_view(), name="create_url"),
    path("post/reply/<int:post_id>/<int:comment_id>", views.ReplyComment.as_view(), name="reply_url")
]