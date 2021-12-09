from os import _exit
from flask import render_template,Response
from tumblr1 import app,db,login_manager
from tumblr1.models import User,Post,Comment,Like,POST_TYPE
from tumblr1 import admin
from flask_login import login_user,logout_user,current_user,login_required
from flask import Flask, render_template, redirect, request, session,make_response, flash,jsonify
# from passlib.hash import sha256_crypt
# from passlib.hash import sha256_crypt
from passlib.hash import sha256_crypt
import werkzeug
from werkzeug.utils import secure_filename
import os

# @login_manager.unauthorized_handler #if user not login the you shoud be use this method and flash message
# def unauthorized():
#     # do stuff
#     return redirect("/")

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif','mp4'])
def allowed_file(filename):
    	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# @app.route('/')
@app.route('/')
def home_page():
    # result=User.query.all()
    # print(result)
    data=Post.query.all()
    # if i.post_likes==True
    # q=Like.query.filter((Like.post_id==1) & (Like.like_post==True)).first()
    # print(q)
    
    # tlike=db.session.query(Like).filter(Like.like_post==True).count()
    # data=db.session.query(User,Post).filter(User.id==Post.user_id).all()
    return render_template('index.html',data=data,POST_TYPE=POST_TYPE)#,result=result)
    # return 'done'

@app.route("/login",methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username1 = request.form.get('username')
        password = request.form.get('password')
        q = User.query.filter_by(username=username1).first()
        encrypt_password=q.password
        print(encrypt_password)
        if q.username == username1 and sha256_crypt.verify(password,encrypt_password):
            login_user(q)
            return redirect('/home')
    if current_user.is_authenticated:
        return redirect('/')
    else:           
        return render_template('users/login.html')

@app.route("/logout",methods=['GET','POST'])
def log_out():
    logout_user()
    return redirect('/')

@app.route('/profile',methods=['GET','POST'])
def user_profile():
    return render_template('users/profile.html')

@app.route('/edit_profile',methods=['GET','POST'])
def edit_profile():
    id=current_user.id
    log_user=User.query.filter_by(id=id).first()
    if request.method == 'POST':
        name = request.form.get('name')
        print(name)
        username = request.form.get('username')
        email = request.form.get('email')
        file=request.files['img']
        print(file)
        print(file.filename,"<<<<<<<<<<<<<<<<<")
        
        # logImg = file.filename if file != '' else log_user.user_image
        
        if file.filename == '' or file.filename != '':# or (file and allowed_file(file.filename)):
            print("kkk")
            # try:
            if file.filename != '':
                print("try if block")
                file.save(os.path.join(app.config['UPLOAD_FOLDER']+'user_profile_images/',file.filename)) #cannot save empty file so i have use try and except exception handling method
        # except:
            print("except block")
            website = request.form.get('website')
            facebook = request.form.get('facebook')
            twitter = request.form.get('twitter')
            instagram = request.form.get('instagram')
            linkedin = request.form.get('linkedin')
            log_user.name=name
            log_user.email=email
            if file.filename == '':
                print("except if block")
                log_user.user_image=log_user.user_image
            else:
                log_user.user_image=file.filename
            print('not empty')
            log_user.website_url=website
            log_user.facebook=facebook
            log_user.twitter=twitter
            log_user.instagram=instagram
            log_user.linkedin=linkedin
            db.session.commit()
            return redirect('/edit_profile')
        else:
            return 'something went wrong'
    return render_template('users/edit_profile.html',log_user=log_user)

@app.route('/change_password',methods=['GET','POST'])
def change_password():
    if request.method == 'POST':
        if current_user.is_authenticated:
            id=current_user.id
        user_pass=User.query.filter_by(id=id).first()
        database_password=user_pass.password    
        old_password=request.form.get('old_password')
        new_password=request.form.get('new_password')
        encrypt_password=sha256_crypt.encrypt(new_password)
        conform_password= request.form.get('conform_password')
        if new_password==conform_password:
            if sha256_crypt.verify(old_password,database_password):
                user_pass.password=encrypt_password
                db.session.commit()
                return 'password changed'
            
@app.route('/home',methods=['GET','POST'])
def home():
    if current_user.is_authenticated:
        return render_template('users/home.html')
    else:
        return 'User not login'

@app.route("/register_user",methods=['GET','POST'])
def register_user():
    if request.method == 'POST':
        name=request.form.get('name')
        username=request.form.get('username')
        email=request.form.get('email')
        password=request.form.get('password')
        password_confirmation=request.form.get('password_confirmation')
        encrypt_password=sha256_crypt.encrypt(password)
        if '@gmail' in email:
            # return email
            result=User(name=name,username=username,email=email,password=encrypt_password)
            db.session.add(result)
            db.session.commit()
            return redirect('/login')
        else:
            return 'Invalid email'
    return render_template('users/register.html')
 
@app.route('/add_post',methods=['GET','POST'])
def add_post():
    if request.method == 'POST':
        post_title=request.form['post_title']
        post_desc=request.form['post_desc']
        img_gif_video= request.files['img_gif_video']
        post_type=request.form['post_type']
        # if request.files['img'] != '':
        #     img_gif_video= request.files['img']
        # if request.files['gif'] !='':
        #     img_gif_video= request.files['gif']
        # if request.files['video'] !='':  
        #     img_gif_video= request.files['video']

        print(post_title,post_desc,img_gif_video.filename,post_type)
        if img_gif_video and allowed_file(img_gif_video.filename):
            filename = secure_filename(img_gif_video.filename)
            img_gif_video.save(os.path.join(app.config['UPLOAD_FOLDER']+'/all_post',filename))            
            user_id=current_user.id
            result=Post(post_title=post_title,post_description=post_desc,post_type=post_type,user_id=user_id,post_data=filename)    
            db.session.add(result)
            db.session.commit()
            return 'Success'
    return render_template('add_post.html')

@app.route("/like",methods=['GET','POST'])
def likes():
    if request.method == 'POST':
        resp={}
        if current_user.is_authenticated:
            like_post1=bool(request.form['like_post'])
            post_id1=request.form['post_id']
            user_id1=current_user.id
            unlike=Like.query.filter((Like.user_id==user_id1) & (Like.post_id==post_id1) & (Like.like_post==False)).first()
            like=Like.query.filter((Like.user_id==user_id1) & (Like.post_id==post_id1) & (Like.like_post==True)).first()
            # print(result.like_post,result.post_id,result.user_id)
            if like:
                resp['status']='like'
                like.like_post=False
                db.session.commit()
                return jsonify(resp)
            if unlike:
                resp['status']="unlike"
                unlike.like_post=True
                db.session.commit()
                return jsonify(resp)
            else:
                print("else block run")
                result=Like(like_post=like_post1,post_id=post_id1,user_id=user_id1)
                db.session.add(result)
                print(like_post1,post_id1,user_id1)
                db.session.commit()
                resp['status']='success'
                return jsonify(resp)
            
        resp['status']="unauthorized_user"
        return jsonify(resp)
         
   