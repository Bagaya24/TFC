from flask import Flask, request, render_template, redirect, Response, url_for, jsonify
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
    categorie_id: Mapped[int] = mapped_column(Integer,
                                              ForeignKey(Categories.id, ondelete="CASCADE", onupdate="CASCADE"),
                                              nullable=False)
    prix: Mapped[float] = mapped_column(db.Numeric(10, 2), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    quantite: Mapped[int] = mapped_column(Integer, nullable=False)
    date_d_ajout = mapped_column(DATE, default=datetime.now().date(), nullable=False)
    date_fabrication = mapped_column(DATE, nullable=True)
    date_expiration = mapped_column(DATE, nullable=True)
    nutriments = mapped_column(Text, nullable=True)
    details_specifiques = mapped_column(db.Text, nullable=True)
    devise: Mapped[str] = mapped_column(String(10), default="USD")

    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}


with app.app_context():
    db.create_all()


@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('index.html')


@app.route("/prompt", methods=["POST"])
def prompt():
    messages = request.json["messages"]
    conversation = construction_conversation(messages)

    return Response(assistant(conversation), mimetype="text/event-stream")


@app.route("/api")
def api_produit():
    produits = db.session.execute(db.select(Produits)).scalars().all()
    result = []
    for produit in produits:
        result.append({
            'id': produit.id,
            'nom': produit.nom,
            'categorie': produit.categorie_id.nom,
            'prix': str(produit.prix),
            'description': produit.description,
            'quantite': produit.quantite,
            'date_creation': produit.date_creation.strftime('%Y-%m-%d'),
            'date_fabrication': produit.date_fabrication.strftime('%Y-%m-%d') if produit.date_fabrication else None,
            'date_expiration': produit.date_expiration.strftime('%Y-%m-%d') if produit.date_expiration else None,
            'nutriments': produit.nutriments,
            'details_specifiques': produit.details_specifiques
        })
    return jsonify(result)


@app.route("/alimentaire", methods=["POST", "GET"])
def alimentaire():
    form = FormAliment()
    produit_alimentaire = db.session.execute(db.select(Produits).where(Produits.categorie_id == 1)).scalars().all()
    if request.method == "POST":
        nom = form.nom.data
        quantite = form.quantite.data
        prix = form.prix.data
        date_fabrication = form.date_fabrication.data
        date_expiration = form.date_expiration.data
        description = form.description.data
        nutriment = form.nutriment.data
        nouveau_produit_alimentaire = Produits(
            nom=nom,
            categorie_id=1,
            quantite=quantite,
            prix=prix,
            description=description,
            date_expiration=date_expiration,
            date_fabrication=date_fabrication,
            nutriments=nutriment,
        )
        db.session.add(nouveau_produit_alimentaire)
        db.session.commit()
        return redirect(url_for("alimentaire"))
    return render_template("page_tableau_alimentaire.html", form=form, produits=produit_alimentaire)


@app.route("/alimentaire/effacer", methods=["POST"])
def effacer_aliment():
    if request.method == "POST":
        id_produit_a_effacer = request.form.get("id")
        produit_a_effacer = db.get_or_404(Produits, id_produit_a_effacer)
        db.session.delete(produit_a_effacer)
        db.session.commit()
        return redirect(url_for("alimentaire"))


@app.route("/boisson", methods=["POST", "GET"])
def boisson():
    form = FormBoisson()
    produit_boisson = db.session.execute(db.select(Produits).where(Produits.categorie_id == 2)).scalars().all()
    for produit in produit_boisson:
        print(produit)
    if request.method == "POST":
        nom = form.nom.data
        quantite = form.quantite.data
        prix = form.prix.data
        date_fabrication = form.date_fabrication.data
        date_expiration = form.date_expiration.data
        description = form.description.data
        nutriment = form.nutriment.data
        nouveau_produit_boisson = Produits(
            nom=nom,
            categorie_id=2,
            quantite=quantite,
            prix=prix,
            description=description,
            date_expiration=date_expiration,
            date_fabrication=date_fabrication,
            nutriments=nutriment,
        )
        db.session.add(nouveau_produit_boisson)
        db.session.commit()
        return redirect(url_for("boisson"))
    return render_template("page_tableau_boisson.html", form=form, produits=produit_boisson)


