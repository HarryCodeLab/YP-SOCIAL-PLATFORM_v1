__version__ = "1.0.3"
__Author__ = '''Harry <lokimaharry8@gmail.com> <harrycodelab@gmail.com>'''
__Copyright__ = '''Copyright (c) <2026> <Harry Code Lab>. All rights reserved'''
__License__ = """The MIT License"""
__PROJECT_SUMMARY__='''
THIS PROJECT WAS BUILT SPECIALLY FOR YPs(Young Presbyterians) in the PCC(Presbyterian Church in Cameroon)

A social media platform built for YP members from all over the PCC to meet, learn more about God, share their faith with each other, study the Bible with each other, pray for each other and learn from YP/Sunday School teachers from videos, rather than scrolling endlessly on Internet sites (turning doom scrolling into Faith-Scrolling ).
Special Thanks to all my friends who helped me make this Project successful.
In the future this project would be progressively updated.
Everything with CHRIST, Keep close to CHRIST.'''

from flask import Flask, render_template, request, redirect, url_for, session, flash, render_template_string
from pymongo.server_api import ServerApi
import pymongo
from pymongo import MongoClient
from flask_login import LoginManager, UserMixin, login_user, current_user, logout_user,login_required
from flask_socketio import SocketIO,emit
from werkzeug.security import generate_password_hash,check_password_hash
from werkzeug.utils import secure_filename
from itsdangerous import *
import datetime
import time
import random
from internetarchive import get_item
import uuid
import os
from bson import ObjectId
from dotenv import load_dotenv

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
env_path = os.path.join(BASE_DIR, ".env")
load_dotenv()


app = Flask(__name__)
app.secret_key = os.environ.get("APP_SECRET_KEY")
socketio = SocketIO(app, cors_allowed_origins="*")

MONGO_URI = os.getenv("MONGODB_URI")

client = pymongo.MongoClient(MONGO_URI, server_api=ServerApi('1'))
db = client['yp_social_db']

user_collection = db["users"]
post_collection = db["posts"]
comment_collection = db["comments"]
prayer_request_collection = db["prayer_requests"]
likes= db["likes"]
prayed_for = db["prayed_for"]
completed_goals = db["completed_goals"]
video_collection = db["videos"]

post_collection.create_index("created_at", expireAfterSeconds=259201)
comment_collection.create_index("created_at", expireAfterSeconds=259201)
prayer_request_collection.create_index("created_at", expireAfterSeconds=259201)
completed_goals.create_index("created_at", expireAfterSeconds=648000)

admin_password=os.environ.get("ADMIN_PASSWORD")

# Initializing Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login' 

class User(UserMixin):
    def __init__(self, user_data):
        self.id = str(user_data['_id']) 
        self.username = user_data["username"]
        self.email = user_data['email']
        self.congregation = user_data['congregation']
        self.phone_number = user_data['phone_number']
        self.role = user_data["role"]
        self.profile_pic = user_data["profile_pic_url"]
        self.about_me = user_data["about_me"]

    @staticmethod
    def get(user_id):
        # Helper to find user by MongoDB ObjectId string
        from bson.objectid import ObjectId
        try:
            user_data = user_collection.find_one({"_id": ObjectId(user_id)})
            if user_data:
                return User(user_data)
        except:
            return None
        return None

# 2. Define the mandatory user loader
@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

