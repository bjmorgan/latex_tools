#! /usr/bin/env ruby

tex_document = ARGV[0]
bibtex_document = ARGV[1]

tex_file = File.open( tex_document, 'r' )
bibdata = File.open( bibtex_document, 'r' ).read

cites = tex_file.read.scan( /cite\{([^\}]+)\}/ ).map{ |m| m[0].split(/,\s*/) }.flatten.uniq
bib_text = cites.map{ |cite| Regexp.new( "@[a-z]+\{#{cite}.*?\}\s*\}\n", Regexp::MULTILINE ).match( bibdata ) } 

puts bib_text.join("\n")
