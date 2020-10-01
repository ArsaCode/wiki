# Wiki - MemoGDS

Site contenant des memo qui peuvent être ajoutés/modifiés par les visiteurs de la page.

## Back/Front

Le back et le front sont faits avec Django (les templates HTML/CSS sont générées par Django).

## Base de données

BDD configurée par défaut sur PostgreSQL.

## Variables environnement obligatoires

Les deux sont obligatoires (utilisées dans `wiki/settings.py`) :
SKEY : La clé secrète de l'application.
DATABASE_URL : URL de la base de données PostgreSQL.

## Usage

`python3 manage.py makemigrations`
`python3 manage.py migrate`
`python3 manage.py collectstatic`
`python3 manage.py runserver`