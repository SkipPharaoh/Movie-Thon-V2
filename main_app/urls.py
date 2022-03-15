from django.urls import path
from . import views


urlpatterns = [
    path('', views.HomeView.as_view(), name='social'),
    path('movies/', views.movie, name="home"),
    path('social/<int:pk>', views.SocialView.as_view(), name='social_detail'),
    path('add-comment/', views.AddComment.as_view(), name='add-comment'),
    path('social/<int:pk>/edit', views.UpdateComment.as_view(), name='update-comment'),
    path('social/<int:pk>/delete', views.DeleteComment.as_view(), name='delete-comment'),
    path('movie/<int:movie_id>', views.MovieDetail.as_view(), name='movie_detail'),
    path('search/', views.SearchResult.as_view(), name="search"),
    path('social/<int:pk>/comment/', views.CommentOnPost.as_view(), name='comment-on-post'),
    path('like/<int:pk>', views.LikeView, name='like_comment'),

    path('watchlist/<int:pk>/add', views.AddWatch.as_view(), name='add_movie'),
    path('watchlist/<int:pk>/remove', views.RemoveWatch.as_view(), name='remove_movie'),
    path('profile/<int:pk>/watchlist', views.WatchlistView.as_view(), name='watchlist'),

    path('profile/<int:pk>/', views.ProfilePage.as_view(), name='user-profile'),
    path('profile/settings', views.EditSettings.as_view(), name='edit-settings'),
    path('profile/<int:pk>/edit', views.EditProfilePage.as_view(), name='edit-profile-page'),
    path('profile/create', views.CreateProfile.as_view(), name='create-profile'),
    path('accounts/signup/', views.Signup.as_view(), name='signup'),
    path('password/', views.PasswordsChangeView.as_view()),
    path('updated-password/', views.password_success, name='password-success'),
]