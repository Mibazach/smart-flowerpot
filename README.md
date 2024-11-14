# SMART FLOWER POT - CENTER

Simple app for controling remote smart flower pots


## Development NOTES!!!!
> Do not add files to **smart_flowerpot/static**
> Populate db with random data using "mange.py populate_db"


## Production setup **Linux**

1. Create virtual enviroment

```bash
cd smart_flowerpot
python3 -m venv env
```

2. Install requirements

```bash
python3 -m pip install -r requirements.txt
```

3. Collect static files
```bash
mkdir -p smart_flowerpot/static
cd smart_flowerpot
python3 manage.py collectstatic
```

4. Migrate data
```bash
python3 manage.py makemigrations
python3 manage.py migrate
```

5. Create super user
```bash
python3 manage.py createsuperuser
```

6. Run unvicorn script
```bash
chmod u+x run.sh
./run.sh
```

# All commands:
```bash
cd /var/www/
git clone https://github.com/Mibazach/smart-flowerpot.git
cd smart_flowerpot
python3 -m pip install -r requirements.txt
mkdir -p smart_flowerpot/static
cd smart_flowerpot
python3 manage.py collectstatic
python3 manage.py makemigrations
python3 manage.py migrate
chmod u+x run.sh
python3 manage.py createsuperuser
./run.sh
```