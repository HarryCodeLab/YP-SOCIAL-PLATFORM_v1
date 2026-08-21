# YP Connect 🇨🇲

YP Social Platform or simply YP CONNECT is a social platform created to help Young Presbyterians (YPs) connect, communicate, encourage one another, and grow together in their faith.

The idea behind YP Connect came from a simple observation: young people spend a lot of time online, but much of that time can disappear into endless scrolling without creating meaningful connections. I wanted to create a place where YPs could open an app on a boring weekend and actually find something useful, encouraging, and enjoyable to do.

The platform is designed around the Young Presbyterian community. Members can interact through posts and comments, watch videos, participate in goals and challenges, track their progress, and eventually have more opportunities to communicate and support one another across congregations.

---

## 💡 The Problem

Young Presbyterian groups have communities full of ideas, conversations, activities, Bible studies, challenges, and people who want to encourage each other. However, these interactions can become scattered across different platforms and messaging groups.

Important announcements can get buried. Discussions can disappear into chat histories. Members from different congregations may have very few opportunities to interact with each other online.

At the same time, young people already spend a significant amount of time on social media. Instead of creating another platform designed purely around entertainment, I wanted to create a platform where social interaction could also encourage faith, learning, participation, and community.

This led to the idea of YP Connect.

---

## 🚀 The Solution

YP Connect brings several community-focused features into one platform.

Users can create posts and interact with other members through comments. The platform also includes goals and a progress dashboard so users can keep track of their progress on theit goals.

Video content can be shared with the community, with comments allowing users to discuss the content rather than simply watching it.

The long-term vision is to make YP Connect a place where YP members from different congregations can meet, participate in Bible challenges, prepare for rallies, share ideas, encourage one another, and make prayer requests.

The goal is not to simply build another social media platform. The goal is to build a community.

---

## 🛠️ Technologies Used

YP Connect is primarily built with Python and Flask on the backend, with HTML, CSS, and JavaScript used for the web interface.

### Backend
- Python
- Flask
- Flask-SocketIO
- PyMongo
- MongoDB Atlas

### Frontend
- HTML
- CSS
- JavaScript

### Other Services
- Cloudinary for planned image storage and media management
- Internet Archive for video storage
- Render for web deployment

---

## 📱 Building on Android

One of the most unusual parts of this project is that much of the development was done directly from an Android phone.

I use **Pydroid 3** as my Python development environment. Pydroid 3 allows Python programs to be written and executed on Android, making it possible for me to develop the Flask application without needing a real computer.

I also use **Termux**, an Android terminal environment that provides a Linux-like command-line environment. During development, I used Termux to experiment with MongoDB and run a local MongoDB server while learning how databases and applications communicate.

This setup was not always easy, but it allowed me to learn and build using the hardware I had available.

---

## 🧩 Challenges During Development

Building YP Connect has involved many challenges.

One of the first major challenges was learning how different parts of a web application communicate with each other. I had to learn HTML and JavaScript while simultaneously building the Flask backend. At first, even simple things such as displaying comments or connecting a form to a Flask route could be confusing.

Database connectivity was another major challenge. I experimented with MongoDB, PyMongo, Flask-PyMongo, MongoDB Atlas, and a local MongoDB server hosted through Termux. There were connection problems, DNS issues, and configuration errors that required a lot of debugging.

Another major problem involved posts and synchronization. Initially, users sometimes had to synchronize before seeing new posts, and synchronization could cause posts to appear more than once. Learning Socket.IO helped solve this problem by allowing the application to communicate with users in real time. After implementing Socket.IO, posts and comments became much more stable.

Deployment introduced another set of challenges. The application worked locally, but getting it running on the web required understanding environment variables, production configuration, database connections, and server behavior. I also had to learn that development settings such as Flask's debug mode should not simply be carried into production.

Profile pictures presented another challenge. I initially experimented with storing image URLs and local static files before deciding that a cloud-based solution such as Cloudinary would be more appropriate once the platform has more real users.

---

## 🔐 Security and Configuration

Sensitive credentials are kept outside the source code using environment variables.

The project uses a .env file during local development for secrets such as database credentials and API keys. The .env file is not intended to be committed to GitHub.

In production, environment variables are configured through the hosting platform instead of being stored directly in the repository.

---

## 🌱 Current Status

YP Connect is currently deployed on the web and is being tested by real users.

The project has reached its first **5 users**, which is an important milestone because the platform is no longer being tested only by its developer.

The current focus is on improving the user interface, fixing bugs discovered through real-world use, collecting feedback, and preparing the platform for wider testing.

---

## 🔮 Future Plans

Future development may include:

- More community interaction features
- Better profile customization
- Cloud-based profile pictures
- More Bible challenges
- Prayer request features
- Rally study resources
- Improved notifications
- Better administration tools
- Android and IOS packaging using Capacitor
- Expansion to more congregations
- More tools for YP groups across Cameroon

The long-term goal is to make YP Connect useful beyond a single congregation and allow YP members from different parts of Cameroon to connect with one another.

---

## ❤️ Why I Built It

YP Connect started as a project, but I don't want it to remain just another teenager's coding project sitting on GitHub.

I want it to become something people actually use.

I want a YP member to be able to open YP Connect on a boring weekend, find a Bible challenge, see what other members are talking about, watch something interesting, complete a goal, encourage someone, or simply feel connected to the wider YP community.

The goal is simple:

<<< Build technology that brings people together instead of simply giving them something else to scroll through. >>>

---

## 👨‍💻 About the Developer

YP Connect is being developed by a young developer from Cameroon who is learning software development by building real projects.

Rather than following only tutorials, this project has been an opportunity to learn Python, Flask, databases, JavaScript, Socket.IO, deployment, APIs, cloud services, and application design through solving real problems.

The project is still growing, and feedback from users is an important part of deciding what comes next.

---

## 📜 Project Status

YP Connect is currently live on the web at "https://yp-connect.onrender.com" and undergoing testing with its first users.
Every bug, suggestion, and piece of feedback helps shape the next version.

Thanks for reading.            
           
Harry Code Lab /<build with purpose/>
