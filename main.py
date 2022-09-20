from ast import Sub
from flask import Flask, render_template, flash, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy.orm.exc import UnmappedInstanceError
import os
from form import AddTeacher, AddSubject, RemoveTeacher

app = Flask(__name__)

app.config['SECRET_KEY'] = "mustafatima123"
#######################################
###### SETUP SQL DATABAE SECTION ######
#######################################
basedir = os.path.abspath(os.path.dirname(__file__))

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
    os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
Migrate(app, db)
#######################################
############ SETUP MODELS #############
#######################################


class Teachers_M(db.Model):
    __tablename__ = "Teachers"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    # set up a one to many relationship between teachers table and subjects table
    subject = db.relationship(
        "Subjects_M", backref="Teachers_M", uselist=False)

    def __init__(self, name) -> None:
        self.name = name

    def __repr__(self) -> str:
        if self.subject:
            return f"T: {self.name} teachs {self.subject.name}"
        else:
            return f"Teacher name is {self.name} and has no subject assigned yed!"


class Subjects_M(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    # creating a foreign key for subjects table
    teacher_id = db.Column(db.Integer, db.ForeignKey('Teachers.id'))

    def __init__(self, name, teacher_id) -> None:
        self.name = name
        self.teacher_id = teacher_id

########################################
####### SETUP VIWES -- HAVE FORM #######
########################################


@app.route('/')
def index():
    return render_template("home.html")


@app.route('/add_teacher', methods=['GET', 'POST'])
def add_teacher():
    form = AddTeacher()
    if form.validate_on_submit():
        name = form.name.data
        new_teacher = Teachers_M(name)
        db.session.add(new_teacher)
        db.session.commit()
        flash(f"A teacher by the name of {name} added")
        return redirect(url_for('add_teacher'))
    return render_template('add_teacher.html', form=form)


@app.route('/list_teacher')
def list_teacher():
    teachers = Teachers_M.query.all()
    return render_template('list.html', teachers=teachers)


@app.route('/delete_teacher', methods=['GET', 'POST'])
def delete_teacher():
    form = RemoveTeacher()
    try:
        if form.validate_on_submit():
            id = form.id.data
            delete_t = Teachers_M.query.get(id)
            db.session.delete(delete_t)
            db.session.commit()
            flash(f"A teacher with the id {id} removed from the list")
            return redirect(url_for('delete_teacher'))
    except UnmappedInstanceError:
        flash(f"The teacher with the id {id} does not exist to remove!")
        return redirect(url_for("delete_teacher"))
    return render_template("delete.html", form=form)


@app.route('/add_subject', methods=['GET', 'POST'])
def add_subject():
    form = AddSubject()
    if form.validate_on_submit():
        name = form.name.data
        id = form.id.data
        new_subject = Subjects_M(name, id)
        db.session.add(new_subject)
        db.session.commit()
        flash(
            f"A subject by the name of {name} add to a teacher with the id {id}")
        return redirect(url_for('add_subject'))
    return render_template('add_subject.html', form=form)


if __name__ == "__main__":
    app.run(debug=True)
