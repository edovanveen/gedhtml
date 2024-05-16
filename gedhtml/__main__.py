import argparse

import gedhtml.file
import gedhtml.language
import gedhtml.webpage


parser = argparse.ArgumentParser(description="GED to static HTML converter")
parser.add_argument("filename", help="GED filename")
parser.add_argument("-s", "--startid", help="ID of person for start page")
parser.add_argument("-o", "--outputdir", help="Output directory", default="")
parser.add_argument("-t", "--title", help="Website title", default="My<br>genealogy")
parser.add_argument("-d", "--description", help="Website description", default="My genealogy page")
parser.add_argument("-l", "--language", help="Language: NL or EN", default="NL")
args = parser.parse_args()

fam_tree = gedhtml.file.load(args.filename)
if args.startid:
    id = args.startid
else:
    ref = list(fam_tree.individuals.keys())[0]
    id = fam_tree.individuals[ref].id

lang = gedhtml.language.choose(args.language)

gedhtml.webpage.generate(fam_tree, id, args.outputdir, args.title, args.description, lang)
