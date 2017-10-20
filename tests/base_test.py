"""Test for the Premis class"""

import lxml.etree as ET
import premis.base as p
import premis.object_base as o

def test_premis_ns():
    """Test premis_ns"""
    assert p.premis_ns('xxx') == '{info:lc/xmlns/premis-v2}xxx'


def test_element():
    """Test PREMIS _element"""
    xml = """<premis:xxx xmlns:premis="info:lc/xmlns/premis-v2"/>"""
    assert ET.tostring(p._element('xxx')) == xml


def test_subelement():
    """Test PREMIS _subelement"""
    xml = """<premis:xxx xmlns:premis="info:lc/xmlns/premis-v2"/>"""
    parent_xml = """<premis:premis xmlns:premis="info:lc/xmlns/premis-v2"/>"""
    parent = ET.fromstring(parent_xml)
    assert ET.tostring(p._subelement(parent, 'xxx')) == xml


def test_identifier():
    """Test identifier"""
    object_identifier = p.identifier('local', 'id01')
    object_related = p.identifier('local', 'id01', 'relatedObject')
    event_identifier = p.identifier('local', 'id01', 'event')
    object_id = '<premis:objectIdentifier xmlns:premis="info:lc/xmlns/premis-v2">' \
                '<premis:objectIdentifierType>local</premis:objectIdentifierType>' \
                '<premis:objectIdentifierValue>id01</premis:objectIdentifierValue>' \
                '</premis:objectIdentifier>'
    xml_related = '<premis:relatedObjectIdentification xmlns:premis="info:lc/xmlns/premis-v2">' \
                  '<premis:relatedObjectIdentifierType>local</premis:relatedObjectIdentifierType>' \
                  '<premis:relatedObjectIdentifierValue>id01</premis:relatedObjectIdentifierValue>' \
                  '</premis:relatedObjectIdentification>'
    xml_event = '<premis:eventIdentifier xmlns:premis="info:lc/xmlns/premis-v2">' \
                '<premis:eventIdentifierType>local</premis:eventIdentifierType>' \
                '<premis:eventIdentifierValue>id01</premis:eventIdentifierValue>' \
                '</premis:eventIdentifier>'

    assert ET.tostring(object_identifier) == object_id
    assert ET.tostring(object_related) == xml_related
    assert ET.tostring(event_identifier) == xml_event


def test_parse_identifier_type_value():
    """Test parse_identifier_type_value"""
    object_identifier = p.identifier('local', 'id01')
    object_related = p.identifier('local', 'id01', 'relatedObject')
    event_identifier = p.identifier('local', 'id01', 'event')

    (idtype, idval) = p.parse_identifier_type_value(object_identifier)
    assert idtype == 'local'
    assert idval == 'id01'
    (idtype, idval) = p.parse_identifier_type_value(object_related, 'relatedObject')
    assert idtype == 'local'
    assert idval == 'id01'
    (idtype, idval) = p.parse_identifier_type_value(event_identifier, 'event')
    assert idtype == 'local'
    assert idval == 'id01'


def test_premis():
    """Test PREMIS root generation"""
    tree = ET.tostring(p.premis())
    xml = """<premis:premis
             xsi:schemaLocation="info:lc/xmlns/premis-v2 http://www.loc.gov/standards/premis/premis.xsd"
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
    object_id = '<premis:objectIdentifier xmlns:premis="info:lc/xmlns/premis-v2" ' \
                'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">' \
                '<premis:objectIdentifierType>local</premis:objectIdentifierType>' \
                '<premis:objectIdentifierValue>id01</premis:objectIdentifierValue>' \
                '</premis:objectIdentifier>'
    assert ET.tostring(p.parse_identifier(obj)) == object_id

