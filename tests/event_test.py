"""Test for the Premis event class"""

import xml.etree.ElementTree as ET
import premis_tools.premis as p
import premis_tools.event as e

def test_event_outcome():
    """Test premis_event_outcome"""
    ET.register_namespace('premis', 'info:lc/xmlns/premis-v2')
    outcome = e.premis_event_outcome('success', 'OK')
    xml = '<premis:eventOutcomeInformation xmlns:premis="info:lc/xmlns/premis-v2">' \
          '<premis:eventOutcome>success</premis:eventOutcome>' \
          '<premis:eventOutcomeDetail><premis:eventOutcomeDetailNote>OK' \
          '</premis:eventOutcomeDetailNote></premis:eventOutcomeDetail>' \
          '</premis:eventOutcomeInformation>'
    assert ET.tostring(outcome) == xml

def test_event():
    """Test premis_event"""
    ET.register_namespace('premis', 'info:lc/xmlns/premis-v2')
    event = e.premis_event(
        p.premis_identifier('a', 'b', 'event'), 'c', 'd', 'e',
        linking_objects=[p.premis_identifier('f', 'g')])
    xml = '<premis:event xmlns:premis="info:lc/xmlns/premis-v2">' \
          '<premis:eventIdentifier><premis:eventIdentifierType>a' \
          '</premis:eventIdentifierType><premis:eventIdentifierValue>b' \
          '</premis:eventIdentifierValue></premis:eventIdentifier>' \
          '<premis:eventType>c</premis:eventType>' \
          '<premis:eventDateTime>d</premis:eventDateTime>' \
          '<premis:eventDetail>e</premis:eventDetail>' \
          '<premis:linkingObjectIdentifier>' \
          '<premis:linkingObjectIdentifierType>f</premis:linkingObjectIdentifierType>' \
          '<premis:linkingObjectIdentifierValue>g</premis:linkingObjectIdentifierValue>' \
          '</premis:linkingObjectIdentifier></premis:event>'
    assert ET.tostring(event) == xml


def test_iter_events():
    """Test iter_events"""
    # TODO


def test_find_event_by_id():
    """Test find_event_by_id"""
    # TODO


def test_event_count():
    """Test event_count"""
    # TODO


def test_event_with_type_and_detail():
    """Test premis_event_with_type_and_detail"""
    # TODO


def test_events_with_outcome():
    """Test events_with_outcome"""
    # TODO

