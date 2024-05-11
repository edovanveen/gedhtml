from gedhtml.utils import concat


def _template(fam_names, links, colors):

    name_str = concat([f'"{f}"' for f in fam_names], ', ')
    link_str = concat([f'"{a}"' for a in links], ', ')
    color_str = concat([f'"{c}"' for c in colors], ', ')

    return (
        '          <canvas id="pedigree"></canvas>\n'
        '          <script>\n'
       f'            const names = [{name_str}];\n'
       f'            const links = [{link_str}];\n'
       f'            const colors = [{color_str}];\n'
       f'            drawChart("pedigree", names, links, colors);\n'
        '          </script>\n'
        )


def _count_max_ancestors(family_tree, ref):
    
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


def make_plot(family_tree, ref):

    individual = family_tree.individuals[ref]

    base_colors = [["#AFDE43", "#C2EA63"],
                   ["#D9DB4B", "#E8EA63"],
                   ["#D99D36", "#EAB863"],
                   ["#D97B41", "#EA9763"]]
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
                    names += [parents[0].newline_name,
                              parents[1].newline_name]
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
            max_gen = _count_max_ancestors(family_tree, indiv.ref)
            names[-16+i] += f"\\n(+{max_gen})"

    return _template(names, links, colors)
