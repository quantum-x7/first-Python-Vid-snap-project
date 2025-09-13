from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import uuid
import os
UPLOAD_FOLDER = "user_uploads" #This is an constant variable to make sure the all uploaded files in the same folder in uniform way
ALLOWED_EXTENSIONS = {'png','jpg','jpeg'} #this is also an constant variable to store the ethical exetension to allowed in the our app
app = Flask(__name__) #intialize the app varible
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER 

#this is an home page
@app.route("/")
def home():
    return render_template("index.html")

#This is an creat Reel page
@app.route("/create", methods = ["POST","GET"]) # in this line we handle the both requests method (POST or GET)
def create():
    myid = str(uuid.uuid1()) #generating a unique id to storing an uploaded file data
    if request.method == "POST": 
        # print(request.files.keys())
        rec_id = (request.form.get("uuid")) # get tthe uuid
        desc = (request.form.get("text")) # get the description
        input_files = [] #all the files here uploded by the user input files
        for key , value in request.files.items():
            print(key,value)
            file = request.files[key]
            if file:
                file_name =  secure_filename(file.filename) #ensuring that the filename must be secure
                folder_path = os.path.join(app.config["UPLOAD_FOLDER"],rec_id) #make an filder path structure upload_folder --> uuid sub folder

                # here we check that the path for upload folder is exist if not exist then we make an directory
                if not(os.path.exists(folder_path)):
                    os.mkdir(os.path.join(app.config["UPLOAD_FOLDER"],rec_id)) # here the upper structure is made
        
                file.save(os.path.join(app.config['UPLOAD_FOLDER'],rec_id,file_name)) # file is save here 
                input_files.append(file_name) # the all ensured scure file name is appended to input files

                #Here we can save the description from the user
                with open(os.path.join(app.config['UPLOAD_FOLDER'],rec_id,'desc.txt'),'w',encoding='utf-8') as f:
                    f.write(desc)

                #Here's the all the securd input file is saved
                for fl in input_files:
                    with open (os.path.join(app.config['UPLOAD_FOLDER'],rec_id,'input.txt'),'a') as f:
                        f.write(f"file '{fl}'\nduration 1\n")

    return render_template("create.html",myid=myid)

@app.route("/gallery")
def gallery():
    reels = os.listdir("static/reels")
    return render_template("gallery.html",reels=reels)

app.run(debug=True)