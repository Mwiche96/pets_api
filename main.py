from fastapi import FastAPI, HTTPException
import asyncio


from api.v1.database.database import get_database_connection, create_tables
from api.v1.models.owners import UpdateOwner, Owner
from api.v1.models.pets import Pet, UpdatePet
from  api.v1.services.services import get_owner_by_id, get_pet_by_id, create_owner, create_pet, update_pet, update_owner, delete_owner, delete_pet


app = FastAPI()

async def main():
    conn = await get_database_connection()
    await create_tables(conn)
    await conn.close()

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())



# creation end points 
@app.post("/owners")
async def create_owner_handler(owner: Owner):
    conn = await get_database_connection()
    try:
        created_owner = await create_owner(conn, owner)
    except Exception as e:
        await conn.close()
        raise HTTPException(status_code=400, detail=str(e))
    else:
        await conn.close()
        return created_owner

@app.post("/pets")
async def create_pet_handler(pet: Pet):
    conn = await get_database_connection()
    try:
        pet_create = await create_pet(conn, pet)
    except Exception as e:
        await conn.close()
        raise HTTPException(status_code=400, detail=str(e))
    else:
        await conn.close()
        return pet_create


# fetching end points
@app.get("/owners/{owner_id}")
async def get_owner_by_id_handler(owner_id: int):
    conn = await get_database_connection()
    try:
        get_owner_id = await get_owner_by_id(conn, int(owner_id))
    except Exception as e:
        await conn.close()
        raise HTTPException(status_code=404, detail="Owner not found")
    else:
        await conn.close()
        return get_owner_id

@app.get("/pets/{pet_id}")
async def get_pet_by_id_handler(pet_id: int):
    conn = await get_database_connection()
    try:
        pet_by_id = await get_pet_by_id(conn, int(pet_id))
    except Exception as e:
        await conn.close()
        raise HTTPException(status_code=404, detail="Pet not found")
    else:
        await conn.close()
        return pet_by_id


# updating end points
@app.put("/owners/{owner_id}")
async def update_owner_handler(owner_id: int, owner: UpdateOwner):
    conn = await get_database_connection()
    try:
        owner_update = await update_owner(conn, int(owner_id), owner)
    except Exception as e:
        await conn.close()
        raise HTTPException(status_code=400, detail=str(e))
    else:
        await conn.close()
        return owner_update

@app.put("/pets/{pet_id}")
async def update_pet_handler(pet_id: int, pet: UpdatePet):
    conn = await get_database_connection()
    try:
        pet_update = await update_pet(conn, int(pet_id), pet)
    except Exception as e:
        await conn.close()
        raise HTTPException(status_code=400, detail=str(e))
    else:
        await conn.close()
        return pet_update


# deleting end points
@app.delete("/owners/{owner_id}")
async def delete_owner_handler(owner_id: int):
    conn = await get_database_connection()
    try:
        owner_delete = await delete_owner(conn, int(owner_id))
    except Exception as e:
        await conn.close()
        raise HTTPException(status_code=404, detail="Owner not found")
    else:
        if not owner_delete:
            await conn.close()
            raise HTTPException(status_code=404, detail="Owner not found")
        await conn.close()
        return owner_delete


@app.delete("/pets/{pet_id}")
async def delete_pet_handler(pet_id: int):
    conn = await get_database_connection()
    try:
        pet_delete = await delete_pet(conn, int(pet_id))
    except Exception as e:
        await conn.close()
        raise HTTPException(status_code=404, detail="Pet not found")
    else:
        if not pet_delete:
            await conn.close()
            raise HTTPException(status_code=404, detail="Pet not found")
        await conn.close()
        return pet_delete

