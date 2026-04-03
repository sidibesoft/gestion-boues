from flask import Blueprint, render_template, redirect, url_for, flash
from app import db
from app.models import Equipement
from app.forms import EquipementForm

equipements_bp = Blueprint("equipements", __name__)

@equipements_bp.route("/")
def index():
    equipements = Equipement.query.order_by(Equipement.libelle_e).all()
    return render_template("equipements/index.html", equipements=equipements)

@equipements_bp.route("/nouveau", methods=["GET", "POST"])
def nouveau():
    form = EquipementForm()
    if form.validate_on_submit():
        e = Equipement(libelle_e=form.libelle_e.data, type_eqt=form.type_eqt.data, annee=form.annee.data)
        db.session.add(e)
        db.session.commit()
        flash(f"Équipement « {e.libelle_e} » ajouté.", "success")
        return redirect(url_for("equipements.index"))
    return render_template("equipements/form.html", form=form, titre="Nouvel équipement")

@equipements_bp.route("/<int:id>/modifier", methods=["GET", "POST"])
def modifier(id):
    e = Equipement.query.get_or_404(id)
    form = EquipementForm(obj=e)
    if form.validate_on_submit():
        form.populate_obj(e)
        db.session.commit()
        flash("Mis à jour.", "success")
        return redirect(url_for("equipements.index"))
    return render_template("equipements/form.html", form=form, titre="Modifier")

@equipements_bp.route("/<int:id>/supprimer", methods=["POST"])
def supprimer(id):
    e = Equipement.query.get_or_404(id)
    db.session.delete(e)
    db.session.commit()
    flash("Supprimé.", "warning")
    return redirect(url_for("equipements.index"))