@app.route('/')
@login_required
def home():
    
    if not current_user.is_authenticated:
        return redirect(url_for('login'))            
        
    verses = (
    '"Let us be concerned for one another, to help one another to show love and to do Good." HEBREWS 10:24',
    '"Trust in the LORD with all your heart; do not depend on your own understanding. Seek his will in all you do, and he will show you which path to take." PROVERBS 3:5-6',
    '"Put on all of God’s armor so that you will be able to stand firm against all strategies of the devil. "EPHESIANS 6:11',
    '"Put on all of God’s armor so that you will be able  to stand firm against all strategies of the devil." EPHESIANS 6:11',
    '"I have told you all this so that you may have peace in me. Here on earth you will have many trials and sorrows. But take heart, because I have overcome the world." JOHN 16:33','"Don’t forget to show hospitality to strangers,  for some who have done this  have entertained angels without realizing it!" HEBREWS 13:2',
    ' "Keep your lives free from the love of money,  and be satisfied with what you have. For God has said, "I will never leave you, I will never abandon you."  "HEBREWS 13:5 ',
    '"Do not rebuke an older man, but appeal to him as if he were your father. Treat the younger men as your brothers" 1 TIMOTHY 5:3',
    '"Do not be afraid or discouraged,  for I the Lord your God am with you wherever you go" Joshua 1:9b',
     '"Honour the Lord and serve him sincerely and faithfully. "Joshua 24:14',
     '"For we are God’s masterpiece. He has created us anew in Christ Jesus, so that we can do the good things he planned for us long ago."  EPHESIANS 2:10',
     ' "If you become angry,  do not let your anger lead you into sin,  and do not stay angry all day"  EPHESIANS 4:26',
     ' "Dear friends, never take revenge. Leave that to the righteous anger of God. For the Scriptures say, “I will take revenge; I will pay them back,” says the Lord." ROMANS 12:19  '
    )
    random_verse = random.choice(verses)
    #db_search = list(user_collection.find({"username":{"$regex":request.form["search"]}}))
    return render_template("home.html",verse=random_verse)#,db_search=db_search)        
    
@app.route('/search')
@login_required
def search():
    db_search = list(user_collection.find({"username":{"$regex":request.form["search"]}}))
    return render_template("home.html",verse=random_verse,db_search=db_search)          
    
    
@app.route('/View_your_profile')
@login_required
def view_my_profile():
    return redirect(url_for("view_profile"))        

@app.route("/login",methods=["GET", "POST"])
def login(): 
    if current_user.is_authenticated:
        return redirect(url_for('view_profile'))    
    
    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password'].strip()
        email = request.form["email"].strip()
        number = request.form["number"].strip()
        congregation = request.form["congregation"].strip()
        about_me = request.form["about_me"].strip()
    
        save_user_dict = {
            "username": username.title(),
            "password_hash": generate_password_hash(password),
            "email": email.lower(),
            "role" : "User",
            "phone_number": number,
            "congregation": congregation.upper(),
            "profile_pic_url" : " '{{url_for('static', filename='bin.png')}}' ",
            "about_me" : about_me.capitalize()
        }
        
        # Insert into MongoDB
        result = user_collection.insert_one(save_user_dict)
        
        save_user_dict['_id'] = result.inserted_id
        
        user_obj = User(save_user_dict)
       
        login_user(user_obj, remember=True)
        flash('Logged in successfully.') 
        return redirect(url_for('help')) 
        
    return render_template("login.html")    
        
@app.route("/become_an_admin", methods=["GET", "POST"])
@login_required
def become_an_admin():
    
    if not current_user.is_authenticated:
        flash("Please log in first.")
        return redirect(url_for('login'))
    
    if request.method == "POST":
        password = request.form["password"].strip()
        is_valid = check_password_hash(admin_password, password)
        
        if is_valid:
            user_collection.update_many(
                {"_id": ObjectId(current_user.id)},
                {"$set": {"role": "Admin"}}
            )
            flash("Congratulations! You are now an admin.")
            return redirect(url_for('view_profile'))
        else:
            flash("Wrong admin password.")
            return redirect(url_for('become_an_admin'))
    
    return render_template("admin_login.html")
    
@app.route("/edit_profile", methods=["GET", "POST"])
@login_required
def edit_profile():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    
    if request.method == "POST":
        username = request.form["username"].strip()
        email = request.form["email"].strip()
        congregation = request.form["congregation"].strip()
        about_me = request.form["about_me"].strip()
        phone_number = request.form["phone_number"].strip()
        
        user_collection.update_many(
            {"_id": ObjectId(current_user.id)},
            {"$set": {
                "username": username,
                "email": email,
                "congregation": congregation,
                "about_me": about_me,
                "phone_number": phone_number,
            }}
        )
        flash("Profile updated!")
        return redirect(url_for("view_profile"))
    
    return render_template("edit_profile.html")
           
@app.route("/submit", methods=["GET", "POST"])        
@login_required
def view_profile():
    if current_user.is_authenticated:  
        user_count = user_collection.count_documents({})
        return render_template("profile.html",user_count=user_count)
    return redirect(url_for('login'))
          
