import os
from flask import Flask, render_template, redirect, request, session, flash, url_for
from flask_sqlalchemy import SQLAlchemy
from flask import jsonify
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime
from datetime import datetime, date


# Configure application
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///todo.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "your_secret_key"

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# Create new table for users
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

# Create new table for tasks
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    task_text = db.Column(db.Text, nullable=False)
    completed = db.Column(db.Boolean, default=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
# Create tables
with app.app_context():
    db.create_all()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    session.clear()

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password_hash, password):
            session["user_id"] = user.id
            return redirect("/tasks")
        else:
            flash("Invalid username and/or password.", "error")

    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    session.clear()

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        if not username:
            flash("Please provide a username.", "error")
        elif not password:
            flash("Please provide a password.", "error")
        elif password != confirmation:
            flash("Passwords do not match.", "error")
        else:
            hashed_password = generate_password_hash(password)
            new_user = User(username=username, password_hash=hashed_password)
            db.session.add(new_user)
            db.session.commit()

            session["user_id"] = new_user.id
            return redirect("/login")

    return render_template("register.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


@app.route("/tasks")
def tasks():
    user_id = session.get("user_id")
    if user_id is None:
        return redirect("/login")

    # Fetch both completed and active tasks
    active_tasks = Task.query.filter_by(user_id=user_id, completed=False).all()
    completed_tasks = Task.query.filter_by(user_id=user_id, completed=True).all()

    return render_template("tasks.html", active_tasks=active_tasks, completed_tasks=completed_tasks)


@app.route("/complete_task/<int:task_id>")
def complete_task(task_id):
    user_id = session.get("user_id")
    if user_id is None:
        return redirect("/login")

    task = Task.query.get(task_id)

    if task and task.user_id == user_id:
        task.completed = True
        db.session.commit()
        flash("Task completed successfully!", "success")
    else:
        flash("Task not found or you do not have permission.", "error")

    # Redirect to the appropriate page (tasks or completed_tasks)
    redirect_url = request.args.get("redirect")
    if redirect_url == "completed_tasks":
        return redirect(url_for("completed_tasks"))
    else:
        return redirect(url_for("tasks"))


@app.route("/completed_tasks")
def completed_tasks():
    user_id = session.get("user_id")
    if user_id is None:
        return redirect("/login")

    completed_tasks = Task.query.filter_by(user_id=user_id, completed=True).all()

    return render_template("completed_tasks.html", completed_tasks=completed_tasks)


@app.route("/add_task", methods=["GET", "POST"])
def add_task():
    if request.method == "POST":
        user_id = session.get("user_id")
        task_text = request.form.get("task_text")

        if not task_text:
            flash("Please provide a task description.", "error")
        else:
            new_task = Task(user_id=user_id, task_text=task_text)
            db.session.add(new_task)
            db.session.commit()
            flash("Task added successfully!", "success")

            return redirect(url_for("tasks"))

    return render_template("add_task.html")


# Update the existing delete_task route to handle redirect URL
@app.route("/delete_task/<int:task_id>", methods=["POST"])
def delete_task(task_id):
    user_id = session.get("user_id")
    if user_id is None:
        return redirect("/login")

    task = Task.query.get(task_id)

    if task and task.user_id == user_id:
        db.session.delete(task)
        db.session.commit()
        flash("Task deleted successfully!", "success")

        # Redirect to the appropriate page (tasks or completed_tasks)
        redirect_url = request.args.get("redirect")
        if redirect_url == "completed_tasks":
            return redirect(url_for("completed_tasks"))
        else:
            return redirect(url_for("tasks"))
    else:
        return jsonify({"status": "error", "message": "Task not found or you do not have permission."})


# Add the new route to display delete task confirmation page from completed_tasks
@app.route("/delete_task_page_completed/<int:task_id>")
def delete_task_page_completed(task_id):
    user_id = session.get("user_id")
    if user_id is None:
        return redirect("/login")

    task = Task.query.get(task_id)

    if task and task.user_id == user_id:
        return render_template("delete_task.html", task=task)
    else:
        flash("Task not found or you do not have permission.", "error")
        return redirect(url_for("completed_tasks"))


if __name__ == "__main__":
    app.run(debug=True)
