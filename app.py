from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
import os



app = Flask(__name__)
app.secret_key = "Secret Key"

db_user = os.environ.get('POSTGRES_DB_USER')
db_psw = os.environ.get('POSTGRES_DB_PSW')
db_host = os.environ.get('SERVICE_POSTGRES_SERVICE_HOST')

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://{0}:{1}@{2}/courses'.format(
    db_user, db_psw, db_host
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


#Creating model table for our CRUD database
class Data(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100))
    website = db.Column(db.String(100))
    date = db.Column(db.Date())


    def __init__(self, name, website, date):

        self.name = name
        self.website = website
        self.date = date


db.create_all()


#This is the index route where we are going to
#query on all our employee data
@app.route('/')
def Index():
    all_data = Data.query.order_by(Data.date.desc()).all()

    return render_template("index.html", courses = all_data)



#this route is for inserting data to mysql database via html forms
@app.route('/insert', methods = ['POST'])
def insert():

    if request.method == 'POST':

        name = request.form['name']
        website = request.form['website']
        date = request.form['date']


        my_data = Data(name, website, date)
        db.session.add(my_data)
        db.session.commit()

        flash("Course Inserted Successfully")

        return redirect(url_for('Index'))


#this is our update route where we are going to update our employee
@app.route('/update', methods = ['GET', 'POST'])
def update():

    if request.method == 'POST':
        my_data = Data.query.get(request.form.get('id'))

        my_data.name = request.form['name']
        my_data.website = request.form['website']
        my_data.date = request.form['date']

        db.session.commit()
        flash("Course Updated Successfully")

        return redirect(url_for('Index'))




#This route is for deleting our course
@app.route('/delete/<id>/', methods = ['GET', 'POST'])
def delete(id):
    my_data = Data.query.get(id)
    db.session.delete(my_data)
    db.session.commit()
    flash("Course Deleted Successfully")

    return redirect(url_for('Index'))






if __name__ == "__main__":
    app.run()
