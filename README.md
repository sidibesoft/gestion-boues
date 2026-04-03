# 🌊 GBV — Gestion des Boues de Vidange
> Application web Flask de gestion complète du cycle de vie des boues de vidange : fosses septiques, stations de traitement, ménages, flotte de véhicules et personnel.

---

## 📐 Architecture — MCD retranscrit

```
Commune ──(POSSEDER)──> StationTraitement
    |                          |
(APPARTENIR)              (DÉVERSER)
    |                          |
  Ménage <──(CONCERNER)── FosseSeptique ──(CONTENIR)──> Eau
                                                          |
                                                    (TRANSFÉRER)
                                                          |
Chauffeur ──(CONDUIRE)──> Véhicule <────────────────────┘
```

**Relations implémentées :**
| Relation | Type | Tables |
|---|---|---|
| POSSEDER | 1,N | `commune` → `station_traitement` |
| APPARTENIR | 1,N | `commune` → `menage` |
| DÉVERSER | M,N | `station_traitement` ↔ `fosse_septique` (table `deverser`) |
| CONCERNER | M,N | `fosse_septique` ↔ `menage` (table `concerner`) |
| CONTENIR | 1,N | `fosse_septique` → `eau` |
| TRANSFÉRER | M,N | `eau` ↔ `vehicule` (table `transferer`) |
| CONDUIRE | 1,1 | `chauffeur` → `vehicule` |

---

## 🗂 Structure du projet

```
gestion_boues/
├── app/
│   ├── __init__.py          # Factory pattern Flask
│   ├── models.py            # Tous les modèles SQLAlchemy
│   ├── forms.py             # Formulaires WTForms
│   ├── routes/
│   │   ├── main.py          # Dashboard
│   │   ├── communes.py
│   │   ├── stations.py
│   │   ├── fosses.py
│   │   ├── eaux.py
│   │   ├── vehicules.py
│   │   ├── menages.py
│   │   ├── chauffeurs.py
│   │   ├── personnels.py
│   │   └── equipements.py
│   └── templates/
│       ├── base.html        # Layout principal (sidebar verte)
│       ├── dashboard.html
│       ├── _macros.html     # Macro render_field
│       ├── communes/        # index.html + form.html
│       ├── stations/        # index.html + form.html + detail.html
│       ├── fosses/          # index.html + form.html + detail.html
│       ├── eaux/
│       ├── vehicules/
│       ├── menages/
│       ├── chauffeurs/
│       ├── personnels/
│       └── equipements/
├── config.py                # Dev / Prod / Test
├── run.py                   # Point d'entrée
├── Procfile                 # Déploiement Render/Heroku
├── requirements.txt
├── .env.example
└── .gitignore
```

---

## ⚙️ PARTIE 1 — Installation et préparation de l'environnement

### 1.1 Prérequis

- Python 3.10 ou supérieur
- Git
- (Optionnel pour la prod) PostgreSQL 14+

### 1.2 Cloner le projet

```bash
git clone https://github.com/votre-utilisateur/gestion_boues.git
cd gestion_boues
```

### 1.3 Créer et activer l'environnement virtuel

```bash
# Créer l'environnement
python -m venv venv

# Activer (Linux / macOS)
source venv/bin/activate

# Activer (Windows PowerShell)
.\venv\Scripts\Activate.ps1

# Activer (Windows CMD)
venv\Scripts\activate.bat
```

> Le prompt doit afficher `(venv)` devant votre ligne de commande.

### 1.4 Installer les dépendances

```bash
pip install -r requirements.txt
```

### 1.5 Configurer les variables d'environnement

```bash
# Copier le fichier d'exemple
cp .env.example .env

# Éditer .env
nano .env   # ou notepad .env sous Windows
```

Contenu minimal du `.env` pour le développement :

```dotenv
FLASK_APP=run.py
FLASK_ENV=development
SECRET_KEY=une-cle-secrete-tres-longue-et-aleatoire
DEV_DATABASE_URL=sqlite:///boues_dev.db
```

---

## 🗄️ PARTIE 2 — Base de données

### 2.1 Initialiser Flask-Migrate

```bash
flask db init
```

### 2.2 Générer la première migration

```bash
flask db migrate -m "Initial schema — toutes les tables GBV"
```

### 2.3 Appliquer la migration (créer les tables)

```bash
flask db upgrade
```

> Les tables suivantes sont créées : `commune`, `station_traitement`, `fosse_septique`,
> `eau`, `vehicule`, `menage`, `chauffeur`, `personnel`, `equipement`,
> `deverser`, `concerner`, `transferer`.

