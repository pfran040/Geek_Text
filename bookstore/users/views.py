from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages # to display alert messages when the form data is valid
from .forms import UserSignUpForm, ProfileUpdateForm, UserUpdateForm, UserProfileForm, BioForm, NicknameForm, EditAddressForm, DeleteAddressForm, CreditCardForm, DeleteCreditCardConfirmation
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.http import HttpResponseRedirect
from django.contrib.auth.forms import PasswordChangeForm
from .models import Profile, Address, CreditCard


# User registration page
def signup(request):
    # If the request is a post, then proceed w/ the form
    if request.method == 'POST':
        form = UserSignUpForm(request.POST)
        # To validate the form
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for { username }.')
            return redirect ('store-home-page')
    # if the request is not a post, then show a blank form
    else:
        # to use the form at signup we create an instance of the form we imported on top:
        form = UserSignUpForm()
    return render(request, 'users/signup.html', {'form': form})

# When the user clicks on the profile menu, he/she will be redirected here
@login_required
def settingsHome(request):
    return redirect('settings:profile-settings')

# Profile page
@login_required
def profile(request):
    if request.method == 'POST':
        user_ProfileForm = UserProfileForm(request.POST, instance=request.user)
        user_BioForm = BioForm(request.POST, instance=request.user.profile)
        user_NicknameForm = NicknameForm(request.POST, instance=request.user.profile)

        if user_ProfileForm.is_valid() and user_BioForm.is_valid() and user_NicknameForm.is_valid():
            user_ProfileForm.save()
            user_BioForm.save()
            user_NicknameForm.save()
            messages.success(request, f'Your profile has been updated successfully')
            return HttpResponseRedirect(request.path_info)
        else:
            messages.warning(request, f'There were some errors updating you profile.')

    else:
        user_ProfileForm = UserProfileForm(instance=request.user)
        user_BioForm = BioForm(instance=request.user.profile)
        user_NicknameForm = NicknameForm(instance=request.user.profile)


    context = {
        'user_ProfileForm': user_ProfileForm,
        'user_BioForm': user_BioForm,
        'user_NicknameForm': user_NicknameForm
    }

    return render(request, 'users/profile.html', context)


# Billing page (credit card and billing address)
@login_required
def billingSettings(request):

    address_slug = None
    primaryAddressCheck = False
    # Get user address list
    user_AddressList = Address.objects.all().filter(user__user__username=request.user)
    user_creditCards = CreditCard.objects.all().filter(user__user__username=request.user)

    for address in user_AddressList:
        if address.primaryAddress == True:
            primaryAddressCheck = True

    context = {
        'user_AddressList': user_AddressList,
        'primaryAddressCheck': primaryAddressCheck,
        'user_creditCards': user_creditCards,
    }

    return render(request, 'users/billing.html', context)


@login_required
def addAddress(request):

    address_slug = None

    if request.method == 'POST':
        user_AddressForm = EditAddressForm(request.POST)

        if user_AddressForm.is_valid():
            newaddress = user_AddressForm.save(commit=False)
            newaddress.user_id = request.user.profile.id
            newaddress.save()

            messages.success(request, f'New address added')
            return redirect('settings:billing-settings')
        else:
            messages.warning(
                request, f'There were some errors updating you profile.')

    else:
        user_AddressForm = EditAddressForm()

    context = {
        'user_AddressForm': user_AddressForm
    }

    return render(request, 'users/addAddress.html', context)


# Page to change user Addresses
@login_required
def addressChange(request, address_slug):

    # Gets name of the address based on id
    currentAddress = Address.objects.all().get(pk=address_slug)

    if request.method == 'POST':
        user_AddressForm = EditAddressForm(request.POST, instance=currentAddress)

        if user_AddressForm.is_valid():
            user_AddressForm.save()
            messages.success(request, f'Your address has been updated successfully')
            return HttpResponseRedirect(request.path_info)
        elif DeleteAddressForm():
            Address.objects.filter(id=address_slug).delete()
            return redirect('settings:billing-settings')
        else:
            messages.warning(request, f'There were some errors updating you profile.')

    else:
        user_AddressForm = EditAddressForm(instance=currentAddress)

    context = {
        'address_slug': address_slug,
        'user_AddressForm': user_AddressForm,
    }
    return render(request, 'users/addressChange.html', context)


@login_required
def addCreditCard(request):

    creditcard_slug = None

    if request.method == 'POST':
        user_CreditCardForm = CreditCardForm(request.POST)

        if user_CreditCardForm.is_valid():
            newcreditcard = user_CreditCardForm.save(commit=False)
            newcreditcard.user_id = request.user.profile.id
            newcreditcard.save()

            messages.success(request, f'New Credit Card added')
            return redirect('settings:billing-settings')
        else:
            messages.warning(
                request, f'There were some errors updating you Credit Card.')

    else:
        user_CreditCardForm = CreditCardForm()

    context = {
        'user_CreditCardForm': user_CreditCardForm
    }

    return render(request, 'users/addCreditCard.html', context)


@login_required
def creditCardChange(request, creditcard_slug):

    # Gets name of the credit card based on id
    currentCreditCard = CreditCard.objects.all().get(pk=creditcard_slug)

    if request.method == 'POST':
        if 'save_changes' in request.POST:  # handle editing form
            user_CreditCardForm = CreditCardForm(request.POST, instance=currentCreditCard)

            if user_CreditCardForm.is_valid():
                user_CreditCardForm.save()
                messages.success(request, f'Your address has been updated successfully')
                return HttpResponseRedirect(request.path_info)

        elif 'delete' in request.POST:  # handle deleting
            currentCreditCard.delete()
            return redirect('settings:billing-settings')

        else:
            messages.warning(
                request, f'There were some errors updating you credit card.')

    else:
        user_CreditCardForm = CreditCardForm(instance=currentCreditCard)

    context = {
        'creditcard_slug': creditcard_slug,
        'user_CreditCardForm': user_CreditCardForm,
    }
    return render(request, 'users/creditCardChange.html', context)


# Username and email form
@login_required
def accountSettings(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)

        if u_form.is_valid():
            u_form.save()
            messages.success(request, f'Your account has been updated successfully')
            return HttpResponseRedirect(request.path_info)
        else:
            messages.warning(request, f'ERROR! Please read below')

    else:
        u_form = UserUpdateForm(instance=request.user)

    context = {
        'u_form': u_form
    }
    return render(request, 'users/account.html', context)


# User password reset page
@login_required
def securitySettings(request):
    if request.method == 'POST':
        u_Passform = PasswordChangeForm(request.user, request.POST)

        if u_Passform.is_valid():
            u_Passform.save()
            # update_session_auth_hash(request, u_Passform)
            update_session_auth_hash(request, u_Passform.user)
            messages.success(request, f'Your password has been updated successfully')
            return HttpResponseRedirect(request.path_info)
        else:
            messages.warning(request, f'ERROR!')

    else:
        u_Passform = PasswordChangeForm(request.user)

    context = {
        'u_Passform': u_Passform
    }
    return render(request, 'users/security.html', context)