@app.route("/chats", methods=["GET"])
@login_required  
def write_message():
    if not current_user.is_authenticated:
        return redirect(url_for("login"))        

    posts = list(post_collection.find().sort("_id", -1))
    post_count = post_collection.count_documents({})
    
    for post in posts:
        post["comments"] = list(
            comment_collection.find({"post_id": post["_id"]}).sort("_id", 1)
        )
        post["comment_count"] = comment_collection.count_documents({"post_id": post["_id"]})
        
        like_filter = {
        "user_id": ObjectId(current_user.id),
        "post_id": post["_id"]
    }
    
        post["already_liked"]= likes.find_one(like_filter) 
        post["like_count"] = likes.count_documents({"post_id": post["_id"]})
        post["same_author"] = ObjectId(current_user.id) == ObjectId(post["Author_id"])
        post["is_admin"] = user_collection.find_one({"_id":post["Author_id"]})
        
    return render_template("chat.html", posts=posts ,post_count=post_count)

@socketio.on("send_message")
def handle_message_event(data):
    if not current_user.is_authenticated:
        return redirect(url_for("login"))     

    new_post = {
        "Author": current_user.username,
        "Author_id": ObjectId(current_user.id),
        "message": data["message"],
        "created_at": str(datetime.datetime.utcnow()),
        "date": str(datetime.datetime.now().strftime("%d %b %Y at %I:%M %p")),
    }
    
    inserted_post = post_collection.insert_one(new_post)
    
    new_post["_id"] = str(inserted_post.inserted_id)
    new_post["Author_id"] = str(new_post["Author_id"])
    new_post["created_at"] = new_post["created_at"]
    new_post["like_count"] = 0
    new_post["comments"] = []

    emit("receive_message", new_post, broadcast=True)
              
@app.route("/View_auth_profile/<auth_id>", methods= ["GET","POST"])
@login_required
def view_auth_profile(auth_id):
    if not current_user.is_authenticated:
        return redirect(url_for("login"))
    authors = list(user_collection.find({"_id":ObjectId(auth_id)}))
    for author in authors:
        user_collection.find({"_id":auth_id})
        
    return render_template("author_profile.html",authors=authors)
              
@app.route("/comment/<post_id>", methods=["POST","GET"])
@login_required
def comment(post_id):

    if not current_user.is_authenticated:
        return redirect(url_for("login"))

    if request.method == "POST":
        comment_text = request.form["comment"].strip()

        comment_collection.insert_one({
            "post_id": ObjectId(post_id),
            "author": current_user.username,
            "author_id": ObjectId(current_user.id),
            "comment": comment_text,
            "created_at": datetime.datetime.utcnow(),
            "date": datetime.datetime.now().strftime("%d %b %Y at %I:%M %p")
    })
    return redirect(url_for("write_message"))
    
@app.route("/goals", methods= ["POST","GET"])      
@login_required
def view_goals():
    #if not current_user.is_authenticated():
#        return redirect(url_for("login"))
        
    if request.method == "GET":
       # goals = {
        Monday = (
        "Pray for five people today",
        "Tell someone about Jesus today",
        "Read a psalm today",
        "Revise on a Sunday school lesson or bible topic today and share insights with a friend",
        "Thank God at least  5 times for this day")
        
        Tuesday = (
        "Pray for five people today",
        "Share with someone today",
        "Encourage someone today",
        "Write a Bible study plan today",
        "Be of help to someone today")
        
        Wednesday = (
        "Pray for five people today",
        "Rehearse the lyrics of 2 or more gospel songs today",
        "Complete your Bible challenges for today",
        "Start your day with a five minute prayer before using your phone",
        "Read the YP promise or anthem and think about how to live it out today",
        "Write one thing you learned about God today")
        
        Thursday = (
        "Pray for five people today",
        "Pray with your family or a friend",
        "Do one act of kindness anonymously",
        "Spend 30minutes a way from social media and spend that time with God",
        'Forgive someone who hurt you and pray for them'
        )
        
        Friday = (
        "Pray for five people today",
        "Help someone without expecting anything in return",
        "Listen to a gospel song and reflect on it's message",
        "Reflect on any temptation which God helped you overcome",
        "Write anything you're thankful to God for",
        )
        
        Saturday = (
        "Pray for five people today",
        "Ask God to help someone who once helped you",
        "Memorize one Bible verse today",
        "Read one chapter of the bible and write what you've learned",
        "Write a short prayer in your prayer Journal"
        )
        
        Sunday = (
        "Pray for five people today",
        "Share your faith with one friend or family member",
        "Read a psalm before going to bed",
        "Ask someone how you can prayer for them",
        "Encourage one person with a Bible verse"
        )
     #   }
        now = datetime.datetime.now()
        day = now.strftime("%A")
        time = int(now.strftime("%H"))

        progress = completed_goals.find_one({
        "user_id": ObjectId(current_user.id),
        "day":  day
        })

    return render_template("goals.html", day=day, Monday=Monday, Tuesday=Tuesday,Wednesday=Wednesday, Thursday=Thursday, Friday=Friday,Saturday=Saturday, Sunday=Sunday, time=time, progress=progress)
        
