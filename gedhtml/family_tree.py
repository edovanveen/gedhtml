from dataclasses import dataclass


def _truncate_names(names):
    for name in names:
        if len(name) > 0:
            if name[0].isalpha() and name[-1].isalpha():
                yield name


@dataclass 
class Individual:
    ref: str
    notes: list[str]
    fam_child_refs: list[str]
    fam_spouse_refs: list[str]
    sex: str = "U"
    first_name: str = ""
    last_name_prefix: str = ""
    last_name: str = ""
    birth_date: str = ""
    birth_place: str = ""
    baptism_date: str = ""
    baptism_place: str = ""
    death_date: str = ""
    death_place: str = ""
    burial_date: str = ""
    burial_place: str = ""

    @property
    def id(self) -> str:
        return self.ref[1:-1]
    
    @property
    def link(self) -> str:
        return f"{self.id}.html"

    @property
    def birth_year(self) -> int | None:
        if self.birth_date == "":
            return None
        for part in reversed(self.birth_date.split(' ')):
            try:
                return int(part)
            except ValueError:
                pass
        return None
    
    @property
    def private(self) -> bool:
        for note in self.notes:
            if note == "private":
                return True
        if self.birth_year is None or self.birth_year < 1940:
            return False
        return True

    @property
    def name(self) -> str:
        if self.private:
            return self.initial
        else:
            return self.full_name

    @property
    def full_name(self) -> str:
        if self.last_name_prefix == "":
            return f"{self.first_name} {self.last_name}"
        else:
            return f"{self.first_name} {self.last_name_prefix} {self.last_name}"
    
    @property
    def newline_name(self) -> str:
        short_first_name, short_last_name = self.short_name
        if self.private:
            return self.initial
        else:
            return f"{short_first_name}\\n{short_last_name}"

    @property
    def short_name(self) -> tuple[str, str]:

        first_names = self.first_name.split(' ')
        short_first_name = first_names[0]
        for name in _truncate_names(first_names[1:]):
            short_first_name += f" {name[0]}."

        short_last_name = ""
        for prefix in _truncate_names(self.last_name_prefix.split(' ')):
            short_last_name += f"{prefix[0]}. "
        last_names = self.last_name.split(' ')
        short_last_name += last_names[0]
        for name in _truncate_names(last_names[1:]):
            short_last_name += f" {name}"

        return short_first_name, short_last_name
    
    @property
    def first_last_name(self):
        return self.last_name.split(' ')[0]

    @property
    def initial(self) -> str:
        if len(self.first_name) > 0:
            return self.first_name[0]
        else:
            return ""


@dataclass
class Family:
    ref: str
    child_refs: list[str]
    husband_ref: str = ""
    wife_ref: str = ""
    marriage_date: str = ""
    marriage_place: str = ""


class FamilyTree:

    def __init__(self):
        self.individuals = dict()  # Keys: Individual.ref; values: Individual
        self.families = dict()  # Keys: Family.ref; values: Family

    def add_individual(self, individual: Individual):
        self.individuals[individual.ref] = individual

    def add_family(self, family: Family):
        self.families[family.ref] = family

    def get_children(self, individual: Individual) -> list[Individual]:
        children = []
        for ref in individual.fam_spouse_refs:
            family = self.families[ref]
            for child_ref in family.child_refs:
                children.append(self.individuals[child_ref])
        return children

    def get_parents(self, individual: Individual) -> list[Individual]:
        parents = []
        for ref in individual.fam_child_refs:
            family = self.families[ref]
            if family.husband_ref != "":
                parents.append(self.individuals[family.husband_ref])
            if family.wife_ref != "":
                parents.append(self.individuals[family.wife_ref])
        return parents

    def get_spouses(self, individual: Individual) -> tuple[list[Individual], list[Family]]:
        spouses = []
        marriages = []
        for ref in individual.fam_spouse_refs:
            family = self.families[ref]
            if family.husband_ref != "" and family.husband_ref != individual.ref:
                spouses.append(self.individuals[family.husband_ref])
            elif family.wife_ref != "" and family.wife_ref != individual.ref:
                spouses.append(self.individuals[family.wife_ref])
            marriages.append(family)
        return spouses, marriages

    def get_siblings(self, individual: Individual) -> list[Individual]:
        siblings = []
        for ref in individual.fam_child_refs:
            family = self.families[ref]
            for child_ref in family.child_refs:
                if child_ref != individual.ref:
                    siblings.append(self.individuals[child_ref])
        return siblings
