from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Profile
from .forms import ProfileUpdateForm


@login_required()
def profile(request, template_name='account/custom_users/profile.html'):
    return render(request, template_name)

@login_required()
def profile_edit(request, template_name='account/custom_users/profile_edit.html'):
    existing_profile = get_object_or_404(Profile, user=request.user)
    profile_form = ProfileUpdateForm(instance=existing_profile)

    if request.method == 'POST':
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=existing_profile)

        if profile_form.is_valid():
            profile = profile_form.save(commit=False)
            profile.user = request.user
            profile.save()
            messages.success(request, 'Profile Updated for {}'.format(request.user.username), extra_tags='html_safe')
            # return redirect('custom_users:profile')
            return redirect('home')

    context = {
        'profile_form': profile_form,
        'existing_profile': existing_profile,
        }

    return render(request, template_name, context)





