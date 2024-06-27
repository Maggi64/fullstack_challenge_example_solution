from pydantic import BaseModel
from typing import List

class CountryDetails(BaseModel):
    code: str
    name: str
    region: str
    languages: List[str]
    population: int
    favorite: bool

class PaginatedCountries(BaseModel):
    countries: List[CountryDetails]
    total: int

class FavoriteUpdateRequest(BaseModel):
    code: str
    favorite: bool
