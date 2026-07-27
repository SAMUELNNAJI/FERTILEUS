from django.urls import path
from . import views

urlpatterns = [
    path('',                      views.home,        name='home'),
    path('about/',                views.about,       name='about'),
    path('egg-donation/',         views.egg_donation, name='egg_donation'),
    path('calculator/',           views.calculator,  name='calculator'),
    path('blog/',                 views.blog,        name='blog'),
    path('blog/<slug:slug>/',     views.blog_post,   name='blog_post'),
    path('contact/',              views.contact,     name='contact'),
    path('comments/<int:comment_id>/delete/', views.delete_comment, name='delete_comment'),
    path('comments/<int:comment_id>/edit/', views.edit_comment, name='edit_comment'),
    path('comments/<int:comment_id>/like/', views.like_comment, name='like_comment'),
]
