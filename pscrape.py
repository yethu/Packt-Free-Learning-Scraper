from bs4 import BeautifulSoup
from colorama import Fore, Back, Style
from models.book import Book
from orator.exceptions.query import QueryException
from tabulate import tabulate
import argparse
import common
import getpass
import json
import requests


def get_form_id(s, config: dict) -> str:
    headers = common.build_headers(config['login_url'], config['user_agent'])
    response = s.get(config['login_url'], headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    form_build_id_tag = soup.find('input', {'name': 'form_build_id'})
    return form_build_id_tag['value']


def get_ebooks_by_page(s, config, page):
    params = {
        'page': page
    }
    headers = common.build_headers(config['ebook_url'], config['user_agent'])
    response = s.get(config['ebook_url'], headers=headers, params=params)
    soup = BeautifulSoup(response.text, 'html.parser')
    product_account_list = soup.find('div', {'id': 'product-account-list'})
    raw_titles = product_account_list.find_all('div', {'class': 'title'})
    titles = map(common.parse_title, [title.text for title in raw_titles])
    raw_authors = product_account_list.find_all('div', {'class': 'author'})
    authors = [author.text.strip() for author in raw_authors]

    return zip(titles, authors)


def get_page_count(s, config) -> int:
    params = {
        'page': 1
    }
    headers = common.build_headers(config['ebook_url'], config['user_agent'])
    response = s.get(config['ebook_url'], headers=headers, params=params)
    soup = BeautifulSoup(response.text, 'html.parser')
    product_account_list = soup.find('div', {'id': 'product-account-list'})
    page_count = len(product_account_list.find_all(
        'a', {'class': 'solr-page-page-selector-page'})) + 1

    return page_count


def store_books(book):
    b = Book()
    b.title = book[0]
    b.authors = 'N/A' if len(book[1]) == 0 else book[1]
    try:
        b.save()
        print(f'{Fore.GREEN}█{Style.RESET_ALL}', end='')
    except QueryException:
        print(f'{Fore.RED}█{Style.RESET_ALL}', end='')


def sync_books():
    print(f'{Back.GREEN}syncing books{Style.RESET_ALL}')
    config = None
    with open('config.json') as config_file:
        config = json.load(config_file)

    if config is not None:
        s = requests.Session()
        print('getting log in form')
        form_build_id = get_form_id(s, config)
        print('loggin in')
        login(s, form_build_id, config)
        print('getting page count')
        page_count = get_page_count(s, config)
        print('syncing books')
        for page in range(1, page_count + 1):
            print(f'{Back.GREEN}retrieving page {page}{Style.RESET_ALL}', end='')
            [store_books(book) for book in get_ebooks_by_page(s, config, page)]
            print()


def login(s, form_build_id: str, config: dict):
    password = getpass.getpass()

    login_data = {
        'name': config['username'],
        'pass': password,
        'op': 'Log in',
        'form_id': 'packt_v3_account_login_form',
        'form_build_id': form_build_id
    }
    headers = common.build_headers(config['login_url'], config['user_agent'])
    # TODO: check login failure
    s.post(config['login_url'], data=login_data, headers=headers)


def list_books():
    table = []
    for book in Book.order_by('title').get():
        table.append([book.title, book.authors])

    print(tabulate(table, headers=['Title', 'Authors'], tablefmt='pipe'))


def title_search(title: str):
    return Book.query().where('title', 'like', f'%{title}%').order_by('title').get()


def perform_search(title: str):
    table = []
    for book in title_search(title):
        table.append([book.title, book.authors])

    print(tabulate(table, headers=['Title', 'Authors'], tablefmt='pipe'))


def get_current_book() -> str:
    print(f'{Back.GREEN}checking current book{Style.RESET_ALL}')
    config = None
    with open('config.json') as config_file:
        config = json.load(config_file)

    if config is not None:
        headers = common.build_headers(
            config['free_learning_url'], config['user_agent'])
        response = requests.get(config['free_learning_url'], headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        title = soup.select_one('.dotd-title > h2')
        return title.text.strip()


def check_current_book(no_local = False):
    current_book = get_current_book()
    print(f'Current Book: {current_book}')
    if not no_local:
        message = f'{Back.GREEN}CLAIMED{Style.RESET_ALL}' if book_exists_in_db(
            current_book) else f'{Back.RED}NOT CLAIMED{Style.RESET_ALL}'
        print(f'Status: {message}')


def book_exists_in_db(title: str) -> bool:
    return Book.where('title', title).first() is not None


def clear_database():
    Book.query().delete()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', action='store_true',
                        help='sync local book list with server')
    group = parser.add_argument_group('check current free book')
    group.add_argument('-c', action='store_true',
                       help='check current free book')
    group.add_argument('--no-local', action='store_true',
                       help='do not check against local database')
    parser.add_argument('-l', action='store_true',
                        help='print local book list')
    parser.add_argument('-d', action='store_true', help='clear local database')
    parser.add_argument('-st', type=str, default='',
                        metavar='TERM', help='perform a naive title search')
    args = parser.parse_args()

    if args.s:
        sync_books()
    elif args.l:
        list_books()
    elif args.c:
        check_current_book(args.no_local)
    elif args.d:
        clear_database()
    elif args.st:
        perform_search(args.st)


if __name__ == '__main__':
    main()
