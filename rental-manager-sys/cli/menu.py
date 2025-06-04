import sys
from db import session
from models.tenant import Tenant
from models.property import Property
from models.room import Room
from models.lease import Lease
from models.payment import Payment
from tabulate import tabulate

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
    if tenants:
        data = [[t.id, t.name, t.email] for t in tenants]
        print(tabulate(data, headers=["ID", "Name", "Email"], tablefmt="fancy_grid"))
    else:
        print("No tenants found.")

    print("\n--- Properties ---")
    if properties:
        data = [[p.id, p.address, p.rent] for p in properties]
        print(tabulate(data, headers=["ID", "Address", "Rent"], tablefmt="fancy_grid"))
    else:
        print("No properties found.")

    print("\n--- Leases ---")
    if leases:
        data = [[l.id, l.tenant.name, l.room.room_number, l.room.property.address, l.duration_months] for l in leases]
        print(tabulate(data, headers=["ID", "Tenant", "Room", "Property", "Duration (months)"], tablefmt="fancy_grid"))
    else:
        print("No leases found.")

    print("\n--- Rooms ---")
    if rooms:
        data = [[r.id, r.room_number, r.property.address, "Occupied" if r.is_occupied else "Vacant"] for r in rooms]
        print(tabulate(data, headers=["ID", "Room No.", "Property", "Status"], tablefmt="fancy_grid"))
    else:
        print("No rooms found.")
    vacant_rooms = session.query(Room).filter(Room.is_occupied == False).all()
    print("\n--- Vacant Rooms ---")
    if vacant_rooms:
        data = [[vr.room_number, vr.property.address] for vr in vacant_rooms]
        print(tabulate(data, headers=["Room No.", "Property"], tablefmt="fancy_grid"))
    else:
        print("No vacant rooms.")

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
            print(f"{lease.id}: Tenant {lease.tenant.name}, Room {lease.room.room_number}, Property {lease.room.property.address}")
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
        
    if payments:
        data = []
        for p in payments:
            tenant_name = getattr(getattr(p.lease, 'tenant', None), 'name', 'Unknown')
            data.append([p.id, p.lease_id, tenant_name, p.amount, p.payment_date.strftime('%Y-%m-%d')])
        table = tabulate(data, headers=["Payment ID", "Lease ID", "Tenant", "Amount", "Date"], tablefmt="fancy_grid")
        return table        
    else:
        return "No payments recorded."
print("\n--- Payments ---")
print(view_payments(session))


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
