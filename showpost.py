@app.route("/p/<string:slug>/")
def show_post(slug):
    return ("Mostrando el post {}".format(slug))