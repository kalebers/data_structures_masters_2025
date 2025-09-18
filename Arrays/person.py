import random
import string

# Garantir replicabilidade
random.seed(42)

# Classe que define dado sendo armazenado
class Person:
    def __init__(self, data):
        self.matricula = data
        self.nome = None
        self.salario = None
        self.setor = None
        
    def __repr__(self):
        return (f"{self.matricula}")

# Função para gerar dados aleatórios
def generate_random_persons(n):
    matriculas_em_uso = set()
    people = []

    for _ in range(n):
        matricula = unique_matricula(matriculas_em_uso)
        
        person = Person(matricula)
        person.nome = ''.join(random.choices(string.ascii_uppercase, k=7))
        person.salario = round(random.uniform(1500, 20000), 2)
        person.setor = random.randint(1, 100)
        people.append(person)

    return people

# Função para gerar número de matrícula único
def unique_matricula(matriculas_em_uso):
    matricula = ''.join(random.choices(string.digits, k=9))
    while matricula in matriculas_em_uso:
        matricula = ''.join(random.choices(string.digits, k=9))
    matriculas_em_uso.add(matricula)

    return matricula