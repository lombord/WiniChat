"""Chat WebSocket Consumers"""

import asyncio
from functools import wraps
from typing import Iterable

from channels.generic import websocket as WS
from channels.db import database_sync_to_async as DSA


class MyLogger:
    HEADER = "\033[95m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"

    @classmethod
    def warning(cls, msg):
        print(f"{cls.WARNING}Warning:{msg}")

    @classmethod
    def error(cls, msg, prefix="Error"):
        print(f"{cls.FAIL}{prefix}: {msg}")


def exclude_sender(method):
    """
    Decorator to exclude sender
    """

    @wraps(method)
    async def wrapper(self, event: dict):
        # check if sender is not current channel
        if self.channel_name != event.get("channel_name", None):
            return await method(self, event)

    return wrapper


class GroupConsumerMixin:
    """Mixin to handle group related WS events"""

    # group channel layer pattern
    group_layer_p = "group_%s"
    # group ws events pattern
    group_event_p = "grp_%s_evt"

    def __init__(self, *args, **kwargs) -> None:
        # dict to cache connected groups
        self.conn_groups = {}
        super().__init__(*args, **kwargs)

    async def group_handler(self, event: str, **kwargs):
        """
        Base handler for group events
        """
        await getattr(self, self.group_event_p % event)(**kwargs)

    async def grp_created_evt(self, group_id, **kwargs):
        """'Created' event handler, called when group is created

        Args:
            group_id: created group id
        """
        await self.send_session_event("new_chat", self.group_data(group_id))

    async def grp_update_evt(self, group_id, data, **kwargs):
        """'Update' event handler, called when group is edited

        Args:
            group_id: edited group id
            data (dict): changes data
        """
        await self.notify_members(
            group_id, "group_update", {"group_id": group_id, "data": data}
        )

    async def grp_deleted_evt(self, group_id, people, **kwargs):
        """'Deleted' event handler, called when group is deleted

        Args:
            group_id: deleted group id
            people (list[id]): list of people to notify
        """

        await self.notify_users(people, "remove_chat", self.group_data(group_id))

    async def grp_connect_evt(self, group_id, **kwargs):
        """'Connect' event handler, called when channel
        wants to connect to a group

        Args:
            group_id: connecting group
        """

        assert group_id not in self.conn_groups, (
            "You are already connected to group: %s" % group_id
        )

        group = await self.get_group(group_id)
        await self.join_layer(self.group_layer_p % group_id)
        self.conn_groups[group_id] = group
        print("%s connected to group: %s" % (self.user, group_id))

    async def grp_disconnect_evt(self, group_id, **kwargs):
        """'Disconnect' event handler, called when channel wants to
        disconnect from a group

        Args:
            group_id: disconnecting group
        """

        del self.conn_groups[group_id]
        await self.leave_layer(self.group_layer_p % group_id)
        print("%s disconnected from group: %s" % (self.user, group_id))

    def group_data(self, group_id, data=None):
        """Generates group data for user events"""
        return {"type": "group", "chat_id": group_id, "data": data}

    async def grp_invite_evt(self, group_id, members, **kwargs):
        """'Invite' event handler, called when users are invited to a group

        Args:
            group_id: invited group id
            members (list): list of invited members
        """

        cor1 = self.notify_users(
            map(lambda m: m["user"]["id"], members),
            "new_chat",
            self.group_data(group_id),
        )
        cor2 = self.send_group_event(group_id, "new_members", members)
        await asyncio.gather(cor1, cor2)

    async def grp_join_evt(self, group_id, member, **kwargs):
        cor1 = self.notify_user(
            member["user"]["id"], "new_chat", self.group_data(group_id)
        )
        cor2 = self.send_group_event(
            group_id,
            "new_members",
            [member],
            safe=False,
        )
        await asyncio.gather(cor1, cor2)

    def group_leave_tasks(self, group_id, user_id):
        """Common tasks for leaving a group"""
        cor1 = self.notify_user(user_id, "remove_chat", self.group_data(group_id))
        cor2 = self.send_group_event(group_id, "remove_members", [user_id])
        return [cor1, cor2]

    async def grp_leave_evt(self, group_id, user_id, **kwargs):
        """'Leave' event handler, called when user leaves a group

        Args:
            group_id: leaving group id
            user_id: leaving user id
        """

        await asyncio.gather(*self.group_leave_tasks(group_id, user_id))

    async def grp_ban_evt(self, group_id, ban, **kwargs):
        """'Ban' event handler, called when user is banned from a group"""

        tasks = self.group_leave_tasks(group_id, ban["user"]["id"])
        tasks.append(self.send_group_event(group_id, "ban", ban, exclude=False))
        await asyncio.gather(*tasks)

    async def grp_unban_evt(self, group_id, user_id, **kwargs):
        """'Unban' event handler, called when user is unbanned"""

        group = self.conn_groups[group_id]
        tasks = []
        if await DSA(group.has_member)(user_id):
            tasks.append(
                self.notify_user(user_id, "new_chat", self.group_data(group_id))
            )
        tasks.append(self.send_group_event(group_id, "unban", user_id))
        await asyncio.gather(*tasks)

    async def grp_new_role_evt(self, group_id, role, **kwargs):
        """'New Role' event handler, called when new group role is created"""
        await self.send_group_event(group_id, "new_role", role)

    async def grp_role_update_evt(self, group_id, role_id, data, **kwargs):
        """'Role Update' event handler, called when group role is updated"""

        assert role_id and data
        await self.send_group_event(
            group_id, "role_updated", data, extra_data={"role_id": role_id}
        )

    async def grp_role_change_evt(self, group_id, user_id, data, **kwargs):
        """'Role Change' event handler, called when user role is changed"""
        assert user_id and data
        await self.send_group_event(
            group_id, "change_role", data, extra_data={"user_id": user_id}
        )

    async def grp_role_del_evt(self, group_id, role_id, new_role, **kwargs):
        """'Role Delete' event handler, called when group role is deleted"""

        assert role_id and new_role and isinstance(new_role, dict)
        await self.send_group_event(
            group_id,
            "del_role",
            new_role,
            extra_data={"role_id": role_id},
            exclude=False,
        )

    async def grp_send_evt(self, group_id, data, **kwargs):
        """'Send Message' event handler, called when group message is sent"""

        # send new message to group listeners
        cor1 = self.send_group_event(group_id, "new_msg", data.copy())
        cor2 = self.notify_members(
            group_id, "new_msg", self.group_data(group_id, data.copy())
        )
        await asyncio.gather(cor1, cor2)

    async def grp_edit_msg_evt(self, group_id, msg_id, data, **kwargs):
        """'Edit Message' event handler, called when group message is edited"""

        await self.send_group_event(
            group_id, "edit_msg", {"msg_id": msg_id, "data": data}
        )

    async def grp_del_msg_evt(self, group_id, msg_id, **kwargs):
        await self.send_group_event(group_id, "del_msg", {"msg_id": msg_id})

    # Group utility methods
    @DSA
    def get_group(self, group_id):
        """Retrieves group from DB based on group id"""
        return self.user.allowed_groups.get(pk=group_id)

    async def notify_members(
        self, group_id, event: str, data=None, exclude: Iterable = None
    ):
        """Base method to notify group members

        Args:
            group_id: Group id
            event (str): Sending event
            data (Any): Data to send with event. Defaults to None.
            exclude (Iterable, optional): Users to exclude. Defaults to None.
        """
        group = self.conn_groups[group_id]
        qs = group.online_ids
        if exclude:
            qs = qs.exclude(pk__in=exclude)
        members = await DSA(list)(qs)
        await self.notify_users(members, event, data)
        print(f"Notified members:\n{members}")

    def get_group_layer(self, group_id):
        layer = self.group_layer_p % group_id
        # check if user is connected to the group
        assert layer in self.groups
        return layer

    async def send_group_event(
        self,
        group_id,
        event: str,
        data=None,
        exclude=True,
        safe=True,
        extra_data=None,
        **kwargs,
    ):
        """Base method to send group events to group's channel layer members.

        Args:
            group_id: Group id
            event (str): Sending event
            data (Any, optional): Sending data. Defaults to None.
            exclude (bool, optional): Exclude sender?. Defaults to True.
            safe (bool, optional): Is it safe sending?. Defaults to True.
            extra_data (Any, optional): Extra data to send. Defaults to None.
        """
        layer = self.group_layer_p % group_id
        if safe:
            # check if user is connected to group
            assert layer in self.groups

        data = {"group_id": group_id, "data": data}
        if extra_data:
            data.update(extra_data)
        await self.send_event(layer, "group", event, data, exclude=exclude, **kwargs)


