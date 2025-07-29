from ..models import Room 
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView , ListView  , CreateView
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.urls import reverse_lazy

class RoomDetailView(LoginRequiredMixin , DetailView):
    model = Room
    template_name = "rooms/room.html"
    pk_url_kwarg = "room_id"


class RoomView(LoginRequiredMixin, ListView):
    model = Room
    template_name = "index.html"
    context_object_name = "object_list"


class RoomCreateView(CreateView):
    model = Room
    fields = ['room_name', 'room_description']
    template_name = 'rooms/add_room.html'
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        form.instance.room_author = self.request.user
        response = super().form_valid(form)

        channel_layer = get_channel_layer()
        room_data = {
            "id": self.object.id,
            "room_name": self.object.room_name,
            "room_description": self.object.room_description,
            "room_author": self.object.room_author.username,
            "created_at": self.object.created_at.strftime("%Y-%m-%d %H:%M"),
        }
        async_to_sync(channel_layer.group_send)(
            "rooms",
            {
                "type": "room.created",
                "room": room_data,
            }
        )
        return response

