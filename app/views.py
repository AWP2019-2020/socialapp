from django.http import HttpResponse
from django.shortcuts import render

from django.views import View
from django.views.generic import TemplateView, ListView

from app.models import Post

def index(request):
    return HttpResponse("Welcome to the SocialApp!")

# def index(request):
#     post_list = Post.objects.all()
#     return render(request, 'index.html', {'post_list': post_list})


class PostListView(View):

    def get(self, request, *args, **kwargs):
        post_list = Post.objects.all()
        return render(request, 'index.html', {'post_list': post_list})


# class PostListView(TemplateView):
#     template_name = 'index.html'

#     def get_context_data(self):
#         post_list = Post.objects.all()
#         context = {
#             'post_list': post_list
#         }
#         return context


# class PostListView(ListView):
#     template_name = 'index.html'
#     model = Post
#     context_object_name = 'post_list'


def post_detail(request, pk):
    post = Post.objects.get(id=pk)
    return render(request, "post_detail.html", {"post": post})