class ChatConsumerMixin:
    """
    Mixin to handler Private Chat related WS events
    """

    # private chat channel layer pattern
    chat_layer_p = "chat_%s"
    # private chat events pattern
    chat_event_p = "chat_%s_event"

    def __init__(self, *args, **kwargs) -> None:
        # dict to cache connected chats
        self.conn_chats = {}
        super().__init__(*args, **kwargs)

    async def chat_handler(self, event: str, **kwargs):
        """
        Base handler for chat events
        """
        await getattr(self, self.chat_event_p % event)(**kwargs)

    # Chat event handlers
    async def chat_connect_event(self, chat_id, **kwargs):
        """
        'Connect' event handler, called when channel wants to
        connect to a chat

        Args:
            chat_id: connecting chat id
        """
        assert chat_id not in self.conn_chats, (
            "You are already connected to chat: %s" % chat_id
        )

        chat = await self.get_chat(chat_id)
        await self.join_layer(self.chat_layer_p % chat_id)
        self.conn_chats[chat_id] = chat
        print("%s connected to chat: %s" % (self.user, chat_id))

    async def chat_disconnect_event(self, chat_id, **kwargs):
        """
        'Disconnect' event handler, called when channel wants to
        disconnect from a chat

        Args:
            chat_id: disconnecting chat id
        """

        del self.conn_chats[chat_id]
        await self.leave_layer(self.chat_layer_p % chat_id)
        print("%s disconnected from chat: %s" % (self.user, chat_id))

    async def chat_send_event(self, chat_id, data: dict, **kwargs):
        """
        'Send' event handler, called when chat message is sent

        Args:
            chat_id: Chat ids
            data (dict): Message data
        """
        # send data to all sessions that are connected to the chat
        cor1 = self.send_chat_event(chat_id, "%s:new" % chat_id, data.copy())

        # notify companion incase they haven't joint the chat yet
        cor2 = self.notify_companion(
            chat_id,
            "new_msg",
            {"type": "chat", "chat_id": chat_id, "data": data.copy()},
        )
        await asyncio.gather(cor1, cor2)

    async def chat_new_event(self, chat_id, **kwargs):
        """
        'New' event called, when new chat is created

        Args:
            chat_id: created chat id
        """

        await self.notify_companion(
            chat_id, "new_chat", {"type": "chat", "chat_id": chat_id}
        )

    async def chat_edit_msg_event(self, chat_id, msg_id, data, **kwargs):
        """
        'Edit Message' event called, when chat messages is edited

        Args:
            chat_id: Chat id
            msg_id (int): Edited message id
            data (dict): Edited data
        """

        await self.send_chat_event(
            chat_id, "%s:update" % chat_id, {"msg_id": msg_id, "data": data}
        )

    async def chat_del_msg_event(self, chat_id, msg_id, **kwargs):
        """
        'Delete Message' event called, when chat messages is deleted

        Args:
            chat_id: Chat id
            msg_id (int): Deleted message id
        """

        await self.send_chat_event(chat_id, "%s:delete" % chat_id, {"msg_id": msg_id})

    # chat utility methods
    @DSA
    def get_chat(self, chat_id):
        """Retrieves chat from DB based on chat id"""
        return self.user.get_chats().get(pk=chat_id)

    def get_chat_layer(self, chat_id):
        """Get chat channel layer based on chat id"""

        group = self.chat_layer_p % chat_id
        # check if user is in a group
        assert group in self.groups
        return group

    async def notify_companion(self, chat_id, event: str, data=None):
        """
        Notifies companion based on chat id
        """
        chat = self.conn_chats.get(chat_id)
        if not chat:
            chat = await self.get_chat(chat_id)
        await self.notify_users(chat.get_members_id(), event, data)

    async def send_chat_event(
        self, chat_id, event: str, data=None, exclude=True, **kwargs
    ):
        """Base private chat event sender

        Args:
            chat_id: Chat id
            event (str): Sending event
            data (_type_, optional): Sending data. Defaults to None.
            exclude (bool, optional): Exclude sender?. Defaults to True.
        """
        group = self.get_chat_layer(chat_id)
        await self.send_event(group, "chat", event, data, exclude=exclude, **kwargs)


