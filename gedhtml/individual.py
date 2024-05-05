from dataclasses import dataclass

import gedcom
import gedcom.tags


def _replace_unknown(input):
    if input == '':
        return '?'
    else:
        return input


def _gedcom_id(gedcom_data):
    if gedcom_data is None:
        return
    identifier_string = str(gedcom_data)
    return identifier_string.split('@')[1]


@dataclass
class Marriage:
    date: str
    place: str
    individual_id: str
    spouse_id: str
    child_ids: list[str]

    def __str__(self):
        return f"Getrouwd op {_replace_unknown(self.date)} te {_replace_unknown(self.place)}."

class Individual:

    def __init__(self, individual_gedcom_data, gedcom_parser):
        self.gedcom_data = individual_gedcom_data
        self.gedcom_parser = gedcom_parser
        self.parent_ids = []
        self.sibling_ids = []
        self.marriages = []
        self._get_family_members()

    @property
    def id(self):
        return _gedcom_id(self.gedcom_data)
    
    @property
    def link(self):
        return self.id + ".html"

    @property
    def name(self):
        if self.private:
            return f"{self.initial}"
        else:
            return self.full_name

    @property
    def full_name(self):
        name_tuple = self.gedcom_data.get_name()
        return name_tuple[0] + ' ' + name_tuple[1]
    
    @property
    def name_br(self):
        first_name, last_name = self.short_name
        if self.private:
            return self.initial
        else:
            return first_name + '\\n' + last_name
    
    @property
    def short_name(self):
        name_tuple = self.gedcom_data.get_name()
        first_names = name_tuple[0].split(' ')
        first_name = first_names[0]
        if len(first_names) > 1:
            for name in first_names[1:]:
                if len(name) > 0:
                    if name[0].isalpha() and name[-1].isalpha():
                        first_name += f" {name[0]}."
        last_names = name_tuple[1].split(' ')
        last_name = last_names[0]
        if len(last_names) > 1:
            for name in last_names[1:]:
                if len(name) > 0:
                    if name[0].isalpha() and name[-1].isalpha():
                        last_name += f" {name}"
        return first_name, last_name

    @property
    def initial(self):
        name_tuple = self.gedcom_data.get_name()
        first_name = name_tuple[0]
        if len(first_name) > 0:
            return first_name[0]
        else:
            return ""
    
    @property
    def spouse_ids(self):
        return [m.spouse_id for m in self.marriages]
    
    @property
    def birth_year(self):
        if self.birth_date == '?':
            return None
        birth_date_split = self.birth_date.split(' ')
        if len(birth_date_split) == 1:
            return int(self.birth_date)
        else:
            return int(self.birth_date.split(' ')[-1])
    
    @property
    def private(self):
        if self.birth_year is None:
            return False
        elif self.birth_year < 1940:
            return False
        else:
            return True

    @property
    def child_ids(self):
        child_ids = []
        for m in self.marriages:
            child_ids += m.child_ids
        return child_ids
    
    @property
    def birth_date(self):
        birth_date, _, _ = self.gedcom_data.get_birth_data()
        return _replace_unknown(birth_date)
    
    @property
    def birth_place(self):
        _, birth_place, _ = self.gedcom_data.get_birth_data()
        return _replace_unknown(birth_place)
    
    @property
    def baptism_date(self):
        baptism_date, _, _ = self._get_baptism_data()
        return _replace_unknown(baptism_date)
    
    @property
    def baptism_place(self):
        _, baptism_place, _ = self._get_baptism_data()
        return _replace_unknown(baptism_place)
    
    @property
    def death_date(self):
        death_date, _, _ = self.gedcom_data.get_death_data()
        return _replace_unknown(death_date)
    
    @property
    def death_place(self):
        _, death_place, _ = self.gedcom_data.get_death_data()
        return _replace_unknown(death_place)
    
    @property
    def burial_date(self):
        burial_date, _, _ = self.gedcom_data.get_burial_data()
        return _replace_unknown(burial_date)
    
    @property
    def burial_place(self):
        _, burial_place, _ = self.gedcom_data.get_burial_data()
        return _replace_unknown(burial_place)
    
    @property
    def gender(self):
        gender = self.gedcom_data.get_gender()
        return _replace_unknown(gender)
    
    def _get_family_members(self):
        families_child = self.gedcom_parser.get_families(self.gedcom_data, gedcom.tags.GEDCOM_TAG_FAMILY_CHILD)
        families_spouse = self.gedcom_parser.get_families(self.gedcom_data, gedcom.tags.GEDCOM_TAG_FAMILY_SPOUSE)
        parents_raw = []
        siblings_raw = []

        for family in families_child:
            parents_raw += self.gedcom_parser.get_family_members(family, gedcom.parser.FAMILY_MEMBERS_TYPE_PARENTS)
            siblings_raw += self.gedcom_parser.get_family_members(family, gedcom.parser.FAMILY_MEMBERS_TYPE_CHILDREN)
        for family in families_spouse:
            marriage = self._get_marriage_info(family)
            if marriage is not None:
                self.marriages.append(marriage)

        for parent in parents_raw:
            self.parent_ids.append(_gedcom_id(parent))
        for sibling in siblings_raw:
            if sibling is not self.gedcom_data:
                self.sibling_ids.append(_gedcom_id(sibling))

    def _get_marriage_info(self, family):
        
        spouse = None
        date = ''
        place = ''
        element_dictionary = self.gedcom_parser.get_element_dictionary()

        for child_element in family.get_child_elements():
            is_spouse = (child_element.get_tag() == gedcom.tags.GEDCOM_TAG_HUSBAND
                         or child_element.get_tag() == gedcom.tags.GEDCOM_TAG_WIFE)
            
            if is_spouse and child_element.get_value() in element_dictionary:
                element = element_dictionary[child_element.get_value()]
                if element is not self.gedcom_data:
                    spouse = element
            
        for child_element in family.get_child_elements():
            if child_element.get_tag() == gedcom.tags.GEDCOM_TAG_MARRIAGE:
                for marriage_data in child_element.get_child_elements():
                    if marriage_data.get_tag() == gedcom.tags.GEDCOM_TAG_DATE:
                        date = marriage_data.get_value()
                    if marriage_data.get_tag() == gedcom.tags.GEDCOM_TAG_PLACE:
                        place = marriage_data.get_value()

        children_raw = self.gedcom_parser.get_family_members(family, gedcom.parser.FAMILY_MEMBERS_TYPE_CHILDREN)

        if spouse is not None or len(children_raw)>0:
            child_ids = []
            for child in children_raw:
                child_ids.append(_gedcom_id(child))
            return Marriage(date, place, self.id, _gedcom_id(spouse), child_ids)

    def _get_notes(self):

        notes = []
        element_dictionary = self.gedcom_parser.get_element_dictionary()

        for child_element in self.gedcom_data.get_child_elements():
            is_note = (child_element.get_tag() == gedcom.tags.GEDCOM_TAG_NOTE
                         and child_element.get_value() in element_dictionary)
            if is_note:
                notes.append(element_dictionary[child_element.get_value()])

        return notes

    def _get_baptism_data(self):
        """Returns the baptism data of a person formatted as a tuple: (`str` date, `str` place, `list` sources)
        :rtype: tuple
        """
        date = ""
        place = ""
        sources = []

        for child in self.gedcom_data.get_child_elements():
            if child.get_tag() == gedcom.tags.GEDCOM_TAG_BAPTISM:
                for childOfChild in child.get_child_elements():

                    if childOfChild.get_tag() == gedcom.tags.GEDCOM_TAG_DATE:
                        date = childOfChild.get_value()

                    if childOfChild.get_tag() == gedcom.tags.GEDCOM_TAG_PLACE:
                        place = childOfChild.get_value()

                    if childOfChild.get_tag() == gedcom.tags.GEDCOM_TAG_SOURCE:
                        sources.append(childOfChild.get_value())

        return date, place, sources

    def list_notes(self):
        if self.private:
            return []
        notes_data = []
        notes = self._get_notes()
        for note in notes:
            text = note.get_value()
            notes_data.append(text)
            if len(text) < 67:
                notes_data[-1] += '<br>\n'
            for note_member in note.get_child_elements():
                text = note_member.get_value()
                notes_data[-1] += text
                if len(text) < 67:
                    notes_data[-1] += '<br>\n'
        return notes_data
    
    def list_parents(self, family_tree_dict):
        parents = []
        for id in self.parent_ids:
            parents.append(family_tree_dict[id])
        return parents
    
    def list_children(self, family_tree_dict):
        children = []
        for id in self.child_ids:
            children.append(family_tree_dict[id])
        return children
    
    def list_siblings(self, family_tree_dict):
        siblings = []
        for id in self.sibling_ids:
            siblings.append(family_tree_dict[id])
        return siblings
    
    def list_spouses(self, family_tree_dict):
        spouses = []
        for id in self.spouse_ids:
            if id is not None:
                spouses.append(family_tree_dict[id])
        return spouses
        
    def describe(self, family_tree_dict, add_link=True):
        baptism_info = ''
        if self.baptism_date != '?' and self.baptism_place != '?':
            baptism_info += f', gedoopt op {self.baptism_date} te {self.baptism_place}'
        burial_info = ''
        if self.burial_date != '?' and self.burial_place != '?':
            burial_info += f', begraven op {self.burial_date} te {self.burial_place}'

        if add_link:
            if len(self.list_children(family_tree_dict)) > 0:
                show_name = f"<a href='{self.link}'><b>{self.name}</b></a>"
            else:
                show_name = f"<a href='{self.link}'>{self.name}</a>"
        else:
            show_name = self.name
        if not self.private:
            return(f"{show_name} ({self.gender}), geboren op {self.birth_date} te {self.birth_place}{baptism_info}, "
                f"gestorven op {self.death_date} te {self.death_place}{burial_info}.")
        else:
            return(f"{show_name}")
