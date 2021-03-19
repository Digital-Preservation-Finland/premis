"""Functions for reading and generating PREMIS Data Dictionaries as
xml.etree.ElementTree data structures.

References:

    * PREMIS http://www.loc.gov/standards/premis/
    * ElementTree
    https://docs.python.org/2.6/library/xml.etree.elementtree.html

"""
from __future__ import unicode_literals

from xml_helpers.utils import decode_utf8
from premis.base import (NAMESPACES, XSI_NS, _element, _subelement, identifier,
                         iter_elements, parse_identifier_type_value, premis_ns,
                         xsi_ns)


def fixity(message_digest, digest_algorithm='MD5'):
    """
    :param message_digest:
    :param digest_algorithm:
    :return: Element object for fixity.
    """
    fixity_el = _element('fixity')
    fixity_algorithm = _subelement(
        fixity_el, 'messageDigestAlgorithm')
    fixity_algorithm.text = decode_utf8(digest_algorithm)
    fixity_checksum = _subelement(fixity_el, 'messageDigest')
    fixity_checksum.text = message_digest
    return fixity_el


def format_designation(format_name, format_version=None):
    """
    :param format_name:
    :param format_version:
    :return: Element object for format designation.
    """
    format_designation_el = _element('formatDesignation')
    format_name_el = _subelement(format_designation_el, 'formatName')
    format_name_el.text = decode_utf8(format_name)
    if format_version:
        format_version_el = _subelement(
            format_designation_el, 'formatVersion')
        format_version_el.text = decode_utf8(format_version)
    return format_designation_el


def format_registry(registry_name, registry_key):
    """
    :param registry_name:
    :param registry_key:
    :return: Element object for format registry.
    """
    format_registry_el = _element('formatRegistry')
    registry_name_el = _subelement(format_registry_el, 'formatRegistryName')
    registry_name_el.text = decode_utf8(registry_name)
    registry_key_el = _subelement(format_registry_el, 'formatRegistryKey')
    registry_key_el.text = decode_utf8(registry_key)
    return format_registry_el


# pylint: disable=redefined-builtin
# Listed as requiring a fix in KDKPAS-2522
def format(child_elements=None):
    """
    :param child_elements:
    :return: Element object for format.
    """
    format_el = _element('format')
    if child_elements:
        for elem in child_elements:
            format_el.append(elem)
    return format_el


def date_created(date):
    """
    :param date:
    :return: Element object for date created.
    """
    date_el = _element('dateCreatedByApplication')
    date_el.text = decode_utf8(date)
    return date_el


def creating_application(child_elements=None):
    """
    :param child_elements:
    :return: Element object for creating application.
    """
    creating_app = _element('creatingApplication')
    if child_elements:
        for elem in child_elements:
            creating_app.append(elem)
    return creating_app


def object_characteristics(composition_level='0', child_elements=None):
    """
    :param composition_level:
    :param child_elements:
    :return: Element object for object characteristics.
    """
    object_char = _element('objectCharacteristics')

    composition = _subelement(
        object_char, 'compositionLevel')
    composition.text = decode_utf8(composition_level)
    if child_elements:
        for elem in child_elements:
            object_char.append(elem)
    return object_char


def relationship(
        relationship_type, relationship_subtype,
        related_object):
    """Create PREMIS relationship DOM segment.

    :relationship_type: Relationship type from PREMIS vocabulary
    :relationship_subtype: Relationship subtype from PREMIS vocabulary
    :related_object: Related object linked to relationship
    :returns: ElementTree DOM tree

    Produces the following PREMIS segment::

      <premis:relationship>

          <premis:relationshipType>structural</premis:relationshipType>
          <premis:relationshipSubType>
              is included in
          </premis:relationshipSubType>

          {{ premis_identifier(prefix=related) }}

      </premis:relationship>

    """
    if related_object is None:
        return None

    _relationship = _element('relationship')

    _type = _subelement(_relationship, 'relationshipType')
    _type.text = decode_utf8(relationship_type)

    _subtype = _subelement(_relationship, 'relationshipSubType')
    _subtype.text = decode_utf8(relationship_subtype)

    (related_type, related_value) = parse_identifier_type_value(
        related_object)

    related_identifier = identifier(
        related_type, related_value, prefix='relatedObject')

    _relationship.append(related_identifier)

    return _relationship


