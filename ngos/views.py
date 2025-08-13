from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import NGOProfile
from .forms import NGOProfileForm

@login_required
def ngo_profile(request):
    try:
        ngo_profile = NGOProfile.objects.get(user=request.user)
        is_new = False
    except NGOProfile.DoesNotExist:
        ngo_profile = None
        is_new = True
    
    if request.method == 'POST':
        form = NGOProfileForm(request.POST, instance=ngo_profile)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            messages.success(request, 'NGO profile updated successfully!')
            return redirect('ngo_profile')
    else:
        form = NGOProfileForm(instance=ngo_profile)
    
    return render(request, 'ngos/ngo_profile.html', {
        'form': form,
        'ngo_profile': ngo_profile,
        'is_new': is_new
    })

def ngo_list(request):
    ngos = NGOProfile.objects.filter(is_verified=True).order_by('organization_name')
    return render(request, 'ngos/ngo_list.html', {'ngos': ngos})

def ngo_detail(request, pk):
    ngo = get_object_or_404(NGOProfile, pk=pk)
    return render(request, 'ngos/ngo_detail.html', {'ngo': ngo})
