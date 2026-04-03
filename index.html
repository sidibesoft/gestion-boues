"""
Formulaires WTForms — Gestion des Boues de Vidange
"""

from flask_wtf import FlaskForm
from wtforms import (
    StringField, FloatField, IntegerField, TextAreaField,
    SelectField, EmailField, SubmitField
)
from wtforms.validators import DataRequired, Optional, Email, Length


# ── Commune ──────────────────────────────────
class CommuneForm(FlaskForm):
    libelle_c = StringField("Libellé", validators=[DataRequired(), Length(max=120)])
    longitude = FloatField("Longitude", validators=[Optional()])
    latitude  = FloatField("Latitude",  validators=[Optional()])
    submit    = SubmitField("Enregistrer")


# ── Station de Traitement ─────────────────────
class StationForm(FlaskForm):
    libelle_statio = StringField("Nom de la station", validators=[DataRequired(), Length(max=150)])
    traitement     = StringField("Type de traitement", validators=[Optional()])
    lots           = IntegerField("Nombre de lots", validators=[Optional()])
    logs           = TextAreaField("Logs", validators=[Optional()])
    description_s  = TextAreaField("Description", validators=[Optional()])
    commune_id     = SelectField("Commune", coerce=int, validators=[DataRequired()])
    submit         = SubmitField("Enregistrer")


# ── Fosse Septique ─────────────────────────────
class FosseForm(FlaskForm):
    longueur_p = FloatField("Longueur (m)", validators=[Optional()])
    largeur_f  = FloatField("Largeur (m)",  validators=[Optional()])
    submit     = SubmitField("Enregistrer")


# ── Eau ────────────────────────────────────────
class EauForm(FlaskForm):
    type_eaux            = StringField("Type d'eau", validators=[DataRequired()])
    volumetrique         = FloatField("Volume (m³)", validators=[Optional()])
    niveau_contamination = SelectField(
        "Niveau de contamination",
        choices=[("", "—"), ("Faible", "Faible"), ("Moyen", "Moyen"), ("Élevé", "Élevé")],
        validators=[Optional()]
    )
    fosse_id = SelectField("Fosse septique", coerce=int, validators=[DataRequired()])
    submit   = SubmitField("Enregistrer")


# ── Véhicule ───────────────────────────────────
class VehiculeForm(FlaskForm):
    immatricule = StringField("Immatriculation", validators=[DataRequired(), Length(max=20)])
    capacite    = FloatField("Capacité (m³)", validators=[Optional()])
    submit      = SubmitField("Enregistrer")


# ── Ménage ─────────────────────────────────────
class MenageForm(FlaskForm):
    latitude   = FloatField("Latitude",  validators=[Optional()])
    longitude  = FloatField("Longitude", validators=[Optional()])
    contact    = StringField("Contact téléphonique", validators=[Optional(), Length(max=30)])
    email      = EmailField("Email", validators=[Optional(), Email()])
    commune_id = SelectField("Commune", coerce=int, validators=[DataRequired()])
    submit     = SubmitField("Enregistrer")


# ── Personnel ──────────────────────────────────
class PersonnelForm(FlaskForm):
    nom_p   = StringField("Nom complet", validators=[DataRequired(), Length(max=100)])
    contact = StringField("Contact",     validators=[Optional(), Length(max=30)])
    email_c = EmailField("Email",        validators=[Optional(), Email()])
    submit  = SubmitField("Enregistrer")


# ── Chauffeur ──────────────────────────────────
class ChauffeurForm(FlaskForm):
    nom_ch      = StringField("Nom complet", validators=[DataRequired(), Length(max=100)])
    contact     = StringField("Contact",     validators=[Optional(), Length(max=30)])
    email       = EmailField("Email",        validators=[Optional(), Email()])
    vehicule_id = SelectField("Véhicule assigné", coerce=int, validators=[Optional()])
    submit      = SubmitField("Enregistrer")


# ── Équipement ─────────────────────────────────
class EquipementForm(FlaskForm):
    libelle_e = StringField("Libellé",        validators=[DataRequired(), Length(max=150)])
    type_eqt  = StringField("Type",           validators=[Optional(), Length(max=80)])
    annee     = IntegerField("Année",         validators=[Optional()])
    submit    = SubmitField("Enregistrer")
