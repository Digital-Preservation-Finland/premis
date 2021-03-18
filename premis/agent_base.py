"""Functions for reading and generating PREMIS Data Dictionaries as
xml.etree.ElementTree data structures.

References:

    * PREMIS http://www.loc.gov/standards/premis/
    * ElementTree
    https://docs.python.org/2.6/library/xml.etree.elementtree.html

"""
from __future__ import unicode_literals

from xml_helpers.utils import decode_utf8
from premis.base import (element, _subelement, iter_elements, premis_ns,
                         NAMESPACES)


def agent(agent_id, agent_name, agent_type, note=None):
    """Returns PREMIS agent element

    :agent_id: PREMIS identifier for the agent
    :agent_name: Agent name
    :agent_type: Agent type

    Returns the following ElementTree structure::

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

    _agent = element('agent')

    _agent.append(agent_id)

    _agent_name = _subelement(_agent, 'agentName')
    _agent_name.text = decode_utf8(agent_name)

    _agent_type = _subelement(_agent, 'agentType')
    _agent_type.text = decode_utf8(agent_type)

    if note is not None:
        _agent_type = _subelement(_agent, 'agentNote')
        _agent_type.text = decode_utf8(note)

    return _agent


def iter_agents(premis):
    """Iterate all PREMIS agents from starting element.

    :starting_element: Element where matching elements are searched
    :returns: Generator object for iterating all elements

    """
    for elem in iter_elements(premis, 'agent'):
        yield elem


def find_agent_by_id(premis, agent_id):
    """Find a PREMIS agent by its agentIdentifierValue

    :premis: ElementTree element
    :agent_id: The PREMIS agent's ID

    :returns: Element if found, None otherwise
    """
    for elem in iter_agents(premis):
        if elem.findtext('.//' + premis_ns(
                'agentIdentifierValue')) == decode_utf8(agent_id):
            return elem

    return None


def agent_count(premis):
    """Return number of agents in PREMIS data dictionary.

    :premis: ElementTree element
    :returns: Integer

    """
    return len([x for x in iter_agents(premis)])


def agents_with_type(agents, agent_type='organization'):
    """Return all agents from list of `agents` with given `agent_type`.

    :task_report: Report to search from
    :returns: Generator object which iterates all (agent_type, agent_name)

    """
    agent_type = decode_utf8(agent_type)

    for _agent in agents:
        agent_name = _agent.findtext(premis_ns('agentName'))
        _agent_type = _agent.findtext(premis_ns('agentType'))

        if _agent_type == agent_type:
            yield (agent_type, agent_name)


# TODO: When doing actual refactoring, resolve redefined-outer-name warning.
def parse_name(agent):
    """
    :param agent: Agent Element object.
    :return: Unicode string
    """
    return decode_utf8(agent.xpath(".//premis:agentName/text()",
                                   namespaces=NAMESPACES)[0])


# TODO: When doing actual refactoring, resolve redefined-outer-name warning.
def parse_agent_type(agent):
    """
    :param agent: Agent Element object.
    :return: Unicode string
    """
    return decode_utf8(agent.xpath(".//premis:agentType/text()",
                                   namespaces=NAMESPACES)[0])


# TODO: When doing actual refactoring, resolve redefined-outer-name warning.
def parse_note(agent):
    """
    :param agent: Agent Element object.
    :return: Unicode string
    """
    return decode_utf8(agent.xpath(".//premis:agentNote/text()",
                                   namespaces=NAMESPACES)[0])
