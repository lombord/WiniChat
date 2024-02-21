from rest_framework.pagination import LimitOffsetPagination
from rest_framework.utils.urls import replace_query_param


class ChatLimitPagination(LimitOffsetPagination):
    default_limit = 30

    def get_previous_link(self):
        url = super().get_previous_link()
        try:
            assert url and self.offset
            if self.offset - self.limit <= 0:
                return replace_query_param(url, self.limit_query_param, self.offset)
        except Exception:
            pass
        return url
