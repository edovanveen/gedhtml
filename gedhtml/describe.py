from gedhtml.family_tree import FamilyTree, Family
from gedhtml.language import Language, Dutch


def _parse_date(date: str, language: Language) -> str:
    date_parsed = date[:]
    for key, value in language.date_mapping.items():
        if key in date:
            date_parsed = date_parsed.replace(key, value)
    return date_parsed


def _describe_date(date: str, language: Language) -> str:
    if date == "":
        return ""
    date_translated = _parse_date(date, language)
    if date_translated[0].isalpha():
        return date_translated
    elif len(date_translated.split(' ')) > 1:
        return f"{language.prepositions['on']} {date_translated}"
    else:
        return f"{language.prepositions['in']} {date_translated}"


def _describe_place(place: str, language: Language) -> str:
    if place == "":
        return ""
    return f"{language.prepositions['at']} {place}"


def _describe_date_and_place(date: str, place: str, language: Language,
                             prefix: str="", suffix: str=""):
    if date == "" and place == "":
        return ""

    description = ""
    if date != "":
        description += f" {_describe_date(date, language)}"
    if place != "":
        description += f" {_describe_place(place, language)}"

    return prefix + description + suffix


def marriage_text(fam: Family, language: Language):
    return _describe_date_and_place(fam.marriage_date, fam.marriage_place,
        language, language.participles["Married"], ".")


def individual_text(family_tree: FamilyTree, ref: str,
                    language: Language=Dutch, add_link: bool=True):

    individual = family_tree.individuals[ref]
    
    # Display name with or without link.
    if add_link:
        if len(family_tree.get_children(individual)) > 0:
            display_name = f"<a href='{individual.link}'><b>{individual.name}</b></a>"
        else:
            display_name = f"<a href='{individual.link}'>{individual.name}</a>"
    else:
        display_name = individual.name
    
    # Don't add any more info if private individual.
    if individual.private:
        return display_name
    
    # Add a lot more info if not private individual.
    birth_info = _describe_date_and_place(individual.birth_date, individual.birth_place,
                                          language, f", {language.participles["born"]}")
    baptism_info = _describe_date_and_place(individual.baptism_date, individual.baptism_place,
                                            language, f", {language.participles["baptised"]}")
    death_info = _describe_date_and_place(individual.death_date, individual.death_place,
                                          language, f", {language.participles["died"]}")
    burial_info = _describe_date_and_place(individual.burial_date, individual.burial_place,
                                           language, f", {language.participles["buried"]}")

    return(f"{display_name} ({individual.sex}){birth_info}{baptism_info}{death_info}{burial_info}.")
