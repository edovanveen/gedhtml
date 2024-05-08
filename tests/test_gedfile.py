import os.path

import gedhtml.file
import gedhtml.webpage


def test_kennedy():
    test_dir = os.path.dirname(__file__)
    input_path = os.path.join(test_dir, 'data', 'kennedies.ged')
    output_path = os.path.join(test_dir, 'output/kennedies')
    fam_tree = gedhtml.file.load(input_path)
    gedhtml.webpage.generate(fam_tree, 'I0', output_path,
                            'Kennedy Genealogy',
                            'Genealogy of the Kennedy family.')
    assert(os.path.isfile(os.path.join(test_dir, 'output/kennedies', 'I0.html')))
    # If running manually, make sure to empty the directory when re-running the test.


def test_royals():
    test_dir = os.path.dirname(__file__)
    input_path = os.path.join(test_dir, 'data', 'royals.ged')
    output_path = os.path.join(test_dir, 'output/royals')
    fam_tree = gedhtml.file.load(input_path)
    gedhtml.webpage.generate(fam_tree, 'I0', output_path,
                            'Royal Genealogy',
                            'Genealogy of the royal family of the UK.')
    assert(os.path.isfile(os.path.join(test_dir, 'output/royals', 'I0.html')))
    # If running manually, make sure to empty the directory when re-running the test.
