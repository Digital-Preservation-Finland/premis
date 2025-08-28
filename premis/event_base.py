"""Functions for reading and generating PREMIS Data Dictionaries as
xml.etree.ElementTree data structures.

References:

    * PREMIS http://www.loc.gov/standards/premis/
    * ElementTree
    https://docs.python.org/2.6/library/xml.etree.elementtree.html

"""

from __future__ import annotations

from collections.abc import Generator, Iterable, Iterator

import lxml.etree as ET
from xml_helpers.utils import decode_utf8

from premis.base import (
    NAMESPACES,
    _element,
    _subelement,
    identifier,
    iter_elements,
    premis_ns,
)


# Listed as requiring a fix in KDKPAS-2522
def outcome(
    outcome: str,
    detail_note: str | None = None,
    detail_extension: list[ET._Element] | None = None,
    single_extension_element: bool = False,
) -> ET._Element:
    """Create PREMIS event outcome DOM structure.

    :param outcome: Event outcome (success, failure)
    :param detail_note: String description for the event outcome
    :param detail_extension: List of detail extension etree elements
    :param single_extension_element:
        True: all element trees in detail_extension are placed in a single
              eventOutcomeDetailExtension element.
        False: each element tree in detail_extension is placed in a separate
               eventOutcomeDetailExtension element.

    :returns:
    The following ElementTree structure::

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

    outcome_ = _subelement(outcome_information, 'eventOutcome')
    outcome_.text = decode_utf8(outcome)

    if detail_note or detail_extension:
        detail = _subelement(outcome_information, 'eventOutcomeDetail')

        if detail_note is not None:
            detail_note_ = _subelement(detail, 'eventOutcomeDetailNote')
            detail_note_.text = decode_utf8(detail_note)

        if detail_extension:
            if single_extension_element:
                # Add all extensions into one eventOutcomeDetailExtension
                # element
                detail_extension_ = _subelement(
                    detail, 'eventOutcomeDetailExtension'
                )
                for extension in detail_extension:
                    detail_extension_.append(extension)
            else:
                # Separate eventOutcomeDetailExtension element for each
                # extension
                for extension in detail_extension:
                    detail_extension_ = _subelement(
                        detail, 'eventOutcomeDetailExtension'
                    )
                    detail_extension_.append(extension)

    return outcome_information


def event(
    event_id: ET._Element,
    event_type: str,
    event_date_time: str,
    event_detail: str,
    child_elements: list[ET._Element] | None = None,
    linking_objects: list[ET._Element] | None = None,
    linking_agents: list[ET._Element] | None = None,
) -> ET._Element:
    """Create PREMIS event element.

    :param event_id: PREMIS event identifier
    :param event_type: Type for the event
    :param event_date_time: Event time
    :param event_detail: Event details
    :param child_elements: Any child elements appended to the event
        (default=None)
    :param linking_objects: Any linking objects appended to the event
        (default=None)
    :param linking_agents: Any linking agents appended to the event
        (default=None)
    :returns: PREMIS event element

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
    event_ = _element('event')

    event_.append(event_id)

    event_type_ = _subelement(event_, 'eventType')
    event_type_.text = decode_utf8(event_type)

    event_date_time_ = _subelement(event_, 'eventDateTime')
    event_date_time_.text = decode_utf8(event_date_time)

    event_detail_ = _subelement(event_, 'eventDetail')
    event_detail_.text = decode_utf8(event_detail)

    if child_elements:
        for elem in child_elements:
            event_.append(elem)

    if linking_agents:
        for agent_ in linking_agents:
            linking_agent = identifier(
                agent_.findtext('.//' + premis_ns('agentIdentifierType')),
                agent_.findtext('.//' + premis_ns('agentIdentifierValue')),
                'linkingAgent')
            event_.append(linking_agent)

    if linking_objects:
        for _object in linking_objects:
            linking_object = identifier(
                _object.findtext('.//' + premis_ns('objectIdentifierType')),
                _object.findtext('.//' + premis_ns('objectIdentifierValue')),
                'linkingObject')
            event_.append(linking_object)

    return event_


