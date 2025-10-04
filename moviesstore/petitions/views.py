from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Petition
from .forms import PetitionForm

from django.db import models

def petition_list(request):
    petitions = Petition.objects.annotate(vote_count=models.Count('votes')).order_by('-vote_count', '-created_at')
    if request.method == 'POST':
        form = PetitionForm(request.POST)
        if form.is_valid():
            petition = form.save(commit=False)
            # If you want to associate the petition with the submitting user, uncomment the next line
            # petition.user = request.user
            petition.save()
            return redirect('petition_list')
    else:
        form = PetitionForm()
    return render(request, 'petitions/petition_list.html', {'petitions': petitions, 'form': form})


@login_required
def vote_petition(request, petition_id):
    petition = get_object_or_404(Petition, id=petition_id)
    if request.user not in petition.votes.all():
        petition.votes.add(request.user)
    return redirect('petition_list')
