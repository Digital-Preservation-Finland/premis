"""Test for the Premis object class"""
from __future__ import unicode_literals

import six

import lxml.etree as ET
import xml_helpers.utils as u
import premis.base as p
import premis.object_base as o


def test_fixity():
    """Test fixity"""
    fixity = o.fixity('xxx', 'yyy')
    xml = ('<premis:fixity xmlns:premis="info:lc/xmlns/premis-v2">'
           '<premis:messageDigestAlgorithm>yyy</premis:messageDigestAlgorithm>'
           '<premis:messageDigest>xxx</premis:messageDigest>'
           '</premis:fixity>')
    assert u.compare_trees(fixity, ET.fromstring(xml))


# pylint: disable=invalid-name
def test_format_designation():
    """Test format_designation"""
    fd = o.format_designation('xxx', 'yyy')
    xml = ('<premis:formatDesignation xmlns:premis="info:lc/xmlns/premis-v2">'
           '<premis:formatName>xxx</premis:formatName>'
           '<premis:formatVersion>yyy</premis:formatVersion>'
           '</premis:formatDesignation>')
    assert u.compare_trees(fd, ET.fromstring(xml))


# pylint: disable=invalid-name
def test_format_registry():
    """Test format_registry"""
    fd = o.format_registry('xxx', 'yyy')
    xml = ('<premis:formatRegistry xmlns:premis="info:lc/xmlns/premis-v2">'
           '<premis:formatRegistryName>xxx</premis:formatRegistryName>'
           '<premis:formatRegistryKey>yyy</premis:formatRegistryKey>'
           '</premis:formatRegistry>')
    assert u.compare_trees(fd, ET.fromstring(xml))


# pylint: disable=invalid-name
def test_format():
    """Test format"""
    fd = o.format_designation('xxx', 'yyy')
    form = o.format(child_elements=[fd])
    xml = ('<premis:format xmlns:premis="info:lc/xmlns/premis-v2">'
           '<premis:formatDesignation>'
           '<premis:formatName>xxx</premis:formatName>'
           '<premis:formatVersion>yyy</premis:formatVersion>'
           '</premis:formatDesignation></premis:format>')
    assert u.compare_trees(form, ET.fromstring(xml))


def test_date_created():
    """Test date_created"""
    date = o.date_created('2012-12-12T12:12:12')
    xml = (
        '<premis:dateCreatedByApplication '
        'xmlns:premis="info:lc/xmlns/premis-v2">'
        '2012-12-12T12:12:12</premis:dateCreatedByApplication>'
    )
    assert u.compare_trees(date, ET.fromstring(xml))


def test_creating_application():
    """Test creating_application"""
    date = o.date_created('2012-12-12T12:12:12')
    create = o.creating_application(child_elements=[date])
    xml = ('<premis:creatingApplication '
           'xmlns:premis="info:lc/xmlns/premis-v2">'
           '<premis:dateCreatedByApplication>2012-12-12T12:12:12'
           '</premis:dateCreatedByApplication>'
           '</premis:creatingApplication>')
    assert u.compare_trees(create, ET.fromstring(xml))


# pylint: disable=invalid-name
def test_object_characteristics():
    """Test object_characteristics"""
    fixity = o.fixity('xxx', 'yyy')
    oc = o.object_characteristics(child_elements=[fixity])
    xml = (
        '<premis:objectCharacteristics xmlns:premis="info:lc/xmlns/premis-v2">'
        '<premis:compositionLevel>0</premis:compositionLevel><premis:fixity>'
        '<premis:messageDigestAlgorithm>yyy</premis:messageDigestAlgorithm>'
        '<premis:messageDigest>xxx</premis:messageDigest>'
        '</premis:fixity></premis:objectCharacteristics>'
    )
    assert u.compare_trees(oc, ET.fromstring(xml))


def test_relationship():
    """Test relationship"""
    rel = o.relationship('a', 'b', p.identifier('c', 'd'))
    xml = ('<premis:relationship xmlns:premis="info:lc/xmlns/premis-v2">'
           '<premis:relationshipType>a</premis:relationshipType>'
           '<premis:relationshipSubType>b</premis:relationshipSubType>'
           '<premis:relatedObjectIdentification>'
           '<premis:relatedObjectIdentifierType>'
           'c</premis:relatedObjectIdentifierType>'
           '<premis:relatedObjectIdentifierValue>'
           'd</premis:relatedObjectIdentifierValue>'
           '</premis:relatedObjectIdentification></premis:relationship>')
    assert u.compare_trees(rel, ET.fromstring(xml))


