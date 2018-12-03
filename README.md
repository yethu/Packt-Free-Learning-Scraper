## Note
This package does not automate downloading books from server. This is a work in progress. **USE AT OWN RISK**

## Warning
Since this is WIP, current iteration of the software stores the username and password in *plaintext* in a configuration file. This is undesirable behavior and will be fixed in next version.

## Building and configuration
run `pip install -r requirements.txt`  
copy `config.example.json` to `config.json` and fill out blank fields

## Usage
```
usage: pscrape.py [-h] [-s] [-l] [-c] [-st TERM]

optional arguments:
  -h, --help  show this help message and exit
  -s          sync local book list with server
  -l          print local book list
  -c          check current free book
  -st TERM    perform a naive title search
```