## Note

This package does not automate downloading books from server. This is a work in progress. **USE AT OWN RISK**

## Building and configuration

run `pip install -r requirements.txt`  
copy `config.example.json` to `config.json` and fill out blank fields  
run `orator migrate -c dbconfig.py`

## Usage

```
usage: pscrape.py [-h] [-s] [-c] [--no-local] [-l] [-d] [-st TERM]

optional arguments:
  -h, --help  show this help message and exit
  -s          sync local book list with server
  -l          print local book list
  -d          clear local database
  -st TERM    perform a naive title search

check current free book:
  -c          check current free book
  --no-local  do not check against local database
```

## TODO

- [x] Remove password from `config.json`
- [ ] Add fuzzy search
- [x] Check current free book without comparing to local database
- [x] Clear local database
- [ ] Batch insert
- [ ] Ask to perform a sync if last sync was done over 24 hours ago
- [x] Memoize scraping functions to re-use downloaded pages
