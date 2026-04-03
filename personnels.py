from flask import Blueprint, render_template, redirect, url_for, flash
from app import db
from app.models import Commune
from app.forms import CommuneForm

communes_bp = Blueprint("communes", __name__)

@communes_bp.route("/")
def index():
    communes = Commune.query.order_by(Commune.libelle_c).all()
    return render_template("communes/index.html", communes=communes)

@communes_bp.route("/nouveau", methods=["GET", "POST"])
def nouveau():
    form = CommuneForm()
    if form.validate_on_submit():
        c = Commune(
            libelle_c=form.libelle_c.data,
            longitude=form.longitude.data,
            latitude=form.latitude.data,
        )
        db.session.add(c)
        db.session.commit()
        flash(f"Commune « {c.libelle_c} » créée.", "success")
        return redirect(url_for("communes.index"))
    return render_template("communes/form.html", form=form, titre="Nouvelle commune")

@communes_bp.route("/<int:id>/modifier", methods=["GET", "POST"])
def modifier(id):
    c = Commune.query.get_or_404(id)
    form = CommuneForm(obj=c)
    if form.validate_on_submit():
        form.populate_obj(c)
        db.session.commit()
        flash("Commune mise à jour.", "success")
        return redirect(url_for("communes.index"))
    return render_template("communes/form.html", form=form, titre="Modifier la commune")

@communes_bp.route("/<int:id>/supprimer", methods=["POST"])
def supprimer(id):
    c = Commune.query.get_or_404(id)
    db.session.delete(c)
    db.session.commit()
    flash("Commune supprimée.", "warning")
    return redirect(url_for("communes.index"))
