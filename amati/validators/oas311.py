"""
Validates the OpenAPI Specification version 3.1.1
"""

from typing import Optional
from typing_extensions import Self

from pydantic import AnyUrl, Field, model_validator

from amati.logging import Log, LogMixin
from amati.fields.email import Email
from amati.fields.openapi_versions import OpenAPI
from amati.fields.spdx_licences import SPDXIdentifier, SPDXURL, VALID_LICENCES
from amati.validators.reference_object import Reference, ReferenceModel
from amati.validators.generic import GenericObject

TITLE = 'OpenAPI Specification v3.1.1'


class ContactObject(GenericObject):
    """
    Validates the Open API Specification contact object - §4.8.3
    """
    name: Optional[str] = None
    url: Optional[AnyUrl] = None
    email: Optional[Email] = None
    _reference: Reference =  ReferenceModel( # type: ignore
        title=TITLE,
        url='https://spec.openapis.org/oas/latest.html#contact-object',
        section='Contact Object'
        )


class LicenceObject(GenericObject):
    """
    A model representing the Open API Specification licence object §4.8.4
     
    OAS uses the SPDX licence list.
    """

    name: str = Field(min_length=1)
    # What difference does Optional make here?
    identifier: SPDXIdentifier = None
    url: SPDXURL = None
    _reference: Reference = ReferenceModel( # type: ignore
        title=TITLE,
        url='https://spec.openapis.org/oas/v3.1.1.html#license-object',
        section='License Object'
        )

    @model_validator(mode='after')
    def check_url_associated_with_identifier(self: Self) -> Self:
        """
        Validate that the URL matches the provided licence identifier.

        This validator checks if the URL is listed among the known URLs for the 
        specified licence identifier.

        Returns:
            The validated licence object
        """
        if self.url is None:
            return self

        # Checked in the type AfterValidator, not necessary to raise a warning here.
        # only done to avoid an unnecessary KeyError
        if self.identifier not in VALID_LICENCES:
            return self

        if str(self.url) not in VALID_LICENCES[self.identifier]:
            LogMixin.log(
                Log(message=f'{self.url} is not associated with the identifier {self.identifier}',
                    type=Warning,
                    reference=self._reference)
                )

        return self


class InfoObject(GenericObject):
    """
    Validates the Open API Specification info object - §4.8.2:
    """
    title: str
    summary: Optional[str] = None
    description: Optional[str] = None
    termsOfService: Optional[str] = None
    contact: Optional[ContactObject] = None
    license: Optional[LicenceObject] = None
    version: str
    _reference: Reference =  ReferenceModel( # type: ignore
        title=TITLE,
        url='https://spec.openapis.org/oas/latest.html#info-object',
        section='Info Object'
    )


class OpenAPIObject(GenericObject):
    openapi: OpenAPI
    info: InfoObject
    _reference: ReferenceModel( # type: ignore
        title=TITLE,
        url='https://spec.openapis.org/oas/latest.html#openapi-object',
        section='OpenAPI Object'
        )


class ServerVariableObject(GenericObject):
    enum: Optional[list[str]] = Field(None, min_length=1)
    default: str = Field(min_length=1)
    description: Optional[str] = None
    _reference: Reference = ReferenceModel( # type: ignore
        title=TITLE,
        url='https://spec.openapis.org/oas/v3.1.1.html#server-variable-object',
        section='Server Variable Object'
        )

    @model_validator(mode='after')
    def check_enum_default(self: Self) -> Self:
        """
        Validate that the default value is in the enum list.

        Returns:
            The validated server variable object
        """
        if self.enum is None: return self

        if self.default not in self.enum:
            LogMixin.log(
                Log(message=f'The default value {self.default} is not in the enum list {self.enum}',
                    type=ValueError,
                    reference=self._reference)
                )

        return self
