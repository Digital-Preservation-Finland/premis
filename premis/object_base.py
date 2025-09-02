"""Functions for reading and generating PREMIS Data Dictionaries as
xml.etree.ElementTree data structures.

References:

    * PREMIS http://www.loc.gov/standards/premis/
    * ElementTree
    https://docs.python.org/3.9/library/xml.etree.elementtree.html

"""
from __future__ import annotations

from collections.abc import Generator, Iterable, Iterator

import lxml.etree as ET
from xml_helpers.utils import decode_utf8, xsi_ns

from premis.base import (
    NAMESPACES,
    _element,
    _subelement,
    identifier,
    iter_elements,
    parse_identifier_type_value,
    premis_ns,
)


def _object_elems_order(elem: ET._Element) -> int:
    """Return order number for given element in premis:object schema.
    This can be used for example with sort().

    All elements for file, representation and bitstream are included,
    the sort order is the same for all these three types.
    """
    return [
        premis_ns('objectIdentifier'),
        premis_ns('preservationLevel'),
        premis_ns('significantProperties'),
        premis_ns('objectCharacteristics'),
        premis_ns('originalName'),
        premis_ns('storage'),
        premis_ns('environment'),
        premis_ns('signatureInformation'),
        premis_ns('relationship'),
        premis_ns('linkingEventIdentifier'),
        premis_ns('linkingIntellectualEntityIdentifier'),
        premis_ns('linkingRightsStatementIdentifier')].index(elem.tag)


def fixity(message_digest: str, digest_algorithm: str = 'MD5') -> ET._Element:
    """
    :param message_digest:
    :param digest_algorithm:
    :returns: Element object for fixity.
    """
    fixity_el = _element('fixity')
    fixity_algorithm = _subelement(
        fixity_el, 'messageDigestAlgorithm')
    fixity_algorithm.text = decode_utf8(digest_algorithm)
    fixity_checksum = _subelement(fixity_el, 'messageDigest')
    fixity_checksum.text = message_digest
    return fixity_el


def format_designation(
    format_name: str, format_version: str | None = None
) -> ET._Element:
    """
    :param format_name:
    :param format_version:
    :returns: Element object for format designation.
    """
    format_designation_el = _element('formatDesignation')
    format_name_el = _subelement(format_designation_el, 'formatName')
    format_name_el.text = decode_utf8(format_name)
    if format_version:
        format_version_el = _subelement(
            format_designation_el, 'formatVersion')
        format_version_el.text = decode_utf8(format_version)
    return format_designation_el


def format_registry(registry_name: str, registry_key: str) -> ET._Element:
    """
    :param registry_name:
    :param registry_key:
    :returns: Element object for format registry.
    """
    format_registry_el = _element('formatRegistry')
    registry_name_el = _subelement(format_registry_el, 'formatRegistryName')
    registry_name_el.text = decode_utf8(registry_name)
    registry_key_el = _subelement(format_registry_el, 'formatRegistryKey')
    registry_key_el.text = decode_utf8(registry_key)
    return format_registry_el


# pylint: disable=redefined-builtin
# Listed as requiring a fix in KDKPAS-2522
def format(child_elements: Iterable[ET._Element] | None = None) -> ET._Element:
    """
    :param child_elements:
    :returns: Element object for format.
    """
    format_el = _element('format')
    if child_elements:
        for elem in child_elements:
            format_el.append(elem)
    return format_el


def date_created(date: str) -> ET._Element:
    """
    :param date:
    :returns: Element object for date created.
    """
    date_el = _element('dateCreatedByApplication')
    date_el.text = decode_utf8(date)
    return date_el


def creating_application_name(name: str) -> ET._Element:
    """
    :param name:
    :returns: Element object for software name.
    """
    name_el = _element('creatingApplicationName')
    name_el.text = decode_utf8(name)
    return name_el


def creating_application_version(version: str) -> ET._Element:
    """
    :param version:
    :returns: Element object for software version.
    """
    version_el = _element('creatingApplicationVersion')
    version_el.text = decode_utf8(version)
    return version_el


