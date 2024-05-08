import argparse
import os
import os.path
import shutil

import gedhtml
import gedhtml.webpage


def generate_website(family_tree, id, output_dir="", title="", description="", filter_refs=None):

    ref = f"@{id}@"

    root_dir = os.path.dirname(os.path.dirname(__file__))
    webfiles_dir = os.path.join(root_dir, 'webfiles')
    webfiles = os.listdir(webfiles_dir)
    for f in webfiles:
        shutil.copy2(os.path.join(webfiles_dir, f), output_dir)

    html_doc = gedhtml.webpage.generate_individual_page(family_tree, ref, title, description)
    path_index = os.path.join(output_dir, "index.html")
    with open(path_index, "w", encoding="utf-8") as file:
        file.write(html_doc)

    html_doc = gedhtml.webpage.generate_name_index(family_tree, title, description)
    path_name_index = os.path.join(output_dir, "name_index.html")
    with open(path_name_index, "w", encoding="utf-8") as file:
        file.write(html_doc)

    refs = list(family_tree.individuals.keys())
    for ref in refs:
        include = True
        if filter_refs is not None:
            i = family_tree.individuals[ref]
            spouses, _ = family_tree.get_spouses(i)
            family = family_tree.get_children(i) + spouses + family_tree.get_parents(i) + family_tree.get_siblings(i) + [i]
            include = False
            for f in family:
                if f.ref in filter_refs:
                    include = True
        if include:
            i = family_tree.individuals[ref]
            html_doc = gedhtml.webpage.generate_individual_page(family_tree, ref, title, description)
            path_individual = os.path.join(output_dir, i.link)
            with open(path_individual, "w", encoding="utf-8") as file:
                file.write(html_doc)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="GED to static HTML converter")
    parser.add_argument("filename", help="GED filename")
    parser.add_argument("-s", "--startid", help="ID of person for start page")
    parser.add_argument("-o", "--outputdir", help="Output directory", default="")
    parser.add_argument("-t", "--title", help="Website title", default="My<br>genealogy")
    parser.add_argument("-d", "--description", help="Website description", default="My genealogy page")
    args = parser.parse_args()

    fam_tree = gedhtml.load_file(args.filename)
    if args.startid:
        id = args.startid
    else:
        ref = list(fam_tree.individuals.keys())[0]
        id = fam_tree.individuals[ref].id

    generate_website(fam_tree, id, args.outputdir, args.title, args.description)
