"""Functions for reading and generating PREMIS Data Dictionaries as
xml.etree.ElementTree data structures.

References:

    * PREMIS http://www.loc.gov/standards/premis/
    * ElementTree
    https://docs.python.org/2.6/library/xml.etree.elementtree.html

"""

import lxml.etree as ET
from xml_helpers.utils import XSI_NS, xsi_ns, decode_utf8

PREMIS_NS = 'info:lc/xmlns/premis-v2'
NAMESPACES = {'premis': PREMIS_NS,
              'xsi': XSI_NS}

# using lxml.etree causes these, but importing c extensions is not a problem
# for us
# pylint: disable=c-extension-no-member


def premis_ns(tag, prefix=""):
    """Prefix ElementTree tags with PREMIS namespace.
    object -> {info:lc...premis}object

    :tag: Tag name as string
    :returns: Prefixed tag

    """
    tag = decode_utf8(tag)

    if prefix:
        prefix = decode_utf8(prefix)
        tag = tag[0].upper() + tag[1:]
        return f'{{{PREMIS_NS}}}{prefix}{tag}'
    return f'{{{PREMIS_NS}}}{tag}'


def _element(tag, prefix="", ns=None):
    """Return _ElementInterface with PREMIS namespace.

    Prefix parameter is useful for adding prefixed to lower case tags. It just
    uppercases first letter of tag and appends it to prefix::

        element = _element('objectIdentifier', 'linking')
        element.tag
        'linkingObjectIdentifier'

    :param tag: Tagname
    :param prefix: Prefix for the tag (default="")
    :param ns: Optional namespace for the element
    :returns: ElementTree element object

    """
    if ns is None:
        ns = {}
    ns['premis'] = PREMIS_NS
    return ET.Element(premis_ns(tag, prefix), nsmap=ns)


def _subelement(parent, tag, prefix="", ns=None):
    """Return subelement for the given parent element.

    Created element is appended to parent element.

    :param parent: Parent element
    :param tag: Element tagname
    :param prefix: Prefix for the tag
    :param ns: Optional namespace for the element
    :returns: Created subelement

    """
    if ns is None:
        ns = {}
    ns['premis'] = PREMIS_NS
    return ET.SubElement(parent, premis_ns(tag, prefix), nsmap=ns)


def identifier(identifier_type, identifier_value, prefix='object', role=None):
    """Return PREMIS identifier segments.

    Produces without prefix the following PREMIS segment::


          <premis:objectIdentifier>
              <premis:objectIdentifierType>
                  preservation-sig-id
              </premis:objectIdentifierType>
              <premis:objectIdentifierValue>
                  c8b978b6-e160-4497-8027-e19fa0297766
              </premis:objectIdentifierValue>
          </premis:objectIdentifier>

    With prefix='relatedObject' the following PREMIS segment::

          <premis:relatedObjectIdentification>
              <premis:relatedObjectIdentifierType>
                  preservation-sip-id
              </premis:relatedObjectIdentifierType>
              <premis:relatedObjectIdentifierValue>
                  1ac641ec-223f-42f4-86c2-9402451d63bf
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
                preservation-sip-id</premis:linkingObjectIdentifierType>
            <premis:linkingObjectIdentifierValue>
                1ac641ec</premis:linkingObjectIdentifierValue>
        </premis:linkingObjectIdentifier>

    With prefix='linking' and role the following PREMIS segment::

        <premis:linkingAgentIdentifier>
            <premis:linkingAgentIdentifierType>
                preservation-agent-id</premis:linkingAgentIdentifierType>
            <premis:linkingAgentIdentifierValue>
                1ac641ec</premis:linkingAgentIdentifierValue>
            <premis:linkingAgentRole>
                validator</premis:linkingAgentRole>
        </premis:linkingAgentIdentifier>

    """
    prefix = decode_utf8(prefix)

    if prefix == 'relatedObject':
        _identifier = _element('Identification', prefix)
    else:
        _identifier = _element('Identifier', prefix)

    _type = _subelement(_identifier, 'IdentifierType', prefix)
    if identifier_type is not None:
        identifier_type = decode_utf8(identifier_type)
    _type.text = identifier_type

    _value = _subelement(_identifier, 'IdentifierValue', prefix)
    if identifier_value is not None:
        identifier_value = decode_utf8(identifier_value)
    _value.text = identifier_value

    if 'linking' in prefix and role is not None:
        _role = _subelement(_identifier, 'Role', prefix)
        _role.text = role

    return _identifier


def parse_identifier_type_value(id_elem, prefix='object'):
    """Return identifierType and IdentifierValue from given PREMIS id.
    If segment contains multiple identifiers, returns first
    occurrence.

    :id_elem: Premis identifier
    :returns: (identifier_type, identifier_value)

    """
    prefix = decode_utf8(prefix)

    if prefix == 'relatedObject':
        if id_elem.tag != premis_ns('relatedObjectIdentification'):
            id_elem = id_elem.find(premis_ns('relatedObjectIdentification'))
        if id_elem is not None:
            return (
                id_elem.find(
                    './' + premis_ns('relatedObjectIdentifierType')).text,
                id_elem.find(
                    './' + premis_ns('relatedObjectIdentifierValue')).text)
        return None
    if id_elem.tag != premis_ns('Identifier', prefix):
        id_elem = id_elem.find(premis_ns('Identifier', prefix))
    if id_elem is not None:
        return (
            id_elem.find('./' + premis_ns('IdentifierType', prefix)).text,
            id_elem.find('./' + premis_ns('IdentifierValue', prefix)).text)
    return None


def premis(child_elements=None, namespaces=None):
    """Create PREMIS Data Dictionary root element.

    :child_elements: Any elements appended to the PREMIS dictionary

    Returns the following ElementTree structure::


        <premis:premis
            xmlns:premis="info:lc/xmlns/premis-v2"
            xmlns:xsi="http://www.w3.org/2001/xmlschema-instance"
            xsi:schemalocation="info:lc/xmlns/premis-v2
                                http://www.loc.gov/standards/premis/v2/premis-v2-3.xsd"
            version="2.2">

    """
    if namespaces is None:
        namespaces = NAMESPACES
    _premis = _element('premis', ns=namespaces)
    _premis.set(
        xsi_ns('schemaLocation'),
        'info:lc/xmlns/premis-v2 '
        'http://www.loc.gov/standards/premis/v2/premis-v2-3.xsd')
    _premis.set('version', '2.2')

    if child_elements:
        for elem in child_elements:
            _premis.append(elem)

    return _premis


def iter_elements(starting_element, tag):
    """Iterate all element from starting element that match the `tag`
    parameter. Tag is always prefixed to PREMIS namespace before matching.

    :starting_element: Element where matching elements are searched
    :returns: Generator object for iterating all elements

    """
    yield from starting_element.findall('.//' + premis_ns(tag))


def parse_identifier(section, prefix='object'):
    """
    :param section:
    :param prefix:
    :return: Element object.
    """
    prefix = decode_utf8(prefix)

    if prefix == 'relatedObject':
        return section.find('.//' + premis_ns('Identification', prefix))
    return section.find('.//' + premis_ns('Identifier', prefix))
