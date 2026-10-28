name = 'anand'
years = 7

dev = {"name":name,"years":years,"skills":["PHP","MYSQL"]}
print(dev['name'])

skills = ["PHP","MySQL","LARAVEL"]
skills.append("PYTHON")

for skill in skills:
    if skill == "PHP":
        print(skill, "Is my key skill")
    else:
        print(skill)

def greet(person,greetings="Hello"):
    return f"{greetings}, {person}!"
print(greet(name))

