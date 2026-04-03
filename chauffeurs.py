from flask import Blueprint, render_template, redirect, url_for, flash
from app import db
from app.models import StationTraitement, Commune
from app.forms import StationForm

stations_bp = Blueprint("stations", __name__)

def _populate_choices(form):
    form.commune_id.choices = [
        (c.id, c.libelle_c) for c in Commune.query.order_by(Commune.libelle_c).all()
    ]

@stations_bp.route("/")
def index():
    stations = StationTraitement.query.order_by(StationTraitement.libelle_statio).all()
    return render_template("stations/index.html", stations=stations)

@stations_bp.route("/nouveau", methods=["GET", "POST"])
def nouveau():
    form = StationForm()
    _populate_choices(form)
    if form.validate_on_submit():
        s = StationTraitement(
            libelle_statio=form.libelle_statio.data,
            traitement=form.traitement.data,
            lots=form.lots.data,
            logs=form.logs.data,
            description_s=form.description_s.data,
            commune_id=form.commune_id.data,
        )
        db.session.add(s)
        db.session.commit()
        flash(f"Station « {s.libelle_statio} » créée.", "success")
        return redirect(url_for("stations.index"))
    return render_template("stations/form.html", form=form, titre="Nouvelle station")

@stations_bp.route("/<int:id>")
def detail(id):
    s = StationTraitement.query.get_or_404(id)
    return render_template("stations/detail.html", station=s)

@stations_bp.route("/<int:id>/modifier", methods=["GET", "POST"])
def modifier(id):
    s = StationTraitement.query.get_or_404(id)
    form = StationForm(obj=s)
    _populate_choices(form)
    if form.validate_on_submit():
        form.populate_obj(s)
        db.session.commit()
        flash("Station mise à jour.", "success")
        return redirect(url_for("stations.index"))
    return render_template("stations/form.html", form=form, titre="Modifier la station")

@stations_bp.route("/<int:id>/supprimer", methods=["POST"])
def supprimer(id):
    s = StationTraitement.query.get_or_404(id)
    db.session.delete(s)
    db.session.commit()
    flash("Station supprimée.", "warning")
    return redirect(url_for("stations.index"))