def environment(characteristic=None,
                purposes=None,
                notes=None,
                child_elements=None):
    """Return the PREMIS environment structure.

    :param characteristic: PREMIS environment characteristic as a string
    :param purposes: A list of environment purposes to be appended
    :param notes: A list of environment notes to be appended
    :param child_elements: A list of child elements to be appended
    :returns: ElementTree DOM tree
    """

    _environment = _element('environment')

    if characteristic:
        char_elem = _subelement(
            _environment, 'environmentCharacteristic')
        char_elem.text = decode_utf8(characteristic)

    if purposes:
        for purpose in purposes:
            purpose_elem = _subelement(
                _environment, 'environmentPurpose')
            purpose_elem.text = decode_utf8(purpose)

    if notes:
        for note in notes:
            note_elem = _subelement(
                _environment, 'environmentNote')
            note_elem.text = decode_utf8(note)

    if child_elements:
        for elem in child_elements:
            _environment.append(elem)

    return _environment


def dependency(names=None, identifiers=None):
    """Returns the PREMIS dependency structure.

    :param names: A list of strings of dependency names
    :param identifiers: A list of PREMIS identifier structures
    :returns: ElementTree DOM tree
    """
    _dependency = _element('dependency')
    if names:
        for name in names:
            name_elem = _subelement(
                _dependency, 'dependencyName')
            name_elem.text = decode_utf8(name)

    if identifiers:
        for identifier_elem in identifiers:
            _dependency.append(identifier_elem)

    return _dependency


def get_dependency_identifier(object_or_identifier):
    """Create new dependency indentifier from object containing
    objectIdentifier or return existing dependencyIdentifier. If both elements
    exists in given ``object_or_identifier`` return dependencyIdentifier
    generated from objectIdentifier"""

    if object_or_identifier.tag == premis_ns("objectIdentifier"):
        object_identifier = object_or_identifier
    else:
        object_identifier = object_or_identifier.find(
            premis_ns('objectIdentifierType'))

    if object_identifier is not None:
        (identifier_type, identifier_value) = parse_identifier_type_value(
            object_or_identifier)

        return identifier(
            identifier_type, identifier_value, 'dependency')

    if object_or_identifier.tag == premis_ns("dependencyIdentifier"):
        dependency_identifier = object_or_identifier
    else:
        dependency_identifier = object_or_identifier.find(
            premis_ns('dependencyIdentifier'))

    if dependency_identifier is not None:
        return dependency_identifier

    raise ValueError(
        "Argument object_or_indentifier must contain"
        "valid objectIdentifier or "
        "dependencyIdentifier: {}".format(
            object_or_identifier))


def object(
        object_id,
        original_name=None,
        child_elements=None,
        representation=False,
        bitstream=False):
    """Return the PREMIS object.

        :object_id: PREMIS identifier
        :original_name: Original name field
        :child_elements=None: Any other element appended
        :representation=False: If true, representation object
        :bitstream=False: If true, bitstream object

    Returns the following ElementTree structure::

        <premis:object xsi:type="premis:representation">

            {{ premis_identifier() }}

            <premis:originalName>varmiste.sig</premis:originalName>

            {{ premis_relationship() }}

        </premis:object>

    """

    _object = _element('object', ns={'xsi': XSI_NS})

    _object.append(object_id)

    if representation:
        _object.set(xsi_ns('type'), 'premis:representation')
    elif bitstream:
        _object.set(xsi_ns('type'), 'premis:bitstream')
    else:
        _object.set(xsi_ns('type'), 'premis:file')

    if original_name:
        _original_name = _subelement(_object, 'originalName')
        _original_name.text = original_name

    if child_elements:
        for elem in child_elements:
            _object.append(elem)

    return _object


def iter_objects(premis_el):
    """Iterate all PREMIS objects from starting element.

    :starting_element: Element where matching elements are searched
    :returns: Generator object for iterating all elements

    """

    for elem in iter_elements(premis_el, 'object'):
        yield elem


def find_object_by_id(premis, object_id):
    """Find a PREMIS object by its objectIdentifierValue
    :premis: ElementTree element
    :object_id: The PREMIS object's ID

    :returns: Element if found, None otherwise
    """
    for elem in iter_objects(premis):
        if elem.findtext('.//' + premis_ns(
                'objectIdentifierValue')) == object_id:
            return elem

    return None


def filter_objects(premis_objects, filtered_objects):
    """Return PREMIS objects from `premis_objects` which are not listed in
    `filtered_objects`

    :premis_objects: Objects to filter
    :filtered_objects: Objects which are removed from `premis_objects`
    :returns: Generator object for iterating all objects

    """
    for elem in premis_objects:
        found = False
        for filter_element in iter_objects(filtered_objects):
            if contains_object(filter_element, elem):
                found = True
        if not found:
            yield elem


