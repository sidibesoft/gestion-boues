from flask import Blueprint, render_template, redirect, url_for, flash
from app import db
from app.models import Chauffeur, Vehicule
from app.forms import ChauffeurForm

chauffeurs_bp = Blueprint("chauffeurs", __name__)

def _populate(form):
    dispo = Vehicule.query.filter(
        ~Vehicule.id.in_([
            c.vehicule_id for c in Chauffeur.query.filter(
                Chauffeur.vehicule_id.isnot(None)
            ).all()
        ])
    ).all()
    form.vehicule_id.choices = [(0, "— Aucun —")] + [
        (v.id, v.immatricule) for v in dispo
    ]

@chauffeurs_bp.route("/")
def index():
    chauffeurs = Chauffeur.query.order_by(Chauffeur.nom_ch).all()
    return render_template("chauffeurs/index.html", chauffeurs=chauffeurs)

@chauffeurs_bp.route("/nouveau", methods=["GET", "POST"])
def nouveau():
    form = ChauffeurForm()
    _populate(form)
    if form.validate_on_submit():
        c = Chauffeur(
            nom_ch=form.nom_ch.data,
            contact=form.contact.data,
            email=form.email.data,
            vehicule_id=form.vehicule_id.data or None,
        )
        db.session.add(c)
        db.session.commit()
        flash(f"Chauffeur {c.nom_ch} créé.", "success")
        return redirect(url_for("chauffeurs.index"))
    return render_template("chauffeurs/form.html", form=form, titre="Nouveau chauffeur")

@chauffeurs_bp.route("/<int:id>/modifier", methods=["GET", "POST"])
def modifier(id):
    c = Chauffeur.query.get_or_404(id)
    form = ChauffeurForm(obj=c)
    _populate(form)
    # Inclure le véhicule actuel dans les choix
    if c.vehicule_id:
        v = Vehicule.query.get(c.vehicule_id)
        if v and (c.vehicule_id, v.immatricule) not in form.vehicule_id.choices:
            form.vehicule_id.choices.append((c.vehicule_id, v.immatricule))
    if form.validate_on_submit():
        form.populate_obj(c)
        c.vehicule_id = form.vehicule_id.data or None
        db.session.commit()
        flash("Mis à jour.", "success")
        return redirect(url_for("chauffeurs.index"))
    return render_template("chauffeurs/form.html", form=form, titre="Modifier")

@chauffeurs_bp.route("/<int:id>/supprimer", methods=["POST"])
def supprimer(id):
    c = Chauffeur.query.get_or_404(id)
    db.session.delete(c)
    db.session.commit()
    flash("Chauffeur supprimé.", "warning")
    return redirect(url_for("chauffeurs.index"))
