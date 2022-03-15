from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import DetailView, ListView
from django.contrib import messages
from .models import Comment, UserProfile, CommentSection, Watchlist
from django.urls import reverse, reverse_lazy
from .forms import CommentForm, SignUpForm, EditProfileForm, PasswordChanged, ProfilePageForm, AddCommentForm, AddWatchlist
from django.contrib.auth.views import PasswordChangeView

# IMPORTS RELATED TO SIGNUP
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm

# Authorization decorators:
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

# Import For Fetch
import requests
import os
from dotenv import load_dotenv
load_dotenv()


TMDB_API_KEY = os.getenv('TMDB_API_KEY')
page = 1

# VIEWS #
                        # Movies #
# Home
    # FETCH REQUEST #
def home(request):
    playing = requests.get(f"https://api.themoviedb.org/3/movie/now_playing?api_key={TMDB_API_KEY}&language=en-US&page={page}").json()

    coming = requests.get(f"https://api.themoviedb.org/3/movie/upcoming?api_key={TMDB_API_KEY}&language=en-US&page={page}").json()

    trending = requests.get(f"https://api.themoviedb.org/3/trending/all/day?api_key={TMDB_API_KEY}").json()
    return render(request, 'home.html', {'res': playing, 'coming': coming, 'trend': trending})

class HomeView(ListView):
    model = Comment
    template_name = 'social.html'


@method_decorator(login_required, name="dispatch")
class SocialView(DetailView):
    model = Comment
    template_name = 'social_detail.html'

    def get_context_data(self, *arg, **kwargs):
        context = super(SocialView, self).get_context_data(**kwargs)
        info = get_object_or_404(Comment, id=self.kwargs['pk'])
        total_likes = info.total_likes()
        liked = False
        if info.likes.filter(id=self.request.user.id).exists():
            liked = True
        context["total_likes"] = total_likes
        context['liked'] = liked
        return context



@method_decorator(login_required, name="dispatch")
class AddComment(CreateView):
    model = Comment
    form_class = CommentForm
    # fields = ['body']
    template_name = 'add_comment.html'
    success_url = '/social/'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(AddComment, self).form_valid(form)

    def get_success_url(self):
        return reverse('social_detail', kwargs={'pk': self.object.pk})



@method_decorator(login_required, name="dispatch")
class CommentOnPost(CreateView):
    model = CommentSection
    form_class = AddCommentForm
    template_name = 'thread_comment.html'
    success_url = '/'

    def form_valid(self, form, *args, **kwargs):
        form.instance.comment_id = self.kwargs['pk']
        form.instance.name = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('social_detail', kwargs={'pk': self.object.pk})  


@method_decorator(login_required, name="dispatch")
class UpdateComment(UpdateView):
    model = Comment
    template_name = 'update_comment.html'
    # fields = ['body']
    form_class = CommentForm
    success_url = '/'



@method_decorator(login_required, name="dispatch")
class DeleteComment(DeleteView):
    model = Comment
    template_name = 'delete_comment.html'
    success_url = '/'


def LikeView(request, pk):
    comment = get_object_or_404(Comment, id=request.POST.get('comment_id'))
    liked = False
    if comment.likes.filter(id=request.user.id).exists():
        comment.likes.remove(request.user)
        liked = False
    else:
        comment.likes.add(request.user)
        liked = True
    return HttpResponseRedirect(reverse('social_detail', args=[str(pk)]))



@method_decorator(login_required, name="dispatch")
class MovieDetail(TemplateView):
    def get(self, request, *args, **kwargs):
        id = kwargs.get('movie_id')
        info = requests.get(f"https://api.themoviedb.org/3/movie/{id}?api_key={TMDB_API_KEY}").json()
        return render(request, 'movie_detail.html', {'info': info})


@method_decorator(login_required, name="dispatch")
class SearchResult(TemplateView):
    def get(self, request, *args, **kwargs):
        search_query = ''
        search_query = request.GET['search']
        result = requests.get(f"https://api.themoviedb.org/3/search/movie?api_key={TMDB_API_KEY}&query={search_query}").json()
        return render (request, 'search_results.html', { 'result': result})










                        # USER MODEL #
# Watchlist

@method_decorator(login_required, name="dispatch")
class WatchlistView(TemplateView):
    model = Watchlist
    form_class = AddWatchlist
    template_name = 'watchlist.html'

    def get_context_data(self, *args, **kwargs):
        context = super(WatchlistView, self).get_context_data(*args, **kwargs)
        user_page = get_object_or_404(UserProfile, id=self.kwargs['pk'])
        context["user_page"] = user_page
        return context
    

class AddWatch(CreateView):
    model = Watchlist
    form_class = AddWatchlist
    # def AddWatchlistView(request, pk):
    #     movie = get_object_or_404(Watchlist, id=request.POST.get('movie_id'))
    #     movie = Watchlist.objects.get(id=pk)

    def form_valid(self, request, form, *args, **kwargs):
        form.instance.user = self.request.user
        id = kwargs.get('movie_id')
        form.instance.movie_id = id
        return super().form_valid(form)
    #     print(id)
    
    def get_success_url(self):
        return HttpResponseRedirect(reverse('movie_detail', args=[str(pk)]))

        # def get(self, request):
        #     form = AddWatchlist() # comes from the auth.forms library - create a new form;

        #     context = {'form': form}
        #     return render(request, "registration/signup.html", context)


        # # post request
        # def post(self, request):

        #     if form.is_valid():
        #         user = form.save() # save the user in the users table
        #         # login functionality
        #         login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        #         return redirect('social')
        #     else:

        #         context = {'form': form}
        #         return render(request, "registration/signup.html", context)









# Profile
@method_decorator(login_required, name="dispatch")
class ProfilePage(DetailView):
    model = UserProfile
    template_name = 'registration/profile.html'

    def get_context_data(self, *args, **kwargs):
        context = super(ProfilePage, self).get_context_data(*args, **kwargs)

        user_page = get_object_or_404(UserProfile, id=self.kwargs['pk'])

        context["user_page"] = user_page
        return context



@method_decorator(login_required, name="dispatch")
class CreateProfile(CreateView):
    model = UserProfile
    form_class = ProfilePageForm
    template_name = 'registration/create_profile.html'
    # fields = '__all__'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('user-profile', kwargs={'pk': self.object.pk})




@method_decorator(login_required, name="dispatch")
class EditProfilePage(UpdateView):
    model = UserProfile
    template_name = 'registration/profile_edit_page.html'
    # fields = '__all__'
    fields = [ 'about', 'image', 'city', 'website', 'linkedin', 'twitter', 'tiktok', 'github', 'discord']
    success_url = '/'



@method_decorator(login_required, name="dispatch")
class EditSettings(UpdateView):
    form_class = EditProfileForm
    template_name = 'registration/edit_settings.html'
    success_url = '/profile'

    def get_object(self):
        return self.request.user


# Signup
class Signup(View):
    # get request
    def get(self, request):
        form = SignUpForm() # comes from the auth.forms library - create a new form;

        context = {'form': form}
        return render(request, "registration/signup.html", context)


    # post request
    def post(self, request):
        form = SignUpForm(request.POST)

        if form.is_valid():
            user = form.save() # save the user in the users table
            # login functionality
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('social')
        else:

            context = {'form': form}
            return render(request, "registration/signup.html", context)


@method_decorator(login_required, name="dispatch")
class PasswordsChangeView(PasswordChangeView):
    form_class = PasswordChanged
    template_name= 'registration/change-password.html'
    success_url = '/updated-password/'

def password_success(request):
    return render(request, 'registration/password_success.html')