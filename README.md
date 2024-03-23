
# WiniChat

![Overview dark theme](/Screenshots/1.png?raw=true)
### [Live Demo](https://winichat.duckdns.org/chat/)

WiniChat is a Real-Time SPA chat app which was inspired by `Telegram` and `Discord`. It implements communication through `private`(DM) and `group` chats with the ability to share `media files` such as photo, audio and video.


#### SPA logic
As mentioned above app is fully `SPA` and to implement that I've used [Vite.js](https://vitejs.dev/) with [Vue.js](https://vuejs.org/) for frontend and [Django](https://docs.djangoproject.com/en/5.0/) along with [DRF](https://www.django-rest-framework.org/) for backend server. Authentication of users is based on `JWT` tokens where user authenticates only once and token will be automatically updated as user uses the app.

#### Real-time logic

`Real-time` communication was implemented using [WebSockets](https://en.wikipedia.org/wiki/WebSocket) protocol.
I've used standard [WebSockets API](https://developer.mozilla.org/en-US/docs/Web/API/WebSocket) for frontend and [django-channels](https://channels.readthedocs.io/en/latest/) for backend.
Communication between servers is based on event-driven logic which was inspired by [socket.io](https://socket.io/).

#### Private Chats
Private chats mostly was inspired by Telegram and has most of its features like sending, deleting, editing messages as well as seen flag. Users can also send photo, audio, video files that they can view, listen and watch using apps custom media players.

#### Groups
Groups have all the features of private chats and are the key feature of app. Their logic is based on `Discord` servers and `Telegram` groups. Users can create two types of groups:

- `Private` - pretty similar to Telegram groups with user roles where each role has it's own permissions and priority.
- `Public` - have same features as private groups and unique identifier which is used to find the group.

After creation they can invite people to the group, change members role, create new roles, ban/unban/kick members, edit group's info(name, photo, description and etc.) as well as it's type. All group actions occur in real time and will be visible to all group members.

### Backstory
Originally I started this project as my final project for my course of Python/Django about 3 months ago. I couldn't decide what topic to choose and eventually came to this idea. I always liked the way messengers work and was interested in implementing them myself. By the end the course I was able to finish only private chats but really wanted to try to implement groups as well so after 1.5 month i was able to finish them too. 
When I started I didn't have an idea of WebSockets and had just started working with REST API so I've learnt a lot by doing this project.
It was a long journey and fun at the same time.


### Future Plans
In this year I'm planning to keep working on this project adding more features, improve core logics and eventually host it when its ready. Honestly I'm really excited and do really hope that this will eventually become a real app that people(at least my friends😃) use on daily basis.

## 🛠️ Used technologies

### 🌐 Backend:
- Django
- Django Rest Framework
- Django Channels


### 🖥️ Frontend:
- Vite
- Vue.js
- Tailwindcss
- Daisyui(mainly for theme)

### 📊 DataBase:
- PostgreSQL



## Update 3/23/2024

- Added SSL certification
- Fixed some bugs

## Update 3/18/2024

- Added Live Demo
- Created docker images for each application
- Fixed bugs and set up the project for deployment
