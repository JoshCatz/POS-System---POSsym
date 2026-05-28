
class POSException(Exception):
    def __init__(self, message:str, status_code:int):
        self.message = message
        self.status_code = status_code

class TableLockedException(POSException):
    def __init__(self, table_number:int, employee_name:str, tablet_id:str):
        super().__init__(
            message=f"Table {table_number} is currently being accessed by {employee_name} on tablet {tablet_id}",
            status_code=423
        )
        self.table_number = table_number
        self.employee_name = employee_name
        self.tablet_id = tablet_id

class NotFoundException(POSException):
    def __init__(self, resource:str):
        super().__init__(
            message=f"Resource not found: {resource}",
            status_code=404
        )
        self.resource = resource

class ForbiddenException(POSException):
    def __init__(self, role:str):
        super().__init__(
            message = f"Role '{role}' does not have permission to perform this action",
            status_code=403
        )
        self.role = role

class UnauthorizedException(POSException):
    def __init__(self):
        super().__init__(
            message = "Invalid or missing credentials",
            status_code = 401
        )

class RedundantException(POSException):
    def __init__(self, redundant:str):
        super().__init__(
            message = f"Redundant Error: {redundant}",
            status_code = 422
        )
        

