# 💰 Application de Gestion Financière Personnelle

Une application web moderne et intuitive pour gérer vos finances personnelles avec Flask et Bootstrap.

## 🚀 Fonctionnalités

### ✨ Fonctionnalités principales
- **Gestion des revenus et dépenses** : Ajoutez facilement vos transactions financières
- **Catégorisation** : Organisez vos transactions par catégories prédéfinies
- **Tableau de bord** : Visualisez votre solde total, revenus et dépenses
- **Historique complet** : Consultez toutes vos transactions avec filtres
- **Graphiques interactifs** : Visualisez vos dépenses et revenus par catégorie
- **Interface responsive** : Fonctionne parfaitement sur mobile et desktop

### 🎯 Catégories disponibles

**Revenus :**
- Salaire
- Freelance
- Ventes
- Investissements
- Autres revenus

**Dépenses :**
- Alimentation
- Transport
- Logement
- Santé
- Loisirs
- Vêtements
- Éducation
- Factures
- Autres dépenses

## 🛠️ Installation

### Prérequis
- Python 3.7 ou supérieur
- pip (gestionnaire de paquets Python)

### Étapes d'installation

1. **Cloner ou télécharger le projet**
   ```bash
   cd /Users/mathiasetienne/Desktop/gestion-financiere
   ```

2. **Installer les dépendances**
   ```bash
   pip install -r requirements.txt
   ```

3. **Lancer l'application**
   ```bash
   python app.py
   ```

4. **Ouvrir dans votre navigateur**
   ```
   http://localhost:5000
   ```

## 📁 Structure du projet

```
gestion-financiere/
├── app.py                 # Application Flask principale
├── requirements.txt       # Dépendances Python
├── finance.db            # Base de données SQLite (créée automatiquement)
├── templates/
│   └── index.html        # Template HTML principal
├── static/
│   ├── css/
│   │   └── style.css     # Styles CSS personnalisés
│   ├── js/
│   │   └── app.js        # Logique JavaScript
│   └── images/           # Images (si nécessaire)
└── README.md             # Documentation
```

## 🔧 Technologies utilisées

- **Backend** : Flask (Python)
- **Base de données** : SQLite avec SQLAlchemy
- **Frontend** : HTML5, CSS3, JavaScript (ES6+)
- **Framework CSS** : Bootstrap 5
- **Graphiques** : Chart.js
- **Icônes** : Font Awesome

## 📊 API Endpoints

### Transactions
- `GET /api/transactions` - Récupérer toutes les transactions
- `POST /api/transactions` - Ajouter une nouvelle transaction
- `DELETE /api/transactions/<id>` - Supprimer une transaction

### Statistiques
- `GET /api/balance` - Obtenir le solde total, revenus et dépenses
- `GET /api/statistics` - Obtenir les statistiques par catégorie

## 🎨 Fonctionnalités de l'interface

### Tableau de bord
- **Cartes de résumé** : Solde total, revenus totaux, dépenses totales
- **Couleurs dynamiques** : Le solde change de couleur selon sa valeur (vert/rouge)

### Formulaire d'ajout
- **Type de transaction** : Revenu ou Dépense
- **Catégories dynamiques** : Les catégories changent selon le type sélectionné
- **Validation** : Tous les champs sont obligatoires
- **Date par défaut** : Aujourd'hui est sélectionné par défaut

### Historique
- **Filtres** : Par type de transaction
- **Actions** : Suppression avec confirmation
- **Affichage** : Montants colorés selon le type (vert pour revenus, rouge pour dépenses)

### Graphiques
- **Graphique en donut** : Dépenses par catégorie
- **Graphique en barres** : Revenus par catégorie
- **Couleurs** : Palettes distinctes pour chaque catégorie

## 🔒 Sécurité et données

- **Base de données locale** : Vos données restent sur votre machine
- **Validation côté serveur** : Toutes les données sont validées
- **Pas de stockage externe** : Aucune donnée n'est envoyée vers des serveurs tiers

## 🚀 Personnalisation

### Ajouter de nouvelles catégories
Modifiez le fichier `static/js/app.js` dans l'objet `categories` :

```javascript
const categories = {
    income: [
        'Salaire',
        'Nouvelle catégorie',  // Ajoutez ici
        // ...
    ],
    expense: [
        'Alimentation',
        'Nouvelle dépense',    // Ajoutez ici
        // ...
    ]
};
```

### Modifier les couleurs
Le fichier `static/css/style.css` contient toutes les couleurs personnalisables.

## 🐛 Dépannage

### L'application ne démarre pas
- Vérifiez que Python 3.7+ est installé
- Installez les dépendances : `pip install -r requirements.txt`
- Vérifiez que le port 5000 n'est pas utilisé

### Erreurs de base de données
- Supprimez le fichier `finance.db` pour recréer la base de données
- Relancez l'application

### Problèmes d'affichage
- Videz le cache de votre navigateur
- Vérifiez que JavaScript est activé

## 📈 Améliorations futures possibles

- [ ] Export des données en CSV/Excel
- [ ] Budgets et alertes
- [ ] Rapports mensuels/annuels
- [ ] Sauvegarde automatique
- [ ] Multi-utilisateurs
- [ ] Application mobile native
- [ ] Synchronisation cloud

## 📝 Licence

Ce projet est open source et libre d'utilisation.

## 🤝 Contribution

Les contributions sont les bienvenues ! N'hésitez pas à :
- Signaler des bugs
- Proposer de nouvelles fonctionnalités
- Améliorer la documentation
- Optimiser le code

---

**Développé avec ❤️ pour une gestion financière simple et efficace !**