def test_environment():
    """Test premis_environment"""
    env = o.environment(characteristic='a',
                        purposes=['b'],
                        child_elements=[o.dependency(), o.dependency()])
    xml = (
        '<premis:environment xmlns:premis="info:lc/xmlns/premis-v2">'
        '<premis:environmentCharacteristic>a'
        '</premis:environmentCharacteristic>'
        '<premis:environmentPurpose>b</premis:environmentPurpose>'
        '<premis:dependency></premis:dependency>'
        '<premis:dependency></premis:dependency>'
        '</premis:environment>')
    assert u.compare_trees(env, ET.fromstring(xml))


def test_dependency():
    """Test premis_dependency"""
    env = o.dependency(
        names=['a'],
        identifiers=[p.identifier('c', 'd', prefix='dependency')])
    xml = (
        '<premis:dependency xmlns:premis="info:lc/xmlns/premis-v2">'
        '<premis:dependencyName>a</premis:dependencyName>'
        '<premis:dependencyIdentifier><premis:dependencyIdentifierType>'
        'c</premis:dependencyIdentifierType><premis:dependencyIdentifierValue>'
        'd</premis:dependencyIdentifierValue></premis:dependencyIdentifier>'
        '</premis:dependency>')
    assert u.compare_trees(env, ET.fromstring(xml))


def test_object():
    """Test premis_premis"""
    obj1 = o.object(p.identifier('a', 'b'), original_name='c')
    obj2 = o.object(p.identifier('a', 'b'), representation=True)
    xml1 = ('<premis:object xmlns:premis="info:lc/xmlns/premis-v2" '
            'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" '
            'xsi:type="premis:file"><premis:objectIdentifier>'
            '<premis:objectIdentifierType>a</premis:objectIdentifierType>'
            '<premis:objectIdentifierValue>b</premis:objectIdentifierValue>'
            '</premis:objectIdentifier><premis:originalName>c'
            '</premis:originalName></premis:object>')
    xml2 = ('<premis:object xmlns:premis="info:lc/xmlns/premis-v2" '
            'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" '
            'xsi:type="premis:representation"><premis:objectIdentifier>'
            '<premis:objectIdentifierType>a</premis:objectIdentifierType>'
            '<premis:objectIdentifierValue>b</premis:objectIdentifierValue>'
            '</premis:objectIdentifier></premis:object>')

    assert u.compare_trees(obj1, ET.fromstring(xml1))
    assert u.compare_trees(obj2, ET.fromstring(xml2))


def test_iter_objects():
    """Test iter_objects"""
    obj1 = o.object(p.identifier('x', 'y1', 'object'))
    obj2 = o.object(p.identifier('x', 'y2', 'object'))
    obj3 = o.object(p.identifier('x', 'y3', 'object'))
    prem = p.premis(child_elements=[obj1, obj2, obj3])
    iterator = o.iter_objects(prem)
    i = 0
    for iter_elem in iterator:
        i = i + 1
        (_, id_value) = p.parse_identifier_type_value(
            p.parse_identifier(iter_elem, 'object'), 'object')
        assert id_value == 'y' + six.text_type(i)
    assert i == 3


def test_find_object_by_id():
    """Test find_object_by_id"""
    object1 = o.object(p.identifier('local', 'id1', 'object'))
    object2 = o.object(p.identifier('local', 'id2', 'object'))
    object3 = o.object(p.identifier('local', 'id3', 'object'))
    xml = p.premis(child_elements=[object1, object2, object3])
    obj = o.find_object_by_id(xml, 'id2')
    assert p.parse_identifier_type_value(p.parse_identifier(obj)) == (
        'local', 'id2')


