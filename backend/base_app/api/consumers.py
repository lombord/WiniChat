from functools import wraps
from channels.generic import websocket as WS
from channels.db import database_sync_to_async as DSA


def exclude_sender(method):
    """
    Decorator to exclude sender
    """
    @wraps(method)
    async def wrapper(self, event: dict):
        # event should contain channel_name to check sender
        if self.channel_name != event.pop('channel_name', None):
            return await method(self, event)
    return wrapper


class ChatConsumerMixin:
    """
    Base Chat consumer mixin to control chat related events.
    """

    # chat group pattern
    chat_p = "chat_%s"

    def __init__(self, *args, **kwargs) -> None:
        # dict to cache joint chats
        self.joint_chats = {}
        super().__init__(*args, **kwargs)

    async def send_chat(self, chat_id, data: dict):
        """
        Controls send_chat event.
        Sends a data if user has joint the chat
        Args:
            chat_id (_type_): chat_id to send a data
            data (dict): data to send
        """

        group = self.chat_p % chat_id
        # check if user is in the group
        assert group in self.groups

        # send data to all sessions that are connected to the chat
        await self.send_chat_event(group, '%s_message' % chat_id,
                                   data.copy(), exclude=True)

        # notify companion incase they haven't joint the chat yet
        await self.notify_companion(chat_id, "last_message",
                                    data.copy())

    async def new_chat(self, chat_id, **kwargs):
        await self.notify_companion(chat_id, "new_chat", {'chat_id': chat_id})

    async def notify_companion(self, chat_id, event: str, data: dict):
        """
        Notifies companion for given chat
        Args:
            chat_id (_type_): chat to get companion from
            event (str): event name to send
            data (dict): data to send with event
        """
        chat = self.joint_chats.get(chat_id)
        if not chat:
            chat = await self.get_chat(chat_id)
        comp_id = chat.get_companion_id(self.user.pk)
        group = self.user_p % comp_id
        await self.send_chat_event(group, event, data)

    async def join_chat(self, chat_id, **kwargs):
        """
        Join a chat if user hasn't joint yet
        Args:
            chat_id (Any): chat to join
        """
        assert chat_id not in self.joint_chats

        chat = await self.get_chat(chat_id)
        await self.join_layer(self.chat_p % chat_id)
        self.joint_chats[chat_id] = chat
        print("%s joint the chat: %s" % (self.user, chat_id))

    async def leave_chat(self, chat_id, **kwargs):
        """
        Leave a chat if user is in it
        Args:
            chat_id (Any): chat to join
        """
        del self.joint_chats[chat_id]
        await self.leave_layer(self.chat_p % chat_id)
        print("%s left the chat: %s" % (self.user, chat_id))

    @DSA
    def get_chat(self, chat_id):
        return self.user.get_chats().get(pk=chat_id)

    async def send_chat_event(self, group: str, event: str,
                              data: dict = None, **kwargs):
        """
        Base send for chat events
        Args:
            group (str): Group name to send an event 
            event (str): Event name
            data (dict, optional): Data to send with an event.
            Defaults to None.
        """
        await self.send_event(group, 'chat', event, data,
                              **kwargs)


class SessionConsumer(ChatConsumerMixin, WS.AsyncJsonWebsocketConsumer):
    """
    Base session consumer to interact with server.
    """

    # sessions group pattern
    user_p = "user_%s"
    # pattern for listeners of a user
    watch_p = "watch_%s"

    async def websocket_connect(self, message):
        """
        Stores user and sets groups
        """
        self.user = self.scope.get('user')
        self.set_groups()
        return await super().websocket_connect(message)

    def set_groups(self):
        """
        Sets base user groups
        """
        pk = self.user.pk
        # group for user sessions
        self.user_g = self.user_p % pk
        # group for user listeners
        self.watch_g = self.watch_p % pk
        self.groups = {self.user_g}

    async def connect(self):
        """
        Accepts connection and updates user status
        """
        await self.accept()
        await self.update_status()
        print('Connected to %s' % self.user)

    async def receive_json(self, content: dict, **kwargs):
        """
        Controls incoming messages and calls event handler
        for that message
        """
        try:
            await getattr(self, content.pop('event'))(**content, **kwargs)
        except Exception as e:
            print(e)

    async def user_edit(self, data: dict, **kwargs):
        """Session profile edit event controller.
        Sends all changes to listeners
        Args:
            data (dict): user profile changes
        """
        await self.send_watch_event("%s_edit", data)

    async def watch_user(self, user_id, **kwargs):
        """
        Used to track events of a user
        """
        await self.join_layer(self.watch_p % user_id)

    async def leave_user(self, user_id, **kwargs):
        """
        Used to stop tracking events of a user
        """
        await self.leave_layer(self.watch_p % user_id)

    async def disconnect(self, code):
        """
        Updates user status before disconnect
        """
        await self.update_status()
        print('Disconnected from %s' % self.user)

    async def update_status(self):
        """
        Updates user status in database.
        if user has just joint sends listeners user_joint
        event.
        if user has completely left and there is no more online
        sessions sends user_left event to listeners
        """
        cnt = self.get_sessions_count()
        if cnt <= 1:
            if cnt:
                event = "%s_joint"
            else:
                event = "%s_left"
            await self.send_watch_event(event)
        await DSA(self.user.update_status)(cnt)

    async def send_watch_event(self, event: str, data: dict = None):
        """
        Sends event to user listeners with given data
        Args:
            event (str): event name
            data (dict, optional): Data to send with event. Defaults to None.
        """
        event = event % self.user.pk
        await self.send_event(self.watch_g, 'user', event, data)

    async def send_event(self, group: str, event_type: str,
                         event: str, data: dict = None,
                         **kwargs):
        """
        Base event-send method
        Args:
            group (str): group name to send event
            event_type (str): type of event (user, chat, etc.)
            event (str): event name
            data (dict, optional): Data to send with event. Defaults to None.
        """
        data = {'event_type': event_type,
                'event': event,
                'data': data}
        await self.send_all(group, data, **kwargs)

    async def join_layer(self, group: str):
        """
        Base method to join a group
        Args:
            group (str): group name to join. 
        """
        self.groups.add(group)
        await self.channel_layer.group_add(group, self.channel_name)

    async def leave_layer(self, group):
        """
        Base method to leave a group
        Args:
            group (str): group name to leave. 
        """
        self.groups.remove(group)
        await self.channel_layer.group_discard(group, self.channel_name)

    @exclude_sender
    async def send_exclude(self, data):
        """
        Base send method that excludes a sender
        """
        await self.send_json(data)

    async def send_all(self, group: str, data: dict, *, exclude=False):
        """
        Base send-group method
        Args:
            group (str): group name to send data
            data (dict): data to send
            exclude (bool, optional): if True sender. Defaults to False.
        """
        type_ = 'send.json'
        if exclude:
            type_ = 'send.exclude'
            data['channel_name'] = self.channel_name
        data.setdefault('type', type_)
        await self.channel_layer.group_send(group, data)

    def get_sessions_count(self):
        """
        Gets the number of online sessions.
        Currently works with only 'InMemoryStorage' class
        """
        sessions = self.channel_layer.groups.get(self.user_g, [])
        return len(sessions)
