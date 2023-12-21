from django.db.models import Q, Min


class ChatMixin:

    def get_unread(self, user):
        """
        Returns new unread messages count for a given user
        """
        messages = self.messages
        if not messages.exists():
            return 0
        expr = ~Q(owner=user) & Q(seen=False)
        try:
            user_latest = messages.filter(owner=user).values_list(
                'created', flat=True).latest('created')
            expr = Q(created__gt=user_latest) & expr
        except:
            pass
        created = (messages.filter(expr)
                   .aggregate(first=Min('created')).get('first'))
        if not created:
            return 0
        return messages.filter(created__gte=created).count()