@app.route("/prayer_request", methods=["GET", "POST"])
@login_required
def write_prayer_request():
    if not current_user.is_authenticated:
        return redirect(url_for("login"))        

    if request.method == "POST":
        Cool = prayer_request_collection.insert_one({
            "Author": current_user.username,
            "Author_id": ObjectId(current_user.id),
            "prayer_request": request.form["prayer_request"],
            "created_at": datetime.datetime.utcnow(),
            "date": datetime.datetime.now().strftime("%d %b %Y at %I:%M %p"),
            #"_id" : ObjectId(Posts.id)
        })
    prayer_requests = list(prayer_request_collection.find().sort("_id", -1))
    count  = prayer_request_collection.count_documents({})
    for pr_rq in prayer_requests:
        pr_rq["prayed_for"] = mongo.db.answered_request.count_documents({
            "request_id": pr_rq["_id"]
        })
        pr_rq["same_author"] = ObjectId(current_user.id) == ObjectId(pr_rq["Author_id"])
        pr_rq["is_admin"] = user_collection.find_one({"_id":pr_rq["Author_id"]})

    return render_template("prayer_request.html", prayer_requests=prayer_requests,count=count)
    
@app.route("/bible_challenge",methods=["POST","GET"])    
@login_required
def view_challenges():
    if not current_user.is_authenticated:
        return redirect(url_for("login"))
    if request.method == "GET":
        Bible_challenges = [
        "Read, understand and explain Hebrews 6",
        "Explain to someone what Jesus meant in Matthew 13:33",
        "Explain to a friend the parable of the weed according to Matthew 13:24-30",
        "Explain why the number 40 is occasionally used in the bible",
        "Study about all of Paul's missionary journeys and write notes and explain to a friend about what you understand from the topic",
        "Read and have an understanding of Revelations 4 and further if you wish",
        "Find 10 chapters in the bible that talks about love and compare them",
        "Read Hebrews and write ten reasons why Jesus is greater than the Old Testament sacrifices.",
        "Find every person whom Jesus forgave personally.",
        "Find every conversation Jesus had with children.",
        "Read the entire book of Ruth and list every act of kindness.",
        "Find, read, and understand every parable about seeds.",
        'Find ten promises beginning with "Fear not" or "Do not be afraid."',
        "Read every chapter mentioning the armour of God or spiritual warfare in Paul's letters",
        "Find every person who saw angels in the New Testament.",
        "Find five prayers in the book of Psalms for difficult times.",
        "Which king began well but finished badly?",
        'Find every "I am..." statement spoken by Jesus in the gospel according to Matthew.',
        "Which disciple doubted the resurrection? Read the whole account.",
        "Find every miracle Jesus performed on a Sabbath.",
        "Find three people whose names God changed. Why did He change them?",
        "Find every person that was thrown into jail for his faith",
        "Which tribe of Israel had an elite military unit of 700 left-handed soldiers who could sling a stone at a hair and not miss?",
        "Which biblical king was a giant whose iron bed was over 13 feet (9 cubits) long and 6 feet wide?",
        "What ingredient did the prophet Elisha throw into a pot of accidentally poisoned stew to make it completely safe to eat?",
        "Which biblical figure only cut his hair once a year because it became too heavy for him, with the annual trimmings weighing about 5 pounds (200 shekels)?",
        "Which prophet was commanded by God to walk around completely naked and barefoot for three years as a sign against Egypt and Ethiopia?",
        "Who is the only woman in the entire Bible whose exact age at death is explicitly recorded in scripture?",
        "What alternative name did the prophet Nathan give to King Solomon at birth, by command of the Lord?"
        "For which king did God make the shadow on the sundial move backward ten degrees as a miraculous sign of healing?",
        "What specific word was used as a military password at the Jordan River, resulting in the slaughter of 42,000 Ephraimites who couldn't pronounce the 'sh' sound?",
        "What was the name of the young man who fell asleep during an exceptionally long sermon by the Apostle Paul, fell out of a third-story window, and was picked up dead?",
        "Why did God choose Moses to rescue Israel, but then try to kill him at a lodging place on the way to Egypt?",
        "Did a medium actually summon the real spirit of the prophet Samuel from the dead, or was it a demonic deception? hint: 1 Samuel 28:7-20",
        "Who exactly was Melchizedek, the King of Salem?"

        ]
        challenges = tuple(random.sample(Bible_challenges,k=2))
        
    return render_template("bible_challenges.html",challenges=challenges)
     
