from random import randint
from flask import Flask, render_template, config, request, url_for
from flask_ngrok import run_with_ngrok
from database import connexionMysql
from flask import request, redirect
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config.from_object(config)
run_with_ngrok(app)


@app.route("/", methods=["post", "get"])
def index():
    return render_template("views/index.html")


@app.route("/catalogue")
def catalogue():
    sqlConnection = connexionMysql()

    """if "delid" in request.args:
        cursor = sqlConnection.cursor(dictionary=True)
        delid = request.args["delid"]
        cursor.execute(f"DELETE FROM produits WHERE pro_id = '{delid}'")
        sqlConnection.commit()"""

    cursor = sqlConnection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM produits")
    results = cursor.fetchall()
    return render_template("views/catalogue.html", results=results)


@app.route("/<libelle>")
def produit(libelle):
    sqlConnection = connexionMysql()
    cursor = sqlConnection.cursor(dictionary=True)
    cursor.execute(f"SELECT * from produits where pro_libelle='{libelle}';")
    details = cursor.fetchall()
    return render_template("views/produit.html", details=details)


@app.route("/ajouter-un-nouveau-produit", methods=["post", "get"])
def newProduct():
    sqlConnection = connexionMysql()
    cursor = sqlConnection.cursor(dictionary=True)
    cursor.execute(f"SELECT * from produits")
    results = cursor.fetchall()

    cursor.execute("SELECT * from categories")
    categories = cursor.fetchall()

    if request.method == "POST":
        libelle = request.form["libelle"]
        category = int(request.form["categorie"])
        couleur = request.form["couleur"]
        prix = request.form["price"]
        quantite = request.form["quantite"]
        reference = (''.join([mot[0] for mot in libelle.split(" ") + couleur.split(" ")]) + str(randint(10000, 99999))).upper()
        f = request.files["file"]
        f.save(os.path.join(app.config['IMAGE-UPLOADS'], f.filename))  # filename = nom du fichier complet
        cursor = sqlConnection.cursor()
        cursor.execute(
            f"INSERT INTO produits (pro_libelle, pro_ref, pro_cat_id, pro_couleur, pro_prix, pro_stock, pro_photo) "
            f"VALUES ('{libelle}','{reference}', '{category}', '{couleur}', '{prix}', '{quantite}', '{f.filename}');")
        sqlConnection.commit()
        return redirect(url_for('catalogue'))
    return render_template("views/addproduct.html", results=results, categories=categories)


@app.route("/inscription")
def register():
    return render_template("views/register.html")


@app.route("/singin")
def connexion():
    return render_template("views/connexion.html")


@app.route("/espace-personnel", methods=["post", "get"])  # post-login
def treatment():
    if request.method == "POST":
        couriell = request.form["couriell"]  # request.args utilisé pour les méthodes GET
        mdp = request.form["mdp"]
        sqlConnection = connexionMysql()
        cursor = sqlConnection.cursor()
        cursor.execute(f"INSERT INTO sujets (couriell, motdepasse) VALUES ('{couriell}', '{mdp}');")
        sqlConnection.commit()
        return render_template("views/catalogue.html")
    else:
        return render_template("views/index.html")


# @app.errorhandler(404)
# def page_not_found(error):
#     return render_template('views/404.jarditou.html'), 404

# Route test version
@app.route("/test")
def itz():
    return render_template("views/test.html")


@app.route("/upload", methods=["post", "get"])
def upld():
    if request.method == "POST":
        f = request.files['file']

        print(f)

        f.save(os.path.join(app.config['IMAGE-UPLOADS'], f.filename))

        print("succes")

        return redirect(request.url)

    return render_template("views/upload.html")


if __name__ == '__main__':
    app.config['DEBUG'] = True
    app.config['TESTING'] = True
    app.config['IMAGE-UPLOADS'] = "D:\Documents\Dropbox\jarditou\static\img"  # spécifie l'emplacement des fichiers à
    # télécharger
    app.run()
