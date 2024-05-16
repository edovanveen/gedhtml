from enum import Enum

from ged4py import GedcomReader

from gedhtml.family_tree import FamilyTree, Individual, Family


class IndiRecord(Enum):
    SEX = "sex"
    NAMEGIVN = "first_name"
    NAMESPFX = "last_name_prefix"
    NAMESURN = "last_name"
    BIRTDATE = "birth_date"
    BIRTPLAC = "birth_place"
    BAPMDATE = "baptism_date"
    BAPMPLAC = "baptism_place"
    DEATDATE = "death_date"
    DEATPLAC = "death_place"
    BURIDATE = "burial_date"
    BURIPLAC = "burial_place"


class IndiRef(Enum):
    FAMC = "fam_child_refs"
    FAMS = "fam_spouse_refs"
    NOTE = "notes"


class FamRecord(Enum):
    HUSB = "husband_ref"
    WIFE = "wife_ref"
    MARRDATE = "marriage_date"
    MARRPLAC = "marriage_place"


class FamRef(Enum):
    CHIL = "child_refs"


def _parse_records(parser, record_name, records_enum, refs_enum):
    for record in parser.records0(record_name):
        kwargs = {"ref": record.xref_id}
        for ref in refs_enum:
            kwargs[ref.value] = []
        for sub_record in record.sub_records:
            tag = sub_record.tag
            try:
                kwargs[records_enum[tag].value] = str(sub_record.value)
            except KeyError:
                try:
                    kwargs[refs_enum[tag].value].append(str(sub_record.value))
                except KeyError:
                    pass
            for subsub_record in sub_record.sub_tags():
                tag = sub_record.tag + subsub_record.tag
                try:
                    kwargs[records_enum[tag].value] = str(subsub_record.value)
                except KeyError:
                    pass
        yield kwargs


def load(file_path: str) -> FamilyTree:
    """Parse a GEDCOM file and return a FamilyTree object."""

    family_tree = FamilyTree()

    with GedcomReader(file_path) as parser:

        # Parse notes, in case notes are by reference
        notes = dict()
        for record in parser.records0("NOTE"):
            notes[record.xref_id] = record.value

        # Parse individuals.
        for kwargs in _parse_records(parser, "INDI", IndiRecord, IndiRef):

            # Fill in notes by reference.
            for i, ref in enumerate(kwargs['notes']):
                if ref[0] == '@' and ref[-1] == '@':
                    kwargs['notes'][i] = notes[ref]

            family_tree.add_individual(Individual(**kwargs))

        # Parse families.
        for kwargs in _parse_records(parser, "FAM", FamRecord, FamRef):
            family_tree.add_family(Family(**kwargs))

        return family_tree
