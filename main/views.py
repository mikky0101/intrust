from django.shortcuts import render, redirect, reverse
from django.contrib.auth import authenticate, login, logout
from .models import Account, Transaction, User
from django.contrib import messages

# Create your views here.
def home(request):
    for user in User.objects.all():
        print(user.get_balance)
    return render(request, "home.html")

def about(request):
    return render(request, "index.html")

def register(request):
    print(request.user)
    if request.method == 'POST' and request.FILES:
        first_name =  request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        middle_name = request.POST.get('middle_name')
        email = request.POST.get('email')
        gender = request.POST.get('gender')
        profile_picture = request.FILES['profile_picture']
        city = request.POST.get('city')
        state = request.POST.get('state')
        zip_code = request.POST.get('zip_code')
        phone_number = request.POST.get('phone_number')
        account_type = request.POST.get('account_type')
        password = request.POST.get('password')
        username = request.POST.get('username')
        user = User.objects.create(profile_picture=profile_picture, password=password, sex=gender, email=email, zipcode=zip_code, first_name=first_name, last_name=last_name, city=city, middle_name=middle_name, state=state, phone_number=phone_number, account_type=account_type, username= username)
        user.save()
    return render(request, "open-account.html")

def logout_view(request):
    logout(request.user)
    return redirect("main:home")

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.info(request, f'succesfully logged in as {request.user}')
            return redirect("main:transfer")
        else:
            messages.warning(request, "invalid login details, login again!")
            return redirect("main:home")

def profile(request, pk):
    user = User.objects.get(id = pk)
    account = Account.objects.get(user=user)
    account_number = account.number
    transactions = Transaction.objects.filter(sender=request.user)
    print(user)
    context = {
        "user": user,
        "account_number": account_number,
        "transactions": transactions
    }
    return render(request, "index.html", context)

def transfer_confirm(request, ref):
    transaction = Transaction.objects.get(ref=ref)
    user_pin = int(transaction.sender.pin)
    account = Account.objects.get(user=request.user)
    account_number = account.number
    context = {
        "transaction": transaction,
        "user": request.user,
        "account_number": account_number
    }
    if request.method == 'POST':
        pin = request.POST.get("account_number")
        pin = int(pin)
        print(type(pin))
        print(type(user_pin))
        if user_pin == pin:
            messages.success(request, "Transaction Successful")
            messages.success(request, f'{transaction.amount_tf} send to {transaction.receiver}')
            # return redirect("main:profile", pk=request.user.id)
            return render(request, "succesful.html")
        else:
            messages.warning(request, "incorrect pin")
            messages.warning(request, "you have 2 more attempts")
            print(messages)
            return redirect("main:confirmation", ref=transaction.ref)
    return render(request, "stage2.html", context )

def transfer(request):
    print(request.user.get_balance())
    account = Account.objects.get(user=request.user)
    account_number = account.number
    tr = Transaction.objects.first()
    user = request.user
    context = {
        "user": user,
        "account_number": account_number
    }
    if request.method == 'POST':
        number = request.POST.get("account_number")
        amount = request.POST.get("amount")
        receiver = Account.objects.get(number=number)
        new_trans = Transaction.objects.create(sender=request.user, receiver=receiver, amount_tf=amount)
        return redirect("main:confirmation", ref=new_trans.ref)
    return render(request, "transfer.html", context)

def history(request, ref):
    account = Account.objects.get(user=request.user)
    account_number = account.number
    transaction = Transaction.objects.get(ref=ref)
    context = {
        "user": request.user,
        "account_number": account_number,
        "transaction": transaction
    }
    return render(request, "history.html", context)

def transaction_history(request, us):
    transactions = Transaction.objects.filter(sender=request.user)
    for a in transactions:
        print(a.date)
    account = Account.objects.get(user=request.user)
    account_number = account.number
    context = {
        "user": request.user,
        "account_number": account_number,
        "transactions": transactions
    }
    return render(request, "transactions.html", context)