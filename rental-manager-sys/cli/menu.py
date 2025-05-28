from db import session
from models import Tenant, Property, Lease

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

def create_lease():
    tenant_id = int(input("Enter tenant ID: "))
    property_id = int(input("Enter property ID: "))
    duration = int(input("Enter duration (months): "))
    lease = Lease(tenant_id=tenant_id, property_id=property_id, duration_months=duration)
    session.add(lease)
    session.commit()
    print("Lease created successfully.")

def view_data():
    tenants = session.query(Tenant).all()
    properties = session.query(Property).all()
    leases = session.query(Lease).all()

    print("\n--- Tenants ---")
    for t in tenants:
        print(t)
    print("\n--- Properties ---")
    for p in properties:
        print(p)
    print("\n--- Leases ---")
    for l in leases:
        print(l)

def menu():
    print("""
            _______ R.M SYSTEM _______
                    
                1. Create Tenant
                2. Create Property
                3. Create Lease
                4. View All Data
                5. Exit
            ___________________________   
                """)

    choice = input("Choose an option: ")
    if choice == '1':
        create_tenant()
    elif choice == '2':
        create_property()
    elif choice == '3':
        create_lease()
    elif choice == '4':
        view_data()
    elif choice == '5':
        print("EXITED.")
        
    else:
        print("Invalid choice.")
