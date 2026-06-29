from pydantic import BaseModel

class RoleResponse(BaseModel):
    id: int
    name: str
    description: str | None = None

    model_config = {"from_attributes": True}

class AssignRoleRequest(BaseModel):
    role_id: int