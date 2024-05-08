from gedhtml.family_tree import FamilyTree, Family


def _describe_date_place(prefix, date, place, suffix=""):
    if date == "" and place == "":
        return ""
    description = prefix
    if date != "":
        if date[0].isalpha():
            description += f" {date}"
        elif len(date.split(' ')) > 1:
            description += f" op {date}"
        else:
            description += f" in {date}"
    if place != "":
        description += f" te {place}"
    return description + suffix


def describe_marriage(fam: Family):
    return _describe_date_place("Getrouwd", fam.marriage_date, fam.marriage_place, ".")


def describe_individual(family_tree: FamilyTree, ref: str, add_link: bool=True):

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
    birth_info = _describe_date_place(", geboren", individual.birth_date, individual.birth_place)
    baptism_info = _describe_date_place(", gedoopt", individual.baptism_date, individual.baptism_place)
    death_info = _describe_date_place(", gestorven", individual.death_date, individual.death_place)
    burial_info = _describe_date_place(", begraven", individual.burial_date, individual.burial_place)

    return(f"{display_name} ({individual.sex}){birth_info}{baptism_info}{death_info}{burial_info}.")
