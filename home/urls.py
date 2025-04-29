from django.urls import path

from . import views

urlpatterns = [
    path("",views.Home_page, name="home"),
    path("home/",views.Auth_Home_Page, name="auth_home"),
    path('home/search',views.SearchMovie,name="search_movie"),
    path('home/filter/',views.FilterMovie,name="filter_movie"),
    path('home/search-result/',views.SearchResult,name="search_result"),
    path('home/addtofavourites/',views.AddToFavourites,name="add_to_fav"),
    path('home/forget-password',views.ForgetPassword,name="forget_pass"),
    path('home/toggleComment/',views.ToggleComment,name="toggle-comment"),
    path('home/getcasts/',views.getCasts,name="get_casts"),
    path('home/clear-first-login/',views.clearFirstLogin,name="clear_first_login"),
    path('home/slider-movies/',views.GetSliderMovies,name="slider_movies"),
    path('home/favourites',views.AuthFavourites,name="auth_favs"),
    path('home/movies/',views.GetCastMovies,name="get_cast_movies"),
    path('home/movies/<str:name>',views.CastMoviesPage,name="cast_movies"),
    path('home/<str:code>',views.SingleMoviePage, name="single_movie"),
]