def test_filter_objects():
    """Test filter_objects"""
    obj1 = o.object(p.identifier('x', 'y1', 'object'))
    obj2 = o.object(p.identifier('x', 'y2', 'object'))
    obj3 = o.object(p.identifier('x', 'y3', 'object'))
    prem1 = p.premis(child_elements=[obj1, obj2, obj3])
    prem2 = p.premis(child_elements=[obj1, obj3])
    filtered = o.filter_objects(o.iter_objects(prem1), prem2)
    i = 0
    for filt_el in filtered:
        i = i + 1
        (_, id_value) = p.parse_identifier_type_value(
            p.parse_identifier(filt_el, 'object'), 'object')
        assert id_value == 'y2'
    assert i == 1


def test_contains_object():
    """Test contains_object"""
    obj1 = o.object(p.identifier('x', 'y1', 'object'))
    obj2 = o.object(p.identifier('x', 'y2', 'object'))
    obj3 = o.object(p.identifier('x', 'y3', 'object'))
    prem1 = p.premis(child_elements=[obj1, obj2, obj3])
    prem2 = p.premis(child_elements=[obj1, obj2])

    assert o.contains_object(obj3, prem1)
    assert not o.contains_object(obj3, prem2)


def test_object_count():
    """Test object_count"""
    obj1 = o.object(p.identifier('x', 'y1', 'object'))
    obj2 = o.object(p.identifier('x', 'y2', 'object'))
    obj3 = o.object(p.identifier('x', 'y3', 'object'))
    prem = p.premis(child_elements=[obj1, obj2, obj3])
    assert o.object_count(prem) == 3


def test_objects_with_type():
    """Test objects_with_type"""
    obj1 = o.object(p.identifier('x1', 'y1', 'object'))
    obj2 = o.object(p.identifier('x1', 'y2', 'object'))
    obj3 = o.object(p.identifier('x2', 'y3', 'object'))
    filtered = o.objects_with_type([obj1, obj2, obj3], 'x1')
    i = 0
    for filt_el in filtered:
        i = i + 1
        (id_type, _) = p.parse_identifier_type_value(
            p.parse_identifier(filt_el, 'object'), 'object')
        assert id_type == 'x1'
    assert i == 2


def test_parse_object_type():
    """Test parse_object_type"""
    obj = o.object(p.identifier('x', 'y', 'object'), representation=True)
    assert o.parse_object_type(obj).endswith('representation')


# pylint: disable=invalid-name
def test_parse_fixity():
    """Test parse_fixity"""
    fixity = o.fixity('xxx', 'yyy')
    oc = o.object_characteristics(child_elements=[fixity])
    obj = o.object(p.identifier('x', 'y', 'object'), child_elements=[oc])
    assert o.parse_fixity(obj) == ('yyy', 'xxx')


# pylint: disable=invalid-name
def test_parse_format():
    """Test parse_format"""
    fd = o.format_designation('xxx', 'yyy')
    form = o.format(child_elements=[fd])
    oc = o.object_characteristics(child_elements=[form])
    obj = o.object(p.identifier('x', 'y', 'object'), child_elements=[oc])
    assert o.parse_format(obj) == ('xxx', 'yyy')


# pylint: disable=invalid-name
def test_parse_format_noversion():
    """Test parse_format"""
    fd = o.format_designation('xxx')
    form = o.format(child_elements=[fd])
    oc = o.object_characteristics(child_elements=[form])
    obj = o.object(p.identifier('x', 'y', 'object'), child_elements=[oc])
    assert o.parse_format(obj) == ('xxx', None)


# pylint: disable=invalid-name
def test_parse_format_registry():
    """Test parse_format"""
    fd = o.format_registry('xxx', 'yyy')
    form = o.format(child_elements=[fd])
    oc = o.object_characteristics(child_elements=[form])
    obj = o.object(p.identifier('x', 'y', 'object'), child_elements=[oc])
    assert o.parse_format_registry(obj) == ('xxx', 'yyy')


def test_parse_original_name():
    """Test parse_original_name"""
    obj = o.object(p.identifier('x', 'y', 'object'), original_name='aaa')
    assert o.parse_original_name(obj) == 'aaa'


