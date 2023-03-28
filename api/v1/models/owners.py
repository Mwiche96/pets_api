from pydantic import BaseModel
from typing import Optional, List

# defining a class for owners
class Owner(BaseModel):
        owner_id: int       
        first_name: Optional[str]
        last_name: Optional[str]
        age: Optional[int] 
        city: Optional[str]
        alive: Optional[bool] = True
        pets_id: Optional[int] 



# To create an update class for the put method
class UpdateOwner(BaseModel):
        owner_id: Optional[int] 
        first_name: Optional[str]
        last_name: Optional[str]
        age: Optional[int] 
        city: Optional[str] 
        alive: Optional[bool] 
        pets_id: Optional[int]





