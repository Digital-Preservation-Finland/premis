"""Functions for reading and generating PREMIS Data Dictionaries as
xml.etree.ElementTree data structures.

References:

    * PREMIS http://www.loc.gov/standards/premis/
    * ElementTree
    https://docs.python.org/2.6/library/xml.etree.elementtree.html

"""


from premis.premis import _element, _subelement, premis_ns, \
    premis_identifier, iter_elements

def premis_event_outcome(outcome, detail_note=None, detail_extension=None):
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
    _outcome.text = outcome

    detail = _subelement(outcome_information, 'eventOutcomeDetail')

    if detail_note:
        _detail_note = _subelement(detail, 'eventOutcomeDetailNote')
        _detail_note.text = detail_note

    if detail_extension:
        _detail_extension = _subelement(detail, 'eventOutcomeDetailExtension')
        _detail_extension.text = detail_extension

    return outcome_information


def premis_event(
        identifier, event_type, event_date_time, event_detail,
        child_elements=None, linking_objects=None):
    """Create PREMIS event element.

    :identifier: PREMIS event identifier
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

    event = _element('event')

    event.append(identifier)

    _event_type = _subelement(event, 'eventType')
    _event_type.text = event_type

    _event_date_time = _subelement(event, 'eventDateTime')
    _event_date_time.text = event_date_time

    _event_detail = _subelement(event, 'eventDetail')
    _event_detail.text = event_detail

    if child_elements:
        for elem in child_elements:
            event.append(elem)

    if linking_objects:
        for _object in linking_objects:
            linking_object = premis_identifier(
                _object.findtext('.//' + premis_ns('objectIdentifierType')),
                _object.findtext('.//' + premis_ns('objectIdentifierValue')),
                'linkingObject')
            event.append(linking_object)

    return event


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
                './/' + premis_ns('eventIdentifierValue')) == event_id:
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

    :events: Iterable of events
    :outcome: Return all events that has the outcome
    :returns: Iterable of events

    """
    for _event in events:
        _event_outcome = _event.findtext('/'.join([
            premis_ns('eventOutcomeInformation'),
            premis_ns('eventOutcome')]))
        if _event_outcome == event_outcome:
            yield _event
