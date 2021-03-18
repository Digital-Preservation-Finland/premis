"""Test for the Premis event class"""
from __future__ import unicode_literals

import six
from pytest import raises

import lxml.etree as ET
import xml_helpers.utils as u

import premis.base as p
import premis.event_base as e

# using lxml.etree causes these, but importing c extensions is not a problem
# for us
# pylint: disable=c-extension-no-member


def test_outcome():
    """Test event_outcome"""
    outcome = e.outcome('success', 'OK')
    xml = (
        '<premis:eventOutcomeInformation xmlns:premis="info:lc/xmlns/premis-v2">'
        '<premis:eventOutcome>success</premis:eventOutcome>'
        '<premis:eventOutcomeDetail><premis:eventOutcomeDetailNote>OK'
        '</premis:eventOutcomeDetailNote></premis:eventOutcomeDetail>'
        '</premis:eventOutcomeInformation>'
    )
    assert u.compare_trees(outcome, ET.fromstring(xml))


def test_event():
    """Test event"""
    event = e.event(
        p.identifier('a', 'b', 'event'), 'c', 'd', 'e',
        linking_objects=[p.identifier('f', 'g')])
    xml = ('<premis:event xmlns:premis="info:lc/xmlns/premis-v2">'
           '<premis:eventIdentifier><premis:eventIdentifierType>a'
           '</premis:eventIdentifierType><premis:eventIdentifierValue>b'
           '</premis:eventIdentifierValue></premis:eventIdentifier>'
           '<premis:eventType>c</premis:eventType>'
           '<premis:eventDateTime>d</premis:eventDateTime>'
           '<premis:eventDetail>e</premis:eventDetail>'
           '<premis:linkingObjectIdentifier>'
           '<premis:linkingObjectIdentifierType>f</premis:linkingObjectIdentifierType>'
           '<premis:linkingObjectIdentifierValue>g</premis:linkingObjectIdentifierValue>'
           '</premis:linkingObjectIdentifier></premis:event>')
    assert u.compare_trees(event, ET.fromstring(xml))


def test_iter_events():
    """Test iter_events"""
    event1 = e.event(p.identifier('local', 'id1', 'event'), 'tyyppi1',
                     '2012-12-12T12:12:12', 'detaili1')
    event2 = e.event(p.identifier('local', 'id2', 'event'), 'tyyppi2',
                     '2012-12-12T12:12:12', 'detaili2')
    event3 = e.event(p.identifier('local', 'id3', 'event'), 'tyyppi3',
                     '2012-12-12T12:12:12', 'detaili2')
    premisroot = p.premis(child_elements=[event1, event2, event3])
    i = 0
    for event in e.iter_events(premisroot):
        i = i + 1
        assert e.parse_event_type(event) == 'tyyppi' + six.text_type(i)
    assert i == 3


def test_find_event_by_id():
    """Test find_event_by_id"""
    event1 = e.event(p.identifier('local', 'id1', 'event'), 'tyyppi',
                     '2012-12-12T12:12:12', 'detaili1')
    event2 = e.event(p.identifier('local', 'id2', 'event'), 'tyyppi',
                     '2012-12-12T12:12:12', 'detaili2')
    event3 = e.event(p.identifier('local', 'id3', 'event'), 'tyyppi2',
                     '2012-12-12T12:12:12', 'detaili2')
    xml = p.premis(child_elements=[event1, event2, event3])
    event = e.find_event_by_id(xml, 'id2')
    assert p.parse_identifier_type_value(p.parse_identifier(event, 'event'),
                                         'event') == ('local', 'id2')


def test_event_count():
    """Test event_count"""
    event1 = e.event(p.identifier('local', 'id1', 'event'), 'tyyppi',
                     '2012-12-12T12:12:12', 'detaili1')
    event2 = e.event(p.identifier('local', 'id2', 'event'), 'tyyppi',
                     '2012-12-12T12:12:12', 'detaili2')
    event3 = e.event(p.identifier('local', 'id3', 'event'), 'tyyppi2',
                     '2012-12-12T12:12:12', 'detaili2')
    xml = p.premis(child_elements=[event1, event2, event3])
    assert e.event_count(xml) == 3


def test_event_with_type_and_detail():
    """Test event_with_type_and_detail"""
    event1 = e.event(p.identifier('local', 'id1', 'event'), 'tyyppi',
                     '2012-12-12T12:12:12', 'detaili1')
    event2 = e.event(p.identifier('local', 'id2', 'event'), 'tyyppi',
                     '2012-12-12T12:12:12', 'detaili2')
    event3 = e.event(p.identifier('local', 'id3', 'event'), 'tyyppi2',
                     '2012-12-12T12:12:12', 'detaili2')
    i = 0
    for event in e.event_with_type_and_detail([event1, event2, event3],
                                              'tyyppi', 'detaili2'):
        i = i + 1
        assert e.parse_event_type(event) == 'tyyppi'
        assert e.parse_detail(event) == 'detaili2'
    assert i == 1


