"""Functions for reading and generating PREMIS Data Dictionaries as
xml.etree.ElementTree data structures.

References:

    * PREMIS http://www.loc.gov/standards/premis/
    * ElementTree
    https://docs.python.org/3.9/library/xml.etree.elementtree.html

"""
from __future__ import annotations

from collections.abc import Generator, Iterable

import lxml.etree as ET
from xml_helpers.utils import decode_utf8

from premis.base import (
    NAMESPACES,
    _element,
    _subelement,
    iter_elements,
    premis_ns,
)


def agent(
    agent_id: ET._Element,
    agent_name: str,
    agent_type: str,
    note: str | None = None,
) -> ET._Element:
    """Returns PREMIS agent element

    :param agent_id: PREMIS identifier for the agent
    :param agent_name: Agent name
    :param agent_type: Agent type
    :param note: Agent note

    :returns:
    The following ElementTree structure::

        <premis:agent>
            <premis:agentIdentifier>
                <premis:agentIdentifierType>
                    preservation-agent-id</premis:agentIdentifierType>
                <premis:agentIdentifierValue>
                    preservation-agent-check_virus_clamscan.py-0.63-1422
                </premis:agentIdentifierValue>
            </premis:agentIdentifier>
            <premis:agentName>check_virus_clamscan.py</premis:agentName>
            <premis:agentType>software</premis:agentType>
        </premis:agent>

    """
    agent_ = _element('agent')

    agent_.append(agent_id)

    agent_name_ = _subelement(agent_, 'agentName')
    agent_name_.text = decode_utf8(agent_name)

    agent_type_ = _subelement(agent_, 'agentType')
    agent_type_.text = decode_utf8(agent_type)

    if note is not None:
        agent_type_ = _subelement(agent_, 'agentNote')
        agent_type_.text = decode_utf8(note)

    return agent_


def iter_agents(premis: ET._Element) -> Generator[ET._Element]:
    """Iterate all PREMIS agents from starting element.

    :param starting_element: Element where matching elements are searched
    :returns: Generator object for iterating all elements

    """
    yield from iter_elements(premis, 'agent')


def find_agent_by_id(premis: ET._Element, agent_id: str) -> ET._Element | None:
    """Find a PREMIS agent by its agentIdentifierValue

    :param premis: ElementTree element
    :param agent_id: The PREMIS agent's ID

    :returns: Element if found, None otherwise
    """
    for elem in iter_agents(premis):
        if elem.findtext('.//' + premis_ns(
                'agentIdentifierValue')) == decode_utf8(agent_id):
            return elem

    return None


def agent_count(premis: ET._Element) -> int:
    """Return number of agents in PREMIS data dictionary.

    :param premis: ElementTree element
    :returns: Integer

    """
    return len(list(iter_agents(premis)))


def agents_with_type(
    agents: Iterable[ET._Element], agent_type: str = "organization"
) -> Generator[tuple[str, str | None]]:
    """Return all agents from list of `agents` with given `agent_type`.

    :param agent: Iterable of Agent Element objects
    :param task_report: Report to search from
    :returns: Generator object which iterates all (agent_type, agent_name)

    """
    agent_type = decode_utf8(agent_type)

    for _agent in agents:
        agent_name = _agent.findtext(premis_ns('agentName'))
        agent_type_ = _agent.findtext(premis_ns('agentType'))

        if agent_type_ == agent_type:
            yield (agent_type, agent_name)


def parse_name(agent: ET._Element) -> str:
    """
    :param agent: Agent Element object.
    :returns: Unicode string
    """
    return decode_utf8(
        agent.xpath(".//premis:agentName/text()", namespaces=NAMESPACES)[0]
    )


def parse_agent_type(agent: ET._Element) -> str:
    """
    :param agent: Agent Element object.
    :returns: Unicode string
    """
    return decode_utf8(
        agent.xpath(".//premis:agentType/text()", namespaces=NAMESPACES)[0]
    )


def parse_note(agent: ET._Element) -> str:
    """
    :param agent: Agent Element object.
    :returns: Unicode string
    """
    return decode_utf8(
        agent.xpath(".//premis:agentNote/text()", namespaces=NAMESPACES)[0]
    )
