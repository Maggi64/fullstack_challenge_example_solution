import os
from typing import List, Optional

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette import status

from backend.src.models import CountryDetails, FavoriteUpdateRequest, PaginatedCountries
from backend.src.db_connection import connection

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

@app.get("/countries", response_model=PaginatedCountries)
def get_countries(page: int = 1, size: int = 20, sort_by: str = "name", search: str = None):
    cursor = connection.cursor()
    offset = (page - 1) * size
    sort_column = f"c.{sort_by}" if sort_by in ["name", "population"] else f"r.{sort_by}"
    
    query = """
    SELECT c.code, c.name, r.name AS region, c.population, 
           COALESCE(f.country_code IS NOT NULL, FALSE) AS favorite 
    FROM countries c 
    JOIN regions r ON c.region_code = r.code 
    LEFT JOIN favorites f ON c.code = f.country_code 
    """
    
    if search:
        query += f"WHERE c.name ILIKE '%{search}%' "
    
    query += f"ORDER BY {sort_column} LIMIT {size} OFFSET {offset}"

    cursor.execute(query)
    countries = cursor.fetchall()

    cursor.execute("SELECT COUNT(*) FROM countries")
    total = cursor.fetchone()[0]

    countries_list = []
    for country in countries:
        cursor.execute("SELECT l.name FROM languages l JOIN country_link_languages cl ON l.code = cl.language_code WHERE cl.country_code = %s", (country[0],))
        languages = cursor.fetchall()
        countries_list.append(CountryDetails(
            code=country[0],
            name=country[1], 
            region=country[2], 
            languages=[lang[0] for lang in languages], 
            population=country[3], 
            favorite=country[4]
        ))

    return PaginatedCountries(countries=countries_list, total=total)

@app.post("/favorites", status_code=status.HTTP_204_NO_CONTENT)
def update_favorite(request: FavoriteUpdateRequest):
    cursor = connection.cursor()
    if request.favorite:
        cursor.execute("INSERT INTO favorites (country_code) VALUES (%s) ON CONFLICT DO NOTHING", (request.code,))
    else:
        cursor.execute("DELETE FROM favorites WHERE country_code = %s", (request.code,))
    connection.commit()
    return

@app.get("/favorites", response_model=list[CountryDetails])
def get_favorites():
    cursor = connection.cursor()
    query = """
    SELECT c.code, c.name, r.name AS region, c.population, TRUE AS favorite 
    FROM countries c 
    JOIN regions r ON c.region_code = r.code 
    JOIN favorites f ON c.code = f.country_code
    """
    
    cursor.execute(query)
    countries = cursor.fetchall()

    countries_list = []
    for country in countries:
        cursor.execute("SELECT l.name FROM languages l JOIN country_link_languages cl ON l.code = cl.language_code WHERE cl.country_code = %s", (country[0],))
        languages = cursor.fetchall()
        countries_list.append(CountryDetails(
            code=country[0],
            name=country[1], 
            region=country[2], 
            languages=[lang[0] for lang in languages], 
            population=country[3], 
            favorite=country[4]
        ))

    return countries_list