from sqlalchemy.schema import CreateTable
from app.models import User, Task


print(CreateTable(User.__table__))
print(CreateTable(Task.__table__))