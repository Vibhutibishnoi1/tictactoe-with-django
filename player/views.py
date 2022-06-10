from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied

from django.views.generic import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy

from .forms import InvitationForm
from .models import Invitation
from gameplay.models import Game

# Create your views here.

@login_required
def home(request):
    #games_first_player=Game.objects.filter(first_player = request.user, status='F')
    #games_second_player=Game.objects.filter(first_player = request.user, status='S')
    #all_my_games=list(games_first_player) + list(games_second_player)
    #replacing the above code with the code below

    my_games=Game.objects.games_for_user(request.user)
    active_games = my_games.active()
    finished_games= my_games.difference(active_games)
    invitations=request.user.invitations_received.all()

    return render(request,"player/home.html", {'active_games' : active_games, 'finished_games': finished_games, 'invitations': invitations})


@login_required
def new_invitation(request):
    if request.method=="POST":
        invitation= Invitation(from_user=request.user)
        form=InvitationForm(instance=invitation, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('player_home')
    else:
        form=InvitationForm()
    return render(request, "player/new_invitation_form.html", {'form': form})    


@login_required
def accept_invitation(request,id):
    invitation= get_object_or_404(Invitation, pk=id)
    if not request.user==invitation.to_user:
        raise PermissionDenied
    if request.method=="POST":
        if "accept" in request.POST :
            game=Game.objects.create(first_player=invitation.to_user, second_player=invitation.from_user)  
        invitation.delete()
        return redirect(game)     
    else:
        return render(request, "player/accept_invitation_form.html", {'invitation': invitation})    

#exercise: find a way to trigger 404 error and permissiondenied error in the browser from accept_invitation page to verify both work correctly        


class SignUpView(CreateView):
    form_class=UserCreationForm
    template_name: str="player/signup_form.html"
    success_url=reverse_lazy('player_home')