def creating_application(
    child_elements: Iterable[ET._Element] | None = None,
) -> ET._Element:
    """
    :param child_elements:
    :returns: Element object for creating application.
    """
    creating_app = _element('creatingApplication')
    if child_elements:
        for elem in child_elements:
            creating_app.append(elem)
    return creating_app


def object_characteristics(
    composition_level: str = "0",
    child_elements: Iterable[ET._Element] | None = None,
) -> ET._Element:
    """
    :param composition_level:
    :param child_elements:
    :returns: Element object for object characteristics.
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
    relationship_type: str,
    relationship_subtype: str,
    related_objects: Iterable[ET._Element],
) -> ET._Element | None:
    """Create PREMIS relationship DOM segment.

    :param relationship_type: Relationship type from PREMIS vocabulary
    :param relationship_subtype: Relationship subtype from PREMIS vocabulary
    :param related_objects: Iterable of related objects linked to relationship
    :returns: ElementTree DOM tree or None

    Produces the following PREMIS segment::

      <premis:relationship>

          <premis:relationshipType>structural</premis:relationshipType>
          <premis:relationshipSubType>
              is included in
          </premis:relationshipSubType>

          {{ premis_identifier(prefix=related) }}

      </premis:relationship>

    """
    if not related_objects:
        return None

    relationship_ = _element('relationship')

    type_ = _subelement(relationship_, 'relationshipType')
    type_.text = decode_utf8(relationship_type)

    subtype_ = _subelement(relationship_, 'relationshipSubType')
    subtype_.text = decode_utf8(relationship_subtype)

    for related_object in related_objects:
        (related_type, related_value) = parse_identifier_type_value(
            related_object)

        related_identifier = identifier(
            related_type, related_value, prefix='relatedObject')

        relationship_.append(related_identifier)

    return relationship_


def environment(
    characteristic: str | None = None,
    purposes: list[str] | None = None,
    notes: list[str] | None = None,
    child_elements: Iterable[ET._Element] | None = None,
) -> ET._Element:
    """Return the PREMIS environment structure.

    :param characteristic: PREMIS environment characteristic as a string
    :param purposes: A list of environment purposes to be appended
    :param notes: A list of environment notes to be appended
    :param child_elements: A list of child elements to be appended
    :returns: ElementTree DOM tree
    """
    environment_ = _element('environment')

    if characteristic:
        char_elem = _subelement(
            environment_, 'environmentCharacteristic')
        char_elem.text = decode_utf8(characteristic)

    if purposes:
        for purpose in purposes:
            purpose_elem = _subelement(
                environment_, 'environmentPurpose')
            purpose_elem.text = decode_utf8(purpose)

    if notes:
        for note in notes:
            note_elem = _subelement(
                environment_, 'environmentNote')
            note_elem.text = decode_utf8(note)

    if child_elements:
        for elem in child_elements:
            environment_.append(elem)

    return environment_


def dependency(
    names: list[str] | None = None,
    identifiers: Iterable[ET._Element] | None = None,
) -> ET._Element:
    """Returns the PREMIS dependency structure.

    :param names: A list of strings of dependency names
    :param identifiers: A list of PREMIS identifier structures
    :returns: ElementTree DOM tree
    """
    dependency_ = _element('dependency')
    if names:
        for name in names:
            name_elem = _subelement(
                dependency_, 'dependencyName')
            name_elem.text = decode_utf8(name)

    if identifiers:
        for identifier_elem in identifiers:
            dependency_.append(identifier_elem)

    return dependency_


def get_dependency_identifier(
    object_or_identifier: ET._Element,
) -> ET._Element:
    """Create new dependency indentifier from object containing
    objectIdentifier or return existing dependencyIdentifier. If both elements
    exists in given ``object_or_identifier`` return dependencyIdentifier
    generated from objectIdentifier
    """
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
        "Argument object_or_indentifier must contain valid objectIdentifier or"
        f" dependencyIdentifier: {object_or_identifier}"
    )


def object(
    object_id: ET._Element,
    alt_ids: Iterable[ET._Element] | None = None,
    original_name: str | None = None,
    child_elements: Iterable[ET._Element] | None = None,
    representation: bool = False,
    bitstream: bool = False,
) -> ET._Element:
    """Return the PREMIS object.

    :param object_id: PREMIS identifier
    :param alt_ids: List of alternative identifiers
    :param original_name: Original name field
    :param child_elements=None: Any other element appended
    :param representation=False: If true, representation object
    :param bitstream=False: If true, bitstream object
    :returns:
    The following ElementTree structure::

        <premis:object xsi:type="premis:representation">

            {{ premis_identifier() }}

            <premis:originalName>varmiste.sig</premis:originalName>

            {{ premis_relationship() }}

        </premis:object>

    """
    alt_ids = alt_ids or []

    object_ = _element('object', ns=NAMESPACES)

    object_.append(object_id)

    if alt_ids:
        for alt_id in alt_ids:
            object_.append(alt_id)

    if representation:
        object_.set(xsi_ns('type'), 'premis:representation')
    elif bitstream:
        object_.set(xsi_ns('type'), 'premis:bitstream')
    else:
        object_.set(xsi_ns('type'), 'premis:file')

    object_elements_ = []

    if original_name:
        original_name_ = _element('originalName')
        original_name_.text = original_name
        object_elements_.append(original_name_)

    if child_elements:
        object_elements_.extend(child_elements)

    # Sort elements before appending them to the _object
    object_elements_.sort(key=_object_elems_order)
    for elem in object_elements_:
        object_.append(elem)

    return object_


def iter_objects(premis_el: ET._Element) -> Generator[ET._Element]:
    """Iterate all PREMIS objects from starting element.

    :param starting_element: Element where matching elements are searched
    :returns: Generator object for iterating all elements

    """
    yield from iter_elements(premis_el, 'object')


def find_object_by_id(
    premis: ET._Element, object_id: str
) -> ET._Element | None:
    """Find a PREMIS object by its objectIdentifierValue

    :param premis: ElementTree element
    :param object_id: The PREMIS object's ID

    :returns: Element if found, None otherwise
    """
    for elem in iter_objects(premis):
        if elem.findtext('.//' + premis_ns(
                'objectIdentifierValue')) == object_id:
            return elem

    return None


def filter_objects(
    premis_objects: Iterable[ET._Element], filtered_objects: ET._Element
) -> Generator[ET._Element]:
    """Return PREMIS objects from `premis_objects` which are not listed in
    `filtered_objects`

    :param premis_objects: Objects to filter
    :param filtered_objects: Objects which are removed from `premis_objects`
    :returns: Generator object for iterating all objects

    """
    for elem in premis_objects:
        found = False
        for filter_element in iter_objects(filtered_objects):
            if contains_object(filter_element, elem):
                found = True
        if not found:
            yield elem


def contains_object(
    object_element: ET._Element, search_from_element: ET._Element
) -> bool:
    """Return True if `search_from_element` contains the `object_element`
    object or objectIdentifier.

    :param object_element: PREMIS object or identifier
    :param search_from_element: PREMIS object to search from
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


