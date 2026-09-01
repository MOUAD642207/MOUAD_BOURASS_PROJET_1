# 🇲🇦 Maroc Invest - Plateforme d'Investissement

## 📋 Présentation du Projet

**Maroc Invest** est une plateforme web complète dédiée à la **promotion de l'investissement au Maroc**. Elle offre une vision globale des opportunités économiques, des grands projets structurants et des indicateurs clés du Royaume.

### 🎯 Objectifs du site

- **Informer** : Mettre à disposition des données économiques et démographiques fiables
- **Visualiser** : Proposer des cartes interactives et des graphiques dynamiques
- **Attirer** : Encourager les investisseurs nationaux et internationaux
- **Connecter** : Mettre en relation les investisseurs avec les organismes compétents
- **Veiller** : Assurer une veille économique via des médias et sources officielles

---

## ✨ Fonctionnalités principales

### 1. 🗺️ Carte Interactive des Régions
- Visualisation des 12 régions du Maroc
- Données : superficie, population, densité, chef-lieu
- Zoom, déplacement et sélection des régions
- Tableau de bord régional détaillé

### 2. 📊 Dashboard Économique (Streamlit)
- Indicateurs clés (PIB, chômage, inflation, etc.)
- Graphiques interactifs (Plotly)
- Évolution démographique (1960-2050)
- Analyse du marché du travail
- Budget de l'État par ministère
- Taux de scolarisation par cycle

### 3. 📬 Newsletter
- Formulaire d'inscription
- API FastAPI pour la gestion des abonnés
- Stockage des données dans `subscribers.json`
- Envoi de newsletters (script `send_newsletter.py`)

### 4. 📈 Veille Économique
- Accès aux principaux médias économiques : Hespress, Le Desk, Médias24, La Vie éco, Hiba Press, Le360, Bank Al-Maghrib, HCP, MAP
- Ressources officielles pour l'investissement

### 5. 💼 Opportunités d'Investissement
- Secteurs porteurs : Énergies renouvelables, Industrie, Digital, Tourisme, AgriTech, FinTech
- Avantages fiscaux et financiers
- Focus sur les provinces du Sud (Dakhla, Laâyoune)
- Budget alloué > 77 milliards DH depuis 2015

---

## 🛠️ Technologies Utilisées

### Frontend
- HTML5 : Structure des pages
- CSS3 : Mise en page et design
- Bootstrap 5 : Framework responsive
- JavaScript : Interactions dynamiques
- Plotly.js : Graphiques interactifs

### Backend
- Python 3.9+ : Langage principal
- Streamlit : Dashboard interactif
- FastAPI : API REST pour la newsletter
- Uvicorn : Serveur ASGI

### Données
- JSON : Stockage des données
- Pandas : Manipulation des données
- NumPy : Calculs numériques

### Déploiement
- Git : Contrôle de version
- GitHub : Hébergement du code

---


---

## 🚀 Comment Lancer le Projet

### Prérequis

Avant de commencer, assurez-vous d'avoir :

- Python 3.9 ou supérieur : [python.org](https://www.python.org/)
- Git : [git-scm.com](https://git-scm.com/)
- Navigateur : Chrome/Firefox/Edge

---

### Installation des Dépendances

```bash
# 1. Ouvrir un terminal dans le dossier du projet
cd MOUAD_BOURASS_PROJET_1

# 2. Installer les dépendances Python
pip install streamlit pandas numpy plotly fastapi uvicorn requests

# OU avec un fichier requirements.txt
pip install -r requirements.txt




# Lancer le dashboard
streamlit run dashboard.py
📌 Accès : Ouvrez http://localhost:8501 dans votre navigateur



# Lancer l'API de la newsletter
uvicorn app:app --reload --port 8000
📌 Accès : Ouvrez http://localhost:8000 dans votre navigateur

Endpoints disponibles
Endpoint	Méthode	Description
/	GET	Formulaire newsletter
/api/subscribe	POST	Inscription à la newsletter
/api/stats	GET	Statistiques des abonnés
/api/subscribers	GET	Liste des abonnés
/api/newsletter-emails	GET	Emails des abonnés




# Méthode 1 : Ouvrir directement le fichier
# Double-cliquez sur index.html

# Méthode 2 : Avec un serveur Python
python -m http.server 8001
# Puis ouvrez http://localhost:8001

# Méthode 3 : Avec Node.js (si installé)
npx http-server -p 8001


# Exécuter le script d'envoi
python send_newsletter.py



