import os
import os.path
import shutil
from typing import Callable

from yattag import indent
from yattag.indentation import XMLTokenError

from gedhtml.describe import individual_text, marriage_text
from gedhtml.family_tree import FamilyTree, Individual
from gedhtml.language import Language, Dutch
import gedhtml.html_template as template
import gedhtml.pedigree as pedigree
from gedhtml.utils import concat


class _HtmlTagger:
    """Wrap a string argument with an html tag, given by any method name.
    Keywords will be turned into html tag attributes; if you want to use the
    keyword 'class', use 'klass' instead, because the former is a reserved
    word in Python.
    
    >>> html = _HtmlTagger()
    >>> html.a('link text', klass='my-class', href='https://www.python.org')
    \"<a class='my-class' href='https://www.python.org'>link text</a>\\n\"
    """
    def __getattr__(self, tag: str) -> Callable:
        def wrapper(content: str, **kwargs: str) -> str:
            attribute_text = ""
            for key, value in kwargs.items():
                attribute_text += f" {"class" if key == "klass" else key}='{value}'"
            return f"<{tag}{attribute_text}>{content}</{tag}>\n"
        return wrapper


class _NameCounter:
    """Group individuals in a family tree by initial and last name."""
    
    def __init__(self, family_tree: FamilyTree, unknown_str="unknown"):
        self.family_tree = family_tree
        self.unknown_str = unknown_str

        # Main data structure in this class.
        # key: initial
        # value: dict with:
        #     key: last name
        #     value: list of individuals, sorted by full name
        self._data = self._group_names()

    def _group_names(self):

        data = dict()
        for individual in self.family_tree.individuals.values():

            # Skip private individuals.
            if individual.private:
                continue
            last_name = individual.first_last_name

            # Do some filtering on last name.
            if last_name == '':
                add_name = self.unknown_str
            elif not last_name[0].isalpha():
                name_split = last_name.split(' ')
                if len(name_split) > 1:
                    add_name = name_split[1]
            else:
                add_name = last_name
            initial = add_name[0]

            # Add to data structure.
            if initial not in data.keys():
                data[initial] = dict()

            if add_name not in data[initial].keys():
                data[initial][add_name] = [individual]
            else:
                data[initial][add_name].append(individual)

        # Data is complete but needs to be sorted.
        data = dict(sorted(data.items()))  # Sort initials
        for initial in data.keys():
            data[initial] = dict(sorted(data[initial].items()))  # Sort last names.
            for last_name in data[initial].keys():
                data[initial][last_name].sort(key=lambda x: x.name)  # Sort first names.

        return data

    def items(self):
        for initial, name_dict in self._data.items():
            yield initial, name_dict

    def initials(self):
        return self._data.keys()


def generate_individual_page(fam_tree: FamilyTree, ref: str,
                             title="My genealogy", description="My genealogy",
                             lang: Language=Dutch):

    individual = fam_tree.individuals[ref]
    html = _HtmlTagger()

    header = html.h1(individual.name)
    header += html.h2(individual_text(fam_tree, ref, lang, False))

    content = html.h2(lang.header_pedigree)
    content += pedigree.make_plot(fam_tree, ref)

    content += html.h2(lang.header_children)
    content += html.ul(concat([html.li(individual_text(fam_tree, f.ref, lang))
                                     for f in fam_tree.get_children(individual)]))

    content += html.h2(lang.header_parents)
    content += html.ul(concat([html.li(individual_text(fam_tree, f.ref, lang))
                                     for f in fam_tree.get_parents(individual)]))

    content += html.h2(lang.header_siblings)
    content += html.ul(concat([html.li(individual_text(fam_tree, f.ref, lang))
                                     for f in fam_tree.get_siblings(individual)]))

    content += html.h2(lang.header_spouses)
    spouses, marriages = fam_tree.get_spouses(individual)
    if individual.private:
        content += html.ul(concat([html.li(individual_text(fam_tree, f.ref, lang))
                                         for f in spouses]))
    else:
        content += html.ul(concat([html.li(individual_text(fam_tree, f.ref, lang)
                                                 + " " + marriage_text(m, lang))
                                         for f, m in zip(spouses, marriages)]))

    content += html.h2(lang.header_notes)
    if not individual.private:
        content += html.p(concat([note.replace('\n', '<br>')
                                        for note in individual.notes]))

    menu = template.menu(lang.link_text_start_page,
                         lang.link_text_name_index,
                         lang.link_text_about_page)
    html_page = template.main(title, description, menu, header, content)

    try:
        return indent(html_page)
    except XMLTokenError:
        print(f"Indentation issue encountered for {individual.link}")
        return html_page
    

