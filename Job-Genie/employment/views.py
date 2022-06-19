from django.shortcuts import  HttpResponse, HttpResponseRedirect, render
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError

from .models import User, Employee, Company, History


# Create your views here.
def index(request):

    # Authenticated users view their inbox
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse("company"))

    # Everyone else is prompted to sign in
    else:
        return HttpResponseRedirect(reverse("login"))

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        email = request.POST["email"]
        password = request.POST["password"]
        user = authenticate(request, username=email, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "employment/login.html", {
                "message": "Invalid email and/or password."
            })
    else:
        return render(request, "employment/login.html")

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

def register(request):
    if request.method == "POST":
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "employment/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(email, email, password)
            user.save()
        except IntegrityError as e:
            print(e)
            return render(request, "employment/register.html", {
                "message": "Email address already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "employment/register.html")


@login_required
def employee_view(request):
    his  = History.objects.filter(user = request.user)
    if Employee.objects.filter(user = request.user):
        emp = Employee.objects.get(user = request.user)
    else:
        emp = None
    content= {
        'history':his,
        'employ': emp,
    }
    return render(request, "employment/employee.html", content)


@login_required
def companies(request):
    comp = Company.objects.all()
    if Employee.objects.filter(user = request.user):
        emp = Employee.objects.get(user = request.user)
    else:
        emp=None
    context={
        'companies': comp,
        'employee': emp,
    }
    return render(request, "employment/companies.html", context)


@login_required
def create_company(request):
    if request.method == "POST":
        comapny = request.POST.get("company")
        c = Company.objects.create(name = comapny, creator = request.user)
        c.save()
        return HttpResponseRedirect(reverse("your_company"))
    else:
        return render(request, "employment/create_company.html")


@login_required
def your_company(request):
    comp = Company.objects.filter(creator = request.user)
    context={
        'companies': comp
    }
    return render(request, "employment/your_company.html", context)


@login_required
def join_company(request, id):
    print(id)
    if Employee.objects.filter(user = request.user):
        emp = Employee.objects.get(user = request.user)
        if emp.company != None:
            history = History.objects.create(user = request.user, company = emp.company, join_date = emp.join_date)
            history.save()
        emp.delete()
        comp=Company.objects.get(name = id)
        emp = Employee.objects.create(user = request.user, company = comp)
        emp.save()
        return HttpResponseRedirect(reverse("employee"))
    else:
        comp=Company.objects.get(name = id)
        print(comp)
        emp = Employee.objects.create(user = request.user, company = comp)
        emp.save()
        return HttpResponseRedirect(reverse("employee"))


@login_required
def company_dashboard(request, id):
    comp = Company.objects.get(name = id)
    his  = History.objects.filter(company = Company.objects.get(name = id))
    emp = Employee.objects.filter(company = Company.objects.get(name = id))
    if Employee.objects.filter(user = request.user):
        emp2 = Employee.objects.get(user = request.user)
    else:
        emp2=None
    content = {
        'history' : his,
        'employee' : emp,
        'company' : comp,
        'employ':emp2
    }
    print(comp)
    return render(request, "employment/company_dashboard.html", content)


@login_required
def leave_company(request):
    emp = Employee.objects.get(user=request.user)
    history = History.objects.create(user = request.user, company = emp.company, join_date = emp.join_date)
    history.save()
    emp.company = None
    emp.save()
    his  = History.objects.filter(user = request.user)
    if Employee.objects.filter(user = request.user):
        emp = Employee.objects.get(user = request.user)
    print(emp.company)
    content= {
        'history':his,
        'employ': emp,
    }
    return render(request, "employment/employee.html", content)

