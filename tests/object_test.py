"""Test for the Premis object class"""

import xml.etree.ElementTree as ET
import premis_tools.premis as p
import premis_tools.object as o


def test_relationship():
    """Test premis_relationship"""
    ET.register_namespace('premis', 'info:lc/xmlns/premis-v2')
    rel = o.premis_relationship('a', 'b', p.premis_identifier('c', 'd'))
    xml = '<premis:relationship xmlns:premis="info:lc/xmlns/premis-v2">' \
          '<premis:relationshipType>a</premis:relationshipType>' \
          '<premis:relationshipSubType>b</premis:relationshipSubType>' \
          '<premis:relatedObjectIdentification><premis:relatedObjectIdentifierType>' \
          'c</premis:relatedObjectIdentifierType><premis:relatedObjectIdentifierValue>' \
          'd</premis:relatedObjectIdentifierValue>' \
          '</premis:relatedObjectIdentification></premis:relationship>'
    assert ET.tostring(rel) == xml

def test_environment():
    """Test premis_environment"""
    ET.register_namespace('premis', 'info:lc/xmlns/premis-v2')
    rel = o.premis_environment(p.premis_identifier('c', 'd'))
    xml = '<premis:environment xmlns:premis="info:lc/xmlns/premis-v2"><premis:dependency>' \
          '<premis:dependencyIdentifier><premis:dependencyIdentifierType>' \
          'c</premis:dependencyIdentifierType><premis:dependencyIdentifierValue>' \
          'd</premis:dependencyIdentifierValue></premis:dependencyIdentifier>' \
          '</premis:dependency></premis:environment>'
    assert ET.tostring(rel) == xml

    rel = o.premis_environment(p.premis_identifier('c', 'd', 'dependency'))
    xml = '<premis:environment xmlns:premis="info:lc/xmlns/premis-v2"><premis:dependency>' \
          '<premis:dependencyIdentifier><premis:dependencyIdentifierType>' \
          'c</premis:dependencyIdentifierType><premis:dependencyIdentifierValue>' \
          'd</premis:dependencyIdentifierValue></premis:dependencyIdentifier>' \
          '</premis:dependency></premis:environment>'
    assert ET.tostring(rel) == xml


def test_object():
    """Test premis_premis"""
    ET.register_namespace('premis', 'info:lc/xmlns/premis-v2')
    ET.register_namespace('xsi', 'http://www.w3.org/2001/XMLSchema-instance')
    obj1 = o.premis_object(p.premis_identifier('a', 'b'), original_name='c')
    obj2 = o.premis_object(p.premis_identifier('a', 'b'), representation=True)
    xml1 = '<premis:object xmlns:premis="info:lc/xmlns/premis-v2" ' \
           'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" ' \
           'xsi:type="premis:file"><premis:objectIdentifier>' \
           '<premis:objectIdentifierType>a</premis:objectIdentifierType>' \
           '<premis:objectIdentifierValue>b</premis:objectIdentifierValue>' \
           '</premis:objectIdentifier><premis:originalName>c' \
           '</premis:originalName></premis:object>'
    xml2 = '<premis:object xmlns:premis="info:lc/xmlns/premis-v2" ' \
           'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" '\
           'xsi:type="premis:representation"><premis:objectIdentifier>' \
           '<premis:objectIdentifierType>a</premis:objectIdentifierType>' \
           '<premis:objectIdentifierValue>b</premis:objectIdentifierValue>' \
           '</premis:objectIdentifier></premis:object>'

    assert ET.tostring(obj1) == xml1
    assert ET.tostring(obj2) == xml2


def test_iter_objects():
    """Test iter_objects"""
    # TODO


def test_filter_objects():
    """Test filter_objects"""
    # TODO


def test_contains_object():
    """Test contains_object"""
    # TODO


def test_object_count():
    """Test contains_object"""
    # TODO


def test_objects_with_type():
    """Test contains_object"""
    # TODO

