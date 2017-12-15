"""Functions for reading and generating PREMIS Data Dictionaries as
xml.etree.ElementTree data structures.

References:

    * PREMIS http://www.loc.gov/standards/premis/
    * ElementTree
    https://docs.python.org/2.6/library/xml.etree.elementtree.html

"""
import lxml.etree
from copy import deepcopy
from premis.base import _element, _subelement, premis_ns, \
    identifier, iter_elements, NAMESPACES
from xml_helpers.utils import decode_utf8, encode_utf8


def outcome(outcome, detail_note=None, detail_extension=None):
    """Create PREMIS event outcome DOM structure.

    :outcome: Event outcome (success, failure)
    :detail_note: Description for the event outcome

    Returns the following ElementTree structure::

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
    _outcome.text = decode_utf8(outcome)

    detail = _subelement(outcome_information, 'eventOutcomeDetail')

    if detail_note is not None:
        _detail_note = _subelement(detail, 'eventOutcomeDetailNote')
        _detail_note.text = decode_utf8(detail_note)

    if detail_extension is not None:
        if type(detail_extension) is list:
            _detail_extension = _subelement(detail, 'eventOutcomeDetailExtension')
            for ext in detail_extension:
                _detail_extension.append(ext)
        elif lxml.etree.iselement(detail_extension):
            _detail_extension = _subelement(detail, 'eventOutcomeDetailExtension')
            _detail_extension.append(detail_extension)
        else:
            raise TypeError

    return outcome_information


def event(
        event_id, event_type, event_date_time, event_detail,
        child_elements=None, linking_objects=None, linking_agents=None):
    """Create PREMIS event element.

    :event_id: PREMIS event identifier
    :event_type: Type for the event
    :event_date_time: Event time
    :event_detail: Event details
    :child_elements: Any child elements appended to the event (default=None)
    :linking_objects: Any linking objects appended to the event (default=None)

    Returns the following ElementTree structure::

        <premis:event>

            <premis:eventType>digital signature validation</premis:eventType>
            <premis:eventDateTime>2015-02-03T13:04:25</premis:eventDateTime>
            <premis:eventDetail>
                Submission information package digital signature validation
            </premis:eventDetail>

            {{ child elements }}

        </premis:event>

    """

    _event = _element('event')

    _event.append(event_id)

    _event_type = _subelement(_event, 'eventType')
    _event_type.text = decode_utf8(event_type)

    _event_date_time = _subelement(_event, 'eventDateTime')
    _event_date_time.text = decode_utf8(event_date_time)

    _event_detail = _subelement(_event, 'eventDetail')
    _event_detail.text = decode_utf8(event_detail)

    if child_elements:
        for elem in child_elements:
            _event.append(elem)

    if linking_agents:
        for _agent in linking_agents:
            linking_agent = identifier(
                _agent.findtext('.//' + premis_ns('agentIdentifierType')),
                _agent.findtext('.//' + premis_ns('agentIdentifierValue')),
                'linkingAgent')
            _event.append(linking_agent)

    if linking_objects:
        for _object in linking_objects:
            linking_object = identifier(
                _object.findtext('.//' + premis_ns('objectIdentifierType')),
                _object.findtext('.//' + premis_ns('objectIdentifierValue')),
                'linkingObject')
            _event.append(linking_object)

    return _event


def iter_events(premis):
    """Iterate all PREMIS events from starting element.

    :starting_element: Element where matching elements are searched
    :returns: Generator object for iterating all elements

    """
    for elem in iter_elements(premis, 'event'):
        yield elem


def find_event_by_id(premis, event_id):
    """Find a PREMIS event by its eventIdentifierValue

    :premis: ElementTree element
    :event_id: The PREMIS event's ID

    :returns: Element if found, None otherwise
    """
    for elem in iter_events(premis):
        if elem.findtext(
                './/' + premis_ns('eventIdentifierValue')) == decode_utf8(event_id):
            return elem

    return None


def event_count(premis):
    """Return number of events in PREMIS data dictionary.

    :premis: ElementTree element
    :returns: Integer

    """
    return len([x for x in iter_events(premis)])


def event_with_type_and_detail(events, event_type, event_detail):
    """Return all events from list of `events` with given
    `event_identifier_type` matching the PREMIS eventIdentifierType field.

    :events: Iterable of events
    :event_identifier_type: Identifier type as string
    :returns: Iterator with all matching events

    """

    for _event in events:
        _event_type = encode_utf8(_event.findtext(premis_ns('eventType')))
        _event_detail = encode_utf8(_event.findtext(premis_ns('eventDetail')))

        if _event_type == event_type and _event_detail == event_detail:
            yield _event


def events_with_outcome(events, outcome):
    """Iterate over all events with given outcome

    :events: Iterable of events
    :outcome: Return all events that has the outcome
    :returns: Iterable of events

    """
    for _event in events:
        _event_outcome = encode_utf8(_event.findtext('/'.join([
            premis_ns('eventOutcomeInformation'),
            premis_ns('eventOutcome')])))
        if _event_outcome == outcome:
            yield _event


def parse_event_type(event_elem):
    try:
        return encode_utf8(event_elem.xpath(".//premis:eventType/text()",
                                            namespaces=NAMESPACES)[0])
    except IndexError:
        return ""


def parse_datetime(event_elem):
    return encode_utf8(event_elem.xpath(".//premis:eventDateTime/text()",
                            namespaces=NAMESPACES)[0])


def parse_detail(event_elem):
    try:
        return encode_utf8(event_elem.xpath(".//premis:eventDetail/text()",
                                namespaces=NAMESPACES)[0])
    except IndexError:
        return ""


def parse_outcome(event_elem):
    return encode_utf8(event_elem.xpath(
        ".//premis:eventOutcomeInformation/premis:eventOutcome/text()",
                       namespaces=NAMESPACES)[0])


def parse_outcome_detail_note(event_elem):
    try:
        return encode_utf8(event_elem.xpath(
            ".//premis:eventOutcomeInformation/premis:eventOutcomeDetail/premis:eventOutcomeDetailNote/text()",
                           namespaces=NAMESPACES)[0])
    except IndexError:
        return ""


def parse_outcome_detail_extension(event_elem):
    detail_extension = []
    return event_elem.find(
        ".//premis:eventOutcomeInformation/premis:eventOutcomeDetail/premis:eventOutcomeDetailExtension",
        namespaces=NAMESPACES)

