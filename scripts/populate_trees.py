
from home.models import Tree

def populate_trees(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    for line in lines:
        name, scientific_name = line.strip().split(' - ')
        Tree.objects.create(name=name, scientific_name=scientific_name)

populate_trees('trees_dataset.txt')
print("Árvores populadas com sucesso!")