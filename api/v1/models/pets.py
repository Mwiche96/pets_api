from pydantic import BaseModel
from typing import Optional

# defining a class for pet
class Pet(BaseModel):
     pet_id: int 
     name: Optional[str]
     type: Optional[str]
     age: Optional[int]
     colour: Optional[str]
     alive: Optional[bool] = True
     owner_id: Optional[int]


# Defining an update class for put parameter
class UpdatePet(BaseModel):
     pet_id: Optional[int] 
     name: Optional[str] 
     type: Optional[str] 
     age: Optional[int] 
     colour: Optional[str] 
     alive: Optional[bool] 
     owner_id: Optional[int] 