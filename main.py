from flask import Blueprint, render_template, redirect, url_for, flash
from app import db
from app.models import Menage, Commune
from app.forms import MenageForm

menages_bp = Blueprint("menages", __name__)

def _populate(form):
    form.commune_id.choices = [
        (c.id, c.libelle_c) for c in Commune.query.order_by(Commune.libelle_c).all()
    ]

@menages_bp.route("/")
def index():
    menages = Menage.query.order_by(Menage.created_at.desc()).all()
    return render_template("menages/index.html", menages=menages)

@menages_bp.route("/nouveau", methods=["GET", "POST"])
def nouveau():
    form = MenageForm()
    _populate(form)
    if form.validate_on_submit():
        m = Menage(
            latitude=form.latitude.data,
            longitude=form.longitude.data,
            contact=form.contact.data,
            email=form.email.data,
            commune_id=form.commune_id.data,
        )
        db.session.add(m)
        db.session.commit()
        flash(f"Ménage #{m.id} créé.", "success")
        return redirect(url_for("menages.index"))
    return render_template("menages/form.html", form=form, titre="Nouveau ménage")

@menages_bp.route("/<int:id>/modifier", methods=["GET", "POST"])
def modifier(id):
    m = Menage.query.get_or_404(id)
    form = MenageForm(obj=m)
    _populate(form)
    if form.validate_on_submit():
        form.populate_obj(m)
        db.session.commit()
        flash("Mis à jour.", "success")
        return redirect(url_for("menages.index"))
    return render_template("menages/form.html", form=form, titre="Modifier")

@menages_bp.route("/<int:id>/supprimer", methods=["POST"])
def supprimer(id):
    m = Menage.query.get_or_404(id)
    db.session.delete(m)
    db.session.commit()
    flash("Ménage supprimé.", "warning")
    return redirect(url_for("menages.index"))