@app.route("/submit_goals", methods=["POST", "GET"])
@login_required    
def submit_completed_goals():
    if not current_user.is_authenticated:
        return redirect(url_for("login"))
        
    if request.method == "POST":
        completed_goals.insert_one({
            "user_id": ObjectId(current_user.id),
            "completed_goals": int(request.form["goals_completed"]),
            "day": str(datetime.datetime.now().strftime("%A")),
            "created_at": str(datetime.datetime.utcnow()),
            "submitted_at": datetime.datetime.now(),
            #"time_stamp":datetime.datetime.now("%x")
        })
    return redirect(url_for("view_goals"))

@app.route("/about_yp",methods=["POST","GET"])
@login_required
def about_yp():
    if not current_user.is_authenticated:
        return redirect(url_for("login"))
    return render_template("about_yp.html")
    
@app.route('/view_anthem')       
@login_required 
def view_anthem():
    if not current_user.is_authenticated:
        return redirect(url_for("login"))
    return render_template("yp_anthem.html")    
      
@app.route('/view_promise')       
@login_required
def view_promise():
    if not current_user.is_authenticated:
        return redirect(url_for("login"))
    return render_template("yp_promise.html")    
        
@app.route('/view_aim')       
@login_required 
def view_aim():
    if not current_user.is_authenticated:
        return redirect(url_for("login"))
    return render_template("yp_aim.html")        
      
@app.route('/view_motto')        
@login_required
def view_motto():
    if not current_user.is_authenticated:
        return redirect(url_for("login"))
    return render_template("yp_motto.html")        
    
@app.route("/chats/like_post/<post_id>", methods=["POST","GET"])       
@login_required
def like_post(post_id):
    if not current_user.is_authenticated:
        return redirect(url_for("login"))
    if request.method == "GET":
        like_filter = {
        "user_id": ObjectId(current_user.id),
        "post_id": ObjectId(post_id)
    }
    
        existing_like = likes.find_one(like_filter)
    
        if not existing_like:
            likes.insert_one(like_filter)
        else:
            likes.delete_one(like_filter)
        
        return redirect(url_for("write_message"))
        
@app.route("/chats/delete_post/<post_id>/<author_id>",methods=["GET","POST"])
@login_required
def delete_post(post_id,author_id):
    if not current_user.is_authenticated:
        return redirect(url_for("login"))
    if request.method == "GET":
        
        if current_user.role == "Admin":
            post_collection.delete_many({"_id":ObjectId(post_id)})
            comment_collection.delete_many({"post_id":ObjectId(post_id)})
            likes.delete_many({"post_id":ObjectId(post_id)})
            
        elif ObjectId(current_user.id) == ObjectId(author_id):
            post_collection.delete_many({"_id":ObjectId(post_id)})
            comment_collection.delete_many({"post_id":ObjectId(post_id)})
            likes.delete_many({"post_id":ObjectId(post_id)})
            
        else:
            return redirect(url_for("write_message"))
            
    return redirect(url_for("write_message"))
       
