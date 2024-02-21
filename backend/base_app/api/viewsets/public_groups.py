from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet

from ...models import Group

from ..serializers import GroupSerializer, MemberSerializer, PublicGroupSerializer


class PGroupViewSet(ReadOnlyModelViewSet):
    serializer_class = PublicGroupSerializer
    lookup_field = "pk"
    lookup_url_kwarg = "group_pk"
    root_obj_name = "group"

    def get_queryset(self):
        user = self.request.user
        if self.request.method == "PUT":
            return Group.objects.search_groups("", user).prefetch_latest()
        query = self.request.GET.get("q")
        return Group.objects.search_groups(query, user)

    def update(self, request, *args, **kwargs):
        group = self.get_object()
        role = group.default_role
        member = group.members.create(user=request.user, role=role)
        context = self.get_serializer_context()
        grp_data = GroupSerializer(instance=group, context=context).data
        mem_data = MemberSerializer(instance=member, context=context).data
        return Response({"group": grp_data, "member": mem_data})
