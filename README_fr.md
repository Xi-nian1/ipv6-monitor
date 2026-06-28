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

### 4. Configurer le Réveil Automatique du Planificateur de Tâches Windows

Nous devons configurer le Planificateur de tâches Windows pour exécuter automatiquement `ipv6.exe` au **Démarrage** et lors de la **Sortie de veille** :

1. **Modifier les chemins XML** : Ouvrez le fichier `task.xml` dans le Bloc-notes. Localisez les balises `<Command>` et `<WorkingDirectory>` tout en bas, et remplacez `C:\path\to\your\folder` par le chemin absolu réel où vous avez enregistré `ipv6.exe`. Enregistrez le fichier.
2. **Ouvrir le terminal** : Appuyez sur `Win + X` et ouvrez **Windows PowerShell (Admin)** ou **Terminal (Admin)**.
3. **Importer la tâche** : Utilisez la commande `cd` pour accéder au répertoire de votre projet, puis exécutez la commande suivante pour importer la tâche :
```powershell
schtasks /create /tn "IPv6_Monitor" /xml .\task.xml /f
```
4. Une fois importé avec succès, le script s'exécutera automatiquement et silencieusement en arrière-plan et enverra l'e-mail à chaque fois que le système démarre ou se réveille de la veille/hibernation.
