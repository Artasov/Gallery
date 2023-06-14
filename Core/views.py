from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.db import transaction
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils import timezone
from django.utils.crypto import get_random_string

from APP_shop.models import Product
from Core.funcs import send_email_by_template
from Core.models import User, UnconfirmedUser, UnconfirmedPasswordReset, Promo


def main(request):
    now = timezone.now()
    promos = Promo.objects.filter(
        date_published__lte=now,
        date_expired__gte=now,
    )
    return render(request, 'Core/main.html', {
        'promos': promos,
    })


def profile(request):
    return render(request, 'Core/profile.html')


@transaction.atomic
def signup(request):
    if request.user.is_authenticated:
        logout(request)

    if request.method == "POST":
        username = request.POST.get('username', '')
        email = request.POST.get('email', '')
        password = request.POST.get('password', '')

        try:
            validate_email(email)
        except ValidationError:
            return render(request, 'Core/registration/signup.html', context={
                'invalid': 'The Email field must be filled in, must have the type ***@***.***',
                'username': username, 'email': email})

        if len(password) < 6:
            return render(request, 'Core/registration/signup.html', context={
                'invalid': 'The password field must contain at least 6 characters.',
                'username': username, 'email': email})

        if len(username) < 6:
            username = email[0:email.find('@')]

        if User.objects.filter(username=username).exists():
            return render(request, 'Core/registration/signup.html', context={
                'invalid': 'User with this name already exists.',
                'username': username, 'email': email})

        if User.objects.filter(email=email).exists():
            return render(request, 'Core/registration/signup.html', context={
                'invalid': 'User with such an email already exists.',
                'username': username, 'email': email})

        confirmation_code = get_random_string(40)
        UnconfirmedUser.objects.create(
            username=username,
            email=email,
            password=make_password(password),
            confirmation_code=confirmation_code
        )

        send_email_by_template(
            subject='Completion of registration',
            to_email=email,
            template='Core/email_templates/email_signup_confirmation.html',
            context={'link': request.get_host() + reverse('signup_confirmation', args=[confirmation_code])}
        )

        return render(request, 'Core/check_email.html')

    return render(request, 'Core/registration/signup.html')


@transaction.atomic
def signup_confirmation(request, confirmation_code):
    if request.user.is_authenticated:
        logout(request)

    unconfirmed_user = UnconfirmedUser.objects.filter(confirmation_code=confirmation_code).first()
    if unconfirmed_user:
        User.objects.create(username=unconfirmed_user.username,
                            email=unconfirmed_user.email,
                            password=unconfirmed_user.password)
        unconfirmed_user.delete()

        return render(request, 'Core/registration/signin.html', context={
            'success': 'You have successfully registered.'
        })
    else:
        return render(request, 'Core/invalid.html', {'invalid': '404', 'redirect': 'signup'})


def signin(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect('signin')

    if request.method == "POST":
        # CHECKING EMAIL OR USERNAME AUTH
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        if '@' in username:
            username = User.objects.get(email=username).username
        else:
            username = request.POST['username']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('main')
        else:
            return render(request, 'Core/registration/signin.html', context={
                'invalid': 'Invalid username/email or password',
                'username': username})

    return render(request, 'Core/registration/signin.html')


def password_reset(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect('password_reset')

    if request.method == "POST":
        email = request.POST.get('email', '')
        try:
            validate_email(email)
        except ValidationError:
            return render(request, 'Core/registration/password_reset_stage_1.html', context={
                'invalid': 'The Email field must be filled in, must have the type ***@***.***', })
        if not User.objects.filter(email=email).exists():
            return render(request, 'Core/registration/password_reset_stage_1.html', context={
                'invalid': 'User with this email does not exists', })

        confirmation_code = get_random_string(40)
        UnconfirmedPasswordReset.objects.create(email=email,
                                                confirmation_code=confirmation_code)

        send_email_by_template(subject='Password reset',
                               to_email=email,
                               template='Core/email_templates/email_password_reset_confirmation.html',
                               context={'link': request.get_host() + reverse('password_reset_confirmation',
                                                                             args=[confirmation_code])})
        return render(request, 'Core/check_email.html')

    return render(request, 'Core/registration/password_reset_stage_1.html')


@transaction.atomic
def password_reset_confirmation(request, confirmation_code):
    if request.user.is_authenticated:
        return redirect('logout')

    if request.method == "POST":
        if UnconfirmedPasswordReset.objects.filter(confirmation_code=confirmation_code).exists():
            unconfirmedpasswordreset_ = UnconfirmedPasswordReset.objects.get(confirmation_code=confirmation_code)
            user_ = User.objects.get(email=unconfirmedpasswordreset_.email)
            user_.password = make_password(request.POST.get('new_password', ''))
            user_.save()
            unconfirmedpasswordreset_.delete()
            return render(request, 'Core/registration/signin.html', {'success': 'Password changed'})
        else:
            return render(request, 'Core/invalid.html', {'invalid': '404', 'redirect': 'signup'})

    return render(request, 'Core/registration/password_reset_stage_2.html', context={
        'confirmation_code': confirmation_code
    })
