# Front-admin
Repo pour l'appli front administration

## Comment la démarrer

Il faut d'abord rentrer dans l'environnement de développement
```bash
./venv/Scripts/activate
```

Ensuite pour démarrer l'application il va falloir utiliser uvicorn, depuis le répertoire racine du microservice
```
uvicorn main:app --reload --port 8000
```