@app.route("/prayer_request/<request_id>",methods=["GET","POST"])    
@login_required
def prayed_for(request_id):
    if not current_user.is_authenticated:
        return redirect(url_for("login"))
    if request.method == "POST":
        already_prayed_for = mongo.db.answered_request.find_one({
        "request_id":ObjectId(request_id),
        "user_id":ObjectId(current_user.id)})
        
        if not already_prayed_for:
            mongo.db.answered_request.insert_one({
                "request_id":ObjectId(request_id),
                "user_id":ObjectId(current_user.id),
            })
            
        else:
            pass
        return redirect(url_for("write_prayer_request"))
              
@app.route("/prayer_requests/delete_request/<request_id>/<author_id>",methods=["GET","POST"])
@login_required
def delete_request(request_id,author_id):
    if not current_user.is_authenticated:
        return redirect(url_for("login"))
    if request.method == "GET":
        
        if ObjectId(current_user.id) == ObjectId(author_id):
            prayer_request_collection.delete_many({"_id":ObjectId(request_id)})
            mongo.db.answered_request.delete_many({"request_id":ObjectId(request_id)})
            
        else:
            return redirect(url_for("write_prayer_request"))
            
    return redirect(url_for("write_prayer_request"))
        
@app.route("/upload_video",methods=["GET","POST"])
@login_required
def upload_page():
    if not current_user.is_authenticated:
        return redirect(url_for("login"))
    if current_user.role != "Admin":
        return redirect(url_for("home"))
    return  render_template("upload_vid.html")
     
@app.route("/upload-to-archive",methods=["GET","POST"])
@login_required
def upload_video():
    if not current_user.is_authenticated:
        return redirect(url_for("login"))
        
        
    identifier = f"YP_SOCIAL_PLATFORM-{uuid.uuid4().hex}"
    os.makedirs("temp_uploads", exist_ok=True)
    video_file = request.files['video']        
    filename = secure_filename(video_file.filename)
    temp_path=os.path.join("temp_uploads",filename)
        
    try:
        video_file.save(temp_path)
        item = get_item(identifier)
        r = item.upload(
            files=[temp_path],
            metadata={
                "title":request.form["title"],
                "mediatype" : "movies"
            },
                access_key=os.environ.get("IA_ACCESS_KEY"),
                secret_key=os.environ.get("IA_SECRET_KEY")
            )
        os.remove(temp_path)
    except Exception as e:
        os.remove(temp_path)
        return render_template_string("""<h1>Sorry, an exception occurred. The video couldn't be uploaded, check your internet connection and try again</h1><form action = "/View_your_profile">
    <button type="submit" class="btn-profile">Back</button>
</form>""")      
        return redirect(url_for("home"))
        
    video_url = f"https://archive.org/download/{identifier}/{filename}"
        
    video_collection.insert_one({
        "video_url":video_url,
        "author_id":ObjectId(current_user.id),
        "author":current_user.username,
        "title":request.form["title"].title(),
        "caption":request.form["caption"].capitalize(),
        "date":datetime.datetime.now().strftime("%d %b %Y at %I:%M %p"),
        })
        
    return redirect(url_for("home"))
        
@app.route("/view_videos",methods=["POST","GET"])
@login_required
def view_videos():
   if not current_user.is_authenticated:
        return redirect(url_for("login"))
        
   videos = list(video_collection.find().sort("_id", -1)) 
   video_count=video_collection.count_documents({})
   for video in videos:
       like_filter = {
        "user_id": ObjectId(current_user.id),
        "video_id": ObjectId(video["_id"])
    }
       video["comments"] = list(
            comment_collection.find({"video_id": video["_id"]}).sort("_id", 1)
        )
       video["comment_count"] = comment_collection.count_documents({"video_id": video["_id"]})
       video["like_count"] = likes.count_documents({"video_id": video["_id"]})
       video["same_author"] = ObjectId(current_user.id) == ObjectId(video["author_id"])
       video["already_liked"]= likes.find_one(like_filter) 
           
   return render_template("view_videos.html",videos=videos,video_count=video_count)
    
@app.route("/video_lessons/like_video/<video_id>", methods=["POST","GET"])       
@login_required
def like_video(video_id):
    if not current_user.is_authenticated:
        return redirect(url_for("login"))
    if request.method == "GET":
        like_filter = {
        "user_id": ObjectId(current_user.id),
        "video_id": ObjectId(video_id)
    }
        existing_like = likes.find_one(like_filter)
    
        if not existing_like:
            likes.insert_one(like_filter)
        else:
            likes.delete_one(like_filter)
        
        return redirect(url_for("view_videos"))   
               
