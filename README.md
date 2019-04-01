# youtuber
Significant youtube's channel(s) metadata grabber

---

### Host requirements
Python 3 (tested with Python 3.6)

### Database requirements
Any [SqlAlchemy compilant database](https://docs.sqlalchemy.org/en/latest/dialects/index.html#included-dialects)

### Python requirements
`$ pip install -r Requirements.txt`

### Settings
This repo contains _settings.yaml.template_ which must be filled up with proper values and renamed to _settings.yaml_

### Init database
`$ python database.py`

**CAUTION**: it drops and recreates brand new database

### Run script
`$ python run.py`
