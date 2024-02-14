# python-softdesk
Projet 10 OCR Formation Python

Réalisation d'une API RESTful (backend sécurisé) avec Django pour permettre à une application (Softdesk Support) de remonter et suivre des problèmes techniques.



Récupération du code source de l'application:
Cloner le projet à l'aide de votre terminal en tapant la commande :
```
   git clone https://github.com/AlexBotswana/python-softdesk.git
```
Créer un environnement virtuel à l'aide de votre terminal, se positionner dans le répertoire python-softdesk et taper la commande suivante:
```
   py -m venv softdesk-venv
```
puis l'activer : 
```
   ./softdesk-venv/Scripts/activate
```
Installation des requirements.txt (se positionner dans le répertoire du projet):
```
   pip install -r requirements.txt
```

Démarrage 
Dans le répertoire du projet python-softdesk\softdesk, taper les commandes suivantes:
```
   py manage.py makemigrations
   py manage.py migrate
   py manage.py runserver
```
L'application web est disponible en local à l'adresse: 
```
   http://localhost:8000/
```