@app.route("/progress_dashboard",methods=["GET","POST"])
@login_required
def view_dashboard():
    if not current_user.is_authenticated:
        return redirect(url_for("login"))    
    
    goal_data = list(completed_goals.find(
    {"user_id":ObjectId(current_user.id)
    })
    )

    return render_template("dashboard.html",goal_data=goal_data)
              
@app.route("/comment_vid/<video_id>", methods=["POST","GET"])
@login_required
def comment_vid(video_id):

    if not current_user.is_authenticated:
        return redirect(url_for("login"))

    if request.method == "POST":
        comment_text = request.form["comment"].strip()

        comment_collection.insert_one({
            "video_id": ObjectId(video_id),
            "author": current_user.username,
            "author_id": ObjectId(current_user.id),
            "comment": comment_text,
            "date": datetime.datetime.now().strftime("%d %b %Y at %I:%M %p")
    })
    return redirect(url_for("view_videos"))

@app.route("/video_lessons/delete_video/<video_id>/<author_id>",methods=["GET","POST"])
@login_required
def delete_video(video_id,author_id):
    if not current_user.is_authenticated:
        return redirect(url_for("login"))
    if request.method == "GET":
                    
        if ObjectId(current_user.id) == ObjectId(author_id):
            post_collection.delete_many({"_id":ObjectId(video_id)})
            comment_collection.delete_many({"post_id":ObjectId(video_id)})
            likes.delete_many({"video_id":ObjectId(video_id)})
            
        else:
            return redirect(url_for("view_videos"))
            
    return redirect(url_for("view_videos"))
    
@app.route("/sign_out_user",methods=["GET","POST"])    
@login_required
def sign_out():
    if request.method == "GET":
        user_collection.delete_one({"_id":ObjectId(current_user.id)})
        completed_goals.delete({"user_id":ObjectId(current_user.id)})
        logout_user()
        
    return redirect(url_for("login"))
    
@app.route("/help")
@login_required
def help():
    if not current_user.is_authenticated:
        return redirect(url_for("login"))    
    return render_template("help.html")
        
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    socketio.run(app, debug=False, host="0.0.0.0", port=port)
    
#_______________________________FINISHING PRAYER_______________________________________
'''LORD, THANK YOU FOR HELPING ME BUILD THIS PROJECT FOR YP MEMBERS LIKE ME TO COME CLOSER TO YOU AND STUDY WITH EACH OTHER.
FATHER LORD, I PRAY THAT YOU HELP THIS PROJECT TO BECOME A DAILY TOOL FOR YP MEMBERS TO SPEND THEIR TIME THE RIGHT WAY, DOING THE RIGHT THINGS.
I ALSO PRAY FOR ALL MY FRIENDS WHO HELPED ME AND MOTIVATED ME WITH THIS PROJECT THAT YOU'LL ALWAYS BLESS THEM AND BE WITH THEM.
GOD, YOU KNOW MY BIGGEST BATTLES. YOU KNOW THE WAR GOING ON IN MY MIND AND HEART RIGHT NOW, YOU KNOW HOW MY DAD'S GIVING ME A HARD TIME WITH MY CAREER OPTION AND MY PROJECTS PLUS ALL THIS DOCTORING STUFF. I'VE CHOSEN MY PATH AND THAT'S ENGINEERING BUT HE JUST CAN'T SEEM TO ACCEPT IT. 
AND I WISH I COULD BOUNCE BACK IN SCHOOL AS THE TOP-DAWG AGAIN. I'VE BEEN HAVING EMPTY FEELINGS IN MY HEART AND NOT KNOWING HOW TO FEEL.
FATHER I PRAY THAT YOU GRANT ME INNER PEACE DURING THIS MOMENTS OF SADNESS AND EMPTINESS.
AND ALSO, GOD PLEASE HELP ME WITH BETTER TOOLS SO AS TO IMPROVE MY SKILLS
WE ASK ALL THIS THROUGH JESUS CHRIST YOUR SON OUR LORD; AMEN'''    
