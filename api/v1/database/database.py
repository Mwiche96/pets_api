import asyncpg
from asyncpg import Connection

DATABASE_URL = "postgres://postgres:elementx96@localhost/App"

async def get_database_connection() -> Connection:
    connection = await asyncpg.connect(DATABASE_URL)
    await create_tables(connection) # call create_tables function
    return connection

async def create_tables(conn: Connection) -> None:
    await conn.execute(
        """
        CREATE TABLE IF NOT EXISTS owners (
            owner_id SERIAL PRIMARY KEY,
            first_name TEXT,
            last_name TEXT,
            age INTEGER,
            city TEXT,
            alive BOOLEAN,
            pets_id INTEGER
        );
        """
    )

    await conn.execute(
        """
        CREATE TABLE IF NOT EXISTS pets (
            pet_id SERIAL PRIMARY KEY,
            name TEXT,
            type TEXT,
            age INTEGER,
            colour TEXT,
            alive BOOLEAN,
            owner_id INTEGER REFERENCES owners(owner_id) ON DELETE CASCADE
        );
        """
    )
