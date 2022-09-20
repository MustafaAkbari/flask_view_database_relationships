from ast import Sub
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField


class AddTeacher(FlaskForm):
    name = StringField("Teacher Name: ")
    submit = SubmitField("Add Teacher")


class RemoveTeacher(FlaskForm):
    id = IntegerField("Teacher id: ")
    submit = SubmitField("Delete Teacher")


class AddSubject(FlaskForm):
    name = StringField("Name of subject: ")
    id = IntegerField("Id of teacher: ")
    submit = SubmitField("Add subject: ")
