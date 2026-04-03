import os
from app import create_app, db
from app.models import (
    Commune, StationTraitement, FosseSeptique,
    Eau, Vehicule, Menage, Chauffeur, Personnel, Equipement
)

app = create_app(os.environ.get("FLASK_ENV", "default"))

@app.shell_context_processor
def make_shell_context():
    return dict(
        db=db,
        Commune=Commune,
        StationTraitement=StationTraitement,
        FosseSeptique=FosseSeptique,
        Eau=Eau,
        Vehicule=Vehicule,
        Menage=Menage,
        Chauffeur=Chauffeur,
        Personnel=Personnel,
        Equipement=Equipement,
    )

if __name__ == "__main__":
    app.run(debug=True)
