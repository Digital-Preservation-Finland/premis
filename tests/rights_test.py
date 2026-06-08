import lxml.etree as ET
import pytest
from xml_helpers.utils import compare_trees

from premis.rights_base import (other_rights_information, rights,
                                statute_information)


def test_rights_other_rights_information():
    """Test generating premis:rights with other rights information"""
    rights_ = rights(
        statement_identifier_type="preservation-rights",
        statement_identifier_value="urn:uuid:blah",
        basis="fi-dpres-sensitive-data",
        child_elements=[
            other_rights_information(
                basis="käsittelyperuste",
                start_date="2020",
                end_date="2022"
            )
        ]
    )

    xml = ET.tostring(ET.fromstring("""
        <premis:rights xmlns:premis="info:lc/xmlns/premis-v2">
          <premis:rightsStatement>
            <premis:rightsStatementIdentifier>
              <premis:rightsStatementIdentifierType>preservation-rights</premis:rightsStatementIdentifierType>
              <premis:rightsStatementIdentifierValue>urn:uuid:blah</premis:rightsStatementIdentifierValue>
            </premis:rightsStatementIdentifier>
            <premis:rightsBasis>fi-dpres-sensitive-data</premis:rightsBasis>
            <premis:otherRightsInformation>
              <premis:otherRightsBasis>k&#228;sittelyperuste</premis:otherRightsBasis>
              <premis:otherRightsApplicableDates>
                <premis:startDate>2020</premis:startDate>
                <premis:endDate>2022</premis:endDate>
              </premis:otherRightsApplicableDates>
            </premis:otherRightsInformation>
          </premis:rightsStatement>
        </premis:rights>
    """), method="c14n2", strip_text=True)

    assert compare_trees(rights_, ET.fromstring(xml))

def test_rights_statute_information():
    """Test generating premis:rights with statute information"""
    rights_ = rights(
        statement_identifier_type="preservation-rights",
        statement_identifier_value="urn:uuid:blah",
        basis="fi-dpres-sensitive-data",
        child_elements=[
            statute_information(
                jurisdiction="fi",
                citation="käsittelyperuste",
                start_date="2020",
                end_date="2022"
            )
        ]
    )

    xml = ET.tostring(ET.fromstring("""
        <premis:rights xmlns:premis="info:lc/xmlns/premis-v2">
          <premis:rightsStatement>
            <premis:rightsStatementIdentifier>
              <premis:rightsStatementIdentifierType>preservation-rights</premis:rightsStatementIdentifierType>
              <premis:rightsStatementIdentifierValue>urn:uuid:blah</premis:rightsStatementIdentifierValue>
            </premis:rightsStatementIdentifier>
            <premis:rightsBasis>fi-dpres-sensitive-data</premis:rightsBasis>
            <premis:statuteInformation>
              <premis:statuteJurisdiction>fi</premis:statuteJurisdiction>
              <premis:statuteCitation>k&#228;sittelyperuste</premis:statuteCitation>
              <premis:statuteApplicableDates>
                <premis:startDate>2020</premis:startDate>
                <premis:endDate>2022</premis:endDate>
              </premis:statuteApplicableDates>
            </premis:statuteInformation>
          </premis:rightsStatement>
        </premis:rights>
    """), method="c14n2", strip_text=True)

    assert compare_trees(rights_, ET.fromstring(xml))


def test_other_rights_forbid_missing_end_date():
    """
    Attempt generating an other rights information object with end date
    but no start date; this is forbidden
    """
    with pytest.raises(ValueError) as exc:
        other_rights_information(
            basis="käsittelyperuste",
            end_date="2020"
        )

    assert "'start_date' has to be provided" in str(exc.value)


def test_statute_information_forbid_missing_end_date():
    """
    Attempt generating a statute information object with end date
    but no start date; this is forbidden
    """
    with pytest.raises(ValueError) as exc:
        statute_information(
            jurisdiction="fi",
            citation="käsittelyperuste",
            end_date="2020"
        )

    assert "'start_date' has to be provided" in str(exc.value)


def test_other_rights_no_date():
    """
    Test generating other_rights information object with no date information
    """
    other_rights = other_rights_information(basis="käsittelyperuste")

    xml = ET.tostring(ET.fromstring("""
        <premis:otherRightsInformation xmlns:premis="info:lc/xmlns/premis-v2">
          <premis:otherRightsBasis>k&#228;sittelyperuste</premis:otherRightsBasis>
        </premis:otherRightsInformation>
    """), method="c14n2", strip_text=True)

    assert compare_trees(other_rights, ET.fromstring(xml))


def test_statute_information_no_date():
    """
    Test generating statute information object with no date information
    """
    other_rights = statute_information(
        jurisdiction="fi", citation="käsittelyperuste"
    )

    xml = ET.tostring(ET.fromstring("""
        <premis:statuteInformation xmlns:premis="info:lc/xmlns/premis-v2">
          <premis:statuteJurisdiction>fi</premis:statuteJurisdiction>
          <premis:statuteCitation>k&#228;sittelyperuste</premis:statuteCitation>
        </premis:statuteInformation>
    """), method="c14n2", strip_text=True)

    assert compare_trees(other_rights, ET.fromstring(xml))