### 2.4 (Optionnel) Insérer des données de test

```bash
flask shell
```

```python
from app import db
from app.models import Commune, StationTraitement, FosseSeptique, Eau, Vehicule, Menage, Chauffeur

# Créer une commune
c = Commune(libelle_c="Abidjan Plateau", longitude=-3.9969, latitude=5.3600)
db.session.add(c)
db.session.flush()

# Créer une station
s = StationTraitement(libelle_statio="STEP Abidjan Nord", traitement="Lagunage aéré", lots=3, commune_id=c.id)
db.session.add(s)
db.session.flush()

# Créer une fosse
f = FosseSeptique(longueur_p=4.0, largeur_f=2.5)
db.session.add(f)
db.session.flush()

# Lier la fosse à la station (DÉVERSER)
f.stations.append(s)

# Créer une eau
e = Eau(type_eaux="Boues primaires", volumetrique=5.5, niveau_contamination="Élevé", fosse_id=f.id)
db.session.add(e)

db.session.commit()
print("Données insérées !")
exit()
```

---

## 🚀 PARTIE 3 — Lancer l'application en développement

```bash
flask run
```

ou directement :

```bash
python run.py
```

Ouvrez votre navigateur sur : **http://127.0.0.1:5000**

Vous verrez le **tableau de bord** avec les compteurs de chaque entité et les accès rapides.

---

## 🧪 PARTIE 4 — Tests

### 4.1 Créer le fichier de tests

```bash
mkdir tests
touch tests/__init__.py
touch tests/test_models.py
```

**`tests/test_models.py`**

```python
import pytest
from app import create_app, db
from app.models import Commune, FosseSeptique, Eau

@pytest.fixture
def app():
    app = create_app("testing")
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

def test_commune_creation(app):
    with app.app_context():
        c = Commune(libelle_c="Test Commune", longitude=-3.99, latitude=5.36)
        db.session.add(c)
        db.session.commit()
        assert Commune.query.count() == 1
        assert Commune.query.first().libelle_c == "Test Commune"

def test_fosse_volume(app):
    with app.app_context():
        f = FosseSeptique(longueur_p=4.0, largeur_f=3.0)
        db.session.add(f)
        db.session.commit()
        assert f.volume_theorique == 12.0

def test_dashboard_route(client):
    response = client.get("/")
    assert response.status_code == 200

def test_communes_index(client):
    response = client.get("/communes/")
    assert response.status_code == 200
```

### 4.2 Lancer les tests

```bash
pip install pytest
pytest tests/ -v
```

---

## 🌐 PARTIE 5 — Déploiement en production

### Option A — Render.com (recommandé, gratuit)

#### 5.A.1 Préparer le projet pour PostgreSQL

Vérifiez que `requirements.txt` contient `psycopg2-binary` et `gunicorn`. ✅

#### 5.A.2 Pousser sur GitHub

```bash
git init
git add .
git commit -m "Initial commit — GBV Flask"
git remote add origin https://github.com/votre-utilisateur/gestion_boues.git
git push -u origin main
```

#### 5.A.3 Créer le service sur Render

