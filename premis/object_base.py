"""Functions for reading and generating PREMIS Data Dictionaries as
xml.etree.ElementTree data structures.

References:

    * PREMIS http://www.loc.gov/standards/premis/
    * ElementTree
    https://docs.python.org/2.6/library/xml.etree.elementtree.html

"""


from premis.base import _element, _subelement, premis_ns, \
    identifier, parse_identifier_type_value, iter_elements, xsi_ns, XSI_NS, NAMESPACES
from xml_helpers.utils import encode_utf8, decode_utf8

def fixity(message_digest, digest_algorithm='MD5'):
    fixity_el = _element('fixity')
    fixity_algorithm = _subelement(
        fixity_el, 'messageDigestAlgorithm')
    fixity_algorithm.text = decode_utf8(digest_algorithm)
    fixity_checksum = _subelement(fixity_el, 'messageDigest')
    fixity_checksum.text = decode_utf8(message_digest)
    return fixity_el


def format_designation(format_name, format_version=None):
    format_designation_el = _element('formatDesignation')
    format_name_el = _subelement(format_designation_el, 'formatName')
    format_name_el.text = decode_utf8(format_name)
    if format_version:
        format_version_el = _subelement(
            format_designation_el, 'formatVersion')
        format_version_el.text = decode_utf8(format_version)
    return format_designation_el


def format_registry(registry_name, registry_key):
    format_registry_el = _element('formatRegistry')
    registry_name_el = _subelement(format_registry_el, 'formatRegistryName')
    registry_name_el.text = decode_utf8(registry_name)
    registry_key_el = _subelement(format_registry_el, 'formatRegistryKey')
    registry_key_el.text = decode_utf8(registry_key)
    return format_registry_el


def format(child_elements=None):
    format_el = _element('format')
    if child_elements:
        for elem in child_elements:
            format_el.append(elem)
    return format_el


def date_created(date):
    date_el = _element('dateCreatedByApplication')
    date_el.text = decode_utf8(date)
    return date_el


def creating_application(child_elements=None):
    creating_app = _element('creatingApplication')
    if child_elements:
        for elem in child_elements:
            creating_app.append(elem)
    return creating_app


def object_characteristics(composition_level='0', child_elements=None):
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


def environment(object_or_identifier=None):
    """Return the PREMIS environment structure.

    :dependency_identifier: PREMIS identifier structure
    :returns: None

    Returns the following ElementTree structure::

        <premis:environment>
            <premis:dependency>

                {{ dependency_identifier }}

            </premis:dependency>
        </premis:environment>

    """

    _environment = _element('environment')

    if object_or_identifier is None:
        return _environment

    if not isinstance(object_or_identifier, list):
        object_or_identifier = [object_or_identifier]

    for _identifier in object_or_identifier:
        dependency_identifier = get_dependency_identifier(_identifier)
        dependency = _subelement(_environment, 'dependency')
        dependency.append(dependency_identifier)

    return _environment


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
        _original_name.text = decode_utf8(original_name)

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
                'objectIdentifierValue')) == decode_utf8(object_id):
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

    key_identifier_value = iter_elements(
        object_element, 'objectIdentifierValue').next()

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

        if _object_identifier_type == decode_utf8(object_identifier_type):
            yield _object


def parse_object_type(obj):
    return encode_utf8(obj.xpath('./@xsi:type',
                       namespaces=NAMESPACES)[0])


def parse_fixity(obj):
    algorithm = encode_utf8(obj.xpath(".//premis:messageDigestAlgorithm",
                                      namespaces=NAMESPACES)[0].text)
    digest = encode_utf8(obj.xpath(".//premis:messageDigest",
                                   namespaces=NAMESPACES)[0].text)
    return (algorithm, digest)


def parse_format(obj):
    format_name = encode_utf8(obj.xpath(".//premis:formatName",
                                        namespaces=NAMESPACES)[0].text)
    format_version = obj.xpath(".//premis:formatVersion",
                               namespaces=NAMESPACES)
    if len(format_version) > 0:
        format_version = encode_utf8(format_version[0].text)
    else:
        format_version = None
    return (format_name, format_version)


def parse_format_registry(obj):
    format_registry_name = encode_utf8(
        obj.xpath(".//premis:formatRegistryName",
                  namespaces=NAMESPACES)[0].text)
    format_registry_key = encode_utf8(
        obj.xpath(".//premis:formatRegistryKey",
                  namespaces=NAMESPACES)[0].text)
    return (format_registry_name, format_registry_key)


def parse_original_name(premis_object):
    return encode_utf8(premis_object.xpath(".//premis:originalName/text()",
                                           namespaces=NAMESPACES)[0])


def parse_environment(premis_elem):
    try:
        return premis_elem.xpath(".//premis:environment",
                                 namespaces=NAMESPACES)[0]
    except IndexError:
        return ""

def parse_dependency(premis_elem):
    try:
        return premis_elem.xpath(".//premis:environment/premis:dependency",
                                 namespaces=NAMESPACES)[0]
    except IndexError:
        return ""


def parse_relationship(premis_elem):
    try:
        return premis_elem.xpath(".//premis:relationship",
                                 namespaces=NAMESPACES)[0]
    except IndexError:
        return ""


def parse_relationship_type(premis_elem):
    try:
        return encode_utf8(premis_elem.xpath(
            ".//premis:relationshipType/text()",
            namespaces=NAMESPACES)[0])
    except IndexError:
        return ""

def parse_relationship_subtype(premis_elem):
    try:
        return encode_utf8(premis_elem.xpath(
            ".//premis:relationshipSubType/text()",
            namespaces=NAMESPACES)[0])
    except IndexError:
        return ""
