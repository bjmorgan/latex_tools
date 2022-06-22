#! /usr/bin/env python

# script for validating .bib files against the Morgan group style guide

import argparse
import bibtexparser
import re

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('bibfile', type=str, help="bibtex file to be checked.")
    args = parser.parse_args()
    return args

def parse_bibfile(bibfile):
    with open(bibfile, 'r') as bf:
        bib_database = bibtexparser.load(bf)
    return bib_database.entries

def get_surname_from_bibtex_string(string):
    regexp = re.compile(r' \{[\w\s]+\}')
    if "," in string:
        surname = string.split(',')[0]
    elif regexp.search(string):
        regexp = re.compile(r' \{([\w\s]+)\}')
        surname = regexp.search(string)[1].replace(" ", "")
    else:
        surname = string.split(' ')[-1]
    return clean_author_strings(surname)

def clean_author_strings(string):
    subs = [[r'\{\\\'\{e\}\}', 'e'],
            [r'\{\\AA\}', 'A'],
            [r'ü', 'u'],
            [r'ö', 'o']]
    for s in subs:
        string = re.sub(s[0], s[1], string)
    return string

def parse_author_record(record):
    authors = record.split(' and ')
    surnames = [get_surname_from_bibtex_string(s) for s in authors]
    if len(surnames) == 1:
        author_string = surnames[0]
    elif len(surnames) == 2:
        author_string = f'{surnames[0]}And{surnames[1]}'
    else:
        author_string = f'{surnames[0]}EtAl'
    return author_string

def parse_journal_record(record):
    strings = re.findall('(\w+)', record)
    return ''.join(strings)

def check_record(record):
    check_title(record)
    check_bibtex_string(record)

def check_title(record):
    # check for illegal LaTeX commands
    title = record.get('title')
    latex_commands = set(re.findall(r'\\[a-z]+', title))
    illegal_commands = set(["\\less", "\\greater"])
    errors = latex_commands.intersection(illegal_commands)
    if errors:
        print(f'Non-standard LaTeX commands in {record["ID"]}: {errors}')

def check_bibtex_string(record):
    author = record.get('author')
    journal = record.get('journal')
    year = record.get('year')
    if author:
        author_string = parse_author_record(author)
    else:
        pass
    if journal:
        journal_string = parse_journal_record(journal)
    else:
        pass
    if year:
        year_string = year
    else:
        pass
    target_id = f'{author_string}_{journal_string}{year}'
    actual_id = record['ID']
    if target_id not in actual_id:
        print(f'Unexpected ID for {actual_id}: Suggested ID is {target_id}')

def main():
    args = parse_args()
    db = parse_bibfile(args.bibfile)
    for record in db:
        if record['ENTRYTYPE'] == 'article':
            check_record(record)

if __name__ == '__main__':
    main()
