"""Test for the Premis class"""
from __future__ import unicode_literals

import lxml.etree as ET
import xml_helpers.utils as u
import premis.base as p
import premis.object_base as o

# using lxml.etree causes these, but importing c extensions is not a problem
# for us
# pylint: disable=c-extension-no-member


def test_premis_ns():
    """Test premis_ns"""
    assert p.premis_ns('xxx') == '{info:lc/xmlns/premis-v2}xxx'


def test_element():
    """Test PREMIS element"""
    xml = """<premis:xxx xmlns:premis="info:lc/xmlns/premis-v2"/>"""
    assert u.compare_trees(p.element('xxx'), ET.fromstring(xml))


def test_subelement():
    """Test PREMIS subelement"""
    xml = """<premis:xxx xmlns:premis="info:lc/xmlns/premis-v2"/>"""
    parent_xml = """<premis:premis xmlns:premis="info:lc/xmlns/premis-v2"/>"""
    parent = ET.fromstring(parent_xml)
    assert u.compare_trees(p.subelement(parent, 'xxx'), ET.fromstring(xml))


def test_identifier():
    """Test identifier"""
    object_identifier = p.identifier('local', 'id01')
    object_related = p.identifier('local', 'id01', 'relatedObject')
    event_identifier = p.identifier('local', 'id01', 'event')
    linking_agent_identifier = p.identifier(
        'local', 'id01', prefix='linkingAgent', role='tester')
    object_id = (
        '<premis:objectIdentifier xmlns:premis="info:lc/xmlns/premis-v2">'
        '<premis:objectIdentifierType>local</premis:objectIdentifierType>'
        '<premis:objectIdentifierValue>id01</premis:objectIdentifierValue>'
        '</premis:objectIdentifier>'
    )
    xml_related = (
        '<premis:relatedObjectIdentification xmlns:premis="info:lc/xmlns/premis-v2">'
        '<premis:relatedObjectIdentifierType>local</premis:relatedObjectIdentifierType>'
        '<premis:relatedObjectIdentifierValue>id01</premis:relatedObjectIdentifierValue>'
        '</premis:relatedObjectIdentification>'
    )
    xml_event = (
        '<premis:eventIdentifier xmlns:premis="info:lc/xmlns/premis-v2">'
        '<premis:eventIdentifierType>local</premis:eventIdentifierType>'
        '<premis:eventIdentifierValue>id01</premis:eventIdentifierValue>'
        '</premis:eventIdentifier>'
    )
    xml_linking_agent = (
        '<premis:linkingAgentIdentifier xmlns:premis="info:lc/xmlns/premis-v2">'
        '<premis:linkingAgentIdentifierType>local</premis:linkingAgentIdentifierType>'
        '<premis:linkingAgentIdentifierValue>id01</premis:linkingAgentIdentifierValue>'
        '<premis:linkingAgentRole>tester</premis:linkingAgentRole>'
        '</premis:linkingAgentIdentifier>'
    )

    assert u.compare_trees(object_identifier, ET.fromstring(object_id))
    assert u.compare_trees(object_related, ET.fromstring(xml_related))
    assert u.compare_trees(event_identifier, ET.fromstring(xml_event))
    assert u.compare_trees(linking_agent_identifier,
                           ET.fromstring(xml_linking_agent))


def test_parse_identifier_type_value():
    """Test parse_identifier_type_value"""
    object_identifier = p.identifier('local', 'id01')
    object_related = p.identifier('local', 'id01', 'relatedObject')
    event_identifier = p.identifier('local', 'id01', 'event')

    (idtype, idval) = p.parse_identifier_type_value(object_identifier)
    assert idtype == 'local'
    assert idval == 'id01'
    (idtype, idval) = p.parse_identifier_type_value(
        object_related, 'relatedObject'
    )
    assert idtype == 'local'
    assert idval == 'id01'
    (idtype, idval) = p.parse_identifier_type_value(event_identifier, 'event')
    assert idtype == 'local'
    assert idval == 'id01'


def test_premis():
    """Test PREMIS root generation"""
    tree = ET.tostring(p.premis())
    xml = """<premis:premis
             xsi:schemaLocation="info:lc/xmlns/premis-v2 http://www.loc.gov/standards/premis/v2/premis-v2-3.xsd"
             xmlns:premis = "info:lc/xmlns/premis-v2"
             xmlns:xsi = "http://www.w3.org/2001/XMLSchema-instance"
             version="2.2"/>"""
    tree_xml = ET.tostring(ET.fromstring(xml))
    assert tree == tree_xml


def test_iter_elements():
    """Test iter_elements"""
    obj1 = o.object(p.identifier('local', 'id01'), original_name='nimi1')
    obj2 = o.object(p.identifier('local', 'id02'), original_name='nimi2')
    obj3 = o.object(p.identifier('local', 'id03'), original_name='nimi3')
    xml = p.premis(child_elements=[obj1, obj2, obj3])
    i = 0
    for name in p.iter_elements(xml, 'originalName'):
        i = i + 1
        assert name.text == 'nimi' + str(i)
    assert i == 3


def test_parse_identifier():
    """Test parse_identifier"""
    obj = o.object(p.identifier('local', 'id01'))
    object_id = (
        '<premis:objectIdentifier xmlns:premis="info:lc/xmlns/premis-v2" '
        'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">'
        '<premis:objectIdentifierType>local</premis:objectIdentifierType>'
        '<premis:objectIdentifierValue>id01</premis:objectIdentifierValue>'
        '</premis:objectIdentifier>'
    )

    assert u.compare_trees(p.parse_identifier(obj), ET.fromstring(object_id))
