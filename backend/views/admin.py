from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import user_passes_test
from .ldap import ldap
from backend.models import Item, Checkout, CheckoutItem, User
from django.contrib.auth.models import UserManager
from django.contrib.auth.forms import UserChangeForm
from pinax.eventlog.models import log


def admin_check(user):
    # check if user is an admin here
    return user.is_superuser


@user_passes_test(admin_check)
def dashboard(request):
    return render(request, 'admin/dashboard.html', {'title': 'Admin Dashboard'})


@user_passes_test(admin_check)
def show_users(request):
    users = User.objects.all()
    return render(request, 'admin/userList.html', {'title': 'Users | Admin', 'users': users})


@user_passes_test(admin_check)
def show_user(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    return render(request, 'admin/showUser.html', {'title': user.first_name + ' | Admin', 'user': user})


@user_passes_test(admin_check)
def add_user(request):
    if request.method == "POST":
        form = UserChangeForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.save()
            # for now redirect back to item listings. Until detailed page is done

            log(
                user=request.user,
                action="ITEM_TYPE_CREATED",
                obj=obj,
                extra={
                }
            )
            return redirect('userList')
    else:



        return render(request, 'admin/addUser.html', {'title': 'Add User | Admin', 'form': form})


def promote_to_staff(username):

    users = User.objects.filter(username = username)
    if not users:
        #get them from ldap again
        ldap_user = ldap.get_user_by_username(username)
        #add them
        user = User.objects.create_user(username=username, email = ldap.get_email(ldap_user))
        user.first_name=ldap.get_first_name(ldap_user)
        user.last_name=ldap.get_last_name(ldap_user)
        user.is_staff = True
        user.save()

        return HttpResponse(status=204)
    else:
        user = users[0]
        user.is_staff = True
        user.save()
        return HttpResponse(status=204)


@user_passes_test(admin_check)
def edit_user(request, user_id):
    if request.method == "POST":
        user = get_object_or_404(User, pk=user_id)

        if request.POST['user_type'] == "user":
            user.is_staff = False
            user.is_superuser = False
        elif request.POST['user_type'] == "labassistant":
            user.is_staff = True
            user.is_superuser = False
        elif request.POST['user_type'] == "admin":
            user.is_staff = True
            user.is_superuser = True

        if "password" in request.POST:
            if len(request.POST['password']) > 0:
                print("setting password")
                user.set_password(request.POST['password'])
            else:
                print("blank password, not setting")

        user.save()

        log(
            user=request.user,
            action="USER_MODIFIED",
            obj=user,
            extra={}
        )

        return redirect('adminUserList')
    else:
        user = get_object_or_404(User, pk=user_id)
        user_type = ""
        if user.is_staff and user.is_superuser:
            user_type = "admin"
        elif user.is_staff:
            user_type = "labassistant"
        else:
            user_type = "user"

        return render(request, 'admin/editUser.html', {'title': 'Edit User | Admin', 'user': user,'user_type':user_type})

