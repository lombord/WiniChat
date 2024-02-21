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
        bio = fake.sentence(nb_words=rr(10, 15))
        user = User(username=username, email=email,
                    first_name=first, last_name=last,
                    bio=bio)
        user.set_password(pwd)
        try:
            user.full_clean()
        except Exception as e:
            continue
        user.save()


def generate_messages(chat: PChat, n: int):
    users = [chat.from_user, chat.to_user]
    for _ in range(n):
        owner = choice(users)
        msg = fake.sentence(nb_words=rr(20, 60))
        PMessage.objects.create(owner=owner, chat=chat, content=msg)


def generate_chats():
    people = User.objects.all()
    for p1 in people:
        for p2 in people.order_by('?')[:rr(10, 20)]:
            try:
                chat = PChat.objects.create(from_user=p1, to_user=p2)
                generate_messages(chat, rr(4, 30))
            except Exception as e:
                pass
