# -*- coding: utf-8 -*-
from flask import Flask, flash, render_template, request, redirect, url_for
from forms import SignupForm, PostForm, LoginForm
from flask_login import LoginManager,current_user, login_user, logout_user, login_required
from models import users, User, get_user
from werkzeug.urls import url_parse

app = Flask(__name__)
app.config['SECRET_KEY'] = '7110c8ae51a4b5af97be6534caef90e4bb9bdcb3380af008f90b23a5d1616bf319bc298105da20fe'

login_manager = LoginManager(app)
login_manager.login_view = "login"
#login_manager.init_app(app)

# @login_manager.user_loader
# def load_user(user_id):
#     return User.get_by_id(int(user_id))

@app.route("/p/<string:slug>/")
def show_post(slug):
    return render_template("post_view.html", slug_title=slug)

posts = []
@app.route("/")
def index():
    return render_template("index.html", posts=posts)
    
@app.route("/admin/post/", methods=['GET', 'POST'], defaults={'post_id': None})
@app.route("/admin/post/<int:post_id>/", methods=['GET', 'POST'])
@login_required
def post_form(post_id):
    form = PostForm()
    if form.validate_on_submit():
        title = form.title.data
        title_slug = form.title_slug.data
        content = form.content.data
        post = {'title': title, 'title_slug': title_slug, 'content': content}
        posts.append(post)
        return redirect(url_for('index'))
    return render_template("admin/post_form.html", form=form)


@app.route("/signup2/", methods=["GET", "POST"])
def show_signup_form():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = SignupForm()
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        password = form.password.data
        # Creamos el usuario y lo guardamos
        user = User(len(users) + 1, name, email, password)
        flash('usuario')
        alert(name, email, password)
        flash(user)
        flash('         ')
        users.append(user)
       
           
        # Dejamos al usuario logueado
        login_user(user, remember=True)
        next_page = request.args.get('next', None)
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template("signup_form2.html", form=form , users=users)
    
#@app.route("/signup3/", methods=["GET", "POST"]) #not in use
#def show_signup3_form():
#    form = SignupForm()
#    if form.validate_on_submit():
#        name = form.name.data
#        email = form.email.data
#        password = form.password.data
#        next = request.args.get('next', None)
#        if next:
#            return redirect(next)
#        return redirect(url_for('index'))
#    return render_template("signup_form2.html", form=form)
    
   
# @app.route("/signup/", methods=["GET", "POST"])
# def show_signup2_form():
#     if request.method == 'POST':
#         name = request.form['name']
#         email = request.form['email']
#         password = request.form['password']
#         next = request.args.get('next', None)
#         if next:
#             return redirect(next)
#         return redirect(url_for('index'))
#     return render_template("signup_form.html")
    
# @app.route('/procesar', methods=['POST'])
# def procesar():
#     nombre = request.form.get("name")
#     email = request.form.get("email")
#     password = request.form.get("password")
    
#     return render_template("mostrar.html", nombre=nombre, email=email)

@login_manager.user_loader
def load_user(user_email):
    for user in users:
        if user.email == (user_email):
            return user
    return None



@app.route('/login', methods=['GET', 'POST'])
def login():
    flash('pruebo un mensaje empiezo login...')
    if current_user.is_authenticated:
        flash('Te redirijo a index xq estas autenticado')

        return redirect(url_for('admin/index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = get_user(form.email.data)
        flash(form.email.data)
        flash('El usuario es :')
        flash(user)
        if user is not None and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            flash('Logged in successfully.')
            next_page = request.args.get('next')
            if not next_page or url_parse(next_page).netloc != '':
                next_page = url_for('index')
            return redirect(next_page)
        flash('Te redirijo a ... pero NO  estas autenticado')
    return render_template('login_form.html', form=form)
 
@app.route('/logout')
def logout():
    flash('Logged  OUT  successfully.')
    logout_user()
    return redirect(url_for('index'))   
    
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True)
  
