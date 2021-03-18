"""Functions for reading and generating PREMIS Data Dictionaries as
xml.etree.ElementTree data structures.

References:

    * PREMIS http://www.loc.gov/standards/premis/
    * ElementTree
    https://docs.python.org/2.6/library/xml.etree.elementtree.html

"""
from __future__ import unicode_literals

from xml_helpers.utils import decode_utf8

from premis.base import (element, subelement, premis_ns, identifier,
                         iter_elements, NAMESPACES)


def outcome(event_outcome, detail_note=None, detail_extension=None,
            single_extension_element=False):
    """Create PREMIS event outcome DOM structure.

    :event_outcome: Event outcome (success, failure)
    :detail_note: String description for the event outcome
    :detail_extension: List of detail extension etree elements
    :single_extension_element:
        True: all element trees in detail_extension are placed in a single
              eventOutcomeDetailExtension element.
        False: each element tree in detail_extension is placed in a separate
               eventOutcomeDetailExtension element.

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

    outcome_information = element('eventOutcomeInformation')

    _outcome = subelement(outcome_information, 'eventOutcome')
    _outcome.text = decode_utf8(event_outcome)

    detail = subelement(outcome_information, 'eventOutcomeDetail')

    if detail_note is not None:
        _detail_note = subelement(detail, 'eventOutcomeDetailNote')
        _detail_note.text = decode_utf8(detail_note)

    if detail_extension:
        if single_extension_element:
            # Add all extensions into one eventOutcomeDetailExtension element
            _detail_extension = subelement(detail,
                                           'eventOutcomeDetailExtension')
            for extension in detail_extension:
                _detail_extension.append(extension)
        else:
            # Separate eventOutcomeDetailExtension element for each extension
            for extension in detail_extension:
                _detail_extension = subelement(detail,
                                               'eventOutcomeDetailExtension')
                _detail_extension.append(extension)

    return outcome_information


# pylint: disable=too-many-arguments, too-many-locals
# too-many-arguments: The given arguments are used to form the Element obj.
def event(event_id, event_type, event_date_time, event_detail,
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
    _event = element('event')

    _event.append(event_id)

    _event_type = subelement(_event, 'eventType')
    _event_type.text = decode_utf8(event_type)

    _event_date_time = subelement(_event, 'eventDateTime')
    _event_date_time.text = decode_utf8(event_date_time)

    _event_detail = subelement(_event, 'eventDetail')
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
    event_id = decode_utf8(event_id)

    for elem in iter_events(premis):
        identifier_ = elem.findtext('.//' + premis_ns('eventIdentifierValue'))
        if identifier_ == event_id:
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
        _event_type = _event.findtext(premis_ns('eventType'))
        _event_detail = _event.findtext(premis_ns('eventDetail'))

        if _event_type == event_type and _event_detail == event_detail:
            yield _event


def events_with_outcome(events, event_outcome):
    """Iterate over all events with given outcome

    :param events: Iterable of events
    :param event_outcome: Return all events that have this outcome
    :returns: Iterable of events

    """
    outcome_ = decode_utf8(event_outcome)

    for _event in events:
        _event_outcome = _event.findtext('/'.join([
            premis_ns('eventOutcomeInformation'),
            premis_ns('eventOutcome')]))
        if _event_outcome == outcome_:
            yield _event


def parse_event_type(event_elem):
    """
    :param event_elem: Premis event element.
    :return: String
    """
    try:
        return event_elem.xpath(
            ".//premis:eventType/text()",
            namespaces=NAMESPACES)[0]
    except IndexError:
        return ""


def parse_datetime(event_elem):
    """
    :param event_elem: Premis event element.
    :return: String
    """
    return event_elem.xpath(
        ".//premis:eventDateTime/text()",
        namespaces=NAMESPACES)[0]


def parse_detail(event_elem):
    """
    :param event_elem: Premis event element.
    :return: String
    """
    try:
        return event_elem.xpath(
            ".//premis:eventDetail/text()",
            namespaces=NAMESPACES)[0]
    except IndexError:
        return ""


def parse_outcome(event_elem):
    """
    :param event_elem: Premis event element.
    :return: String
    """
    return event_elem.xpath(
        ".//premis:eventOutcomeInformation/premis:eventOutcome/text()",
        namespaces=NAMESPACES)[0]


def parse_outcome_detail_note(event_elem):
    """
    :param event_elem: Premis event element.
    :return: String
    """
    try:
        return event_elem.xpath(
            (".//premis:eventOutcomeInformation/premis:eventOutcomeDetail/"
             "premis:eventOutcomeDetailNote/text()"),
            namespaces=NAMESPACES)[0]
    except IndexError:
        return ""


def parse_outcome_detail_extension(event_elem):
    """
    :param event_elem: Premis event element.
    :return: String
    """
    return event_elem.find(
        (".//premis:eventOutcomeInformation/premis:eventOutcomeDetail/"
         "premis:eventOutcomeDetailExtension"),
        namespaces=NAMESPACES)
