from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField, DecimalField, IntegerField, TextAreaField
from wtforms.validators import DataRequired, Email


class FormAliment(FlaskForm):
    nom = StringField(label="Nom", validators=[DataRequired()])
    prix = DecimalField(label="Prix", validators=[DataRequired()])
    quantite = IntegerField(label="Quantite", validators=[DataRequired()])
    date_fabrication = DateField(label="Date de fabrication", validators=[DataRequired()])
    date_expiration = DateField(label="Date d'expiration", validators=[DataRequired()])
    description = TextAreaField(label="Description", validators=[DataRequired()])
    nutriment = TextAreaField(label="Nutriment")
    btn_ajouter = SubmitField(label="ajouter")
    btn_annuler = SubmitField(label="annuler")


class FormBoisson(FlaskForm):
    nom = StringField(label="Nom", validators=[DataRequired()])
    prix = DecimalField(label="Prix", validators=[DataRequired()])
    quantite = IntegerField(label="Quantite", validators=[DataRequired()])
    date_fabrication = DateField(label="Date de fabrication", validators=[DataRequired()])
    date_expiration = DateField(label="Date d'expiration", validators=[DataRequired()])
    description = TextAreaField(label="Description", validators=[DataRequired()])
    nutriment = TextAreaField(label="Nutriment")
    btn_ajouter = SubmitField(label="ajouter")
    btn_annuler = SubmitField(label="annuler")
    
class FormEletromenager(FlaskForm):
    nom = StringField(label="Nom", validators=[DataRequired()])
    prix = DecimalField(label="Prix", validators=[DataRequired()])
    quantite = IntegerField(label="Quantite", validators=[DataRequired()])
    type = TextAreaField(label="Type", validators=[DataRequired()])
    description = TextAreaField(label="Description", validators=[DataRequired()])
    btn_ajouter = SubmitField(label="ajouter")
    btn_annuler = SubmitField(label="annuler")
    
class FormComestique(FlaskForm):
    nom = StringField(label="Nom", validators=[DataRequired()])
    prix = DecimalField(label="Prix", validators=[DataRequired()])
    quantite = IntegerField(label="Quantite", validators=[DataRequired()])
    date_fabrication = DateField(label="Date de fabrication", validators=[DataRequired()])
    date_expiration = DateField(label="Date d'expiration", validators=[DataRequired()])
    type = TextAreaField(label="type", validators=[DataRequired()])
    description = TextAreaField(label="Description", validators=[DataRequired()])
    btn_ajouter = SubmitField(label="ajouter")
    btn_annuler = SubmitField(label="annuler")