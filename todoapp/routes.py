from todoapp import app, db, bcrypt
from todoapp.forms import RegistrationForm, LoginForm, TaskForm, AccountUpdateForm
from todoapp.models import User, Task
from flask import render_template, redirect, request
from flask_login import login_user, current_user, logout_user




@app.route("/", methods=["GET","POST"])
def tasks_view():
    form = TaskForm()

    
    if not current_user.is_authenticated:
        return redirect('/login')

    if form.validate_on_submit():
        
        task = Task(title=form.title.data, done=False, user_id = current_user.id)
        db.session.add(task)
        db.session.commit()

        return redirect("/")

    tasks = Task.query.filter_by(user_id=current_user.id)

    return render_template("index.html", tasks=tasks, form=form)

@app.route("/update", methods=["POST"])
def task_done():
    id = request.form.get('id')
    done = True if request.form.get('done') == 'on' else False

    task = Task.query.filter_by(id=id).first()  
    task.done = done

    db.session.add(task)
    db.session.commit()

    return redirect("/")


@app.route("/delete", methods=["POST"])
def task_delete():
    id = request.form.get('id')


    task = Task.query.filter_by(id=id).first()  
    

    db.session.delete(task)
    db.session.commit()

    return redirect("/")
    

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/register", methods=["GET","POST"])
def register():

    
    if current_user.is_authenticated:
        return redirect('/')

    form = RegistrationForm()

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data,password=hashed_password, email=form.email.data)
        db.session.add(user)
        db.session.commit()
        print(f'registered {form.username.data}')
        return redirect("/")
    print('load register')
    return render_template("register.html", form=form)

@app.route("/login", methods=["GET","POST"])
def login():

    if current_user.is_authenticated:
        return redirect('/')


    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect('/')

    return render_template("login.html", form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect('/login')

@app.route("/profile", methods=["GET","POST"])
def profile():
    if not current_user.is_authenticated:
        return redirect('/login')
    
    form = AccountUpdateForm()

    if form.validate_on_submit():
        current_user.email = form.email.data
        current_user.username = form.username.data
        db.session.add(current_user)
        db.session.commit()
        return redirect("/profile")

    
    form.email.data = current_user.email
    form.username.data = current_user.username
    return render_template("profile.html", form=form)

