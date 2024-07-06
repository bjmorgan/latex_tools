#! /usr/bin/env python

import re
import argparse

def extract_citations(latex_files):
    unique_citations = set()
    for latex_file in latex_files:
        with open(latex_file, 'r') as file:
            content = file.read()
        
        cite_pattern = r'\\(?:cite|onlinecite)\{([^}]+)\}'
        citations = re.findall(cite_pattern, content)
        
        for citation in citations:
            unique_citations.update(citation.split(','))
    
    return list(unique_citations)

def extract_bibtex_entries(bibtex_file, citations):
    with open(bibtex_file, 'r') as file:
        content = file.read()
    
    entry_pattern = re.compile(r'(@\w+\{([^,]+),[\s\S]+?\n\})', re.MULTILINE)
    entries = entry_pattern.findall(content)
    
    selected_entries = []
    for entry, key in entries:
        if key.strip() in citations:
            selected_entries.append(entry)
    
    return selected_entries

def parse_arguments():
    parser = argparse.ArgumentParser(description='Extract BibTeX entries based on LaTeX citations.')
    parser.add_argument('bibtex_file', help='Path to the BibTeX file')
    parser.add_argument('latex_files', nargs='+', help='Path(s) to one or more LaTeX files')
    return parser.parse_args()

def main():
    args = parse_arguments()
    
    citations = extract_citations(args.latex_files)
    selected_entries = extract_bibtex_entries(args.bibtex_file, citations)
    
    for entry in selected_entries:
        print(entry)
        print()

if __name__ == "__main__":
    main()
