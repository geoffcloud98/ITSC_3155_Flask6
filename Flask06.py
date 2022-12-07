# FLASK Tutorial 1 -- We show the bare bones code to get an app up and running

# imports
import os                 # os is used to get environment variables IP & PORT
import os.path
import sqlite3
from flask import Flask   # Flask is the web app that we will customize
from flask import render_template
from flask import request
from flask import redirect, url_for 
from DATABASE import db
from MODELS import Note as Note
from MODELS import User as User



app = Flask(__name__)     # create an app

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///flask_note_appp.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']= False

#  Bind SQLAlchemy db object to this Flask app
db.init_app(app)

# Setup models
with app.app_context():
    db.create_all()   # run under the app context




# @app.route is a decorator. It gives the function "index" special powers.
# In this case it makes it so anyone going to "your-url/" makes this function
# get called. What it returns is what is shown as the web page
@app.route('/')
@app.route('/index')
def index():
    # retrieve user from database
    a_user = db.session.query(User).filter_by(email='gcloud@uncc.edu').one()

    return render_template("index.html", user = a_user)

@app.route('/notes')
def get_notes():
    # retrieve user from database
    a_user = db.session.query(User).filter_by(email='gcloud@uncc.edu').one()
    # retrieve notes from database
    my_notes = db.session.query(Note).all()

    return render_template('notes.html', notes = my_notes, user = a_user)

@app.route('/notes/<note_id>')
def get_note(note_id):
    a_user = db.session.query(User).filter_by(email='gcloud@uncc.edu').one()
    my_note = db.session.query(Note).filter_by(id=note_id)

    
    return render_template('note.html', note = my_note[int(note_id)], user = a_user)

@app.route('/notes/new', methods = ['GET', 'POST'])
def new_note():

    #check if method is used for request
    if (request.method == 'POST'):
        #get title
        title = request.form['title']
        # get note
        text = request.form['noteText']
        #create date stamp
        from datetime import date
        today = date.today()
        #format mm//dd//yyyy
        today = today.strftime("%m-%d-%Y")
        new_record = Note(title, text, today)
        db.session.add(new_record)
        db.session.commit()

        #ready to render response - redirect to notes listing
        return redirect(url_for('get_notes'))
    else:
        # GET request - show new note form
        # retrieve user from database
        a_user = db.session.query(User).filter_by(email='gcloud@uncc.edu').one()
        return render_template('new.html', user = a_user)

app.run(host=os.getenv('IP', '127.0.0.1'),port=int(os.getenv('PORT', 5000)),debug=True)

# To see the web page in your web browser, go to the url,
#   http://127.0.0.1:5000

# Note that we are running with "debug=True", so if you make changes and save it
# the server will automatically update. This is great for development but is a
# security risk for production.