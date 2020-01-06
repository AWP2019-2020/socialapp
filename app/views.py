from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import (
    TemplateView, ListView,
    CreateView, UpdateView, DeleteView, DetailView
)

from app.forms import CommentForm, PostForm, UserProfileForm
from app.models import Post, Comment, User, UserProfile


# def index(request):
#     return HttpResponse("Welcome to the SocialApp!")

def index(request):
    post_list = Post.objects.all()
    return render(request, 'index.html', {'post_list': post_list})


# class PostListView(View):

#     def get(self, request, *args, **kwargs):
#         post_list = Post.objects.all()
#         return render(request, 'index.html', {'post_list': post_list})


# class PostListView(TemplateView):
#     template_name = 'index.html'

#     def get_context_data(self):
#         post_list = Post.objects.all()
#         context = {
#             'post_list': post_list
#         }
#         return context


class PostListView(ListView):
    template_name = 'index.html'
    model = Post
    context_object_name = 'post_list'


def post_detail(request, pk):
    post = Post.objects.get(id=pk)
    form = CommentForm()
    return render(request, "post_detail.html", {"post": post, "form": form})


class UserProfileView(LoginRequiredMixin, DetailView):
    template_name = 'user_profile.html'
    context_object_name = 'userprofile'

    def get_object(self):
        user = User.objects.get(id=self.kwargs['pk'])
        userprofile = user.profile.first()
        return userprofile


class UserProfileRelationsView(LoginRequiredMixin, DetailView):
    template_name = 'user_profile_relations.html'
    context_object_name = 'userprofile'

    def get_object(self):
        user = User.objects.get(id=self.kwargs['pk'])
        userprofile = user.profile.first()
        return userprofile


class UserProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = UserProfile
    form_class = UserProfileForm
    template_name = 'user_profile_update.html'

    def get_context_data(self, **kwargs):
        context = super(UserProfileUpdateView, self).get_context_data(**kwargs)
        user = self.object.user
        context['form'].fields['first_name'].initial = user.first_name
        context['form'].fields['last_name'].initial = user.last_name
        context['form'].fields['e_mail'].initial = user.email
        return context

    def form_valid(self, form):
        data = form.cleaned_data
        self.object.birthday = data['birthday']
        self.object.country_id = data['country']
        self.request.user.first_name = data['first_name']
        self.request.user.last_name = data['last_name']
        self.request.user.email = data['e_mail']
        self.object.save()
        self.request.user.save()
        return redirect(reverse_lazy("user_profile",
                                     kwargs={"pk": self.request.user.id}))


@login_required
def comment_create(request, pk):
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            post = Post.objects.get(id=pk)
            Comment.objects.create(
                created_by=request.user,
                post=post,
                **form.cleaned_data
            )
            return redirect(reverse_lazy("post_detail", kwargs={"pk": pk}))


class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    fields = ['text']

    def form_valid(self, form):
        post = Post.objects.get(id=self.kwargs['pk'])
        Comment.objects.create(
            created_by=self.request.user,
            post=post,
            **form.cleaned_data
        )
        return redirect(reverse_lazy("post_detail", kwargs={"pk": self.kwargs['pk']}))


class CommentEditView(LoginRequiredMixin, UpdateView):
    model = Comment
    fields = ['text']
    pk_url_kwarg = 'pk_comment'
    template_name = 'comment_update.html'

    def form_valid(self, form):
        comment = Comment.objects.get(pk=self.kwargs['pk_comment'])
        comment.text = form.cleaned_data['text']
        comment.save()
        return redirect(reverse_lazy("post_detail", kwargs={"pk": self.kwargs['pk']}))


class CommentDeleteView(LoginRequiredMixin, DeleteView):
    template_name = "comment_delete.html"
    model = Comment
    pk_url_kwarg = 'pk_comment'

    def get_success_url(self):
        return reverse_lazy("post_detail", kwargs={"pk": self.kwargs['pk']})


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['text', 'image']
    template_name = 'post_create.html'

    def form_valid(self, form):
        post = Post.objects.create(
            created_by=self.request.user,
            **form.cleaned_data
        )
        return redirect(reverse_lazy("post_detail", kwargs={"pk": post.id}))


@login_required
def post_edit(request, pk):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = Post.objects.get(pk=pk)
            post.text = form.cleaned_data['text']
            post.save()
            return redirect(reverse_lazy("post_detail", kwargs={"pk": pk}))
    elif request.method == "GET":
        post = Post.objects.get(pk=pk)
        data = {"text": post.text}
        form = PostForm(initial=data)
        return render(request, "post_update.html", {"post": post, "form": form})


