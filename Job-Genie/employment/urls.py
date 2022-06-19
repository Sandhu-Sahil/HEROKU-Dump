from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("employee", views.employee_view, name="employee"),
    path("companies", views.companies, name="company"),
    path("company", views.your_company, name="your_company"),
    path("create_company", views.create_company, name="create_company"),
    path("join_company/<str:id>", views.join_company, name="join_company"),
    path("company_dashboard/<str:id>", views.company_dashboard, name="company_dashboard"),
    path("leave_company", views.leave_company,name="leave_company"),
]