def contains_object(object_element, search_from_element):
    """Return True if `search_from_element` contains the `object_element`
    object or objectIdentifier.

    :object_element: PREMIS object or identifier
    :search_from_element: PREMIS object to search from
    :returns: Boolean

    """

    key_identifier_value = next(
        iter_elements(object_element, 'objectIdentifierValue')
    )

    # Unfortunately Python 2.6 ElementTree does not support xpath search by
    # element value so we have to search with for-loop

    identifiers = iter_elements(search_from_element, 'objectIdentifierValue')

    for identifier_value in identifiers:
        if identifier_value.text == key_identifier_value.text:
            return True

    return False


def object_count(premis_el):
    """Return number of objects in PREMIS data dictionary.

    :premis: ElementTree element
    :returns: Integer

    """
    return len([x for x in iter_objects(premis_el)])


def objects_with_type(objects, object_identifier_type):
    """Return all objects from list of `objects` with given
    `object_identifier_type` matching the PREMIS objectIdentifierType field.

    :objects: Iterable of objects
    :object_identifier_type: Identifier type as string
    :returns: Iterator with all matching objects

    """
    for _object in objects:

        _object_identifier = _object.find(premis_ns('objectIdentifier'))
        _object_identifier_type = _object_identifier.findtext(
            premis_ns('objectIdentifierType'))

        if _object_identifier_type == object_identifier_type:
            yield _object


def parse_object_type(obj):
    """
    :param obj:
    :return: String
    """
    return obj.xpath('./@xsi:type', namespaces=NAMESPACES)[0]


def parse_fixity(obj):
    """
    :param obj:
    :return: Tuple of strings to represent algorithm and digest.
    """
    algorithm = obj.xpath(
        ".//premis:messageDigestAlgorithm",
        namespaces=NAMESPACES)[0].text
    digest = obj.xpath(
        ".//premis:messageDigest",
        namespaces=NAMESPACES)[0].text
    return (algorithm, digest)


def parse_format(obj):
    """
    :param obj:
    :return: Tuple of strings to represent format name and version.
    """
    format_name = obj.xpath(
        ".//premis:formatName", namespaces=NAMESPACES)[0].text
    format_version = obj.xpath(".//premis:formatVersion",
                               namespaces=NAMESPACES)
    if format_version:
        format_version = format_version[0].text
    else:
        format_version = None
    return (format_name, format_version)


def parse_format_registry(obj):
    """
    :param obj:
    :return: Tuple of strings to represent format registry name and key.
    """
    format_registry_name = obj.xpath(
        ".//premis:formatRegistryName",
        namespaces=NAMESPACES)[0].text
    format_registry_key = obj.xpath(
        ".//premis:formatRegistryKey",
        namespaces=NAMESPACES)[0].text
    return (format_registry_name, format_registry_key)


def parse_original_name(premis_object):
    """
    :param premis_object:
    :return: String
    """
    return premis_object.xpath(
        ".//premis:originalName/text()",
        namespaces=NAMESPACES)[0]


def iter_environments(premis_elem):
    """Iterate all PREMIS environments from starting element.

    :param premis_elem: ElementTree element
    :return: Iterable of premis environments
    """
    for _environment in iter_elements(premis_elem, 'environment'):
        yield _environment


def environments_with_purpose(environments, purpose):
    """Finds the premis environment sections with a specific purpose.
    The function yields only the environments with the given purpose in
    the premis:environmentPurpose contents.

    :param environments: Iterable of premis environments
    :param purpose: The environment purpose as a string
    :return: Iterable of premis environments
    """
    for _environment in environments:
        for purpose_elem in iter_elements(_environment, 'environmentPurpose'):
            if purpose_elem.text == purpose:
                yield _environment


def parse_dependency(premis_elem):
    """
    :param premis_elem:
    :return: String
    """
    try:
        return list(iter_elements(premis_elem, 'dependency'))
    except IndexError:
        return ""


def parse_relationship(premis_elem):
    """
    :param premis_elem:
    :return: String
    """
    try:
        return premis_elem.xpath(".//premis:relationship",
                                 namespaces=NAMESPACES)[0]
    except IndexError:
        return ""


def parse_relationship_type(premis_elem):
    """
    :param premis_elem:
    :return: String
    """
    try:
        return premis_elem.xpath(
            ".//premis:relationshipType/text()",
            namespaces=NAMESPACES)[0]
    except IndexError:
        return ""


def parse_relationship_subtype(premis_elem):
    """
    :param premis_elem:
    :return: String
    """
    try:
        return premis_elem.xpath(
            ".//premis:relationshipSubType/text()",
            namespaces=NAMESPACES)[0]
    except IndexError:
        return ""
