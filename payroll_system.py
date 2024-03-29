from formateur import *
from agent import *
import json

class PayrollSystem:
    employees = []

    @classmethod
    def show_menu(cls):
        print("1. Afficher tous les employés")
        print("2. Ajouter un employé")
        print("3. Supprimer un employé")
        print("4. Quitter")

    @classmethod
    def display_employees(cls):
        print("\nListe des employés:")
        print("Formateurs:")
        for employee in cls.employees:
            if isinstance(employee, Formateur):
                print(employee)
        print("\nAgents:")
        for employee in cls.employees:
            if isinstance(employee, Agent):
                print(employee)

    @classmethod
    def add_employee(cls, employee):
        cls.employees.append(employee)
        print(f"{employee.Nom} a été ajouté avec succès.")

    @classmethod
    def remove_employee(cls, matricule):
        for employee in cls.employees:
            if employee.Matricule == matricule:
                cls.employees.remove(employee)
                print(f"{employee.Nom} a été supprimé avec succès.")
                return
        print("Matricule non trouvé.")

    @classmethod
    def save_employees(cls):
         with open("employees.json", "w") as file:
            data = [{"Matricule": emp.Matricule, "Nom": emp.Nom, "DateNaissance": emp.DateNaissance.strftime("%Y-%m-%d"),
                     "DateEmbauche": emp.DateEmbauche.strftime("%Y-%m-%d"), "SalaireBase": emp.SalaireBase,
                     "Type": type(emp).__name__,
                     "HeureSup": getattr(emp, "HeureSup", ""),
                     "PrimeResponsabilite": getattr(emp, "PrimeResponsabilite", "")} for emp in cls.employees]
            json.dump(data, file)

    @classmethod
    def load_employees(cls):
        try:
            with open("employees.json", "r") as file:
                data = json.load(file)
                cls.employees = []
                for emp_data in data:
                    if emp_data["Type"] == "Agent":
                        employee = Agent(emp_data["Nom"],
                                        datetime.strptime(emp_data["DateNaissance"], "%Y-%m-%d"),
                                        datetime.strptime(emp_data["DateEmbauche"], "%Y-%m-%d"),
                                        emp_data["SalaireBase"],
                                        emp_data["PrimeResponsabilite"])
                    elif emp_data["Type"] == "Formateur":
                        employee = Formateur(emp_data["Nom"],
                                            datetime.strptime(emp_data["DateNaissance"], "%Y-%m-%d"),
                                            datetime.strptime(emp_data["DateEmbauche"], "%Y-%m-%d"),
                                            emp_data["SalaireBase"],
                                            emp_data["HeureSup"])
                    else:
                        # Handle other employee types if needed
                        continue

                    cls.employees.append(employee)
        except FileNotFoundError:
            pass
if __name__ == "__main__":
    while True:
        PayrollSystem.show_menu()
        choice = input("Choisissez une option (1, 2, 3, 4): ")

        if choice == "1":
            PayrollSystem.display_employees()

        elif choice == "2":
            employee_type = input("Choisissez le type d'employé (Formateur/Agent): ")
            nom = input("Nom de l'employé: ")
            date_naissance = datetime.strptime(input("Date de naissance (YYYY-MM-DD): "), "%Y-%m-%d")
            date_embauche = datetime.now()  # Set default to current date
            salaire_base = float(input("Salaire de base: "))

            if employee_type.lower() == "formateur":
                heure_sup = int(input("Heures supplémentaires: "))
                new_employee = Formateur(nom, date_naissance, date_embauche, salaire_base, heure_sup)
            elif employee_type.lower() == "agent":
                prime_responsabilite = float(input("Prime de responsabilité: "))
                new_employee = Agent(nom, date_naissance, date_embauche, salaire_base, prime_responsabilite)
            else:
                print("Type d'employé non reconnu.")
                continue

            PayrollSystem.add_employee(new_employee)

        elif choice == "3":
            matricule = int(input("Matricule de l'employé à supprimer: "))
            PayrollSystem.remove_employee(matricule)

        elif choice == "4":
            print("Programme terminé.")
            break

        else:
            print("Option non valide. Veuillez choisir parmi les options disponibles.")
