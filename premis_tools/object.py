"""Functions for reading and generating PREMIS Data Dictionaries as
xml.etree.ElementTree data structures.

References:

    * PREMIS http://www.loc.gov/standards/premis/
    * ElementTree
    https://docs.python.org/2.6/library/xml.etree.elementtree.html

"""


from premis_tools.premis import _element, _subelement, premis_ns, \
    premis_identifier, get_identifier_type_value, iter_elements, xsi_ns


def premis_relationship(
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

    relationship = _element('relationship')

    _type = _subelement(relationship, 'relationshipType')
    _type.text = relationship_type

    _subtype = _subelement(relationship, 'relationshipSubType')
    _subtype.text = relationship_subtype

    (related_type, related_value) = get_identifier_type_value(
        related_object)

    related_identifier = premis_identifier(
        related_type, related_value, prefix='relatedObject')

    relationship.append(related_identifier)

    return relationship


def premis_environment(object_or_identifier=None):
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

    environment = _element('environment')

    if object_or_identifier is None:
        return environment

    object_identifier = object_or_identifier.find(
        premis_ns('objectIdentifier'))

    if object_identifier is None:
        object_identifier = object_or_identifier

    dependency_identifier_type = object_identifier.find(
        premis_ns('dependencyIdentifierType'))

    if dependency_identifier_type is None:
        (identifier_type, identifier_value) = get_identifier_type_value(
            object_identifier)

        dependency_identifier = premis_identifier(
            identifier_type, identifier_value, 'dependency')
    else:
        dependency_identifier = object_identifier

    dependency = _subelement(environment, 'dependency')
    dependency.append(dependency_identifier)

    return environment


def premis_object(
        identifier,
        original_name=None,
        child_elements=None,
        representation=False):

    """Return the PREMIS object.

        :identifier: PREMIS identifier
        :original_name: Original name field
        :child_elements=None: Any other element appended
        :representation=False:

    Returns the following ElementTree structure::

        <premis:object xsi:type="premis:representation">

            {{ premis_identifier() }}

            <premis:originalName>varmiste.sig</premis:originalName>

            {{ premis_relationship() }}

        </premis:object>

    """

    _object = _element('object')

    _object.append(identifier)

    if representation:
        _object.set(xsi_ns('type'), 'premis:representation')
    else:
        _object.set(xsi_ns('type'), 'premis:file')

    if original_name:
        _original_name = _subelement(_object, 'originalName')
        _original_name.text = original_name

    if child_elements:
        for elem in child_elements:
            _object.append(elem)

    return _object


def iter_objects(premis):
    """Iterate all PREMIS objects from starting element.

    :starting_element: Element where matching elements are searched
    :returns: Generator object for iterating all elements

    """

    for elem in iter_elements(premis, 'object'):
        yield elem


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


def object_count(premis):
    """Return number of objects in PREMIS data dictionary.

    :premis: ElementTree element
    :returns: Integer

    """
    return len([x for x in iter_objects(premis)])


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

