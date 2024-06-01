from flask import Flask, request, render_template, redirect, Response
import ollama
from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, EmailField, IntegerField, PasswordField
from wtforms.validators import Email, DataRequired
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer, String, ForeignKey, Float, DATE
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


app = Flask(__name__)


app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:fazili@localhost/db_stock_supermarche"
app.config["SECRET KEY"] = "cnwdnenoe.'20323oii"

db = SQLAlchemy(model_class=Base)
db.init_app(app)


class Categorie(db.Model):
    __tablename__ = "categorie"
    id_categorie: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, unique=True)
    nom_categorie: Mapped[str] = mapped_column(String, unique=True)


class Produit(db.Model):
    __tablename__ = "produits"
    id_produit: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, unique=True)
    nom_produit: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    prix_produit: Mapped[float] = mapped_column(Float, nullable=False)
    quantite_produit: Mapped[int] = mapped_column(Integer, nullable=False)
    id_categorie_produit: Mapped[int] = mapped_column(Integer, ForeignKey(Categorie.id_categorie,
                                                                          onupdate="CASCADE",
                                                                          ondelete="CASCADE"))
    date_ajout_produit = mapped_column(DATE, nullable=False)


class Alimentaire(db.Model):
    __tablename__ = "produit_alimentaire"
    id_produit: Mapped[int] = mapped_column(Integer, primary_key=True)
    id_sous_categorie: Mapped[int] = mapped_column(Integer, nullable=False)



@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('index.html')


@app.route("/prompt", methods=["POST"])
def prompt():
    messages = request.json["messages"]
    conversation = construction_conversation(messages)

    return Response(assistant(conversation), mimetype="text/event-stream")


@app.route("/alimentaire")
def alimentaire():
    return render_template("page_tableau_alimentaire.html")


@app.route("/boisson")
def boisson():
    return render_template("page_tableau_boisson.html")


@app.route("/cosmetique")
def cosmetique():
    return render_template("page_tableau_cosmetique.html")


@app.route("/eletromenage")
def electromenage():
    return render_template("page_tableau_eletromenage.html")


@app.route("/utilisateur")
def utilisateur():
    return render_template("page_utilisateur.html")


def construction_conversation(message: list) -> list[dict]:
    return [
        {"role": "user" if i % 2 == 0 else "assistant", "content": message}
        for i, message in enumerate(message)
    ]


def assistant(conversation: list[dict]) -> str:
    reponse_assistant = ollama.chat(model="assistant_1",
                                    messages=conversation,
                                    )
    yield reponse_assistant["message"]["content"]


if __name__ == "__main__":
    app.run(debug=True)

