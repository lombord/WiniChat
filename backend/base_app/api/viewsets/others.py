from django.http import Http404
from django.db.models import Q

from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins as MX

from ...models import PMessage
from ..serializers import MessageSerializer


class MessageViewSet(
    MX.RetrieveModelMixin, MX.UpdateModelMixin, MX.DestroyModelMixin, GenericViewSet
):
    """Private chat message ViewSet"""
    
    serializer_class = MessageSerializer

    def get_queryset(self):
        if self.request.method == "DELETE":
            return PMessage.objects.all()
        return PMessage.objects.common_fetch()

    def get_object(self):
        msg = super().get_object()
        if not self.request.user.get_chats().contains(msg.chat):
            raise Http404()
        return msg

    def perform_update(self, serializer: MessageSerializer):
        v_data = serializer.validated_data
        if len(v_data) == 1 and "seen" in v_data:
            msg = serializer.instance
            expr = (
                ~Q(owner=self.request.user)
                & Q(created__lte=msg.created)
                & Q(seen=False)
            )
            msg.chat.messages.filter(expr).update(seen=True)
            msg.seen = True
            return msg
        return serializer.save()