def object_count(premis_el: ET._Element) -> int:
    """Return number of objects in PREMIS data dictionary.

    :param premis: ElementTree element
    :returns: Integer

    """
    return len(list(iter_objects(premis_el)))


def objects_with_type(
    objects: Iterable[ET._Element], object_identifier_type: str | None
) -> Iterator[ET._Element]:
    """Return all objects from list of `objects` with given
    `object_identifier_type` matching the PREMIS objectIdentifierType field.

    :param objects: Iterable of objects
    :param object_identifier_type: Identifier type as string
    :returns: Iterator with all matching objects

    """
    for _object in objects:

        object_identifier_ = _object.find(premis_ns('objectIdentifier'))
        object_identifier_type_ = object_identifier_.findtext(
            premis_ns('objectIdentifierType'))

        if object_identifier_type_ == object_identifier_type:
            yield _object


def parse_object_type(obj: ET._Element) -> str:
    """
    :param obj:
    :returns: String
    """
    return obj.xpath('./@xsi:type', namespaces=NAMESPACES)[0]


def parse_fixity(obj: ET._Element) -> tuple[str | None, str | None]:
    """
    :param obj:
    :returns: Tuple of strings to represent algorithm and digest.
    """
    algorithm = obj.xpath(
        ".//premis:messageDigestAlgorithm",
        namespaces=NAMESPACES)[0].text
    digest = obj.xpath(
        ".//premis:messageDigest",
        namespaces=NAMESPACES)[0].text
    return (algorithm, digest)


