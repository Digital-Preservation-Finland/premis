"""Test for the Premis class"""

import preservation.premis as p
import xml.etree.ElementTree as ET

NAMESPACES = {'premis': 'info:lc/xmlns/premis-v2',
              'xsi': 'http://www.w3.org/2001/XMLSchema-instance'}


def test_premis_ns():
    """TODO: Docstring for test_premis.
    :returns: TODO

    """

    # SIP & METS object identifiers

    sip_identifier = p.premis_identifier('preservation-sip-id', 'csc-sip-001')
    mets_identifier = p.premis_identifier('METS-OBJID', 'mets-objid-999')

    # PREMIS relationship

    relationship = p.premis_relationship(
        relationship_type='structural',
        relationship_subtype='is included in',
        related_object=mets_identifier)

    # PREMIS enviroment

    dependency_identifier = p.premis_identifier(
        'local', 'kdk-sip-premis-object001', 'dependency')

    environment = p.premis_environment(dependency_identifier)

    # PREMIS object

    sip_object = p.premis_object(
        original_name='csc-sip-001.zip',
        identifier=sip_identifier,
        child_elements=[relationship, environment],
        representation=True)

    # Create the PREMIS event

    event_identifier = p.premis_identifier(
        'preservation-event-id', 'event-id-1234', 'event')

    event_outcome = p.premis_event_outcome(
        'success', 'Validation successful - OK')

    event = p.premis_event(
        event_identifier,
        'digital signature validation',
        '1.1.2015',
        'Submission information package signature',
        child_elements=[event_outcome])

    # PREMIS XML & print

    premis = p.premis_premis([sip_object, event])
    print common_xml_utils.utils.serialize(premis, NAMESPACES)

    xml = common_xml_utils.utils..serialize(premis, NAMESPACES)

    premis_root = ET.fromstring(xml)

    print common_xml_utils.utils.serialize(premis_root, NAMESPACES)
