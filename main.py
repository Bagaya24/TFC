from flask import Flask, request, render_template, redirect, Response, url_for
import ollama
from form import FormAliment, FormBoisson, FormComestique, FormEletromenager
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer, String, ForeignKey, Float, DATE, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


app = Flask(__name__)


app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:fazili@localhost/db_stock_supermarche"
app.config["SECRET_KEY"] = "cnwdnenoe.'20323oii"


db = SQLAlchemy(model_class=Base)
db.init_app(app)


class Categories(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nom: Mapped[str] = mapped_column(String(255), nullable=False)


class Produits(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nom: Mapped[str] = mapped_column(String(255), nullable=False)
    categorie_id: Mapped[int] = mapped_column(db.Integer,
                                              ForeignKey(Categories.id, ondelete="CASCADE", onupdate="CASCADE"),
                                              nullable=False)
    prix: Mapped[float] = mapped_column(db.Numeric(10, 2), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    quantite: Mapped[int] = mapped_column(db.Integer, nullable=False)
    date_creation = mapped_column(DATE, default=datetime.now().date(), nullable=False)
    date_fabrication = mapped_column(DATE, nullable=True)
    date_expiration = mapped_column(DATE, nullable=True)
    nutriments = mapped_column(Text, nullable=True)
    details_specifiques = mapped_column(db.Text, nullable=True)


# with app.app_context():
#     db.create_all()

@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('index.html')


@app.route("/prompt", methods=["POST"])
def prompt():
    messages = request.json["messages"]
    conversation = construction_conversation(messages)

    return Response(assistant(conversation), mimetype="text/event-stream")


@app.route("/alimentaire", methods=["POST", "GET"])
def alimentaire():
    form = FormAliment()
    if request.method == "POST":
        return redirect(url_for("alimentaire"))
    return render_template("page_tableau_alimentaire.html", form=form)


@app.route("/boisson", methods=["POST", "GET"])
def boisson():
    form = FormBoisson()
    if request.method == "POST":
        return redirect(url_for("boisson"))
    return render_template("page_tableau_boisson.html", form=form)


@app.route("/cosmetique", methods=["POST", "GET"])
def cosmetique():
    form = FormComestique()
    if request.method == "POST":
        return redirect(url_for("cosmetique"))
    return render_template("page_tableau_cosmetique.html", form=form)


@app.route("/eletromenage", methods=["POST", "GET"])
def electromenage():
    form = FormEletromenager()
    if request.method == "POST":
        return redirect(url_for("electromenage"))
    return render_template("page_tableau_eletromenage.html", form=form)


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
                                    stream=True
                                    )
    for chunk in reponse_assistant:
        yield chunk["message"]["content"]


if __name__ == "__main__":
    app.run(debug=True)

