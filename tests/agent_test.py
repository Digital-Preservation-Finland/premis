"""Test for the Premis agent class"""

import lxml.etree as ET
import premis.base as p
import premis.agent_base as a

def test_agent():
    """Test agent"""
    agent_id = p.identifier('a', 'b', 'agent')
    agent = a.agent(agent_id, 'c', 'd')
    xml = '<premis:agent xmlns:premis="info:lc/xmlns/premis-v2">' \
          '<premis:agentIdentifier><premis:agentIdentifierType>' \
          'a</premis:agentIdentifierType><premis:agentIdentifierValue>' \
          'b</premis:agentIdentifierValue></premis:agentIdentifier>' \
          '<premis:agentName>c</premis:agentName>' \
          '<premis:agentType>d</premis:agentType></premis:agent>'
    assert ET.tostring(agent) == xml


def test_iter_agents():
    """Test iter_agents"""
    agent1 = a.agent(p.identifier('a', 'b', 'agent'), 'nimi1', 'tyyppi')
    agent2 = a.agent(p.identifier('a', 'b', 'agent'), 'nimi2', 'tyyppi')
    agent3 = a.agent(p.identifier('a', 'b', 'agent'), 'nimi3', 'tyyppi')
    premisroot = p.premis(child_elements=[agent1, agent2, agent3])
    i = 0
    for _agent in a.iter_agents(premisroot):
        i = i + 1
        assert a.parse_name(_agent) == 'nimi'+str(i)
    assert i == 3


def test_find_agent_by_id():
    """Test find_agent_by_id"""
    agent1 = a.agent(p.identifier('local', 'id1', 'agent'), 'name', 'type1')
    agent2 = a.agent(p.identifier('local', 'id2', 'agent'), 'name', 'type2')
    agent3 = a.agent(p.identifier('local', 'id3', 'agent'), 'name', 'type3')
    xml = p.premis(child_elements=[agent1, agent2, agent3])
    ag = a.find_agent_by_id(xml, 'id2')
    assert p.parse_identifier_type_value(p.parse_identifier(ag, 'agent'),
                                         'agent') == ('local', 'id2')


def test_agent_count():
    """Test agent_count"""
    agent1 = a.agent(p.identifier('a', 'b', 'agent'), 'nimi', 'tyyppi1')
    agent2 = a.agent(p.identifier('a', 'b', 'agent'), 'nimi', 'tyyppi2')
    agent3 = a.agent(p.identifier('a', 'b', 'agent'), 'nimi', 'tyyppi1')
    premisroot = p.premis(child_elements=[agent1, agent2, agent3])
    assert a.agent_count(premisroot) == 3


def test_agents_with_type():
    """Test agents_with_type"""
    agent1 = a.agent(p.identifier('a', 'b', 'agent'), 'nimi1', 'tyyppi1')
    agent2 = a.agent(p.identifier('a', 'b', 'agent'), 'nimi2', 'tyyppi2')
    agent3 = a.agent(p.identifier('a', 'b', 'agent'), 'nimi3', 'tyyppi1')
    agentlist = []
    i = 1
    for _agent in a.agents_with_type([agent1, agent2, agent3], 'tyyppi1'):
        assert _agent == ('tyyppi1', 'nimi'+str(i))
        agentlist.append(_agent)
        i = i + 2
    assert len(agentlist) == 2


def test_parse_name():
    """Test parse_name"""
    agent = a.agent(p.identifier('a', 'b', 'agent'), 'nimi', 'tyyppi', note='nootti')
    assert a.parse_name(agent) == 'nimi'


def test_parse_agent_type():
    """Test parse_agent_type"""
    agent = a.agent(p.identifier('a', 'b', 'agent'), 'nimi', 'tyyppi', note='nootti')
    assert a.parse_agent_type(agent) == 'tyyppi'


def test_parse_note():
    """Test parse_note"""
    agent = a.agent(p.identifier('a', 'b', 'agent'), 'nimi', 'tyyppi', note='nootti')
    assert a.parse_note(agent) == 'nootti'

