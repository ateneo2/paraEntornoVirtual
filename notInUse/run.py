from flask import Flask, render_template, request, redirect, url_for
from forms import SignupForm

app = Flask(__name__)
app.config['SECRET_KEY'] = '7110c8ae51a4b5af97be6534caef90e4bb9bdcb3380af008f90b23a5d1616bf319bc298105da20fe'
@app.route("/p/<string:slug>/")
def show_post(slug):
    return render_template("post_view.html", slug_title=slug)


posts = []
@app.route("/")
def index():
    return render_template("index.html", num_posts=len(posts))	
    
    
@app.route("/admin/post/")
@app.route("/admin/post/<int:post_id>/")
def post_form(post_id=None):
    return render_template("admin/post_form.html", post_id=post_id)

@app.route("/signup2/", methods=["GET", "POST"])
def show_signup_form():
    form = SignupForm()
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        password = form.password.data
        next = request.args.get('next', None)
        if next:
            return redirect(next)
        return redirect(url_for('index'))
    return render_template("signup_form2.html", form=form)
    
   
@app.route("/signup/", methods=["GET", "POST"])
def show_signup2_form():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        next = request.args.get('next', None)
        if next:
            return redirect(next)
        return redirect(url_for('index'))
    return render_template("signup_form.html")
    
@app.route('/procesar', methods=['POST'])
def procesar():
    nombre = request.form.get("name")
    email = request.form.get("email")
    password = request.form.get("password")
    
    return render_template("mostrar.html", nombre=nombre, email=email)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True)
    
    
    
//@app.route("/signup/", methods=["GET", "POST"])
//def show_signup_form():
  //  if request.method == 'POST':
  //      name = request.form['name']
  //      email = request.form['email']
  //      password = request.form['password']
  //      next = request.args.get('next', None)
    //    if next:
    //        return redirect(next)
    //    return redirect(url_for('index'))
    //return render_template("signup_form.html")
    