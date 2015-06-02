"""Test for the Premis class"""

import xml.etree.ElementTree as ET

REPORT_PATH = 'tests/data/premis_test_validation_report.xml'

PREMIS_NS = 'info:lc/xmlns/premis-v2'
XSI_NS = 'http://www.w3.org/2001/XMLSchema-instance'


class PremisEvent(object):

    """Docstring for PremisEvent. """

    def __init__(self):
        """TODO: to be defined1. """
        pass

    @classmethod
    def fromstring(cls, string):
        """TODO: Docstring for fromstring.

        :string: TODO
        :returns: TODO

        """

        return cls(string)


def premis_ns(tag, prefix=""):
    """TODO: Docstring for premis.

    :tag: TODO
    :returns: TODO

    """
    if prefix:
        tag = tag[0].upper() + tag[1:]
        return '{%s}%s%s' % (PREMIS_NS, prefix, tag)
    return '{%s}%s' % (PREMIS_NS, tag)


def _element(tag, prefix=""):
    """TODO: Docstring for _element.

    :element: TODO
    :returns: TODO

    """
    return ET.Element(premis_ns(tag, prefix))


def _subelement(parent, tag, prefix=""):
    """TODO: Docstring for _element.

    :element: TODO
    :returns: TODO

    """
    return ET.SubElement(parent, premis_ns(tag, prefix))


def xsi_ns(tag):
    """TODO: Docstring for premis.

    :tag: TODO
    :returns: TODO

    """
    return '{%s}%s' % (XSI_NS, tag)


def premis_identifier(identifier_type, identifier_value, prefix=""):
    """Return PREMIS identifier segments.

    Produces without prefix the following PREMIS segment::


          <premis:objectIdentifier>
              <premis:objectIdentifierType>
                  pas-sig-id
              </premis:objectIdentifierType>
              <premis:objectIdentifierValue>
                  pas-sig-c8b978b6-e160-4497-8027-e19fa0297766
              </premis:objectIdentifierValue>
          </premis:objectIdentifier>

    With prefix='relatedObject' the following PREMIS segment::

          <premis:relatedObjectIdentification>
              <premis:relatedObjectIdentifierType>
                  pas-sip-id
              </premis:relatedObjectIdentifierType>
              <premis:relatedObjectIdentifierValue>
                  pas-sip-1ac641ec-223f-42f4-86c2-9402451d63bf
              </premis:relatedObjectIdentifierValue>
          </premis:relatedObjectIdentification>

    With prefix='dependency' the following PREMIS segment::

        <premis:dependencyIdentifier>
            <premis:dependencyIdentifierType>
                local</premis:dependencyIdentifierType>
            <premis:dependencyIdentifierValue>
                kdk-sip-premis-object001</premis:dependencyIdentifierValue>
        </premis:dependencyIdentifier>

    With prefix='linking' the following PREMIS segment::

        <premis:linkingObjectIdentifier>
            <premis:linkingObjectIdentifierType>
                pas-sip-id</premis:linkingObjectIdentifierType>
            <premis:linkingObjectIdentifierValue>
                pas-sip-1ac641ec</premis:linkingObjectIdentifierValue>
        </premis:linkingObjectIdentifier>

    """

    if not prefix:
        prefix = 'object'

    if prefix == 'relatedObject':
        _identifier = _element('Identification', prefix)
    else:
        _identifier = _element('Identifier', prefix)

    _type = _subelement(_identifier, 'IdentifierValue', prefix)
    _type.text = identifier_type

    _value = _subelement(_identifier, 'IdentifierType', prefix)
    _value.text = identifier_value

    return _identifier


def get_identifier_type_value(object_or_identifier):
    """Return identifierType and IdentifierValue from given PREMIS identifier
    or object. If segment contains multiple identifiers, returns first
    occurrence.

    :object_or_identifier: TODO
    :returns: (identifier_type, identifier_value)

    """

    identifier = object_or_identifier

    if identifier.find(premis_ns('objectIdentifier')) is not None:
        identifier = identifier.find(premis_ns('objectIdentifier'))

    if identifier.find(premis_ns('relatedObjectIdentification')) is not None:
        identifier = identifier.find(premis_ns('relatedObjectIdentification'))

    return (
        identifier.find(premis_ns('objectIdentifierType')).text,
        identifier.find(premis_ns('objectIdentifierValue')).text)


def premis_relationship(
        relationship_type, relationship_subtype,
        related_object):

    """TODO: Docstring for premis_relationshi.

    :relationship_type: TODO
    :subtype: TODO
    :related_object_identification: TODO
    :returns: TODO

    Produces the following PREMIS segment::

      <premis:relationship>

          <premis:relationshipType>structural</premis:relationshipType>
          <premis:relationshipSubType>
              is included in
          </premis:relationshipSubType>

          {{ premis_identifier(prefix=related) }}

      </premis:relationship>

    """

    relationship = _element('relationship')

    _type = _subelement(relationship, 'relationshipType')
    _type.text = relationship_type

    _subtype = _subelement(relationship, 'relationshipSubType')
    _subtype.text = relationship_subtype

    (related_type, related_value) = get_identifier_type_value(
        related_object)

    related_identifier = premis_identifier(
        related_type, related_value, prefix='relatedObject')

    relationship.append(related_identifier)

    return relationship


