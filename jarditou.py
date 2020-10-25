from flask import Flask, render_template, config, request
from flask_ngrok import run_with_ngrok

app = Flask(__name__)
app.config.from_object(config)
run_with_ngrok(app)


@app.route("/", methods=["post", "get"])
def index():
    return render_template("views/index.html")


@app.route("/catalogue")
def catalogue():
    return render_template("views/catalogue.html")


@app.route("/produit")  # /blog du mec
def produit():
    posts = [{'name': 'pioche', 'description': 'Casse les cailloux', 'prix': 52},
             {'name': 'mandrin', 'description': 'Fais des trous et des gros', 'prix': 25},
             {'name': 'marteau', 'description': 'Martelle des clous par exemple', 'prix': 2552},
             ]  # liste de chaine de caractère
    return render_template("views/produit.html", posts=posts)  # envoie la variable dans le template


@app.route("/produit/posts/1")
def details():
    posts = [{'name': 'pioche', 'description': 'Casse les cailloux', 'prix': 52},
             {'name': 'mandrin', 'description': 'Fais des trous et des gros', 'prix': 25},
             {'name': 'marteau', 'description': 'Martelle des clous par exemple', 'prix': 2552},
             ]  # liste de chaine de caractère
    return render_template("views/details.html")  # envoie la variable dans le template


@app.route("/inscription")
def register():
    return render_template("views/register.html")


@app.route("/espace-personnel", methods=["post", "get"])  # post-login
def treatment():
    if request.form == "GET":
        couriell = request.form["couriell"]
        mdp = request.form["mdp"]
        print(f"Hello {couriell}, votre mot de passe est le suivant : {mdp}.")
        return render_template("views/traitement.html", couriell=couriell, mdp=mdp)
    else:
        return render_template("views/traitement.html")


@app.errorhandler(404)
def page_not_found(error):
    return render_template('views/404.jarditou.html'), 404


if __name__ == '__main__':
    app.config['DEBUG'] = True
    app.config['TESTING'] = True
    app.run()
