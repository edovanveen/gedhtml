import os.path

import gedhtml


def test_kennedy():
    test_dir = os.path.dirname(__file__)
    input_path = os.path.join(test_dir, 'data', 'kennedies.ged')
    output_path = os.path.join(test_dir, 'output')
    fam_dict = gedhtml.load_file(input_path)
    gedhtml.generate_website(fam_dict, 'I0', output_path,
                            'Kennedy Genealogy',
                            'Genealogy of the Kennedy family.')
    assert(os.path.isfile(os.path.join(test_dir, 'output', 'I0.html')))
    # If running manually, make sure to empty the directory when re-running the test.
