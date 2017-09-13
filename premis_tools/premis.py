"""Functions for reading and generating PREMIS Data Dictionaries as
xml.etree.ElementTree data structures.

References:

    * PREMIS http://www.loc.gov/standards/premis/
    * ElementTree
    https://docs.python.org/2.6/library/xml.etree.elementtree.html

"""


import xml.etree.ElementTree as ET
from common_xml_utils.utils import XSI_NS, xsi_ns, register_namespaces

PREMIS_NS = 'info:lc/xmlns/premis-v2'
NAMESPACES = {'premis': PREMIS_NS,
              'xsi': XSI_NS}

def premis_ns(tag, prefix=""):
    """Prefix ElementTree tags with PREMIS namespace.
    object -> {info:lc...premis}object

    :tag: Tag name as string
    :returns: Prefixed tag

    """
    if prefix:
        tag = tag[0].upper() + tag[1:]
        return '{%s}%s%s' % (PREMIS_NS, prefix, tag)
    return '{%s}%s' % (PREMIS_NS, tag)


def _element(tag, prefix=""):
    """Return _ElementInterface with PREMIS namespace.

    Prefix parameter is useful for adding prefixed to lower case tags. It just
    uppercases first letter of tag and appends it to prefix::

        element = _element('objectIdentifier', 'linking')
        element.tag
        'linkingObjectIdentifier'

    :tag: Tagname
    :prefix: Prefix for the tag (default="")
    :returns: ElementTree element object

    """
    return ET.Element(premis_ns(tag, prefix))


def _subelement(parent, tag, prefix=""):
    """Return subelement for the given parent element. Created element is
    appended to parent element.

    :parent: Parent element
    :tag: Element tagname
    :prefix: Prefix for the tag
    :returns: Created subelement

    """
    return ET.SubElement(parent, premis_ns(tag, prefix))


def premis_identifier(identifier_type, identifier_value, prefix='object'):
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

    """

    if prefix == 'relatedObject':
        _identifier = _element('Identification', prefix)
    else:
        _identifier = _element('Identifier', prefix)

    _value = _subelement(_identifier, 'IdentifierType', prefix)
    _value.text = identifier_type

    _type = _subelement(_identifier, 'IdentifierValue', prefix)
    _type.text = identifier_value

    return _identifier


def get_identifier_type_value(identifier, prefix='object'):
    """Return identifierType and IdentifierValue from given PREMIS id.
    If segment contains multiple identifiers, returns first
    occurrence.

    :identifier: Premis identifier
    :returns: (identifier_type, identifier_value)

    """
    if prefix == 'relatedObject':
        if identifier.tag != premis_ns('relatedObjectIdentification'):
            identifier = identifier.find(premis_ns('relatedObjectIdentification'))
        if identifier is not None:
            return (
                identifier.find(premis_ns('relatedObjectIdentifierType')).text,
                identifier.find(premis_ns('relatedObjectIdentifierValue')).text)
        return None

    if identifier.tag != premis_ns('Identifier', prefix):
        identifier = identifier.find(premis_ns('Identifier', prefix))
    if identifier is not None:
        return (
            identifier.find(premis_ns('IdentifierType', prefix)).text,
            identifier.find(premis_ns('IdentifierValue', prefix)).text)
    return None


def premis_premis(child_elements=None, namespaces=NAMESPACES):
    """Create PREMIS Data Dictionary root element.

    :child_elements: Any elements appended to the PREMIS dictionary

    Returns the following ElementTree structure::


        <premis:premis
            xmlns:premis="info:lc/xmlns/premis-v2"
            xmlns:xsi="http://www.w3.org/2001/xmlschema-instance"
            xsi:schemalocation="info:lc/xmlns/premis-v2
                                http://www.loc.gov/standards/premis/premis.xsd"
            version="2.2">

    """
    register_namespaces(namespaces)
    _premis = _element('premis')
    _premis.set(
        xsi_ns('schemaLocation'),
        'info:lc/xmlns/premis-v2 '
        'http://www.loc.gov/standards/premis/premis.xsd')
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
    for elem in starting_element.findall('.//' + premis_ns(tag)):
        yield elem

