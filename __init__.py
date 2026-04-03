from flask import Blueprint, render_template, redirect, url_for, flash
from app import db
from app.models import Eau, FosseSeptique
from app.forms import EauForm

eaux_bp = Blueprint("eaux", __name__)

def _populate(form):
    form.fosse_id.choices = [
        (f.id, f"Fosse #{f.id}") for f in FosseSeptique.query.all()
    ]

@eaux_bp.route("/")
def index():
    eaux = Eau.query.order_by(Eau.created_at.desc()).all()
    return render_template("eaux/index.html", eaux=eaux)

@eaux_bp.route("/nouveau", methods=["GET", "POST"])
def nouveau():
    form = EauForm()
    _populate(form)
    if form.validate_on_submit():
        e = Eau(
            type_eaux=form.type_eaux.data,
            volumetrique=form.volumetrique.data,
            niveau_contamination=form.niveau_contamination.data or None,
            fosse_id=form.fosse_id.data,
        )
        db.session.add(e)
        db.session.commit()
        flash("Eau enregistrée.", "success")
        return redirect(url_for("eaux.index"))
    return render_template("eaux/form.html", form=form, titre="Nouvelle eau")

@eaux_bp.route("/<int:id>/modifier", methods=["GET", "POST"])
def modifier(id):
    e = Eau.query.get_or_404(id)
    form = EauForm(obj=e)
    _populate(form)
    if form.validate_on_submit():
        form.populate_obj(e)
        db.session.commit()
        flash("Mis à jour.", "success")
        return redirect(url_for("eaux.index"))
    return render_template("eaux/form.html", form=form, titre="Modifier")

@eaux_bp.route("/<int:id>/supprimer", methods=["POST"])
def supprimer(id):
    e = Eau.query.get_or_404(id)
    db.session.delete(e)
    db.session.commit()
    flash("Supprimé.", "warning")
    return redirect(url_for("eaux.index"))
