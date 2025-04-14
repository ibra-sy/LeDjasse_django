# 👗 LeDjassa

**LeDjassa** est une plateforme web complète développée avec Django, dédiée à la **vente de vêtements d’occasion** entre particuliers. Elle intègre un système de **blog**, une boutique e-commerce, une **messagerie interne**, une gestion des **rôles utilisateurs**, un **système d'achat sécurisé** avec confirmation par e-mail, et une **API REST sécurisée**.

🔗 **Dépôt GitHub** : [https://github.com/ibra-sy/LeDjasse_django.git](https://github.com/ibra-sy/LeDjasse_django.git)

---

## 🚀 Fonctionnalités principales

### 🛍️ E-commerce
- Catalogue de vêtements d’occasion
- Ajout, modification, suppression de produits (par les vendeurs)
- Achat avec confirmation d’adresse et e-mail
- Notification par e-mail à l'acheteur et au vendeur
- Validation finale de la vente par le vendeur

### 📝 Blog
- Rédaction d’articles (par les vendeurs)
- Commentaires & likes (par les utilisateurs)
- Système de tags pour classer les articles
- Navigation par article, article suivant/précédent

### 💬 Messagerie interne
- Système de conversation privé entre acheteurs et vendeurs
- Envoi de messages liés à des produits ou des articles

### 🔒 Authentification & rôles
- Inscription, connexion, mot de passe oublié (avec e-mail SMTP)
- Gestion des rôles : **utilisateur** ou **vendeur**
- Seuls les vendeurs peuvent publier produits et articles

### 🔐 Sécurité
- Gestion des données sensibles via `.env`
- SMTP pour envoi de mails sécurisé
- Permissions Django pour protéger les accès

### 🔗 API REST
- Endpoints sécurisés pour les produits et les articles
- Accès via authentification Django

---


## ⚙️ Technologies utilisées

- **Backend** : Django 5
- **Frontend** : HTML, Tailwind CSS
- **Base de données** : SQLite / PostgreSQL
- **Messagerie e-mail** : SMTP avec Gmail
- **API REST** : Django REST Framework (DRF)
- **Outils** : Git, GitHub, PlantUML, Python-dotenv

---

## 🧪 Lancer le projet en local

### 1. Cloner le projet

```bash
git clone https://github.com/ibra-sy/LeDjasse_django.git
cd LeDjasse_django

2. Créer et activer un environnement virtuel
bash
Copier
Modifier
python -m venv env
source env/bin/activate  # Windows : env\Scripts\activate


3. Installer les dépendances
bash
Copier
Modifier
pip install -r requirements.txt


4. Créer un fichier .env
env
Copier
Modifier
EMAIL_HOST_USER=tonemail@gmail.com
EMAIL_HOST_PASSWORD=ton_mot_de_passe_app


5. Appliquer les migrations et lancer le serveur
bash
Copier
Modifier
python manage.py migrate
python manage.py runserver


📂 Structure du projet
bash
Copier
Modifier
LeDjassa_django/
├── blog/                  # Application Blog
├── ecommerce/             # Application Boutique
├── api/                   # API REST
├── templates/             # Templates HTML
├── static/                # Fichiers statiques (CSS, JS, images)
├── le_djassa/             # Configuration principale Django
├── .env                   # Variables d’environnement (non versionné)
└── requirements.txt


🧠 Diagrammes UML
✅ Diagramme de classes

✅ Diagramme de cas d’utilisation

✅ Diagramme de séquence (achat + confirmation)

✅ Diagramme d’activité (processus d’achat)

Les diagrammes sont disponibles dans le dossier /uml/ ou /docs/.

📜 Licence
Ce projet est sous licence MIT.
Vous êtes libre de l’utiliser, le modifier et le redistribuer.

🙋‍♂️ Auteur
Développé par Sylla Scheickna ibrahim
Étudiant à IIT et développeur full-stack passionné par les plateformes web évolutives, le clean code, et les systèmes intelligents.
📧 Email : scheickna.sylla@iit.ci
🔗 GitHub : github.com/ibra-sy
````
## 🏍️🏍️🏍️🏍️🏍️🏍️MOTOCYCLE LOVER👽
