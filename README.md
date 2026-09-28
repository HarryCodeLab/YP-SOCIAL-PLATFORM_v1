# YP Connect 🇨🇲

YP Social Platform or simply YP CONNECT is a social platform created to help Young Presbyterians (YPs) connect, communicate, encourage one another, and grow together in their faith.

The idea behind YP Connect came from a simple observation: young people spend a lot of time online, but much of that time can disappear into endless scrolling without creating meaningful connection. Many people are active online, yet they still feel isolated, uninspired, and disconnected from the people and communities that matter to them.

The platform is designed around the Young Presbyterian community. Members can interact through posts and comments, watch videos, participate in goals and challenges, track their progress, and engage in a more purposeful digital space built around encouragement, growth, and community.

---

## 💡 The Problem

Young Presbyterian groups have communities full of ideas, conversations, activities, Bible studies, challenges, and people who want to encourage each other. However, these interactions can become fragmented. Important announcements can get buried. Discussions can disappear into chat histories. Members from different congregations may have very few opportunities to interact with each other online.

At the same time, young people already spend a significant amount of time on social media. Instead of creating another platform designed purely around entertainment, I wanted to create a platform that feels useful, faithful, and community-centered.

This led to the idea of YP Connect.

---

## 🚀 The Solution

YP Connect brings several community-focused features into one platform.

Users can create posts and interact with other members through comments. The platform also includes goals and a progress dashboard so users can keep track of their progress on their goals.

Video content can be shared with the community, with comments allowing users to discuss the content rather than simply watching it.

The long-term vision is to make YP Connect a place where YP members from different congregations can meet, participate in Bible challenges, prepare for rallies, share ideas, encourage one another, and grow spiritually together.

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
- Cloudinary for image storage and media management
- Internet Archive for video storage
- Render for web deployment

---

## 👥 The Team

YP Connect is being developed by a collaborative team of young developers:

### Harry Code Lab
Full Stack Developer and project founder. Responsible for backend architecture, database design, Flask development, deployment, system improvements, and overall product direction. Started learning to code in October 2024 using paper-based learning and has since built this project through persistence, problem-solving, and a growing love for software development.

### Mercy-Ruth
Frontend and JavaScript Specialist. She brings strong JavaScript skills and helps shape the frontend experience, user interface, and client-side functionality. Mercy-Ruth is a key part of the YP Connect journey and contributes to making the platform more engaging and user-friendly.

Together, we are building technology that brings people together and helps young people connect with purpose.

---

## 📱 Building on Android

One of the most unusual parts of this project is that much of the development was done directly from an Android phone.

I use Pydroid 3 as my Python development environment. Pydroid 3 allows Python programs to be written and executed on Android, making it possible for me to develop the Flask application without needing a laptop or full desktop setup.

I also use Termux, an Android terminal environment that provides a Linux-like command-line environment. During development, I used Termux to experiment with MongoDB and run a local MongoDB server for testing and development.

This setup was not always easy, but it allowed me to learn and build using the hardware I had available.

---

## 🧩 Challenges During Development

Building YP Connect has involved many challenges.

One of the first major challenges was learning how different parts of a web application communicate with each other. I had to learn HTML and JavaScript while simultaneously building the Flask backend, which made the learning curve steep but deeply rewarding.

Database connectivity was another major challenge. I experimented with MongoDB, PyMongo, Flask-PyMongo, MongoDB Atlas, and a local MongoDB server hosted through Termux. There were connection problems, configuration issues, and debugging sessions that took a lot of patience.

Another major problem involved posts and synchronization. Initially, users sometimes had to synchronize before seeing new posts, and synchronization could cause posts to appear more than once. Learning how to manage data flow and update behavior correctly was an important step in making the platform feel reliable.

Deployment introduced another set of challenges. The application worked locally, but getting it running on the web required understanding environment variables, production configuration, database hosting, and deployment workflow on Render.

Profile pictures presented another challenge. I initially experimented with storing image URLs and local static files before deciding that a cloud-based solution such as Cloudinary would be more appropriate for scalability and media management.

---

## 🔐 Security and Configuration

Sensitive credentials are kept outside the source code using environment variables.

The project uses a .env file during local development for secrets such as database credentials and API keys. The .env file is not intended to be committed to GitHub.

In production, environment variables are configured through the hosting platform instead of being stored directly in the repository.

---

## 🌱 Current Status

YP Connect is currently deployed on the web and is being tested by real users.

The project has reached its first 8 users, which is an important milestone because the platform is no longer being tested only by its developer.

Recent work includes improved profile picture integration with Cloudinary, frontend collaboration with Mercy-Ruth, and ongoing fixes based on real user feedback.

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
- Android and iOS packaging using Capacitor
- Expansion to more congregations
- More tools for YP groups across Cameroon

The long-term goal is to make YP Connect useful beyond a single congregation and allow YP members from different parts of Cameroon to connect with one another.

---

## ❤️ Why We Built It

YP Connect started as a project, but we do not want it to remain just another teenager's coding project sitting on GitHub.

We want it to become something people actually use.

We want a YP member to be able to open YP Connect on a boring weekend, find a Bible challenge, see what other members are talking about, watch something interesting, complete a goal, encourage someone, and feel part of something bigger.

The goal is simple:

"Build technology that brings people together instead of simply giving them something else to scroll through."

---

## 👨‍💻 About the Developers

YP Connect is being developed by young developers from Cameroon who are learning software development by building real projects.

Rather than following only tutorials, this project has been an opportunity to learn Python, Flask, databases, JavaScript, Socket.IO, deployment, APIs, cloud services, and application design through hands-on work.

The project is still growing, and feedback from users is an important part of deciding what comes next.

---

## 📜 Project Status

YP Connect is currently live on the web at "https://yp-connect.onrender.com" and undergoing testing with its first users.

Every bug, suggestion, and piece of feedback helps shape the next version.

Thanks for reading.

Harry Code Lab & Mercy-Ruth
Build with purpose.
