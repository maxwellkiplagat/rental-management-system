from db import engine
from db.base import Base
from cli.menu import menu

from models.tenant import Tenant
from models.property import Property
from models.room import Room
from models.lease import Lease
from models.payment import Payment

if __name__ == '__main__':
    Base.metadata.create_all(engine)
    while True:
        menu()