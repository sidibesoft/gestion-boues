from flask import Blueprint, render_template
from app.models import (
    Commune, StationTraitement, FosseSeptique,
    Eau, Vehicule, Menage, Chauffeur, Personnel, Equipement
)

main_bp = Blueprint("main", __name__)

@main_bp.route("/")
def dashboard():
    stats = {
        "communes":   Commune.query.count(),
        "stations":   StationTraitement.query.count(),
        "fosses":     FosseSeptique.query.count(),
        "eaux":       Eau.query.count(),
        "vehicules":  Vehicule.query.count(),
        "menages":    Menage.query.count(),
        "chauffeurs": Chauffeur.query.count(),
        "personnels": Personnel.query.count(),
        "equipements":Equipement.query.count(),
    }
    # Dernières fosses enregistrées
    dernières_fosses = FosseSeptique.query.order_by(
        FosseSeptique.created_at.desc()
    ).limit(5).all()

    return render_template("dashboard.html", stats=stats, fosses=dernières_fosses)
