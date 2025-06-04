import sys
from db import session
from models.tenant import Tenant
from models.property import Property
from models.room import Room
from models.lease import Lease
from models.payment import Payment

def create_tenant():
    name = input("Enter tenant name: ")
    email = input("Enter tenant email: ")
    tenant = Tenant(name=name, email=email)
    session.add(tenant)
    session.commit()
    print(f"Tenant {name} added successfully.")

def create_property():
    address = input("Enter property address: ")
    rent = float(input("Enter monthly rent: "))
    prop = Property(address=address, rent=rent)
    session.add(prop)
    session.commit()
    print(f"Property at {address} added successfully.")

def create_room():
    properties = session.query(Property).all()
    if not properties:
        print("No properties found. Create a property first.")
        return

    print("Select property to add room:")
    for p in properties:
        print(f"{p.id}: {p.address}")
    property_id = int(input("Enter property ID: "))
    prop = session.query(Property).get(property_id)
    if not prop:
        print("Invalid property ID.")
        return

    number = input("Enter room number (e.g., 101): ")
    room = Room(room_number=number, property_id=property_id)
    session.add(room)
    session.commit()
    print(f"Room {number} added to property {prop.address}.")


def create_lease():
    tenants = session.query(Tenant).all()
    rooms = session.query(Room).filter(Room.is_occupied == False).all()
    if not tenants:
        print("No tenants found. Create a tenant first.")
        return
    if not rooms:
        print("No vacant rooms available. Create rooms or free some up first.")
        return

    print("Select tenant:")
    for t in tenants:
        print(f"{t.id}: {t.name}")
    tenant_id = int(input("Enter tenant ID: "))
    tenant = session.query(Tenant).get(tenant_id)
    if not tenant:
        print("Invalid tenant ID.")
        return

    print("Select vacant room:")
    for r in rooms:
        print(f"{r.id}: Room {r.room_number} at Property {r.property.address}")
    room_id = int(input("Enter room ID: "))
    room = session.query(Room).get(room_id)
    if not room or  room.is_occupied:
        print("Invalid or occupied room ID.")
        return

    duration = int(input("Enter lease duration (months): "))

    lease = Lease(tenant_id=tenant_id, room_id=room_id, duration_months=duration)
    session.add(lease)
    
    room.is_occupied = True
    session.add(lease)
    session.commit()
    print(f"Lease created for tenant {tenant.name} in room {room.room_number}.")

    

def view_data():
    tenants = session.query(Tenant).all()
    properties = session.query(Property).all()
    leases = session.query(Lease).all()
    rooms = session.query(Room).all()


    print("\n--- Tenants ---")
    for t in tenants:
        print(t)
    print("\n--- Properties ---")
    for p in properties:
        print(p)
    print("\n--- Leases ---")
    for l in leases:
        print(l)
    print("\n--- Rooms ---")
    for r in rooms:
        status = "Vacant" if not r.is_occupied else "Occupied"
        print(f"Room(id={r.id}, number={r.room_number}, property={r.property.address}, status={status})")

    vacant_rooms = session.query(Room).filter(Room.is_occupied == False).all()
    print("\n--- Vacant Rooms ---")
    if vacant_rooms:
        for vr in vacant_rooms:
            print(f"Room {vr.number} at Property {vr.property.address}")
    else:
        print("No vacant rooms available.")

def delete_tenant():
        try:
            tenant_id = int(input("Enter Tenant ID to delete: "))
            tenant = session.query(Tenant).get(tenant_id)
            if tenant:
                # Before deleting tenant, free up rooms and delete leases
                leases = session.query(Lease).filter(Lease.tenant_id == tenant_id).all()
                for lease in leases:
                    room = session.query(Room).get(lease.room_id)
                    if room:
                        room.is_vacant = True
                    session.delete(lease)
                session.delete(tenant)
                session.commit()
                print(f"Tenant with ID {tenant_id} and related leases deleted.")
            else:
                print("Tenant not found.")
        except Exception as e:
            print(f"Error: {e}")
def record_payment():
        leases = session.query(Lease).all()
        if not leases:
            print("No leases found. Create a lease first.")
            return

        print("Select lease to record payment:")
        for lease in leases:
            print(f"{lease.id}: Tenant {lease.tenant.name}, Room {lease.room.number}, Property {lease.property.address}")
        lease_id = int(input("Enter lease ID: "))
        lease = session.query(Lease).get(lease_id)
        if not lease:
            print("Invalid lease ID.")
            return

        amount = float(input("Enter payment amount: "))
        payment = Payment(lease_id=lease_id, amount=amount)
        session.add(payment)
        session.commit()
        print(f"Payment of {amount} recorded for lease ID {lease_id}.")
def view_payments():
        payments = session.query(Payment).all()
        print("\n--- Payments ---")
        if not payments:
            print("No payments recorded.")
        for p in payments:
            print(f"Payment ID: {p.id}, Lease ID: {p.lease_id}, Tenant: {p.lease.tenant.name}, Amount: {p.amount}, Date: {p.payment_date}")


def menu():
    print("""
            _______ R.M SYSTEM _______
                    
                1. Create Tenant
                2. Create Property
                3. Create Room
                4. Create Lease
                5. View All Data & Payments
                6. Record Payment
                7. Delete Tenant
                8. Exit
            ___________________________   
                """)

    choice = input("Choose an option: ")
    if choice == '1':
        create_tenant()
    elif choice == '2':
        create_property()
    elif choice == '3':
        create_room()
    elif choice == '4':
        create_lease()
    elif choice == '5':
        view_data()
        view_payments()
    elif choice == '6':
        record_payment()
    elif choice == '7':
        delete_tenant()
    elif choice == '8':      
        print("EXITED.") 
        sys.exit()    
    else:
        print("Invalid choice.")
