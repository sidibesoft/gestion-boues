from flask import Blueprint, render_template, redirect, url_for, flash, request
from app import db
from app.models import FosseSeptique, StationTraitement, Menage
from app.forms import FosseForm

fosses_bp = Blueprint("fosses", __name__)

@fosses_bp.route("/")
def index():
    fosses = FosseSeptique.query.order_by(FosseSeptique.created_at.desc()).all()
    return render_template("fosses/index.html", fosses=fosses)

@fosses_bp.route("/nouveau", methods=["GET", "POST"])
def nouveau():
    form = FosseForm()
    if form.validate_on_submit():
        f = FosseSeptique(
            longueur_p=form.longueur_p.data,
            largeur_f=form.largeur_f.data,
        )
        db.session.add(f)
        db.session.commit()
        flash(f"Fosse #{f.id} créée.", "success")
        return redirect(url_for("fosses.index"))
    return render_template("fosses/form.html", form=form, titre="Nouvelle fosse")

@fosses_bp.route("/<int:id>")
def detail(id):
    f = FosseSeptique.query.get_or_404(id)
    stations_dispo = StationTraitement.query.all()
    menages_dispo  = Menage.query.all()
    return render_template(
        "fosses/detail.html", fosse=f,
        stations_dispo=stations_dispo,
        menages_dispo=menages_dispo
    )

@fosses_bp.route("/<int:id>/modifier", methods=["GET", "POST"])
def modifier(id):
    f = FosseSeptique.query.get_or_404(id)
    form = FosseForm(obj=f)
    if form.validate_on_submit():
        form.populate_obj(f)
        db.session.commit()
        flash("Fosse mise à jour.", "success")
        return redirect(url_for("fosses.index"))
    return render_template("fosses/form.html", form=form, titre="Modifier la fosse")

@fosses_bp.route("/<int:id>/supprimer", methods=["POST"])
def supprimer(id):
    f = FosseSeptique.query.get_or_404(id)
    db.session.delete(f)
    db.session.commit()
    flash("Fosse supprimée.", "warning")
    return redirect(url_for("fosses.index"))

@fosses_bp.route("/<int:fosse_id>/ajouter_station/<int:station_id>", methods=["POST"])
def ajouter_station(fosse_id, station_id):
    fosse   = FosseSeptique.query.get_or_404(fosse_id)
    station = StationTraitement.query.get_or_404(station_id)
    if station not in fosse.stations.all():
        fosse.stations.append(station)
        db.session.commit()
        flash(f"Station « {station.libelle_statio} » associée.", "success")
    return redirect(url_for("fosses.detail", id=fosse_id))

@fosses_bp.route("/<int:fosse_id>/ajouter_menage/<int:menage_id>", methods=["POST"])
def ajouter_menage(fosse_id, menage_id):
    fosse  = FosseSeptique.query.get_or_404(fosse_id)
    menage = Menage.query.get_or_404(menage_id)
    if menage not in fosse.menages.all():
        fosse.menages.append(menage)
        db.session.commit()
        flash(f"Ménage #{menage.id} associé.", "success")
    return redirect(url_for("fosses.detail", id=fosse_id))
