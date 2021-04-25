from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap(app)

##CREATE DATABASE
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo.db"
#Optional: But it will silence the deprecation warning in the console.
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


##CREATE TABLE
class todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    description = db.Column(db.String(250), nullable=False)
    due_date = db.Column(db.String(250), nullable=False)
    done = db.Column(db.Boolean, nullable=False)
db.create_all()


class CreateTodoForm(FlaskForm):
    title = StringField("Todo Title", validators=[DataRequired()])
    description = StringField("Description", validators=[DataRequired()])
    due_date = StringField("Due Date", validators=[DataRequired()])
    done = BooleanField("Done")
    submit = SubmitField("Add Todo")


@app.route('/')
def home():
    ##READ ALL RECORDS
    all_todos = db.session.query(todo).all()
    return render_template("index.html", todos=all_todos)


@app.route("/add", methods=["GET", "POST"])
def add():
    form = CreateTodoForm()
    if form.validate_on_submit():
        new_todo = todo(
            title=form.data["title"],
            description=form.data["description"],
            due_date=form.data["due_date"],
            done=form.data["done"]
        )
        db.session.add(new_todo)
        db.session.commit()
        return redirect(url_for('home'))

    return render_template("add.html", form=form)


@app.route("/edit", methods=["GET", "POST"])
def edit():
    if request.method == "POST":
        if "done" in request.form:
            todo_id = request.form["id"]
            todo_to_update = todo.query.get(todo_id)
            todo_to_update.done = bool(request.form["done"])
            db.session.commit()
            return redirect(url_for('home'))
        else:
            todo_id = request.form["id"]
            todo_to_update = todo.query.get(todo_id)
            todo_to_update.done = False
            db.session.commit()
            return redirect(url_for('home'))
    todo_id = request.args['id']
    todo_selected = todo.query.get(todo_id)
    return render_template("edit_todo.html", todo=todo_selected)


if __name__ == "__main__":
    app.run(debug=True)
