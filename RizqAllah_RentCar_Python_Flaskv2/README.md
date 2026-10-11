# Rizq Allah Rent Car - Application Web Python (Flask)

Application Web complète de location de voitures en Algérie développée en **Python (Flask)**, **Jinja2**, et **Tailwind CSS**.

## 🚀 Fonctionnalités
- **Côté Client**:
  - Catalogue interactif des véhicules avec prix en Dinars Algériens (DA).
  - Filtres dynamiques par catégorie, boîte de vitesse, et recherche par wilaya.
  - Formulaire de réservation automatique avec calcul du prix total et notification email immédiate vers le téléphone du propriétaire.
- **Espace Propriétaire (Admin)**:
  - Connexion sécurisée par mot de passe (Par défaut: `1234`).
  - Ajout/Modification/Suppression de véhicules avec **upload direct de photos depuis le téléphone ou le PC**.
  - Modification des paramètres (Nom de l'agence, numéro de téléphone, couleur du thème, logo).
  - Tableau de bord avec statistiques.

## 📦 Installation & Lancement

1. **Installer Python**: Assurez-vous d'avoir Python 3.8+ installé.
2. **Installer les dépendances**:
```bash
pip install -r requirements.txt
```
3. **Lancer le serveur**:
```bash
python app.py
```
4. Ouvrez votre navigateur sur `http://localhost:5000`