def premis_environment(dependency_identifier=None):
    """TODO: Docstring for premis_environment.

    :dependency: TODO
    :returns: TODO

    Produces the following PREMIS segment::

        <premis:environment>
            <premis:dependency>

                {{ dependency_identifier }}

            </premis:dependency>
        </premis:environment>

    """

    environment = _element('environment')

    if dependency_identifier:
        dependency = _subelement(environment, 'dependency')
        dependency.append(dependency_identifier)

    return environment


def premis_object(
        original_name, child_elements=None,
        representation=False):

    """TODO: Docstring for Event.

    :fields: TODO
    :returns: TODO

        <premis:object xsi:type="premis:representation">

            {{ premis_identifier() }}

            <premis:originalName>varmiste.sig</premis:originalName>

            {{ premis_relationship() }}

        </premis:object>

    """

    _object = _element('object')

    _original_name = _subelement(_object, 'originalName')
    _original_name.text = original_name

    if representation:
        _object.set(xsi_ns('type'), 'premis:representation')

    if child_elements:
        for element in child_elements:
            _object.append(element)

    return _object


def premis_premis_ns(child_elements=None):
    """TODO: Docstring for premis_premis.
    :returns: TODO

    """
    _premis = _element('premis')
    _premis.set(
        xsi_ns('schemaLocation'),
        'info:lc/xmlns/premis-v2 '
        'http://www.loc.gov/standards/premis/premis.xsd')

    if child_elements:
        for element in child_elements:
            _premis.append(element)
    return _premis


def premis_event_outcome(outcome, detail_note):
    """TODO: Docstring for premis_event_outcome_information.

    :arg1: TODO
    :returns: TODO

        <premis:eventOutcomeInformation>
            <premis:eventOutcome>success</premis:eventOutcome>
            <premis:eventOutcomeDetail>
                <premis:eventOutcomeDetailNote>
                    mets.xml sha1 4d0c38dedcb5e5fc93586cfa2b7ebedbd63 OK
                </premis:eventOutcomeDetailNote>
            </premis:eventOutcomeDetail>
        </premis:eventOutcomeInformation>


    """

    outcome_information = _element('eventOutcomeInformation')

    _outcome = _subelement(outcome_information, 'eventOutcome')
    _outcome.text = outcome

    detail = _subelement(outcome_information, 'eventOutcomeDetail')

    _detail_note = _subelement(detail, 'eventOutcomeDetailNote')
    _detail_note.text = detail_note

    return outcome_information


def premis_event(
        event_type, event_date_time, event_detail, child_elements=[],
        linking_objects=[]):
    """TODO: Docstring for premis_event.

    :arg1: TODO
    :returns: TODO


        <premis:event>

            <premis:eventType>digital signature validation</premis:eventType>
            <premis:eventDateTime>2015-02-03T13:04:25</premis:eventDateTime>
            <premis:eventDetail>
                Submission information package digital signature validation
            </premis:eventDetail>

            {{ child elements }}

        </premis:event>


    """

    event = _element('event')

    _event_type = _subelement(event, 'eventType')
    _event_type.text = event_type

    _event_date_time = _subelement(event, 'eventDateTime')
    _event_date_time.text = event_date_time

    _event_detail = _subelement(event, 'eventDetail')
    _event_detail.text = event_detail

    for element in child_elements:
        event.append(element)

    for _object in linking_objects:
        linking_object = premis_identifier(
            _object.findtext('.//' + premis_ns('objectIdentifierType')),
            _object.findtext('.//' + premis_ns('objectIdentifierValue')),
            'linkingObject')
        event.append(linking_object)

    return event


def indent(elem, level=0):
    """Indent the elementtree"""
    i = "\n" + level*"  "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:
            indent(elem, level+1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i


def serialize(element):
    """TODO: Docstring for serialize.

    :element: TODO
    :returns: TODO

    """

    def register_namespace(prefix, uri):
        """foo"""
        ns_map = getattr(ET, '_namespace_map')
        ns_map[uri] = prefix

    register_namespace('premis', PREMIS_NS)
    register_namespace('xsi', XSI_NS)

    indent(element)
    return ET.tostring(element)


def test_premis_ns():
    """TODO: Docstring for test_premis.
    :returns: TODO

    """

    # SIP & METS object identifiers

    sip_identifier = premis_identifier('pas-sip-id', 'csc-sip-001')
    mets_identifier = premis_identifier('METS-OBJID', 'mets-objid-999')

    # PREMIS relationship

    relationship = premis_relationship(
        relationship_type='structural',
        relationship_subtype='is included in',
        related_object=mets_identifier)

    # PREMIS enviroment

    dependency_identifier = premis_identifier(
        'local', 'kdk-sip-premis-object001', 'dependency')

    environment = premis_environment(dependency_identifier)

    # PREMIS object

    sip_object = premis_object(
        original_name='csc-sip-001.zip',
        child_elements=[sip_identifier, relationship, environment],
        representation=True)

    # Create the PREMIS event

    event_identifier = premis_identifier(
        'pas-event-id', 'event-id-1234', 'event')

    event_outcome = premis_event_outcome(
        'success', 'Validation successful - OK')

    event = premis_event(
        'digital signature validation',
        '1.1.2015',
        'Submission information package signature',
        child_elements=[event_identifier, event_outcome])

    # PREMIS XML & print

    premis = premis_premis_ns([sip_object, event])
    print serialize(premis)

    xml = serialize(premis)

    premis = ET.fromstring(xml)

    print serialize(premis)

