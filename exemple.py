import tkinter as tk
from tkinter import messagebox, simpledialog


# --- Gestion des contacts ---
class Contact:
    def __init__(self, nom, prenom, email, telephone):
        self.nom = nom
        self.prenom = prenom
        self.email = email
        self.telephone = telephone

    def __str__(self):
        return f"Nom: {self.nom}, Prénom: {self.prenom}, Email: {self.email}, Téléphone: {self.telephone}"

class GestionnaireContact:
    def __init__(self):
        self.contacts = []
        self.charger_contacts()

    def ajouter_contact(self, contact):
        self.contacts.append(contact)
        self.sauvegarder_contacts()

    def afficher_contacts(self):
        return "\n".join([str(contact) for contact in self.contacts])

    def rechercher_contact(self, nom):
        resultat = [contact for contact in self.contacts if contact.nom.lower() == nom.lower()]
        return resultat

    def modifier_contact(self, nom, nouveau_contact):
        for idx, contact in enumerate(self.contacts):
            if contact.nom.lower() == nom.lower():
                self.contacts[idx] = nouveau_contact
                self.sauvegarder_contacts()
                return True
        return False

    def supprimer_contact(self, nom):
        for contact in self.contacts:
            if contact.nom.lower() == nom.lower():
                self.contacts.remove(contact)
                self.sauvegarder_contacts()
                return True
        return False

    def sauvegarder_contacts(self):
        with open('contacts.txt', 'w') as file:
            for contact in self.contacts:
                file.write(f"{contact.nom},{contact.prenom},{contact.email},{contact.telephone}\n")

    def charger_contacts(self):
        try:
            with open('contacts.txt', 'r') as file:
                for line in file:
                    nom, prenom, email, telephone = line.strip().split(',')
                    contact = Contact(nom, prenom, email, telephone)
                    self.contacts.append(contact)
        except FileNotFoundError:
            pass


