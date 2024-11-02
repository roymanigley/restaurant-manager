# Restaurant Manager

## Initial setup

```
python -m venv .venv
pip install -r requirements.txt
python manage.py migrate
python manage.py shell < initial_config.py
```

## Run the Application

```commandline
python manage.py runserver
```

open browser: http://localhost:8000