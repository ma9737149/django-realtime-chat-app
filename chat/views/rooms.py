from django.contrib.auth.decorators import login_required
from ..models import Room 
from django.shortcuts import render 
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView

class RoomDetailView(LoginRequiredMixin , DetailView):
    model = Room
    template_name = "rooms/room.html"
    pk_url_kwarg = "room_id"


@login_required
def index(request):
    return render(request , 'index.html')