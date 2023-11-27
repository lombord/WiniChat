from django.http import Http404

from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins as MX


from .serializers import MessageSerializer
from ..models import PMessage


class MessageViewSet(MX.RetrieveModelMixin,
                     MX.UpdateModelMixin,
                     MX.DestroyModelMixin,
                     GenericViewSet):
    serializer_class = MessageSerializer
    queryset = PMessage.objects.all()

    def get_object(self):
        msg = super().get_object()
        if not self.request.user.get_chats().contains(msg.chat):
            raise Http404
        return msg