@app.route("/boisson/effacer", methods=["POST"])
def effacer_boisson():
    if request.method == "POST":
        id_produit_a_effacer = request.form.get("id")
        produit_a_effacer = db.get_or_404(Produits, id_produit_a_effacer)
        db.session.delete(produit_a_effacer)
        db.session.commit()
        return redirect(url_for("boisson"))


@app.route("/cosmetique", methods=["POST", "GET"])
def cosmetique():
    form = FormComestique()
    produit_cosmetique = db.session.execute(db.select(Produits).where(Produits.categorie_id == 3)).scalars().all()
    if request.method == "POST":
        nom = form.nom.data
        quantite = form.quantite.data
        date_fabrication = form.date_fabrication.data
        date_expiration = form.date_expiration.data
        prix = form.prix.data
        type_produit = form.type.data
        description = form.description.data
        nouveau_produit_cosmetique = Produits(
            nom=nom,
            categorie_id=3,
            quantite=quantite,
            prix=prix,
            description=type_produit,
            date_expiration=date_expiration,
            date_fabrication=date_fabrication,
            details_specifiques=description,
        )
        db.session.add(nouveau_produit_cosmetique)
        db.session.commit()
        return redirect(url_for("cosmetique"))
    return render_template("page_tableau_cosmetique.html", form=form, produits=produit_cosmetique)


@app.route("/cosmetique/effacer", methods=["POST"])
def effacer_cosmetique():
    if request.method == "POST":
        id_produit_a_effacer = request.form.get("id")
        produit_a_effacer = db.get_or_404(Produits, id_produit_a_effacer)
        db.session.delete(produit_a_effacer)
        db.session.commit()
        return redirect(url_for("cosmetique"))


@app.route("/eletromenage", methods=["POST", "GET"])
def electromenage():
    form = FormEletromenager()
    produit_electromenager = db.session.execute(db.select(Produits).where(Produits.categorie_id == 4)).scalars().all()
    if request.method == "POST":
        if request.method == "POST":
            nom = form.nom.data
            quantite = form.quantite.data
            prix = form.prix.data
            type_produit = form.type.data
            description = form.description.data
            nouveau_produit_electromenager = Produits(
                nom=nom,
                categorie_id=4,
                quantite=quantite,
                prix=prix,
                description=type_produit,
                details_specifiques=description,
            )
            db.session.add(nouveau_produit_electromenager)
            db.session.commit()

        return redirect(url_for("electromenage"))
    return render_template("page_tableau_eletromenage.html",
                           form=form, produit=produit_electromenager)


@app.route("/electromenager/effacer", methods=["POST"])
def effacer_electromenager():
    if request.method == "POST":
        id_produit_a_effacer = request.form.get("id")
        produit_a_effacer = db.get_or_404(Produits, id_produit_a_effacer)
        db.session.delete(produit_a_effacer)
        db.session.commit()
        return redirect(url_for("electromenager"))


@app.route("/utilisateur")
def utilisateur():
    return render_template("page_utilisateur.html")


def construction_conversation(message: list) -> list[dict]:
    return [
        {"role": "user" if i % 2 == 0 else "assistant", "content": message}
        for i, message in enumerate(message)
    ]


def assistant(conversation: list[dict]) -> str:
    reponse_assistant = ollama.chat(model="assistant_2",
                                    messages=conversation,
                                    stream=True
                                    )
    for chunk in reponse_assistant:
        yield chunk["message"]["content"]


if __name__ == "__main__":
    app.run(debug=True)

