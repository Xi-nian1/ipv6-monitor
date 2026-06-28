[简体中文](README.md) | [English](README_en.md) | [日本語](README_ja.md) | [Français](README_fr.md)

# IPv6 Monitor & Email Notifier

Il s'agit d'une application d'arrière-plan Windows extrêmement légère qui détecte automatiquement l'adresse IPv6 publique de votre machine locale et l'envoie à une adresse e-mail spécifiée via SMTP lors du **démarrage** du système ou du **réveil de la veille/hibernation**.

## Fonctionnalités
- **Zéro Dépendance** : Utilise uniquement les bibliothèques standard intégrées à Python (`urllib`, `smtplib`, `socket`, etc.). Pas besoin de faire un `pip install` de packages tiers.
- **Exécution Unique** : Ne reste pas en arrière-plan dans une boucle infinie. Il s'exécute une fois, envoie l'e-mail et se ferme immédiatement, préservant ainsi strictement les ressources du système.
- **Déclencheurs Système** : S'intègre parfaitement avec le Planificateur de tâches Windows pour le déclenchement des événements système.

## Utilisation

### 1. Configuration
Copiez `config.example.json`, renommez-le en `config.json`, et remplissez votre configuration e-mail :
```json
{
    "from_email": "your_sender_email@qq.com",
    "auth_code": "your_smtp_auth_code",
    "to_email": "receiver_email@qq.com",
    "check_interval": 300,
    "retry_times": 3,
    "log_file": "ipv6_sender.log",
    "ip_check_services": [
        "https://ipv6.icanhazip.com",
        "https://v6.ident.me",
        "https://ipv6.lookup.test-ipv6.com/ip/"
    ]
}
```
*(Remarque : le format JSON standard ne prend pas en charge les commentaires `//`)*

### 2. Exécuter le Script
Exécutez-le directement avec Python :
```bash
python ipv6.py
```

### 3. Compiler en tant qu'Exécutable EXE (Optionnel)
Pour s'exécuter silencieusement en arrière-plan sans fenêtre de console, il est fortement recommandé de le compiler dans un fichier `.exe` :
```bash
pip install pyinstaller
pyinstaller -F -w ipv6.py
```
Après la compilation, déplacez le fichier `ipv6.exe` généré vers le répertoire racine du projet (assurez-vous qu'il se trouve dans le même répertoire que `config.json`).

### 4. Configurer le Réveil Automatique du Planificateur de Tâches Windows (Tutoriel GUI)

Pour exécuter le programme de manière transparente en arrière-plan au démarrage et lors de la sortie de veille, configurez-le via le "Planificateur de tâches" intégré à Windows :

1. **Ouvrir le Planificateur de tâches** : Appuyez sur `Win + S`, recherchez "Planificateur de tâches" et ouvrez-le.
2. **Créer une tâche** : Dans le volet Actions à droite, cliquez sur **"Créer une tâche..."** (Remarque : ne cliquez pas sur "Créer une tâche de base").
3. **Général** :
   - Nom : `IPv6_Monitor`.
   - Cochez **"Masqué"** en bas.
   - Cochez **"Exécuter même si l'utilisateur n'est pas connecté"** et **"Exécuter avec les autorisations maximales"**.
4. **Déclencheurs** (Créez les deux déclencheurs suivants) :
   - Déclencheur 1 : Lancer la tâche **"À l'ouverture de session"**.
   - Déclencheur 2 : Lancer la tâche **"Sur un événement"**. Journal : **Système**, Source : **Power-Troubleshooter**, ID d'événement : **1** (Cet événement indique la sortie de veille/hibernation).
5. **Actions** :
   - Action : **"Démarrer un programme"**.
   - **Programme/script** : Parcourez et sélectionnez votre `ipv6.exe` empaqueté.
   - **Commencer dans** : Entrez le chemin absolu du dossier contenant `ipv6.exe` (ex. `D:\ipv6\`, **assurez-vous qu'il se termine par une barre oblique inverse et n'utilisez pas de guillemets**).
6. **Conditions** :
   - Décochez "Ne démarrer la tâche que si l'ordinateur est sur secteur" (si vous utilisez un ordinateur portable).
7. Cliquez sur OK et entrez le mot de passe de votre compte Windows pour enregistrer !