def generate_name_index(fam_tree: FamilyTree, title: str, description: str,
                        language: Language=Dutch):
    html = _HtmlTagger()
    name_counter = _NameCounter(fam_tree, language.person_unknown)

    # Generate html for index at top of page.
    header = html.h1(language.header_name_index)
    initials = name_counter.initials()
    content = html.p(
        html.center(
            concat([html.a(init, href=f"#{init}").rstrip() for init in initials], " - ")
        ))

    # Generate html for full list of names.
    dunk = language.date_unknown  # Mike, I'm open! Never mind.
    for initial, last_names in name_counter.items():
        content += html.h2(initial, id=f"{initial}")
        for last_name, individuals in last_names.items():
            content += html.details(
                html.summary(f"{last_name} ({len(individuals)})") +
                html.p(
                    html.ul(
                        concat([
                            html.li(html.a(i.name, href=i.link).rstrip() +
                                    f" ({dunk if i.birth_year is None else i.birth_year})")
                            for i in individuals])
                    )
                )
            )
    
    menu = template.menu(language.link_text_start_page,
                         language.link_text_name_index,
                         language.link_text_about_page)
    html_page = template.main(title, description, menu, header, content)

    return indent(html_page)
    

def generate_about_page_placeholder(title: str, description: str,
                                    language: Language=Dutch):
    html = _HtmlTagger()
    header = html.h1(language.link_text_about_page)
    content = html.p(language.default_content_about)
    menu = template.menu(language.link_text_start_page,
                         language.link_text_name_index,
                         language.link_text_about_page)
    html_page = template.main(title, description, menu, header, content)
    return indent(html_page)


def generate(family_tree: FamilyTree, id: str, output_dir: str="", title: str="",
             description: str="", language: Language=Dutch,
             filter_ids: list[str] | None=None):

    ref = f"@{id}@"
    if filter_ids is None:
        filter_refs = None
    else:
        filter_refs = [f"@{id}@" for id in filter_ids]

    root_dir = os.path.dirname(os.path.dirname(__file__))
    webfiles_dir = os.path.join(root_dir, 'webfiles')
    webfiles = os.listdir(webfiles_dir)
    for f in webfiles:
        shutil.copy2(os.path.join(webfiles_dir, f), output_dir)

    html_doc = generate_individual_page(family_tree, ref, title, description, language)
    path_index = os.path.join(output_dir, "index.html")
    with open(path_index, "w", encoding="utf-8") as file:
        file.write(html_doc)

    html_doc = generate_name_index(family_tree, title, description, language)
    path_name_index = os.path.join(output_dir, "name_index.html")
    with open(path_name_index, "w", encoding="utf-8") as file:
        file.write(html_doc)

    html_doc = generate_about_page_placeholder(title, description, language)
    path_name_index = os.path.join(output_dir, "about.html")
    with open(path_name_index, "w", encoding="utf-8") as file:
        file.write(html_doc)

    refs = list(family_tree.individuals.keys())
    for ref in refs:
        include = True
        if filter_refs is not None:

            i = family_tree.individuals[ref]

            spouses, _ = family_tree.get_spouses(i)
            children = family_tree.get_children(i)
            siblings = family_tree.get_siblings(i)

            # We want ancestors going back 4 generations,
            # because that's how deep the pedigree chart goes.
            ancestors: list[list[Individual]] = [[] for _ in range(4)]
            ancestors[0] = family_tree.get_parents(i)
            for p in range(1, 4):
                for kid in ancestors[p-1]:
                    ancestors[p] += family_tree.get_parents(kid)

            family = [i] + children + spouses + siblings + \
                     ancestors[0] + ancestors[1] + ancestors[2] + ancestors[3]
            include = False
            for fam in family:
                if fam.ref in filter_refs:
                    include = True
        if include:
            i = family_tree.individuals[ref]
            html_doc = generate_individual_page(family_tree, ref, title, description, language)
            path_individual = os.path.join(output_dir, i.link)
            with open(path_individual, "w", encoding="utf-8") as file:
                file.write(html_doc)