def test_events_with_outcome():
    """Test events_with_outcome"""
    outcome1 = e.outcome('success')
    outcome2 = e.outcome('failure')
    outcome3 = e.outcome('success')

    event1 = e.event(p.identifier('local', 'id1', 'event'), 'tyyppi',
                     '2012-12-12T12:12:12', 'detaili1',
                     child_elements=[outcome1])
    event2 = e.event(p.identifier('local', 'id2', 'event'), 'tyyppi',
                     '2012-12-12T12:12:12', 'detaili2',
                     child_elements=[outcome2])
    event3 = e.event(p.identifier('local', 'id3', 'event'), 'tyyppi',
                     '2012-12-12T12:12:12', 'detaili3',
                     child_elements=[outcome3])
    i = 0
    for success in e.events_with_outcome([event1, event2, event3], 'success'):
        assert e.parse_outcome(success) == 'success'
        i = i + 1
    assert i == 2


def test_outcome_extension():
    # Ignore continuation and long lines to make xml human-readable
    # noqa: E131, E501
    # pylint: disable=bad-continuation, line-too-long
    """Test that event outcome with XML extension works"""
    extensions = [ET.fromstring('<xxx />'), ET.fromstring('<yyy />')]
    xml_multiple_extensions = (
        '<premis:eventOutcomeInformation xmlns:premis="info:lc/xmlns/premis-v2">'
            '<premis:eventOutcome>success</premis:eventOutcome>'
            '<premis:eventOutcomeDetail>'
                '<premis:eventOutcomeDetailExtension><xxx /></premis:eventOutcomeDetailExtension>'
                '<premis:eventOutcomeDetailExtension><yyy /></premis:eventOutcomeDetailExtension>'
            '</premis:eventOutcomeDetail>'
        '</premis:eventOutcomeInformation>')

    xml_single_extension = (
        '<premis:eventOutcomeInformation xmlns:premis="info:lc/xmlns/premis-v2">'
            '<premis:eventOutcome>success</premis:eventOutcome>'
            '<premis:eventOutcomeDetail>'
                '<premis:eventOutcomeDetailExtension><xxx /><yyy /></premis:eventOutcomeDetailExtension>'
            '</premis:eventOutcomeDetail>'
        '</premis:eventOutcomeInformation>')

    event = ET.fromstring(xml_multiple_extensions)
    # Should fail, because detail_extension must not be string
    with raises(TypeError):
        e.outcome('success', detail_extension='<xxx />')
    # Should work with XML tree
    assert u.compare_trees(e.outcome('success', detail_extension=extensions), event)

    # Test that extensions are placed in single eventOutcomeDetailExtension element
    event = ET.fromstring(xml_single_extension)
    assert u.compare_trees(
        e.outcome('success', detail_extension=extensions, single_extension_element=True),
        event)


def test_parse_event_type():
    """Test parse_event_type"""
    event = e.event(p.identifier('a', 'b', 'event'), 'tyyppi',
                    '2012-12-12T12:12:12', 'detaili')
    assert e.parse_event_type(event) == 'tyyppi'


def test_parse_datetime():
    """Test parse_datetime"""
    event = e.event(p.identifier('a', 'b', 'event'), 'tyyppi',
                    '2012-12-12T12:12:12', 'detaili')
    assert e.parse_datetime(event) == '2012-12-12T12:12:12'


def test_parse_detail():
    """Test parse_detail"""
    event = e.event(p.identifier('a', 'b', 'event'), 'tyyppi',
                    '2012-12-12T12:12:12', 'detaili')
    assert e.parse_detail(event) == 'detaili'


def test_parse_outcome():
    """Test parse_outcome"""
    extensions = [ET.fromstring('<xxx />')]
    outcome = e.outcome('success', detail_note='xxx',
                        detail_extension=extensions)
    event = e.event(p.identifier('a', 'b', 'event'), 'tyyppi',
                    '2012-12-12T12:12:12', 'detaili', child_elements=[outcome])
    assert e.parse_outcome(event) == 'success'


def test_parse_outcome_detail_note():
    """Test parse_outcome_detail_note"""
    extensions = [ET.fromstring('<xxx />')]
    outcome = e.outcome('success', detail_note='xxx',
                        detail_extension=extensions)
    event = e.event(p.identifier('a', 'b', 'event'), 'tyyppi',
                    '2012-12-12T12:12:12', 'detaili', child_elements=[outcome])
    assert e.parse_outcome_detail_note(event) == 'xxx'


def test_parse_outcome_detail_extension():
    """Test parse_outcome_detail_extension"""
    xml = '<premis:eventOutcomeDetailExtension xmlns:premis="info:lc/xmlns/premis-v2">' \
          '<xxx /></premis:eventOutcomeDetailExtension>'
    tree = ET.fromstring(xml)
    outcome = e.outcome('success', detail_note='xxx',
                        detail_extension=[ET.fromstring('<xxx />')])
    event = e.event(p.identifier('a', 'b', 'event'), 'tyyppi',
                    '2012-12-12T12:12:12', 'detaili', child_elements=[outcome])
    assert u.compare_trees(e.parse_outcome_detail_extension(event), tree)
