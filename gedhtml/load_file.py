import gedcom
from gedcom.element.individual import IndividualElement
import gedcom.tags
import gedcom.parser

from gedhtml.individual import Individual


gedcom.tags.GEDCOM_TAG_NOTE = "NOTE"
gedcom.tags.GEDCOM_TAG_BAPTISM = "BAPM"


def load_file(file_path):
    gedcom_parser = gedcom.parser.Parser()
    gedcom_parser.parse_file(file_path)
    gedcom_data_list = gedcom_parser.get_root_child_elements()
    individuals = dict()
    for gedcom_data in gedcom_data_list:
        if isinstance(gedcom_data, IndividualElement):
            individual = Individual(gedcom_data, gedcom_parser)
            individuals[individual.id] = individual
    return individuals