def test_parse_environment():
    """Test parse_environment"""
    env = o.environment(child_elements=[
        o.dependency(identifiers=[
            p.identifier('c', 'd', 'dependency')
        ])
    ])
    obj = o.object(p.identifier('x', 'y', 'object'), child_elements=[env])
    penv = o.parse_environment(obj)
    xml = ('<premis:environment xmlns:premis="info:lc/xmlns/premis-v2" '
           'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">'
           '<premis:dependency>'
           '<premis:dependencyIdentifier><premis:dependencyIdentifierType>'
           'c</premis:dependencyIdentifierType>'
           '<premis:dependencyIdentifierValue>'
           'd</premis:dependencyIdentifierValue></premis:dependencyIdentifier>'
           '</premis:dependency></premis:environment>')
    assert u.compare_trees(penv[0], ET.fromstring(xml))

    # Add another environment to the object, only the one with the purpose 'a'
    # should be returned
    env2 = o.environment(
        purposes=['a'],
        child_elements=[o.dependency(
            identifiers=[p.identifier('c', 'd', 'dependency')])])
    obj = o.object(p.identifier('x', 'y', 'object'),
                   child_elements=[env, env2])
    penv = o.parse_environment(obj, purpose='a')
    assert len(penv) == 1
    xml = ('<premis:environment xmlns:premis="info:lc/xmlns/premis-v2" '
           'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">'
           '<premis:environmentPurpose>a</premis:environmentPurpose>'
           '<premis:dependency>'
           '<premis:dependencyIdentifier><premis:dependencyIdentifierType>'
           'c</premis:dependencyIdentifierType>'
           '<premis:dependencyIdentifierValue>'
           'd</premis:dependencyIdentifierValue></premis:dependencyIdentifier>'
           '</premis:dependency></premis:environment>')
    assert u.compare_trees(penv[0], ET.fromstring(xml))


def test_parse_dependency():
    """Test parse_dependency"""

    env = o.environment(child_elements=[
        o.dependency(identifiers=[
            p.identifier('e', 'f', prefix='dependency')]),
        o.dependency(identifiers=[
            p.identifier('c', 'd', prefix='dependency')])])
    obj = o.object(p.identifier('x', 'y', 'object'), child_elements=[env])
    dep = o.parse_dependency(obj)

    xml1 = ('<premis:dependency xmlns:premis="info:lc/xmlns/premis-v2" '
            'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">'
            '<premis:dependencyIdentifier><premis:dependencyIdentifierType>'
            'e</premis:dependencyIdentifierType>'
            '<premis:dependencyIdentifierValue>'
            'f</premis:dependencyIdentifierValue>'
            '</premis:dependencyIdentifier>'
            '</premis:dependency>')

    xml2 = ('<premis:dependency xmlns:premis="info:lc/xmlns/premis-v2" '
            'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">'
            '<premis:dependencyIdentifier><premis:dependencyIdentifierType>'
            'c</premis:dependencyIdentifierType>'
            '<premis:dependencyIdentifierValue>'
            'd</premis:dependencyIdentifierValue>'
            '</premis:dependencyIdentifier>'
            '</premis:dependency>')

    test_list = [xml1, xml2]

    i = 0

    for iter_depend in dep:
        assert u.compare_trees(iter_depend, ET.fromstring(test_list[i]))
        i += 1


def test_parse_relationship():
    """Test parse_relationship"""
    rel = o.relationship('a', 'b', p.identifier('c', 'd'))
    obj = o.object(p.identifier('x', 'y', 'object'), child_elements=[rel])
    rel2 = o.parse_relationship(obj)
    xml = ('<premis:relationship xmlns:premis="info:lc/xmlns/premis-v2" '
           'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">'
           '<premis:relationshipType>a</premis:relationshipType>'
           '<premis:relationshipSubType>b</premis:relationshipSubType>'
           '<premis:relatedObjectIdentification>'
           '<premis:relatedObjectIdentifierType>'
           'c</premis:relatedObjectIdentifierType>'
           '<premis:relatedObjectIdentifierValue>'
           'd</premis:relatedObjectIdentifierValue>'
           '</premis:relatedObjectIdentification></premis:relationship>')
    assert u.compare_trees(rel2, ET.fromstring(xml))


def test_parse_relationship_type():
    """Test parse_relationship_type"""
    rel = o.relationship('a', 'b', p.identifier('c', 'd'))
    assert o.parse_relationship_type(rel) == 'a'


def test_parse_relationship_subtype():
    """Test parse_relationship_subtype"""
    rel = o.relationship('a', 'b', p.identifier('c', 'd'))
    assert o.parse_relationship_subtype(rel) == 'b'
