from typing import Optional

from sqlmodel import SQLModel, Field


class Hospital(SQLModel, table=True):
    OrganisationID: Optional[int] = Field(primary_key=True)
    OrganisationCode: str
    OrganisationType: str
    SubType: str
    Sector: str
    OrganisationStatus: str
    IsPimsManaged: bool
    OrganisationName: str
    Address1: Optional[str]
    Address2: Optional[str]
    Address3: Optional[str]
    City: Optional[str]
    County: Optional[str]
    Postcode: str
    Latitude: Optional[float]
    Longitude: Optional[float]
    ParentODSCode: str
    ParentName: str
    Phone: Optional[str]
    Email: Optional[str]
    Website: Optional[str]
    Fax: Optional[str]


class Pharmacy(SQLModel, table=True):
    OrganisationID: int = Field(primary_key=True)
    OrganisationCode: str
    OrganisationType: str
    SubType: str
    OrganisationStatus: str
    IsPimsManaged: bool
    IsEPSEnabled: bool
    OrganisationName: str
    Address1: Optional[str]
    Address2: Optional[str]
    Address3: Optional[str]
    City: Optional[str]
    County: Optional[str]
    Postcode: str
    Latitude: float
    Longitude: float
    ParentODSCode: str
    ParentName: str
    Phone: Optional[str]
    Email: Optional[str]
    Website: Optional[str]
    Fax: Optional[str]


class PharmacyService(SQLModel, table=True):
    ServiceID: Optional[int] = Field(primary_key=True)
    OrganisationID: int = Field(foreign_key="pharmacy.OrganisationID")
    ServiceName: str


class GP(SQLModel, table=True):
    OrganisationID: int = Field(primary_key=True)
    OrganisationCode: str
    OrganisationType: str
    SubType: str
    OrganisationStatus: str
    IsPimsManaged: bool
    IsEPSEnabled: Optional[bool]
    OrganisationName: str
    Address1: Optional[str]
    Address2: Optional[str]
    Address3: Optional[str]
    City: Optional[str]
    County: Optional[str]
    Postcode: str
    Latitude: Optional[float]
    Longitude: Optional[float]
    ParentODSCode: str
    ParentName: str
    Phone: Optional[str]
    Email: Optional[str]
    Website: Optional[str]
    Fax: Optional[str]


class GPService(SQLModel, table=True):
    ServiceID: Optional[int] = Field(primary_key=True)
    OrganisationID: int = Field(foreign_key="gp.OrganisationID")
    ServiceName: str


class Dentist(SQLModel, table=True):
    OrganisationID: int = Field(primary_key=True)
    OrganisationCode: str
    OrganisationType: str
    SubType: str
    OrganisationStatus: str
    IsPimsManaged: bool
    OrganisationName: str
    Address1: Optional[str]
    Address2: Optional[str]
    Address3: Optional[str]
    City: Optional[str]
    County: Optional[str]
    Postcode: str
    Latitude: Optional[float]
    Longitude: Optional[float]
    ParentODSCode: str
    ParentName: str
    Phone: Optional[str]
    Email: Optional[str]
    Website: Optional[str]
    Fax: Optional[str]
