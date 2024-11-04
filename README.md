# SMART FLOWER POT - CENTER

Simple app for controling remote smart flower pots


## Development NOTES!!!!
> Do not add files to **smart_flowerpot/static**
> Populate db with random data using "mange.py populate_db"


## Production setup **Linux**

1. Create virtual enviroment

```bash
python3 -m venv env
```

2. Install requirements

```bash
python3 -m pip install -r requirements.txt
```

3. Set ENV varibles:

```bash
source ~/.bashrc
```

3. Collect static files
```bash
mkdir -p smart_flowerpot/static
python3 manage.py collectstatic
```

4. Migrate data
```bash
mkdir -p smart_flowerpot/static
python3 manage.py collectstatic
```

5. Run unvicorn script
```bash
chmod u+x run.sh
./run.sh
```