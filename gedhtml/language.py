from typing import Protocol


class Language(Protocol):

    link_text_start_page: str
    link_text_name_index: str
    link_text_about_page: str

    header_name_index: str
    header_pedigree: str
    header_children: str
    header_parents: str
    header_siblings: str
    header_spouses: str
    header_notes: str

    date_unknown: str
    person_unknown: str

    default_content_about: str

    date_mapping: dict

    prepositions: dict

    participles: dict


class Dutch:

    link_text_start_page = "Startpagina"
    link_text_name_index = "Namenindex"
    link_text_about_page = "About"

    header_pedigree = "Voorouders"
    header_children = "Kinderen"
    header_parents = "Ouders"
    header_siblings = "Broers en zussen"
    header_spouses = "Echtgenoten"
    header_notes = "Notities"
    header_name_index = "Namenindex"
    
    date_unknown = "onbekend"
    person_unknown = "onbekend"

    default_content_about = "Nou gewoon, voor de leuk."

    date_mapping = {
        'ABOUT': 'ongeveer',
        'BEFORE': 'vóór',
        'AFTER': 'na',
        'BET': 'tussen',
        'AND': 'en',
        'JAN': 'januari',
        'FEB': 'februari',
        'MAR': 'maart',
        'APR': 'april',
        'MAY': 'mei',
        'JUN': 'juni',
        'JUL': 'juli',
        'AUG': 'augustus',
        'SEP': 'september',
        'OCT': 'oktober',
        'NOV': 'november',
        'DEC': 'december'
    }
    
    prepositions = {
        'on': 'op',
        'in': 'in',
        'at': 'te'
    }
    
    participles = {
        'born': 'geboren',
        'baptised': 'gedoopt',
        'died': 'gestorven',
        'buried': 'begraven',
        'Married': 'Getrouwd'
    }
    

class English:

    link_text_start_page = "Start page"
    link_text_name_index = "Name index"
    link_text_about_page = "About"

    header_pedigree = "Ancestors"
    header_children = "Children"
    header_parents = "Parents"
    header_siblings = "Siblings"
    header_spouses = "Spouses"
    header_notes = "Notes"
    header_name_index = "Name index"

    date_unknown = "unknown"
    person_unknown = "unknown"

    default_content_about = "Now ordinary, for the nice."

    date_mapping = {
        'ABOUT': 'about',
        'BEFORE': 'before',
        'AFTER': 'after',
        'BET': 'between',
        'AND': 'and',
        'JAN': 'January',
        'FEB': 'February',
        'MAR': 'March',
        'APR': 'April',
        'MAY': 'May',
        'JUN': 'June',
        'JUL': 'July',
        'AUG': 'August',
        'SEP': 'September',
        'OCT': 'October',
        'NOV': 'November',
        'DEC': 'December'
    }
    
    prepositions = {
        'on': 'on',
        'in': 'in',
        'at': 'at'
    }
    
    participles = {
        'born': 'born',
        'baptised': 'baptised',
        'died': 'died',
        'buried': 'buried',
        'Married': 'Married'
    }


def choose(lang: str="NL") -> Language:
    if lang == "NL":
        return Dutch
    elif lang == "EN":
        return English
    else:
        raise ValueError("Language support only for Dutch ('NL') "
                         "and (steenkolen-) English ('EN').")
