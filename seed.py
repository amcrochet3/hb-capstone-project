"""Script to seed database."""

import os
import json

import crud
import model
import server

os.system("dropdb local_structure")
os.system("createdb local_structure")

model.connect_to_db(server.app)
model.db.create_all()

with open("data/arch_structures.json") as f:
    arch_structure_data = json.loads(f.read())

arch_structures_in_db = []
for arch_structure in arch_structure_data:
    structure_name, structure_type, arch_style, year_built, arch_firm, architect_name, street_address, city, state_or_province, postal_code, country, img_url = (
        arch_structure["structure_name"],
        arch_structure["structure_type"],
        arch_structure["arch_style"],
        arch_structure["year_built"],
        arch_structure["arch_firm"],
        arch_structure["architect_name"],
        arch_structure["street_address"],
        arch_structure["city"],
        arch_structure["state_or_province"],
        arch_structure["postal_code"],
        arch_structure["country"],
        arch_structure["img_url"]
    )

    db_arch_structure = crud.create_arch_strucutre(structure_name, structure_type, arch_style, year_built, arch_firm, architect_name, street_address, city, state_or_province, postal_code, country, img_url)
    arch_structures_in_db.append(db_arch_structure)

model.db.session.add_all(arch_structures_in_db)
model.db.session.commit()


for n in range(10):
    fname = f"John{n}"
    lname = f"Doe{n}"
    email = f"user{n}@test.com"
    password = "test"

    user = crud.create_user(fname, lname, email, password)

    model.db.session.add(user)
    model.db.session.commit()