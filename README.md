## Setup
Requires Python 3.7 or 3.8.

Requires Google Chrome.

Requires ChromeDriver. ChromeDriver version must match Google Chrome version installed. Include the ChromeDriver 
location in your PATH variable. Download at: <https://chromedriver.chromium.org/downloads>

Create a virtual environment with
```shell
python3 -m venv venv
```

On *Windows*, activate the venv with
```shell
\venv\Scripts\activate 
```

On *Unix*, activate with
```shell
. venv/bin/activate
```

Upgrade to the latest pip with
```shell
pip install --upgrade pip
```


Install required libraries (make sure pip is latest version) with 
```shell
pip install -r requirements.txt
```

create the database with
```text
sqlite3 src/data/autos.sqlite
sqlite> .read src/data/create-db.sql
```

run with
```shell
PYTHONPATH=. python3 src/main.py
```
