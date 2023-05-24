"""Script to seed database."""

import os
import json
import requests

import crud
import model
import server

os.system("dropdb local_structure")
os.system("createdb local_structure")

model.connect_to_db(server.app)
model.db.create_all()

for n in range(10):
    fname = f"John{n}"
    lname = f"Doe{n}"
    email = f"user{n}@test.com"
    password = "test"

    user = crud.create_user(fname, lname, email, password)

    unique_dashboard_url = f"/dashboard/{user.user_id}"

    model.db.session.add(user)
    model.db.session.commit()

with open("data/arch_structures.json") as f:
    arch_structure_data = json.loads(f.read())

arch_structures_in_db = []

for arch_structure in arch_structure_data:

    address = (arch_structure['street_address'] + " " + arch_structure['city'])

    if arch_structure['state_or_province'] is not None:
        address = address + " " + arch_structure['state_or_province']
    if arch_structure['postal_code'] is not None:
        address = address + " " + arch_structure['postal_code']

    address = address + " " + arch_structure['country']

    address = address.replace(" ", "%20")
    
    url = f"https://maps.googleapis.com/maps/api/geocode/json?address={address}&key=<YOUR_API_KEY>"

    response = requests.get(url)
    results = response.json()

    if results['status'] == 'OK':
        arch_structure['latitude'] = results['results'][0]['geometry']['location']['lat']
        arch_structure['longitude'] = results['results'][0]['geometry']['location']['lng']

    structure_name, structure_type, arch_style, year_built, arch_firm, architect_name, street_address, city, state_or_province, postal_code, country, arch_img_file_path, lat, lng = (
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
        arch_structure["arch_img_file_path"],
        arch_structure["lat"],
        arch_structure["lng"]
    )

    user_id = 1

    db_arch_structure = crud.create_arch_structure(user_id, structure_name, structure_type, arch_style, year_built, arch_firm, architect_name, street_address, city, state_or_province, postal_code, country, arch_img_file_path, lat, lng)
    arch_structures_in_db.append(db_arch_structure)


with open("data/objectives.json") as f:
    objective_data = json.loads(f.read())

    objectives_in_db = []

    for objective in objective_data:
        objective_id, objective_description = (
            objective["objective_id"],
            objective["objective_description"],
        )

        db_objective = crud.create_objective(objective_id, objective_description)
        objectives_in_db.append(db_objective)

model.db.session.add_all(arch_structures_in_db)
model.db.session.add_all(objectives_in_db)
model.db.session.commit()