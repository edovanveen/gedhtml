from yattag import indent
from yattag.indentation import XMLTokenError

from gedhtml.describe import describe_individual, describe_marriage


def header(title, description):
    return f"""
<!doctype html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="{description}">
    <title>{title}</title>
    <link rel="stylesheet" href="pure-min.css">
    <link rel="stylesheet" href="style.css">
</head>
<body>

<script src="chart.js"></script>
<script src="chartjs-plugin-datalabels.js"></script>
<script src="pedigree.js"></script>
<script src="ui.js"></script>

<div id="layout">

    <a href="#menu" id="menuLink" class="menu-link">
        <span></span>
    </a>

    <div id="menu">
        <div class="pure-menu">
            <a class="pure-menu-heading" href="index.html">{title}</a>

            <ul class="pure-menu-list">
                <li class="pure-menu-item"><a href="index.html" class="pure-menu-link">Startpagina</a></li>
                <li class="pure-menu-item"><a href="name_index.html" class="pure-menu-link">Namenindex</a></li>
                <li class="pure-menu-item"><a href="about.html" class="pure-menu-link">About</a></li>
            </ul>
        </div>
    </div>

    <div id="main">
        <div class="header">

"""


def divider():
    return """
        </div>

        <div class="content">

"""


def footer():
    return """
        </div>
    </div>
</div>

</body>
</html>

"""


def pedigree_html(fam_names, links, colors):
    name_str = ""
    for fam_name in fam_names:
        name_str += f'"{fam_name}", '
    link_str = ""
    for link in links:
        link_str += f'"{link}", '
    color_str = ""
    for color in colors:
        color_str += f'"{color}", '
    return (
        '          <canvas id="pedigree"></canvas>\n'
        '          <script>\n'
       f'            const names = [{name_str[:-2]}];\n'
       f'            const links = [{link_str[:-2]}];\n'
       f'            const colors = [{color_str[:-2]}];\n'
       f'            drawChart("pedigree", names, links, colors);\n'
        '          </script>\n'
        )


def count_max_ancestors(family_tree, ref):
    
    queue = [family_tree.individuals[ref]]
    max_gen = 0
    while len(queue) > 0:
        queue_parents = []
        for indiv in queue:
            parents = family_tree.get_parents(indiv)
            for parent in parents:
                if parent is not None:
                    queue_parents.append(parent)
        if len(queue_parents) > 0:
            max_gen += 1
            queue = queue_parents[:]
        else:
            queue = []
    return max_gen


def make_pedigree(family_tree, ref):

    individual = family_tree.individuals[ref]

    base_colors = [["#AFDE43", "#C2EA63"], ["#D9DB4B", "#E8EA63"], ["#D99D36", "#EAB863"], ["#D97B41", "#EA9763"]]
    no_color = "transparent"
    individuals = [individual]
    names = []
    links = []
    colors = []

    for i in range(4):
        n_prev = 2**i
        individuals_prev = individuals[-n_prev:]
        for person in individuals_prev:
            if person is not None:
                parents = family_tree.get_parents(person)
                if len(parents) == 2:
                    individuals += parents
                    colors += base_colors[i]
                    names += [parents[0].newline_name, parents[1].newline_name]
                    links += [parents[0].link, parents[1].link]
                elif len(parents) == 1:
                    if parents[0].sex == 'M':
                        individuals += [parents[0], None]
                        colors += [base_colors[i][0], no_color]
                        names += [parents[0].newline_name, ""]
                        links += [parents[0].link, ""]
                    else:
                        individuals += [None, parents[0]]
                        colors += [no_color, base_colors[i][1]]
                        names += ["", parents[0].newline_name]
                        links += ["", parents[0].link]
                elif len(parents) == 0:
                    individuals += [None, None]
                    colors += [no_color, no_color]
                    names += ["", ""]
                    links += ["", ""]
            else:
                individuals += [None, None]
                colors += [no_color, no_color]
                names += ["", ""]
                links += ["", ""]

    fourth_gen = individuals[-16:]

    for i, indiv in enumerate(fourth_gen):
        if indiv is not None:
            max_gen = count_max_ancestors(family_tree, indiv.ref)
            names[-16+i] += f"\\n(+{max_gen})"

    return pedigree_html(names, links, colors)


