"""
Module to generate users
"""

from re import compile
from faker import Faker

from random import choice, randrange as rr
from base_app.models import PMessage, User, PChat


fake = Faker()


def generate_users(n: int):
    pattern = compile(r'[^\w\d]+')
    pwd = '2I1^oW0NGV&i'
    for _ in range(n):
        name = fake.unique.name()
        first, last = name.split(maxsplit=1)
        username = pattern.sub('', name.lower())
        email = f"{username}@gmail.com"
        user = User(username=username, email=email,
                    first_name=first, last_name=last)
        user.set_password(pwd)
        user.save()


def generate_messages(chat: PChat, n: int):
    users = [chat.from_user, chat.to_user]
    for _ in range(n):
        owner = choice(users)
        msg = fake.sentence(nb_words=rr(2, 50))
        PMessage.objects.create(owner=owner, chat=chat, content=msg)


def generate_chats():
    people = User.objects.all()
    for p1 in people:
        for p2 in people.order_by('?')[:rr(3, 15)]:
            try:
                chat = PChat.objects.create(from_user=p1, to_user=p2)
                generate_messages(chat, rr(4, 30))
            except:
                pass