1. Aller sur [render.com](https://render.com) → **New Web Service**
2. Connecter votre dépôt GitHub
3. Configurer :

| Champ | Valeur |
|---|---|
| **Runtime** | Python 3 |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `gunicorn run:app` |

4. Ajouter les **variables d'environnement** :

| Variable | Valeur |
|---|---|
| `SECRET_KEY` | `<générer une clé aléatoire>` |
| `FLASK_ENV` | `production` |
| `DATABASE_URL` | *(copiée depuis Render PostgreSQL)* |

#### 5.A.4 Créer la base PostgreSQL sur Render

1. **New → PostgreSQL** → Créer
2. Copier **Internal Database URL**
3. La coller dans la variable `DATABASE_URL` du service web

#### 5.A.5 Appliquer les migrations en production

Dans le terminal Render (Shell) ou via un **Job** :

```bash
flask db upgrade
```

---

### Option B — VPS (Ubuntu 22.04) avec Nginx + Gunicorn

#### 5.B.1 Préparer le serveur

```bash
# Sur le VPS
sudo apt update && sudo apt install -y python3-pip python3-venv nginx postgresql

# Créer un utilisateur dédié
sudo adduser gbv
sudo su - gbv
```

#### 5.B.2 Déployer le code

```bash
git clone https://github.com/votre-utilisateur/gestion_boues.git
cd gestion_boues
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

#### 5.B.3 Créer la base PostgreSQL

```bash
sudo -u postgres psql
```

```sql
CREATE DATABASE gestion_boues;
CREATE USER gbv_user WITH PASSWORD 'MotDePasseSolide';
GRANT ALL PRIVILEGES ON DATABASE gestion_boues TO gbv_user;
\q
```

#### 5.B.4 Configurer `.env` en production

```dotenv
FLASK_ENV=production
SECRET_KEY=une-cle-aleatoire-de-64-caracteres
DATABASE_URL=postgresql://gbv_user:MotDePasseSolide@localhost:5432/gestion_boues
```

#### 5.B.5 Initialiser la DB et tester Gunicorn

```bash
flask db upgrade
gunicorn --bind 0.0.0.0:8000 run:app
# Ctrl+C pour arrêter
```

#### 5.B.6 Créer le service systemd

```bash
sudo nano /etc/systemd/system/gbv.service
```

```ini
[Unit]
Description=GBV Flask Application
After=network.target

[Service]
User=gbv
WorkingDirectory=/home/gbv/gestion_boues
Environment="PATH=/home/gbv/gestion_boues/venv/bin"
EnvironmentFile=/home/gbv/gestion_boues/.env
ExecStart=/home/gbv/gestion_boues/venv/bin/gunicorn --workers 3 --bind unix:/tmp/gbv.sock run:app

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl daemon-reload
sudo systemctl start gbv
sudo systemctl enable gbv
sudo systemctl status gbv
```

#### 5.B.7 Configurer Nginx

```bash
sudo nano /etc/nginx/sites-available/gbv
```

```nginx
server {
    listen 80;
    server_name votre-domaine.com;

    location / {
        include proxy_params;
        proxy_pass http://unix:/tmp/gbv.sock;
    }

    location /static/ {
        alias /home/gbv/gestion_boues/app/static/;
    }
}
```

```bash
sudo ln -s /etc/nginx/sites-available/gbv /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

#### 5.B.8 Activer HTTPS avec Let's Encrypt

```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d votre-domaine.com
```

---

## 📋 PARTIE 6 — Fonctionnalités disponibles

| Module | URL | Actions |
|---|---|---|
| Dashboard | `/` | Vue d'ensemble, statistiques |
| Communes | `/communes/` | Liste, Créer, Modifier, Supprimer |
| Stations | `/stations/` | Liste, Créer, Modifier, Supprimer, Détail + fosses liées |
| Fosses | `/fosses/` | Liste, Créer, Modifier, Détail + associer ménages/stations |
| Eaux | `/eaux/` | Liste, Créer, Modifier, Supprimer |
| Véhicules | `/vehicules/` | Liste, Créer, Modifier, Supprimer |
| Ménages | `/menages/` | Liste, Créer, Modifier, Supprimer |
| Chauffeurs | `/chauffeurs/` | Liste, Créer, Modifier, Supprimer + assignation véhicule |
| Personnel | `/personnels/` | Liste, Créer, Modifier, Supprimer |
| Équipements | `/equipements/` | Liste, Créer, Modifier, Supprimer |

---

## 🔒 Sécurité

- Protection CSRF activée sur tous les formulaires via `Flask-WTF`
- `SECRET_KEY` obligatoirement définie en variable d'environnement
- Validation des données côté serveur (WTForms validators)
- Ne jamais committer le fichier `.env` (protégé par `.gitignore`)

---

## 🔧 Commandes utiles

```bash
# Lancer en développement
flask run

# Ouvrir le shell interactif
flask shell

# Nouvelle migration après modification des modèles
flask db migrate -m "Description du changement"
flask db upgrade

# Réinitialiser la DB en développement
flask shell
>>> db.drop_all()
>>> db.create_all()
>>> exit()

# Voir les routes enregistrées
flask routes
```

---

## 🛠️ Stack technique

| Composant | Technologie |
|---|---|
| Framework web | Flask 3.0 |
| ORM | SQLAlchemy + Flask-SQLAlchemy |
| Migrations | Flask-Migrate (Alembic) |
| Formulaires | Flask-WTF + WTForms |
| Base de données | SQLite (dev) / PostgreSQL (prod) |
| Serveur WSGI | Gunicorn |
| Front-end | Bootstrap 5 + Bootstrap Icons |

---

*Projet GBV — Gestion des Boues de Vidange | Flask Application*