def generate_individual_page(fam_tree, ref,
        title="My<br>genealogy", description="My genealogie"):

    individual = fam_tree.individuals[ref]

    html_string = header(title, description)
    html_string += f"<h1>{individual.name}</h1>\n"
    html_string += f"<h2>{describe_individual(fam_tree, ref, False)}</h2>\n"
    html_string += divider()

    html_string += "<h2>Voorouders</h2>\n"
    html_string += make_pedigree(fam_tree, ref)

    html_string += "<h2>Kinderen</h2><ul>\n"
    for fam in fam_tree.get_children(individual):
        html_string += f"<li>{describe_individual(fam_tree, fam.ref, True)}</li>\n"
    html_string += "</ul>\n"

    html_string += "<h2>Ouders</h2><ul>\n"
    for fam in fam_tree.get_parents(individual):
        html_string += f"<li>{describe_individual(fam_tree, fam.ref, True)}</li>\n"
    html_string += "</ul>\n"

    html_string += "<h2>Broers en zussen</h2><ul>\n"
    for fam in fam_tree.get_siblings(individual):
        html_string += f"<li>{describe_individual(fam_tree, fam.ref, True)}</li>\n"
    html_string += "</ul>\n"

    html_string += "<h2>Echtgenoten</h2><ul>\n"
    spouses, marriages = fam_tree.get_spouses(individual)
    for spouse, marriage in zip(spouses, marriages):
        if individual.private:
            html_string += f"<li>{describe_individual(fam_tree, spouse.ref, True)}</li>\n"
        else:
            html_string += f"<li>{describe_individual(fam_tree, spouse.ref, True)} {describe_marriage(marriage)}</li>\n"
    html_string += "</ul>\n"

    html_string += "<h2>Notities</h2>\n"
    if not individual.private:
        for note in fam_tree.get_notes(individual):
            html_string += f"<p>{note.value.replace('\n', '<br>')}</p>\n"

    html_string += footer()
    try:
        return indent(html_string)
    except XMLTokenError:
        print(f"Indentation issue encountered for {individual.link}")
        return html_string


def add_name(name_dict, name, ref):

    if name == '':
        add_name = "UNKNOWN"
    elif not name[0].isalpha():
        name_split = name.split(' ')
        if len(name_split) > 1:
            add_name = name_split[1]
    else:
        add_name = name

    if add_name not in name_dict.keys():
        name_dict[add_name] = {'count': 1, 'refs': [ref]}
    else:
        name_dict[add_name]['count'] += 1
        name_dict[add_name]['refs'].append(ref)
    

def generate_name_index(fam_tree, title, description):
    html_string = header(title, description)
    html_string += "<h1>Namenindex</h1>\n"
    html_string += divider()

    last_names = dict()
    for ref, individual in fam_tree.individuals.items():
        if not individual.private:
            _, last_name = individual.short_name
            add_name(last_names, last_name, ref)

    last_names_sorted = list(last_names.keys())
    last_names_sorted.sort()
    full_last_name_list = ""
    initial_list = []
    initial = ""
    for name in last_names_sorted:
        if name[0] != initial:
            initial = name[0]
            initial_list.append(initial)
            full_last_name_list += f"<h2 id='{initial}'>{initial}</h2>\n"
        full_last_name_list += "<details>\n"
        full_last_name_list += f"<summary>{name} ({last_names[name]['count']})</summary>\n"
        full_last_name_list += "<p><ul>\n"
        names_dict = {fam_tree.individuals[ref].name: ref for ref in last_names[name]['refs']}
        names_list = list(names_dict)
        names_list.sort()
        for name in names_list:
            ref = names_dict[name]
            person = fam_tree.individuals[ref]
            if not person.private:
                year = fam_tree.individuals[ref].birth_year
            else:
                year = 'UNKNOWN'
            if year is None:
                year = 'UNKNOWN'
            full_last_name_list += f"<li><a href='{person.link}'>{person.name}</a> ({year})</li>\n"
        full_last_name_list += "</ul></p>\n"
        full_last_name_list += "</details>\n"

    html_string += "<p><center>- "
    for initial in initial_list:
        html_string += f"<a href='#{initial}'>{initial}</a> - "
    html_string += "</center></p>\n"

    html_string += f"\n{full_last_name_list}\n"
    html_string += footer()
    return indent(html_string)
