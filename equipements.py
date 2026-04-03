"""
Modèles SQLAlchemy — Gestion des Boues de Vidange
Basé sur le MCD fourni.
"""

from datetime import datetime
from app import db

# ─────────────────────────────────────────────
# Tables d'association (relations M:N)
# ─────────────────────────────────────────────

# DÉVERSER : Station ↔ FosseSeptique
deverser = db.Table(
    "deverser",
    db.Column("station_id", db.Integer, db.ForeignKey("station_traitement.id"), primary_key=True),
    db.Column("fosse_id",   db.Integer, db.ForeignKey("fosse_septique.id"),     primary_key=True),
    db.Column("date_depot", db.DateTime, default=datetime.utcnow),
)

# CONCERNER : FosseSeptique ↔ Ménage
concerner = db.Table(
    "concerner",
    db.Column("fosse_id",  db.Integer, db.ForeignKey("fosse_septique.id"), primary_key=True),
    db.Column("menage_id", db.Integer, db.ForeignKey("menage.id"),         primary_key=True),
)

# TRANSFÉRER : Eau ↔ Véhicule
transferer = db.Table(
    "transferer",
    db.Column("eau_id",       db.Integer,  db.ForeignKey("eau.id"),      primary_key=True),
    db.Column("vehicule_id",  db.Integer,  db.ForeignKey("vehicule.id"), primary_key=True),
    db.Column("date_transfert", db.DateTime, default=datetime.utcnow),
    db.Column("volume_transfere", db.Float, nullable=True),
)


# ─────────────────────────────────────────────
# Entités principales
# ─────────────────────────────────────────────

class Commune(db.Model):
    """Commune administrative."""
    __tablename__ = "commune"

    id         = db.Column(db.Integer, primary_key=True)
    libelle_c  = db.Column(db.String(120), nullable=False)
    longitude  = db.Column(db.Float, nullable=True)
    latitude   = db.Column(db.Float, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relations
    stations = db.relationship("StationTraitement", backref="commune", lazy="dynamic")
    menages  = db.relationship("Menage",            backref="commune", lazy="dynamic")

    def __repr__(self):
        return f"<Commune {self.libelle_c}>"

    def to_dict(self):
        return {
            "id": self.id, "libelle_c": self.libelle_c,
            "longitude": self.longitude, "latitude": self.latitude,
        }


class StationTraitement(db.Model):
    """Station de traitement des boues de vidange."""
    __tablename__ = "station_traitement"

    id            = db.Column(db.Integer, primary_key=True)
    libelle_statio = db.Column(db.String(150), nullable=False)
    traitement    = db.Column(db.String(100), nullable=True)
    lots          = db.Column(db.Integer,  nullable=True)
    logs          = db.Column(db.Text,     nullable=True)
    description_s = db.Column(db.Text,     nullable=True)
    commune_id    = db.Column(db.Integer, db.ForeignKey("commune.id"), nullable=False)
    created_at    = db.Column(db.DateTime, default=datetime.utcnow)

    # Relations
    fosses = db.relationship(
        "FosseSeptique", secondary=deverser, backref="stations", lazy="dynamic"
    )

    def __repr__(self):
        return f"<Station {self.libelle_statio}>"


class FosseSeptique(db.Model):
    """Fosse septique à vidanger."""
    __tablename__ = "fosse_septique"

    id          = db.Column(db.Integer, primary_key=True)
    longueur_p  = db.Column(db.Float, nullable=True, comment="Longueur en mètres")
    largeur_f   = db.Column(db.Float, nullable=True, comment="Largeur en mètres")
    created_at  = db.Column(db.DateTime, default=datetime.utcnow)

    # Relations
    eaux   = db.relationship("Eau",    backref="fosse", lazy="dynamic")
    menages = db.relationship(
        "Menage", secondary=concerner, backref="fosses", lazy="dynamic"
    )

    @property
    def volume_theorique(self):
        if self.longueur_p and self.largeur_f:
            return round(self.longueur_p * self.largeur_f, 2)
        return None

    def __repr__(self):
        return f"<FosseSeptique #{self.id}>"


class Eau(db.Model):
    """Eau/boue contenue dans une fosse septique."""
    __tablename__ = "eau"

    id                    = db.Column(db.Integer, primary_key=True)
    type_eaux             = db.Column(db.String(80), nullable=False)
    volumetrique          = db.Column(db.Float, nullable=True, comment="Volume en m³")
    niveau_contamination  = db.Column(db.String(50), nullable=True)  # ex: Faible/Moyen/Élevé
    fosse_id              = db.Column(db.Integer, db.ForeignKey("fosse_septique.id"), nullable=False)
    created_at            = db.Column(db.DateTime, default=datetime.utcnow)

    # Relations
    vehicules = db.relationship(
        "Vehicule", secondary=transferer, backref="eaux", lazy="dynamic"
    )

    def __repr__(self):
        return f"<Eau {self.type_eaux} — {self.volumetrique}m³>"


class Vehicule(db.Model):
    """Véhicule de transport des boues."""
    __tablename__ = "vehicule"

    id           = db.Column(db.Integer, primary_key=True)
    immatricule  = db.Column(db.String(20), unique=True, nullable=False)
    capacite     = db.Column(db.Float, nullable=True, comment="Capacité en m³")
    created_at   = db.Column(db.DateTime, default=datetime.utcnow)

    # Relations
    chauffeur = db.relationship("Chauffeur", backref="vehicule", uselist=False)

    def __repr__(self):
        return f"<Vehicule {self.immatricule}>"


class Menage(db.Model):
    """Ménage / foyer bénéficiaire du service."""
    __tablename__ = "menage"

    id         = db.Column(db.Integer, primary_key=True)
    latitude   = db.Column(db.Float, nullable=True)
    longitude  = db.Column(db.Float, nullable=True)
    contact    = db.Column(db.String(30), nullable=True)
    email      = db.Column(db.String(120), nullable=True)
    commune_id = db.Column(db.Integer, db.ForeignKey("commune.id"), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Ménage #{self.id} — {self.contact}>"


class Personnel(db.Model):
    """Personnel du service de vidange."""
    __tablename__ = "personnel"

    id        = db.Column(db.Integer, primary_key=True)
    nom_p     = db.Column(db.String(100), nullable=False)
    contact   = db.Column(db.String(30),  nullable=True)
    email_c   = db.Column(db.String(120), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Personnel {self.nom_p}>"


class Chauffeur(db.Model):
    """Chauffeur assigné à un véhicule."""
    __tablename__ = "chauffeur"

    id          = db.Column(db.Integer, primary_key=True)
    nom_ch      = db.Column(db.String(100), nullable=False)
    contact     = db.Column(db.String(30),  nullable=True)
    email       = db.Column(db.String(120), nullable=True)
    vehicule_id = db.Column(db.Integer, db.ForeignKey("vehicule.id"), nullable=True, unique=True)
    created_at  = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Chauffeur {self.nom_ch}>"


class Equipement(db.Model):
    """Équipement utilisé pour la vidange."""
    __tablename__ = "equipement"

    id          = db.Column(db.Integer, primary_key=True)
    libelle_e   = db.Column(db.String(150), nullable=False)
    type_eqt    = db.Column(db.String(80),  nullable=True)
    annee       = db.Column(db.Integer,     nullable=True)
    created_at  = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Equipement {self.libelle_e}>"
