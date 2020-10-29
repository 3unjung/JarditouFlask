from flask import Flask, render_template, config, request
from flask_ngrok import run_with_ngrok
from database import connexionMysql

app = Flask(__name__)
app.config.from_object(config)
run_with_ngrok(app)


@app.route("/", methods=["post", "get"])
def index():
    return render_template("views/index.html")


@app.route("/catalogue")
def catalogue():
    varriable = "je suis une varriable envoyée"
    sqlConnection = connexionMysql()
    cursor = sqlConnection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM produits")
    results = cursor.fetchall()

    return render_template("views/catalogue.html", results=results)


@app.route("/produit")  # blog du mec
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
    if request.method == "POST":
        couriell = request.form["couriell"]  # request.args utilisé pour les méthodes GET
        mdp = request.form["mdp"]
        sqlConnection = connexionMysql()
        cursor = sqlConnection.cursor()
        cursor.execute(f"INSERT INTO sujets (couriell, motdepasse) VALUES ('{couriell}', '{mdp}');")
        sqlConnection.commit()

        return render_template("views/traitement.html", couriell=couriell, mdp=mdp)
    else:
        return render_template("views/index.html")


@app.errorhandler(404)
def page_not_found(error):
    return render_template('views/404.jarditou.html'), 404


if __name__ == '__main__':
    app.config['DEBUG'] = True
    app.config['TESTING'] = True
    app.run()
