"""Test the output-spaces parser."""
import pytest
from .. import utils as u


TEST_TEMPLATES = (
    'MNI152NLin2009cAsym',
    'MNIInfant',
    'MNI152NLin6Asym',
)


def test_output_spaces(monkeypatch):
    """Check the --output-spaces argument parser."""
    with monkeypatch.context() as m:
        m.setattr(u, '_TF_TEMPLATES', TEST_TEMPLATES)
        assert u.output_space('MNI152NLin2009cAsym') == [('MNI152NLin2009cAsym', {})]
        assert u.output_space('MNI152NLin2009cAsym:native') == \
            [('MNI152NLin2009cAsym', {'native': True})]
        assert u.output_space('MNI152NLin2009cAsym:res-2') == \
            [('MNI152NLin2009cAsym', {'res': '2'})]
        assert u.output_space('MNI152NLin6Asym:res-1:res-2') == \
            [('MNI152NLin6Asym', {'res': '1'}), ('MNI152NLin6Asym', {'res': '2'})]
        assert u.output_space('MNIInfant:res-2,cohort-1') == \
            [('MNIInfant', {'res': '2', 'cohort': '1'})]

        with pytest.raises(ValueError):
            u.output_space('UnkownTemplate')


def test_template_parser(monkeypatch):
    """Check the --output-spaces argument parser."""
    with monkeypatch.context() as m:
        m.setattr(u, '_TF_TEMPLATES', TEST_TEMPLATES)

        assert u._template(['MNI152NLin2009cAsym']) == [('MNI152NLin2009cAsym', {})]
        assert u._template(['MNI152NLin2009cAsym', 'MNI152NLin2009cAsym:res-2']) == \
            [('MNI152NLin2009cAsym', {}), ('MNI152NLin2009cAsym', {'res': '2'})]

        assert u._template(['MNI152NLin2009cAsym:res-1', 'MNI152NLin6Asym:res-2']) == \
            [('MNI152NLin2009cAsym', {'res': '1'}), ('MNI152NLin6Asym', {'res': '2'})]

        with pytest.raises(ValueError):
            u._template(['MNI152NLin6Asym:res-2', 'UnkownTemplate:res-2'])

        with pytest.raises(ValueError):
            u._template(['MNI152NLin6Asym:res-2', 'func'])

        assert u._template(['MNI152NLin6Asym:res-2', 'fsnative']) == \
            [('MNI152NLin6Asym', {'res': '2'}), ('fsnative', {})]

        u.ParseTemplates.set_nonstandard_spaces('func')
        assert u._template(['MNI152NLin2009cAsym:res-2', 'func']) == \
            [('MNI152NLin2009cAsym', {'res': '2'}), ('func', {})]

        u.ParseTemplates.set_nonstandard_spaces(['func', 'fsnative'])
        assert u._template(['MNI152NLin2009cAsym:res-2', 'func', 'fsnative']) == \
            [('MNI152NLin2009cAsym', {'res': '2'}), ('func', {}), ('fsnative', {})]
