# 🚀 Guide de Déploiement - Application de Gestion Financière

## 📋 Prérequis
- Compte GitHub (gratuit)
- Compte Railway/Render (gratuit)

## 🎯 Option 1 : Railway (RECOMMANDÉE)

### 1. Préparer le code
```bash
# Initialiser Git
git init
git add .
git commit -m "Initial commit - Gestion Financière App"

# Créer un repository GitHub
# Pousser le code
git remote add origin https://github.com/VOTRE_USERNAME/gestion-financiere.git
git push -u origin main
```

### 2. Déployer sur Railway
1. Aller sur [railway.app](https://railway.app)
2. Se connecter avec GitHub
3. "New Project" → "Deploy from GitHub repo"
4. Sélectionner votre repository
5. Railway détecte automatiquement l'app Python
6. Déploiement automatique !

### 3. Configurer le domaine
1. Dans Railway → Settings → Domains
2. Ajouter un domaine personnalisé
3. Configurer DNS chez IONOS

## 🎯 Option 2 : Render

### 1. Déployer sur Render
1. Aller sur [render.com](https://render.com)
2. Se connecter avec GitHub
3. "New" → "Web Service"
4. Sélectionner votre repository
5. Configuration automatique détectée

### 2. Configurer
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `gunicorn app:app`
- **Environment**: Python 3

## 🌐 Configuration DNS (IONOS)

### Pour un sous-domaine (ex: app.budgetsmart.com)
1. Aller dans votre panel IONOS
2. DNS Management
3. Ajouter un enregistrement CNAME :
   - **Name**: `app`
   - **Value**: `votre-app.railway.app` (ou render.com)
   - **TTL**: 3600

### Pour un domaine complet
1. Changer les nameservers vers Railway/Render
2. Ou configurer les enregistrements A/CNAME

## 🔒 SSL/HTTPS
- **Railway/Render** : SSL automatique et gratuit
- **Certificats** : Let's Encrypt automatique

## 📊 Monitoring
- **Logs** : Disponibles dans Railway/Render
- **Métriques** : CPU, RAM, requêtes
- **Uptime** : Monitoring automatique

## 🔄 Mise à jour
```bash
git add .
git commit -m "Update app"
git push origin main
# Déploiement automatique !
```

## 💰 Coûts
- **Railway** : Gratuit jusqu'à 500h/mois
- **Render** : Gratuit avec limitations
- **Domaine** : Votre coût actuel IONOS
- **SSL** : Gratuit

## 🆘 Support
- **Railway** : Documentation excellente
- **Render** : Support communautaire
- **IONOS** : Support client