class PostEditView(LoginRequiredMixin, UpdateView):
    model = Post
    fields = ['text']
    template_name = 'post_update.html'

    def form_valid(self, form):
        post = Post.objects.get(pk=self.kwargs['pk'])
        post.text = form.cleaned_data['text']
        post.save()
        return redirect(reverse_lazy("post_detail", kwargs={"pk": self.kwargs['pk']}))


@login_required
def post_delete(request, pk):
    if request.method == "POST":
        post = Post.objects.get(pk=pk)
        post.delete()
        return redirect(reverse_lazy("post_list"))
    elif request.method == "GET":
        post = Post.objects.get(pk=pk)
        return render(request, "post_delete.html",
                      {"post": post})


class PostDeleteView(LoginRequiredMixin, DeleteView):
    template_name = "post_delete.html"
    model = Post

    def get_success_url(self):
        return reverse_lazy('post_list')


@login_required
def accept_friend_request(request, user_pk):
    requesting_user = User.objects.get(pk=user_pk)
    user_profile_requesting_user = requesting_user.profile.first()
    user_profile_requested_user = request.user.profile.first()
    user_profile_requested_user.friends.add(requesting_user)
    user_profile_requesting_user.friends.add(request.user)
    user_profile_requesting_user.friend_requests.remove(request.user)
    user_profile_requested_user.save()
    user_profile_requesting_user.save()
    return redirect(reverse_lazy("user_profile", kwargs={"pk": user_pk}))


class AcceptFriendRequestView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        user_pk = self.kwargs['user_pk']
        requesting_user = User.objects.get(pk=user_pk)
        user_profile_requesting_user = requesting_user.profile.first()
        user_profile_requested_user = request.user.profile.first()
        user_profile_requested_user.friends.add(requesting_user)
        user_profile_requesting_user.friends.add(request.user)
        user_profile_requesting_user.friend_requests.remove(request.user)
        user_profile_requested_user.save()
        user_profile_requesting_user.save()
        return redirect(reverse_lazy("user_profile", kwargs={"pk": user_pk}))


@login_required
def reject_friend_request(request, user_pk):
    requesting_user = User.objects.get(pk=user_pk)
    user_profile = requesting_user.profile.first()
    user_profile.friend_requests.remove(request.user)
    user_profile.save()
    return redirect(reverse_lazy("user_profile", kwargs={"pk": user_pk}))


@login_required
def cancel_friend_request(request, user_pk):
    requested_friend = User.objects.get(pk=user_pk)
    user_profile = request.user.profile.first()
    user_profile.friend_requests.remove(requested_friend)
    user_profile.save()
    return redirect(reverse_lazy("user_profile", kwargs={"pk": user_pk}))


class UnfriendView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        friend_pk = self.kwargs['friend_pk']
        friend = User.objects.get(pk=friend_pk)
        request_user_profile = request.user.profile.first()
        request_user_profile.friends.remove(friend)
        friend.profile.first().friends.remove(request.user)
        request_user_profile.save()
        friend.profile.first().save()
        return redirect(reverse_lazy("user_profile", kwargs={"pk": friend_pk}))


class SendFriendRequestView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        requested_user_pk = self.kwargs['user_pk']
        requested_user = User.objects.get(pk=requested_user_pk)
        request_user_profile = request.user.profile.first()
        request_user_profile.friend_requests.add(requested_user)
        request_user_profile.save()
        return redirect(reverse_lazy("user_profile",
                                     kwargs={"pk": requested_user_pk}))


class RegisterView(CreateView):
    template_name = 'register.html'
    form_class = UserCreationForm
    model = User

    def form_valid(self, form):
        data = form.cleaned_data
        user = User.objects.create_user(username=data['username'],
                                        password=data['password1'])
        UserProfile.objects.create(user=user)
        return redirect('post_list')


class LoginView(TemplateView):
    template_name = 'login.html'

    def get_context_data(self):
        form = AuthenticationForm()
        return {'form': form}

    def post(self, request, *args, **kwargs):
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(username=data['username'],
                                password=data['password'])
            login(request, user)
            return redirect(reverse_lazy('post_list'))
        else:
            return render(request, "login.html", {"form": form})


class LogoutView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect(reverse_lazy('post_list'))