class UserConsumerMixin:
    """
    Mixin to handle user related WS events
    """

    # user sessions channel layer pattern
    user_layer_p = "user_%s"

    # user observers channel layer pattern
    watch_layer_p = "watch_%s"

    # user related events pattern
    user_event_p = "user_%s_event"

    async def user_handler(self, event: str, **kwargs):
        """Base user related event handler"""
        await getattr(self, self.user_event_p % event)(**kwargs)

    async def user_watch_event(self, user_id, **kwargs):
        """
        Called to track user
        """
        await self.join_layer(self.watch_layer_p % user_id)

    async def user_leave_event(self, user_id, **kwargs):
        """
        Called to untrack user
        """
        await self.leave_layer(self.watch_layer_p % user_id)

    async def user_edit_event(self, data: dict, **kwargs):
        """
        Called when user profile is updated
        """
        await self.send_watch_event("profile_edited", data)

    async def notify_user(self, user_id, event: str, data=None):
        """Base method to notify user

        Args:
            user_id: user's id to notify
            event (str): Notification event
            data (_type_, optional): Notification data. Defaults to None.
        """
        group = self.user_layer_p % user_id
        await self.send_event(group, "user", event, data, exclude=True)

    async def send_session_event(self, event: str, data=None):
        """Base method to send session related events"""
        await self.send_event(self.user_g, "user", event, data, exclude=True)

    async def notify_users(self, users, event, data=None):
        """Method to notify list of users[id] with given event and data"""

        await asyncio.gather(
            *(self.notify_user(user_id, event, data) for user_id in users)
        )

    @DSA
    def get_sessions_count(self):
        """
        Gets the number of online sessions.
        Currently works only with 'InMemoryStorage' class
        """
        self.user.refresh_from_db(fields=["status"])
        return self.user.status

    async def send_watch_event(self, event: str, data=None):
        """Base method to send watch events"""
        data = {"user_id": self.user.pk, "data": data}
        await self.send_event(self.watch_g, "user", event, data, exclude=True)

    def set_user_groups(self):
        """
        Sets base user channel layer groups
        """
        pk = self.user.pk
        # group for user sessions
        self.user_g = self.user_layer_p % pk
        # group for user listeners
        self.watch_g = self.watch_layer_p % pk
        self.groups = {self.user_g, self.watch_g}


