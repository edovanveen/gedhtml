from enum import Enum

from ged4py import GedcomReader

from gedhtml.family_tree import FamilyTree, Individual, Family, Note


class IndiRecord(Enum):
    SEX = "sex"
    NAMEGIVN = "first_name"
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
    NOTE = "note_refs"


class FamRecord(Enum):
    HUSB = "husband_ref"
    WIFE = "wife_ref"
    MARRDATE = "marriage_date"
    MARRPLAC = "marriage_place"


class FamRef(Enum):
    CHIL = "child_refs"


def parse_records(parser, record_name, records_enum, refs_enum):
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


def load_file(file_path):

    family_tree = FamilyTree()

    with GedcomReader(file_path) as parser:

        # Parse notes.
        for record in parser.records0("NOTE"):
            note_kwargs = {"ref": record.xref_id, "value": record.value}
            family_tree.add_note(Note(**note_kwargs))

        # Parse individuals.
        for kwargs in parse_records(parser, "INDI", IndiRecord, IndiRef):

            # TODO: fix this
            # Start hack to deal with files with direct notes instead of note references.
            note_refs = []
            remove_refs = []
            for i, ref in enumerate(kwargs['note_refs']):
                if ref[0] != '@' or ref[-1] != '@':
                    new_ref = f"{kwargs['ref']}-NOTE{i}"
                    family_tree.add_note(Note(new_ref, ref))
                    note_refs.append(new_ref)
                    remove_refs.append(ref)
            for ref in remove_refs:
                kwargs['note_refs'].remove(ref)
            kwargs['note_refs'] += note_refs
            # End hack.

            for ref in kwargs['note_refs']:
                if family_tree.notes[ref].value == "private":
                    print(f"Forcing record for {kwargs['ref']}: {kwargs['first_name']} {kwargs['last_name']} to be private.")
                    kwargs['override_private'] = True
            family_tree.add_individual(Individual(**kwargs))

        # Parse families.
        for kwargs in parse_records(parser, "FAM", FamRecord, FamRef):
            family_tree.add_family(Family(**kwargs))

        return family_tree
