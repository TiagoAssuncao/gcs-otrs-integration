from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, Permission

def show_login(request):
    if request.method == "GET":
        return render(request, "dust_auth/login.html")
    else:
        context = make_login(request)

        if context.get('is_logged'):
            return redirect(reverse("home"))
        else:
            return render(request, "dust_auth/login.html", context)

def make_login(request):
    form = request.POST
    password = form.get('password')
    email = form.get('email')

    is_logged = False
    try:
        user_tmp = User.objects.get(email=email)
    except:
        messages.error(request, 'O email nao esta cadastrado')
        context = {
            "is_logged": is_logged,
        }
        return context

    user = authenticate(username=user_tmp.username, password=password)

    if user is not None:
        login(request, user)
        message = "Logged"
        is_logged = True
    else:
        messages.error(request, 'Usuario e senha nao conferem')

    context = {
        "is_logged": is_logged,
    }

    return context

def signup(request):
    if request.method == "GET":
        return render(request, "dust_auth/signup.html")
    else:
        form = request.POST
        username = form.get('username')
        password = form.get('password')
        email = form.get('email')
        try:
            user = User.objects.get(email=email)
            messages.error(request, 'Este email ja existe')
            return render(request, "dust_auth/signup.html")
        except:
            pass

        user = User.objects.create_user(username, email, password)
        user.save()
        messages.error(request, 'Usuario cadastrado com sucesso')
        messages.info(request, 'Agora faca o login')

        return redirect(reverse("auth:login"))

def make_logout(request):
    logout(request)
    return redirect(reverse("home"))

def users(request):
    users = User.objects.all()

    user_perm = []
    for user in users:
        can_read = 'checked' if user.has_perm('comment.can_read') else ''
        can_comment = 'checked' if user.has_perm('comment.can_comment') else ''
        user_perm.append({
            "current_user": user,
            "id": user.id,
            "can_read": can_read,
            "can_comment": can_comment,
        })

    context = {"users": user_perm}

    return render(request, "dust_auth/users.html", context)

def make_permissions(request):
    if request.method == "POST":
        form = request.POST
        can_read = form.get("can_read")
        can_comment = form.get("can_comment")

        user_id = int(form.get("user_id"))
        user = User.objects.get(id=user_id)
        user.user_permissions.clear()

        if can_read == "on":
            permission = Permission.objects.get(codename='can_read')
            user.user_permissions.add(permission)

        if can_comment == "on":
            permission = Permission.objects.get(codename='can_comment')
            user.user_permissions.add(permission)

        user.save()

    return redirect(reverse("auth:users"))
