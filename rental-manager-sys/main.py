from db import engine
from db.base import Base
from cli.menu import menu
from models import Tenant, Property, Lease

if __name__ == '__main__':
    Base.metadata.create_all(engine)
    while True:
        menu()