class SessionConsumer(
    UserConsumerMixin,
    ChatConsumerMixin,
    GroupConsumerMixin,
    WS.AsyncJsonWebsocketConsumer,
):
    """
    Base session consumer that includes all types of server WS event handlers.
    """

    # Connected channels count
    __connected = 0
    # Base event handler pattern
    handler_p = "%s_handler"

    async def websocket_connect(self, message):
        """
        Stores user and sets up user channel layer groups
        """
        self.user = self.scope.get("user")
        self.set_user_groups()
        return await super().websocket_connect(message)

    async def connect(self):
        """
        Accepts connection and updates user status
        """
        await self.accept()
        type(self).__connected += 1
        print(
            "Session %r is connected" % self.channel_name,
            "All connections: %d" % self.__connected,
            sep="\n",
        )
        status = await self.get_sessions_count()
        if not status:
            await self.send_watch_event("joint")
        await DSA(self.user.update_status)(1)
        print("Connected to %s" % self.user)

    async def disconnect(self, code):
        """
        Updates user status and notifies user watchers before disconnect
        """
        status = await self.get_sessions_count()
        if status <= 1:
            await self.send_watch_event("left")
        await DSA(self.user.update_status)(-1)
        type(self).__connected -= 1
        print(
            "Disconnected from %s" % self.user,
            "All connections: %d" % self.__connected,
            sep="\n",
        )

    async def receive_json(self, content: dict, **kwargs):
        """
        Base json message event handler.
        Calls base event handler of received event if it exists
        """
        try:
            e_type = content.pop("event_type")
            await getattr(self, self.handler_p % e_type)(**content, **kwargs)
        except Exception as e:
            MyLogger.error(e, prefix="WS Error")

    async def send_event(
        self, group: str, event_type: str, event: str, data=None, **kwargs
    ):
        """
        Base event-send method
        Args:
            group (str): group channel layer to send event
            event_type (str): Base event type (user, chat, etc.)
            event (str): event name
            data (dict, optional): Sending data. Defaults to None.
        """
        data = {"event_type": event_type, "event": event, "data": data}
        await self.send_all(group, data, **kwargs)

    async def join_layer(self, group: str):
        """
        Base method to join channel layer
        """
        self.groups.add(group)
        await self.channel_layer.group_add(group, self.channel_name)

    async def leave_layer(self, group):
        """
        Base method to leave channel layer
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
        Base send-channel-layer method
        Args:
            group (str): channel layer to send event
            data (dict): data to send
            exclude (bool, optional): if true excludes sender.
            Defaults to False.
        """
        type_ = "send.json"
        if exclude:
            type_ = "send.exclude"
            data["channel_name"] = self.channel_name
        data.setdefault("type", type_)
        await self.channel_layer.group_send(group, data)
