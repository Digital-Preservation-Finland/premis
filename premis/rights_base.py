"""Functions for generating premis:rights and related child elements"""

from __future__ import annotations

from collections.abc import Iterable
from typing import NewType

import lxml.etree

from premis.base import _element, _subelement

OtherRightsInformation = NewType("OtherRightsInformation", lxml.etree.Element)
StatuteInformation = NewType("StatuteInformation", lxml.etree.Element)


def statute_information(
        jurisdiction: str,
        citation: str,
        start_date: str | None = None,
        end_date: str | None = None) -> StatuteInformation:
    """
    Create 'premis:statuteInformation'. This is meant to be added into
    the 'premis:rights' element produced by :func:`rights`.
    """
    if end_date and not start_date:
        raise ValueError(
            "'start_date' has to be provided if 'end_date' is set"
        )

    information = StatuteInformation(_element("statuteInformation"))

    jurisdiction_el = _subelement(
        information, "statuteJurisdiction"
    )
    jurisdiction_el.text = jurisdiction

    citation_el = _subelement(information, "statuteCitation")
    citation_el.text = citation

    if start_date:
        applicable_dates = _subelement(
            information, "statuteApplicableDates"
        )

        start_date_el = _subelement(
            applicable_dates, "startDate"
        )
        start_date_el.text = start_date

        if end_date:
            end_date_el = _subelement(
                applicable_dates, "endDate"
            )
            end_date_el.text = end_date

    return information


def other_rights_information(
        basis: str,
        start_date: str | None = None,
        end_date: str | None = None) -> OtherRightsInformation:
    """
    Create 'premis:otherRightsInformation' object
    """
    if end_date and not start_date:
        raise ValueError(
            "'start_date' has to be provided if 'end_date' is set"
        )

    information = OtherRightsInformation(_element("otherRightsInformation"))

    basis_el = _subelement(
        information, "otherRightsBasis"
    )
    basis_el.text = basis

    if start_date:
        applicable_dates = _subelement(
            information, "otherRightsApplicableDates"
        )

        start_date_el = _subelement(applicable_dates, "startDate")
        start_date_el.text = start_date

        if end_date:
            end_date_el = _subelement(applicable_dates, "endDate")
            end_date_el.text = end_date

    return information


def rights(
        statement_identifier_type: str,
        statement_identifier_value: str,
        basis: str,
        child_elements: (
            Iterable[OtherRightsInformation | StatuteInformation]
        ) = None) -> lxml.etree.Element:
    """
    Create 'premis:rights' element
    """
    if child_elements is None:
        child_elements = []

    rights = _element("rights")
    rights_statement = _subelement(rights, "rightsStatement")

    statement_identifier = _subelement(
        rights_statement, "rightsStatementIdentifier"
    )

    statement_identifier_type_el = _subelement(
        statement_identifier, "rightsStatementIdentifierType"
    )
    statement_identifier_type_el.text = statement_identifier_type

    statement_identifier_value_el = _subelement(
        statement_identifier, "rightsStatementIdentifierValue"
    )
    statement_identifier_value_el.text = \
        statement_identifier_value

    basis_el = _subelement(rights_statement, "rightsBasis")
    basis_el.text = basis

    for el in child_elements:
        rights_statement.append(el)

    return rights
