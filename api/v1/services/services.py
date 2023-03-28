from asyncpg import Connection

from api.v1.models import *
from api.v1.models.owners import Owner, UpdateOwner
from api.v1.models.pets import Pet, UpdatePet



# function to create an owners


async def create_owner(conn: Connection, owner: Owner):
    query = "INSERT INTO owners (owner_id, first_name, last_name, age, city, alive, pets_id) VALUES ($1, $2, $3, $4, $5, $6, $7) RETURNING owner_id, first_name, last_name, age, city, alive, pets_id"
    values = (owner.owner_id, owner.first_name, owner.last_name, owner.age, owner.city, owner.alive, owner.pets_id)
    async with conn.transaction():
        row = await conn.fetchrow(query, *values)
        return Owner(**row)



async def update_owner(conn: Connection, owner_id: int, owner: UpdateOwner):
    query = """
        UPDATE owners 
        SET first_name = COALESCE($1, first_name),
            last_name = COALESCE($2, last_name),
            age = COALESCE($3, age),
            city = COALESCE($4, city),
            alive = COALESCE($5, alive),
            pets_id = COALESCE($6, pets_id)
        WHERE owner_id = $7
        RETURNING owner_id, first_name, last_name, age, city, alive
    """
    values = (owner.first_name, owner.last_name, owner.age, owner.city, owner.alive, owner.pets_id, owner_id)
    row = await conn.fetchrow(query, *values)
    return Owner(**row)


# delete an owner
async def delete_owner(conn: Connection, owner_id: int):
    query = "DELETE FROM owners WHERE owner_id=$1"
    values = (int(owner_id))
    await conn.execute(query, owner_id)


# fetch owner by id 
async def get_owner_by_id(conn: Connection, owner_id: int):
    query = "SELECT * FROM owners WHERE owner_id = $1" 
    values = (int(owner_id))
    row = await conn.fetchrow(query, owner_id)
    return Owner(**row)




# function to create a pet
async def create_pet(conn: Connection, pet: Pet):
    query = """
        INSERT INTO pets (pet_id, name, type, age, colour, alive, owner_id)
        VALUES ($1, $2, $3, $4, $5, $6, $7)
        RETURNING pet_id, name, type, age, colour, alive, owner_id
    """
    values = (pet.pet_id, pet.name, pet.type, pet.age, pet.colour, pet.alive, pet.owner_id)
    async with conn.transaction():
        row = await conn.fetchrow(query, *values)
        # update owner table
        update_query = """
            UPDATE owners
            SET pets_id = COALESCE($1, pets_id)
            WHERE owner_id = $2
        """
        await conn.execute(update_query, pet.pet_id, pet.owner_id)
        return Pet(**row)


# update a pet
async def update_pet(conn: Connection, pet_id: int, pet: UpdatePet):
    query = """
        UPDATE pets 
        SET name=COALESCE($1, name),
            type=COALESCE($2, type),
            age=COALESCE($3, age),
            colour=COALESCE($4, colour),
            alive=COALESCE($5, alive),
            owner_id=COALESCE($6, owner_id)
        WHERE pet_id=$7
        RETURNING pet_id, name, type, age, colour, alive, owner_id
    """
    values = (pet.name, pet.type, pet.age, pet.colour, pet.alive, pet.owner_id, pet_id)
    row = await conn.fetchrow(query, *values)
    # update owner table
    update_query = """
            UPDATE owners
            SET pets_id = COALESCE($1, pets_id)
            WHERE owner_id = $2
        """
    await conn.execute(update_query, pet_id, pet.owner_id)
    return Pet(**row)



# delete a pet
async def delete_pet(conn: Connection, pet_id: int):
    query = "DELETE FROM pets WHERE pet_id=$1"
    values = (int(pet_id))
    await conn.execute(query, pet_id)


# fetch pet by id 
async def get_pet_by_id(conn: Connection, pet_id: int):
    query = "SELECT * FROM pets WHERE pet_id = $1" 
    values = (int(pet_id))
    row = await conn.fetchrow(query, pet_id)
    return Pet(**row)
