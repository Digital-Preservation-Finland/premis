"""Test for the Premis object class"""

import lxml.etree as ET
import premis.base as p
import premis.object_base as o


def test_fixity():
    """Test fixity"""
    # TODO


def test_format_designation():
    """Test format_designation"""
    # TODO


def test_format():
    """Test format"""
    # TODO


def test_date_created():
    """Test date_created"""
    # TODO


def test_creating_application():
    """Test creating_application"""
    # TODO


def test_object_characteristics():
    """Test object_characteristics"""
    # TODO


def test_relationship():
    """Test relationship"""
    rel = o.relationship('a', 'b', p.identifier('c', 'd'))
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
    rel = o.environment(p.identifier('c', 'd'))
    xml = '<premis:environment xmlns:premis="info:lc/xmlns/premis-v2"><premis:dependency>' \
          '<premis:dependencyIdentifier><premis:dependencyIdentifierType>' \
          'c</premis:dependencyIdentifierType><premis:dependencyIdentifierValue>' \
          'd</premis:dependencyIdentifierValue></premis:dependencyIdentifier>' \
          '</premis:dependency></premis:environment>'
    assert ET.tostring(rel) == xml

    rel = o.environment(p.identifier('c', 'd', 'dependency'))
    xml = '<premis:environment xmlns:premis="info:lc/xmlns/premis-v2"><premis:dependency>' \
          '<premis:dependencyIdentifier><premis:dependencyIdentifierType>' \
          'c</premis:dependencyIdentifierType><premis:dependencyIdentifierValue>' \
          'd</premis:dependencyIdentifierValue></premis:dependencyIdentifier>' \
          '</premis:dependency></premis:environment>'
    assert ET.tostring(rel) == xml


def test_object():
    """Test premis_premis"""
    obj1 = o.object(p.identifier('a', 'b'), original_name='c')
    obj2 = o.object(p.identifier('a', 'b'), representation=True)
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
    """Test object_count"""
    # TODO


def test_objects_with_type():
    """Test objects_with_type"""
    # TODO

def test_parse_fixity():
    """Test parse_fixity"""
    # TODO


def test_parse_format():
    """Test parse_format"""
    # TODO


def test_parse_originalname():
    """Test parse_originalname"""
    # TODO


def test_parse_environment():
    """Test parse_environment"""
    # TODO


def test_parse_dependency():
    """Test parse_dependency"""
    # TODO


def test_parse_relationship():
    """Test parse_relationship"""
    # TODO


def test_parse_relationshiptype():
    """Test parse_relationshiptype"""
    # TODO


def test_parse_relationshipsubtype():
    """Test parse_relationshipsubtype"""
    # TODO



