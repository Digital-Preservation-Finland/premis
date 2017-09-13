"""Test for the Premis agent class"""

import xml.etree.ElementTree as ET
import premis_tools.premis as p
import premis_tools.agent as a

def test_agent():
    """Test premis_agent"""
    ET.register_namespace('premis', 'info:lc/xmlns/premis-v2')
    agent_id = p.premis_identifier('a', 'b', 'agent')
    agent = a.premis_agent(agent_id, 'c', 'd')
    xml = '<premis:agent xmlns:premis="info:lc/xmlns/premis-v2">' \
          '<premis:agentIdentifier><premis:agentIdentifierType>' \
          'a</premis:agentIdentifierType><premis:agentIdentifierValue>' \
          'b</premis:agentIdentifierValue></premis:agentIdentifier>' \
          '<premis:agentName>c</premis:agentName>' \
          '<premis:agentType>d</premis:agentType></premis:agent>'
    assert ET.tostring(agent) == xml


def test_iter_agents():
    """Test iter_agents"""
    # TODO


def test_agent_count():
    """Test agent_count"""
    # TODO


def test_agents_with_type():
    """Test agents_with_type"""
    # TODO

