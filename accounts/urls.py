from django.urls import path

from . import views

urlpatterns = [
    path("login/",views.Login_page.as_view(),name="login"),
    path("signup/",views.Signup_page.as_view(),name="signup"),
    path("authenticate/", views.Auth_page, name="authenticate"),
    path("forgetpassword",views.AccForgetPassword,name="accforget_pass"),
    path("auth/reset-pass",views.Auth_AccResetPassword,name="auth_accreset_pass"),
    path("<slug:auth_token>",views.email_authentication,name="email_auth"),
    path("reset-pass/<slug:pass_reset_token>",views.AccResetPassword,name="accreset_pass")
]
