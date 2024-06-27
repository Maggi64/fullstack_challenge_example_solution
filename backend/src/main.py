import os
from typing import List, Optional

from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from starlette import status

from backend.src.models import CountryDetails, FavoriteUpdateRequest, PaginatedCountries
from backend.src.db_connection import pool, get_connection

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        f"http://localhost:{os.getenv('FRONTEND_PORT')}",
        f"http://127.0.0.1:{os.getenv('FRONTEND_PORT')}",
        f"https://{os.getenv('CODESPACE_NAME')}-{os.getenv('FRONTEND_PORT')}.app.github.dev",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def fetch_languages(cursor, country_code):
    cursor.execute("""
        SELECT language.name 
        FROM languages language
        JOIN country_link_languages country_language ON language.code = country_language.language_code 
        WHERE country_language.country_code = %s
    """, (country_code,))
    return [lang['name'] for lang in cursor.fetchall()]

def construct_country_query(sort_by, sort_order, search):
    base_query = """
        SELECT country.code, country.name, region.name AS region, country.population, 
               COALESCE(favorite.country_code IS NOT NULL, FALSE) AS favorite 
        FROM countries country 
        JOIN regions region ON country.region_code = region.code 
        LEFT JOIN favorites favorite ON country.code = favorite.country_code 
    """
    if search:
        base_query += "WHERE country.name ILIKE %s "
    
    sort_column = f"country.{sort_by}" if sort_by in ["name", "population"] else "region.name"
    base_query += f"ORDER BY {sort_column} {sort_order} LIMIT %s OFFSET %s"
    return base_query

@app.get("/countries", response_model=PaginatedCountries)
def get_countries(page: int = 1, size: int = 20, sort_by: str = "name", sort_order: str = "asc", search: Optional[str] = None, cursor = Depends(get_connection)):
    offset = (page - 1) * size
    query = construct_country_query(sort_by, sort_order, search)
    search_param = f"%{search}%" if search else None
    
    cursor.execute(query, (search_param, size, offset) if search else (size, offset))
    countries = cursor.fetchall()

    cursor.execute("SELECT COUNT(*) FROM countries")
    total = cursor.fetchone()['count']

    countries_list = [
        CountryDetails(
            code=country['code'],
            name=country['name'], 
            region=country['region'], 
            languages=fetch_languages(cursor, country['code']), 
            population=country['population'], 
            favorite=country['favorite']
        ) 
        for country in countries
    ]

    return PaginatedCountries(countries=countries_list, total=total)

@app.post("/favorites", status_code=status.HTTP_204_NO_CONTENT)
def update_favorite(request: FavoriteUpdateRequest, cursor = Depends(get_connection)):
    if request.favorite:
        cursor.execute("INSERT INTO favorites (country_code) VALUES (%s) ON CONFLICT DO NOTHING", (request.code,))
    else:
        cursor.execute("DELETE FROM favorites WHERE country_code = %s", (request.code,))
    return

@app.get("/favorites", response_model=List[CountryDetails])
def get_favorites(cursor = Depends(get_connection)):
    query = """
        SELECT c.code, c.name, r.name AS region, c.population, TRUE AS favorite 
        FROM countries c 
        JOIN regions r ON c.region_code = r.code 
        JOIN favorites f ON c.code = f.country_code
    """
    
    cursor.execute(query)
    countries = cursor.fetchall()

    countries_list = [
        CountryDetails(
            code=country['code'],
            name=country['name'], 
            region=country['region'], 
            languages=fetch_languages(cursor, country['code']), 
            population=country['population'], 
            favorite=country['favorite']
        ) 
        for country in countries
    ]

    return countries_list
