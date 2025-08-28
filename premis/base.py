"""Functions for reading and generating PREMIS Data Dictionaries as
xml.etree.ElementTree data structures.

References:

    * PREMIS http://www.loc.gov/standards/premis/
    * ElementTree
    https://docs.python.org/2.6/library/xml.etree.elementtree.html

"""
from __future__ import annotations

from collections.abc import Generator, Iterable

import lxml.etree as ET
from xml_helpers.utils import XSI_NS, decode_utf8, xsi_ns

PREMIS_NS = "info:lc/xmlns/premis-v2"
NAMESPACES = {"premis": PREMIS_NS, "xsi": XSI_NS}


def premis_ns(tag: str, prefix: str = "") -> str:
    """Prefix ElementTree tags with PREMIS namespace.
    object -> {info:lc...premis}object

    :param tag: Tag name as string
    :returns: Prefixed tag

    """
    tag = decode_utf8(tag)

    if prefix:
        prefix = decode_utf8(prefix)
        tag = tag[0].upper() + tag[1:]
        return f'{{{PREMIS_NS}}}{prefix}{tag}'
    return f'{{{PREMIS_NS}}}{tag}'


def _element(
    tag: str, prefix: str = "", ns: dict[str, str] | None = None
) -> ET._Element:
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
    ns["premis"] = PREMIS_NS
    return ET.Element(premis_ns(tag, prefix), nsmap=ns)


def _subelement(
    parent: ET._Element,
    tag: str,
    prefix: str = "",
    ns: dict[str, str] | None = None,
) -> ET._Element:
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
    ns["premis"] = PREMIS_NS
    return ET.SubElement(parent, premis_ns(tag, prefix), nsmap=ns)


def identifier(
    identifier_type: str | None,
    identifier_value: str | None,
    prefix: str = "object",
    role: str | None = None,
) -> ET._Element:
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
        identifier_ = _element('Identification', prefix)
    else:
        identifier_ = _element('Identifier', prefix)

    type_ = _subelement(identifier_, 'IdentifierType', prefix)
    if identifier_type is not None:
        identifier_type = decode_utf8(identifier_type)
    type_.text = identifier_type

    value_ = _subelement(identifier_, 'IdentifierValue', prefix)
    if identifier_value is not None:
        identifier_value = decode_utf8(identifier_value)
    value_.text = identifier_value

    if 'linking' in prefix and role is not None:
        role_ = _subelement(identifier_, 'Role', prefix)
        role_.text = role

    return identifier_


def parse_identifier_type_value(
    id_elem: ET._Element, prefix: str = "object"
) -> tuple[str | None, str | None] | None:
    """Return identifierType and IdentifierValue from given PREMIS id.
    If segment contains multiple identifiers, returns first
    occurrence.

    :param id_elem: Premis identifier
    :param prefix: Prefix for the identifier
    :returns: (identifier_type, identifier_value) or None if not found

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


def premis(
    child_elements: Iterable[ET._Element] | None = None,
    namespaces: dict[str, str] | None = None,
) -> ET._Element:
    """Create PREMIS Data Dictionary root element.

    :param child_elements: Any elements appended to the PREMIS dictionary
    :param namespaces: Optional namespaces for the elements

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
    premis_ = _element('premis', ns=namespaces)
    premis_.set(
        xsi_ns('schemaLocation'),
        'info:lc/xmlns/premis-v2 '
        'http://www.loc.gov/standards/premis/v2/premis-v2-3.xsd')
    premis_.set('version', '2.2')

    if child_elements:
        for elem in child_elements:
            premis_.append(elem)

    return premis_


def iter_elements(
    starting_element: ET._Element, tag: str
) -> Generator[ET._Element]:
    """Iterate all element from starting element that match the `tag`
    parameter. Tag is always prefixed to PREMIS namespace before matching.

    :param starting_element: Element where matching elements are searched
    :returns: Generator object for iterating all elements

    """
    yield from starting_element.findall('.//' + premis_ns(tag))


def parse_identifier(
    section: ET._Element, prefix: str = "object"
) -> ET._Element | None:
    """
    :param section:
    :param prefix:
    :return: Element object.
    """
    prefix = decode_utf8(prefix)

    if prefix == 'relatedObject':
        return section.find('.//' + premis_ns('Identification', prefix))
    return section.find('.//' + premis_ns('Identifier', prefix))