def parse_format(obj: ET._Element) -> tuple[str | None, str | None]:
    """
    :param obj:
    :returns: Tuple of strings to represent format name and version.
    """
    format_name = obj.xpath(
        ".//premis:formatName", namespaces=NAMESPACES)[0].text
    format_version = obj.xpath(".//premis:formatVersion",
                               namespaces=NAMESPACES)

    format_version = format_version[0].text if format_version else None
    return (format_name, format_version)


def parse_format_registry(obj: ET._Element) -> tuple[str | None, str | None]:
    """
    :param obj:
    :returns: Tuple of strings to represent format registry name and key.
    """
    format_registry_name = obj.xpath(
        ".//premis:formatRegistryName",
        namespaces=NAMESPACES)[0].text
    format_registry_key = obj.xpath(
        ".//premis:formatRegistryKey",
        namespaces=NAMESPACES)[0].text
    return (format_registry_name, format_registry_key)


def parse_original_name(premis_object: ET._Element) -> str:
    """
    :param premis_object:
    :returns: String
    """
    return premis_object.xpath(
        ".//premis:originalName/text()",
        namespaces=NAMESPACES)[0]


def iter_environments(premis_elem: ET._Element) -> Generator[ET._Element]:
    """Iterate all PREMIS environments from starting element.

    :param premis_elem: ElementTree element
    :returns: Iterable of premis environments
    """
    yield from iter_elements(premis_elem, 'environment')


def environments_with_purpose(
    environments: ET._Element, purpose: str
) -> Iterator[ET._Element]:
    """Finds the premis environment sections with a specific purpose.
    The function yields only the environments with the given purpose in
    the premis:environmentPurpose contents.

    :param environments: Iterable of premis environments
    :param purpose: The environment purpose as a string
    :returns: Iterable of premis environments
    """
    for _environment in environments:
        for purpose_elem in iter_elements(_environment, "environmentPurpose"):
            if purpose_elem.text == purpose:
                yield _environment


def parse_dependency(premis_elem: ET._Element) -> list[ET._Element]:
    """
    :param premis_elem:
    :returns: list of elements
    """
    try:
        return list(iter_elements(premis_elem, "dependency"))
    except IndexError:
        return []


def parse_relationship(premis_elem: ET._Element) -> str:
    """
    :param premis_elem:
    :returns: String
    """
    try:
        return premis_elem.xpath(
            ".//premis:relationship", namespaces=NAMESPACES
        )[0]
    except IndexError:
        return ""


def parse_relationship_type(premis_elem: ET._Element) -> str:
    """
    :param premis_elem:
    :returns: String
    """
    try:
        return premis_elem.xpath(
            ".//premis:relationshipType/text()", namespaces=NAMESPACES
        )[0]
    except IndexError:
        return ""


def parse_relationship_subtype(premis_elem: ET._Element) -> str:
    """
    :param premis_elem:
    :returns: String
    """
    try:
        return premis_elem.xpath(
            ".//premis:relationshipSubType/text()", namespaces=NAMESPACES
        )[0]
    except IndexError:
        return ""