def iter_events(premis: ET._Element) -> Generator[ET._Element]:
    """Iterate all PREMIS events from starting element.

    :param starting_element: Element where matching elements are searched
    :returns: Generator object for iterating all elements

    """
    yield from iter_elements(premis, 'event')


def find_event_by_id(premis: ET._Element, event_id: str) -> ET._Element | None:
    """Find a PREMIS event by its eventIdentifierValue

    :param premis: ElementTree element
    :param event_id: The PREMIS event's ID
    :returns: Element if found, None otherwise

    """
    event_id = decode_utf8(event_id)

    for elem in iter_events(premis):
        identifier = elem.findtext('.//' + premis_ns('eventIdentifierValue'))
        if identifier == event_id:
            return elem

    return None


def event_count(premis: ET._Element) -> int:
    """Return number of events in PREMIS data dictionary.

    :param premis: ElementTree element
    :returns: Integer

    """
    return len(list(iter_events(premis)))


def event_with_type_and_detail(
    events: Iterable[ET._Element], event_type: str, event_detail: str
) -> Iterator[ET._Element]:
    """Return all events from list of `events` with given
    `event_identifier_type` matching the PREMIS eventIdentifierType field.

    :param events: Iterable of events
    :param event_identifier_type: Identifier type as string
    :param event_detail: Event detail as string
    :returns: Iterator with all matching events

    """

    for event_ in events:
        event_type_ = event_.findtext(premis_ns('eventType'))
        event_detail_ = event_.findtext(premis_ns('eventDetail'))

        if event_type_ == event_type and event_detail_ == event_detail:
            yield event_


def events_with_outcome(
    events: Iterable[ET._Element], outcome: str
) -> Iterator[ET._Element]:
    """Iterate over all events with given outcome

    :param events: Iterable of events
    :param outcome: Return all events that has the outcome
    :returns: Iterator of events

    """
    outcome = decode_utf8(outcome)

    for event_ in events:
        event_outcome_ = event_.findtext('/'.join([
            premis_ns('eventOutcomeInformation'),
            premis_ns('eventOutcome')]))
        if event_outcome_ == outcome:
            yield event_


def parse_event_type(event_elem: ET._Element) -> str:
    """
    :param event_elem: Premis event element.
    :return: String
    """
    try:
        return event_elem.xpath(
            ".//premis:eventType/text()", namespaces=NAMESPACES
        )[0]
    except IndexError:
        return ""


def parse_datetime(event_elem: ET._Element) -> str:
    """
    :param event_elem: Premis event element.
    :return: String
    """
    return event_elem.xpath(
        ".//premis:eventDateTime/text()", namespaces=NAMESPACES
    )[0]


def parse_detail(event_elem: ET._Element) -> str:
    """
    :param event_elem: Premis event element.
    :return: String
    """
    try:
        return event_elem.xpath(
            ".//premis:eventDetail/text()", namespaces=NAMESPACES
        )[0]
    except IndexError:
        return ""


def parse_outcome(event_elem: ET._Element) -> str:
    """
    :param event_elem: Premis event element.
    :return: String
    """
    return event_elem.xpath(
        ".//premis:eventOutcomeInformation/premis:eventOutcome/text()",
        namespaces=NAMESPACES,
    )[0]


def parse_outcome_detail_note(event_elem: ET._Element) -> str:
    """
    :param event_elem: Premis event element.
    :return: String
    """
    try:
        return event_elem.xpath(
            ".//premis:eventOutcomeInformation/premis:eventOutcomeDetail/"
            "premis:eventOutcomeDetailNote/text()",
            namespaces=NAMESPACES,
        )[0]
    except IndexError:
        return ""


def parse_outcome_detail_extension(
    event_elem: ET._Element,
) -> ET._Element | None:
    """
    :param event_elem: Premis event element.
    :return: Event element, or None if not found
    """
    return event_elem.find(
        ".//premis:eventOutcomeInformation/premis:eventOutcomeDetail/"
        "premis:eventOutcomeDetailExtension",
        namespaces=NAMESPACES,
    )
