from flask import Blueprint, render_template, redirect, url_for, flash
from app import db
from app.models import Personnel
from app.forms import PersonnelForm

personnels_bp = Blueprint("personnels", __name__)

@personnels_bp.route("/")
def index():
    personnels = Personnel.query.order_by(Personnel.nom_p).all()
    return render_template("personnels/index.html", personnels=personnels)

@personnels_bp.route("/nouveau", methods=["GET", "POST"])
def nouveau():
    form = PersonnelForm()
    if form.validate_on_submit():
        p = Personnel(nom_p=form.nom_p.data, contact=form.contact.data, email_c=form.email_c.data)
        db.session.add(p)
        db.session.commit()
        flash(f"{p.nom_p} ajouté.", "success")
        return redirect(url_for("personnels.index"))
    return render_template("personnels/form.html", form=form, titre="Nouveau personnel")

@personnels_bp.route("/<int:id>/modifier", methods=["GET", "POST"])
def modifier(id):
    p = Personnel.query.get_or_404(id)
    form = PersonnelForm(obj=p)
    if form.validate_on_submit():
        form.populate_obj(p)
        db.session.commit()
        flash("Mis à jour.", "success")
        return redirect(url_for("personnels.index"))
    return render_template("personnels/form.html", form=form, titre="Modifier")

@personnels_bp.route("/<int:id>/supprimer", methods=["POST"])
def supprimer(id):
    p = Personnel.query.get_or_404(id)
    db.session.delete(p)
    db.session.commit()
    flash("Supprimé.", "warning")
    return redirect(url_for("personnels.index"))
