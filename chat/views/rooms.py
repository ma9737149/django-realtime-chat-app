from django.contrib.auth.decorators import login_required
from ..models import Room 
from django.shortcuts import render 
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView , ListView

class RoomDetailView(LoginRequiredMixin , DetailView):
    model = Room
    template_name = "rooms/room.html"
    pk_url_kwarg = "room_id"


class RoomView(LoginRequiredMixin, ListView):
    model = Room
    template_name = "index.html"
    context_object_name = "object_list"