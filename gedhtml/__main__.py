import argparse
import os
import os.path
import shutil

import gedhtml
import gedhtml.webpage


def generate_website(family_tree_dict, id, output_dir="", title="", description="", filter_ids=None):

    root_dir = os.path.dirname(os.path.dirname(__file__))
    webfiles_dir = os.path.join(root_dir, 'webfiles')
    webfiles = os.listdir(webfiles_dir)
    for f in webfiles:
        shutil.copy2(os.path.join(webfiles_dir, f), output_dir)

    html_doc = gedhtml.webpage.generate_individual_page(family_tree_dict, id, title, description)
    path_index = os.path.join(output_dir, "index.html")
    with open(path_index, "w", encoding="utf-8") as file:
        file.write(html_doc)

    html_doc = gedhtml.webpage.generate_name_index(family_tree_dict, title, description)
    path_name_index = os.path.join(output_dir, "name_index.html")
    with open(path_name_index, "w", encoding="utf-8") as file:
        file.write(html_doc)

    ids = list(family_tree_dict.keys())
    for id in ids:
        include = True
        if filter_ids is not None:
            i = family_tree_dict[id]
            family = i.list_children(family_tree_dict) + i.list_spouses(family_tree_dict) + i.list_parents(family_tree_dict) + i.list_siblings(family_tree_dict) + [i]
            include = False
            for f in family:
                if f.id in filter_ids:
                    include = True
        if include:
            html_doc = gedhtml.webpage.generate_individual_page(family_tree_dict, id, title, description)
            path_individual = os.path.join(output_dir, f"{id}.html")
            with open(path_individual, "w", encoding="utf-8") as file:
                file.write(html_doc)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="GED to static HTML converter")
    parser.add_argument("filename", help="GED filename")
    parser.add_argument("-s", "--startid", help="ID of person for start page")
    parser.add_argument("-o", "--outputdir", help="ID of person for start page", default="")
    parser.add_argument("-t", "--title", help="Website title", default="My<br>genealogy")
    parser.add_argument("-d", "--description", help="Website description", default="My genealogy page")
    args = parser.parse_args()

    fam_dict = gedhtml.load_file(args.filename)
    if args.startid:
        id = args.startid
    else:
        id = list(fam_dict.keys())[0]

    generate_website(fam_dict, id, args.outputdir, args.title, args.description)
