"""Functions for reading and generating PREMIS Data Dictionaries as
xml.etree.ElementTree data structures.

References:

    * PREMIS http://www.loc.gov/standards/premis/
    * ElementTree
    https://docs.python.org/2.6/library/xml.etree.elementtree.html

"""


import json
import xml.etree.ElementTree as ET
from premis.premis import element, subelement, iter_elements, premis_ns

def premis_agent(
        identifier, agent_name, agent_type):
    """Returns PREMIS agent element

    :identifier: PREMIS identifier for the agent
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

    agent = element('agent')

    agent.append(identifier)

    _agent_name = subelement(agent, 'agentName')
    _agent_name.text = agent_name

    _agent_type = subelement(agent, 'agentType')
    _agent_type.text = agent_type

    return agent


def iter_agents(premis):
    """Iterate all PREMIS agents from starting element.

    :starting_element: Element where matching elements are searched
    :returns: Generator object for iterating all elements

    """
    for element in iter_elements(premis, 'agent'):
        yield element


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

    for agent in agents:
        agent_name = agent.findtext(premis_ns('agentName'))
        _agent_type = agent.findtext(premis_ns('agentType'))

        if _agent_type == agent_type:
            yield (agent_type, agent_name)

