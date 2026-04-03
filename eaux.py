from flask import Blueprint, render_template, redirect, url_for, flash
from app import db
from app.models import Vehicule
from app.forms import VehiculeForm

vehicules_bp = Blueprint("vehicules", __name__)

@vehicules_bp.route("/")
def index():
    vehicules = Vehicule.query.order_by(Vehicule.immatricule).all()
    return render_template("vehicules/index.html", vehicules=vehicules)

@vehicules_bp.route("/nouveau", methods=["GET", "POST"])
def nouveau():
    form = VehiculeForm()
    if form.validate_on_submit():
        v = Vehicule(immatricule=form.immatricule.data, capacite=form.capacite.data)
        db.session.add(v)
        db.session.commit()
        flash(f"Véhicule {v.immatricule} créé.", "success")
        return redirect(url_for("vehicules.index"))
    return render_template("vehicules/form.html", form=form, titre="Nouveau véhicule")

@vehicules_bp.route("/<int:id>/modifier", methods=["GET", "POST"])
def modifier(id):
    v = Vehicule.query.get_or_404(id)
    form = VehiculeForm(obj=v)
    if form.validate_on_submit():
        form.populate_obj(v)
        db.session.commit()
        flash("Mis à jour.", "success")
        return redirect(url_for("vehicules.index"))
    return render_template("vehicules/form.html", form=form, titre="Modifier")

@vehicules_bp.route("/<int:id>/supprimer", methods=["POST"])
def supprimer(id):
    v = Vehicule.query.get_or_404(id)
    db.session.delete(v)
    db.session.commit()
    flash("Véhicule supprimé.", "warning")
    return redirect(url_for("vehicules.index"))