# --- Interface graphique ---
class MainWindow:
    def __init__(self, root, gestionnaire):
        self.root = root
        self.gestionnaire = gestionnaire
        self.root.title("Gestionnaire de Contacts")
        self.root.geometry("600x500")

        # --- Ajouter un contact ---
        self.add_frame = tk.LabelFrame(root, text="Ajouter un contact", padx=20, pady=20)
        self.add_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        # Champs pour ajouter un contact
        self.nom_label = tk.Label(self.add_frame, text="Nom:")
        self.nom_label.grid(row=0, column=0, pady=5, padx=10)
        self.nom_entry = tk.Entry(self.add_frame)
        self.nom_entry.grid(row=0, column=1, pady=5, padx=10)

        self.prenom_label = tk.Label(self.add_frame, text="Prénom:")
        self.prenom_label.grid(row=1, column=0, pady=5, padx=10)
        self.prenom_entry = tk.Entry(self.add_frame)
        self.prenom_entry.grid(row=1, column=1, pady=5, padx=10)

        self.email_label = tk.Label(self.add_frame, text="Email:")
        self.email_label.grid(row=2, column=0, pady=5, padx=10)
        self.email_entry = tk.Entry(self.add_frame)
        self.email_entry.grid(row=2, column=1, pady=5, padx=10)

        self.telephone_label = tk.Label(self.add_frame, text="Téléphone:")
        self.telephone_label.grid(row=3, column=0, pady=5, padx=10)
        self.telephone_entry = tk.Entry(self.add_frame)
        self.telephone_entry.grid(row=3, column=1, pady=5, padx=10)

        # Bouton pour ajouter un contact
        self.add_button = tk.Button(self.add_frame, text="Ajouter un contact", command=self.ajouter_contact)
        self.add_button.grid(row=4, column=0, columnspan=2, pady=10)

        # --- Affichage des contacts ---
        self.view_frame = tk.LabelFrame(root, text="Contacts enregistrés", padx=20, pady=20)
        self.view_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        # Liste des contacts
        self.contact_listbox = tk.Listbox(self.view_frame, height=10, width=50)
        self.contact_listbox.grid(row=0, column=0, columnspan=2, pady=10)

        # --- Actions (rechercher, modifier, supprimer) ---
        self.action_frame = tk.LabelFrame(root, text="Actions", padx=20, pady=20)
        self.action_frame.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")

        # Boutons d'action
        self.view_button = tk.Button(self.action_frame, text="Afficher les contacts", command=self.afficher_contacts)
        self.view_button.grid(row=0, column=0, pady=5)

        self.search_button = tk.Button(self.action_frame, text="Rechercher un contact", command=self.rechercher_contact)
        self.search_button.grid(row=0, column=1, pady=5)

        self.modify_button = tk.Button(self.action_frame, text="Modifier un contact", command=self.modifier_contact)
        self.modify_button.grid(row=1, column=0, pady=5)

        self.delete_button = tk.Button(self.action_frame, text="Supprimer un contact", command=self.supprimer_contact)
        self.delete_button.grid(row=1, column=1, pady=5)

        # Bouton Quitter
        self.quit_button = tk.Button(root, text="Quitter", command=root.quit)
        self.quit_button.grid(row=3, column=0, columnspan=2, pady=10)

    def ajouter_contact(self):
        nom = self.nom_entry.get()
        prenom = self.prenom_entry.get()
        email = self.email_entry.get()
        telephone = self.telephone_entry.get()

        if nom and prenom and email and telephone:
            contact = Contact(nom, prenom, email, telephone)
            self.gestionnaire.ajouter_contact(contact)
            messagebox.showinfo("Succès", "Contact ajouté avec succès.")
            self.afficher_contacts()

            # Vider les champs de saisie après ajout
            self.nom_entry.delete(0, tk.END)
            self.prenom_entry.delete(0, tk.END)
            self.email_entry.delete(0, tk.END)
            self.telephone_entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Erreur", "Tous les champs sont requis.")

    def afficher_contacts(self):
        self.contact_listbox.delete(0, tk.END)
        contacts = self.gestionnaire.afficher_contacts()
        if contacts:
            self.contact_listbox.insert(tk.END, contacts)
        else:
            messagebox.showinfo("Info", "Aucun contact à afficher.")

    def rechercher_contact(self):
        nom = simpledialog.askstring("Recherche", "Entrez le nom à rechercher:")
        if nom:
            resultat = self.gestionnaire.rechercher_contact(nom)
            if resultat:
                self.contact_listbox.delete(0, tk.END)
                for contact in resultat:
                    self.contact_listbox.insert(tk.END, contact)
            else:
                messagebox.showinfo("Info", "Aucun contact trouvé avec ce nom.")
        else:
            messagebox.showwarning("Erreur", "Veuillez entrer un nom.")

    def modifier_contact(self):
        nom = simpledialog.askstring("Modifier", "Entrez le nom du contact à modifier:")
        if nom:
            contact = simpledialog.askstring("Nouveau Contact", "Entrez les nouvelles informations (Nom, Prénom, Email, Téléphone) séparées par des virgules:")
            if contact:
                try:
                    nom, prenom, email, telephone = contact.split(',')
                    nouveau_contact = Contact(nom.strip(), prenom.strip(), email.strip(), telephone.strip())
                    if self.gestionnaire.modifier_contact(nom, nouveau_contact):
                        messagebox.showinfo("Succès", "Contact modifié avec succès.")
                        self.afficher_contacts()
                    else:
                        messagebox.showinfo("Info", "Aucun contact trouvé avec ce nom.")
                except ValueError:
                    messagebox.showwarning("Erreur", "Le format des informations est incorrect.")
        else:
            messagebox.showwarning("Erreur", "Veuillez entrer un nom.")

    def supprimer_contact(self):
        nom = simpledialog.askstring("Supprimer", "Entrez le nom du contact à supprimer:")
        if nom:
            if self.gestionnaire.supprimer_contact(nom):
                messagebox.showinfo("Succès", "Contact supprimé avec succès.")
                self.afficher_contacts()
            else:
                messagebox.showinfo("Info", "Aucun contact trouvé avec ce nom.")
        else:
            messagebox.showwarning("Erreur", "Veuillez entrer un nom.")


# --- Programme principal ---
def main():
    gestionnaire = GestionnaireContact()

    # Création de la fenêtre principale Tkinter
    root = tk.Tk()

    # Initialisation de l'interface graphique
    window = MainWindow(root, gestionnaire)

    # Lancement de l'interface
    root.mainloop()

if __name__ == "__main__":
    main()
