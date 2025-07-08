from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth import logout
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from SearchApp.forms import RegistrationForm,LostItemForm,FoundItemForm
from django.shortcuts import redirect
from SearchProject import settings
from django.contrib import messages 
from pathlib import Path
from SearchApp.models import FoundItem,LostItem# optional for feedback
from django.core.mail import send_mail,BadHeaderError

# Create your views here.


def home(request):
    return render(request,"home.html",{})

def login(request):
    if request.method == 'POST':
        username = request.POST.get('name')
        password = request.POST.get('pwd')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            auth_login(request, user)# Optional: Add a message
            messages.success(request, f"Welcome back, {user.username}!")
            # Redirect to admin panel if staff, else home
            # Check for 'next' parameter
            next_url = request.GET.get('next')
            if next_url:
                return redirect(next_url)
            # or a custom admin page
            else:
                return redirect('home')
        else:
            messages.error(request, "Invalid username or password.")
            return redirect('login')

    next_url = request.GET.get('next', '')
    return render(request, 'login.html', {'next': next_url})

   


def register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            role = form.cleaned_data.get('role')
            password = form.cleaned_data.get('password1')

            user.set_password(password)  # Hash the password
            if role == 'admin':
                user.is_staff = True
                user.is_superuser = True
                 # Give admin privileges
            user.save()
            return redirect("home")
    else:
        form = RegistrationForm()

    return render(request, "register.html", {"form": form})
    

def log_out(request):
    logout(request)
    return redirect('home') 
    

@login_required(login_url='login')
def reportlost(request):
    if request.method == 'POST':
        form = LostItemForm(request.POST, request.FILES)
        if form.is_valid():
            lost_item = form.save(commit=False)
            lost_item.user = request.user
            lost_item.save()
            return redirect('home')  # or redirect to a confirmation page
    else:
        form = LostItemForm()
    return render(request, 'reportlost.html', {'form': form})


def admin_home(request):
    return render(request,"admin_home.html")

@login_required(login_url='login')
def reportfound(request):
    if request.method == 'POST':
        form = FoundItemForm(request.POST, request.FILES)
        if form.is_valid():
            found_item = form.save(commit=False)
            found_item.reported_by = request.user
            found_item.save()

            found_name = found_item.item_name.strip().lower()
            print("Uploaded found item name:", found_name)

            # Instead of deleting, just mark the lost item as matched
            matching_item = LostItem.objects.filter(item_name__iexact=found_name, is_matched=False).first()

            if matching_item:
                matching_item.is_matched = True
                matching_item.save()
                print(f"[MATCHED] LostItem ID: {matching_item.id} marked as matched.")
            else:
                print("No matching LostItem found with that name.")

            return redirect('found_list')
    else:
        form = FoundItemForm()

    return render(request, 'reportfound.html', {'form': form})





def update_lost(request, id):
    item = get_object_or_404(LostItem, id=id)
    if item.user != request.user:
        return HttpResponse("You are not allowed to update this item.")
    form = LostItemForm(request.POST or None, request.FILES or None, instance=item)
    if form.is_valid():
        form.save()
        return redirect('lost_list')
    return render(request, 'update_lost.html', {'form': form})
 
def update_found(request, id):
    item = get_object_or_404(FoundItem, id=id)
    if item.reported_by != request.user:
        return HttpResponse("You are not allowed to update this item.")
    form = FoundItemForm(request.POST or None, request.FILES or None, instance=item)
    if form.is_valid():
        form.save()
        return redirect('found_list')
    return render(request, 'update_found.html', {'form': form})

@login_required(login_url='login')  
def found_list(request):
    items = FoundItem.objects.all()
    return render(request, 'found_list.html', {'items': items})


@login_required(login_url='login')  
def lost_list(request):
    items = LostItem.objects.all()
    return render(request, 'lost_list.html', {'items': items})

def delete_lost(request, id):
    item = get_object_or_404(LostItem, id=id)
    if item.user != request.user:
        return HttpResponse("You are not allowed to delete this item.")
    item.delete()
    return redirect('lost_list')

def delete_found(request, id):
    item = get_object_or_404(FoundItem, id=id)
    if item.reported_by != request.user:
        return HttpResponse("You are not allowed to delete this item.")
    item.delete()
    return redirect('found_list')

@staff_member_required
def claim_item(request, id):
    item = get_object_or_404(FoundItem, id=id)

    lost_match = LostItem.objects.filter(item_name__icontains=item.item_name).first()
    if lost_match:
        to_email = lost_match.user.email.strip()  # FIX: remove unwanted newline

        try:
            send_mail(
                'Your lost item has been found!',
                f'Hello {lost_match.user.username} ({lost_match.user.first_name}), your item "{lost_match.item_name}" has been found.',
                'admin@example.com',
                [to_email]
            )
            item.is_claimed = True
            item.save()
            lost_match.delete() 
            messages.success(request, f"Email sent to {to_email}.")
        except BadHeaderError:
            messages.error(request, "Invalid header found in email address.")
    else:
        messages.warning(request, f"No matching lost item found for '{item.item_name}'.")

    return redirect('claimdashboard')


@staff_member_required
def claimdashboard(request):
    unclaimed_items = FoundItem.objects.filter(is_claimed=False)
    return render(request, 'claimdashboard.html', {'items': unclaimed_items})

def contact(request):
    return render(request,"contact.html",{})