import mysql.connector

class Contact:
    def __init__(self, nom, prenom, email, telephone):
        self.nom = nom
        self.prenom = prenom
        self.email = email
        self.telephone = telephone

    def __str__(self):
        return f"Nom: {self.nom}, Prénom: {self.prenom}, Email: {self.email}, Téléphone: {self.telephone}"


class GestionnaireContact:
    def __init__(self, host="localhost", user="root", password="", database="gestion_contacts"):
        self.conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        self.cursor = self.conn.cursor()
        self._creer_table()

    def _creer_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS contacts (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nom VARCHAR(255) NOT NULL,
                prenom VARCHAR(255) NOT NULL,
                email VARCHAR(255) NOT NULL,
                telephone VARCHAR(20) NOT NULL
            )
        ''')
        self.conn.commit()

    def ajouter_contact(self, contact):
        self.cursor.execute(
            "INSERT INTO contacts (nom, prenom, email, telephone) VALUES (%s, %s, %s, %s)",
            (contact.nom, contact.prenom, contact.email, contact.telephone)
        )
        self.conn.commit()

    def afficher_contacts(self):
        self.cursor.execute("SELECT nom, prenom, email, telephone FROM contacts")
        contacts = self.cursor.fetchall()
        if not contacts:
            print("Aucun contact à afficher.")
        else:
            for c in contacts:
                print(Contact(*c))

    def rechercher_contact(self, nom):
        self.cursor.execute("SELECT nom, prenom, email, telephone FROM contacts WHERE nom = %s", (nom,))
        contacts = self.cursor.fetchall()
        return [Contact(*c) for c in contacts]

    def modifier_contact(self, nom, nouveau_contact):
        self.cursor.execute(
            "UPDATE contacts SET prenom = %s, email = %s, telephone = %s WHERE nom = %s",
            (nouveau_contact.prenom, nouveau_contact.email, nouveau_contact.telephone, nom)
        )
        self.conn.commit()
        return self.cursor.rowcount > 0

    def supprimer_contact(self, nom):
        self.cursor.execute("DELETE FROM contacts WHERE nom = %s", (nom,))
        self.conn.commit()
        return self.cursor.rowcount > 0

    def __del__(self):
        self.conn.close()


class Main:
    @staticmethod
    def main():
        gestionnaire = GestionnaireContact()

        while True:
            print("\nMenu :")
            print("1. Ajouter un contact")
            print("2. Afficher tous les contacts")
            print("3. Rechercher un contact")
        
            print("4. Modifier un contact")
            print("5. Supprimer un contact")
            print("6. Quitter")

            choix = input("Choisissez une option : ")

            if choix == "1":
                nom = input("Nom : ")
                prenom = input("Prénom : ")
                email = input("Email : ")
                telephone = input("Téléphone : ")
                contact = Contact(nom, prenom, email, telephone)
                gestionnaire.ajouter_contact(contact)
                print("Contact ajouté avec succès.")

            elif choix == "2":
                gestionnaire.afficher_contacts()

            elif choix == "3":
                nom = input("Entrez le nom à rechercher : ")
                resultat = gestionnaire.rechercher_contact(nom)
                if resultat:
                    for contact in resultat:
                        print(contact)
                else:
                    print("Aucun contact trouvé avec ce nom.")

            elif choix == "4":
                nom = input("Entrez le nom du contact à modifier : ")
                prenom = input("Nouveau prénom : ")
                email = input("Nouvel email : ")
                telephone = input("Nouveau téléphone : ")
                nouveau_contact = Contact(nom, prenom, email, telephone)
                if gestionnaire.modifier_contact(nom, nouveau_contact):
                    print("Contact modifié avec succès.")
                else:
                    print("Aucun contact trouvé avec ce nom.")

            elif choix == "5":
                nom = input("Entrez le nom du contact à supprimer : ")
                if gestionnaire.supprimer_contact(nom):
                    print("Contact supprimé avec succès.")
                else:
                    print("Aucun contact trouvé avec ce nom.")

            elif choix == "6":
                print("Au revoir !")
                break

            else:
                print("Option invalide, veuillez réessayer.")


if __name__ == "__main__":
    Main.main()
