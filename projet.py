"""
Projet de Mame Diarra Beye et Oumy LO
"""
from datetime import datetime


class Tache:
    def __init__(
        self,
        nom,
        description,
        date_debut,
        date_fin,
        responsable,
        statut,
        dependances=None,
    ):
        self.nom = nom
        self.description = description
        self.date_debut = datetime.strptime(date_debut, "%d/%m/%Y")
        self.date_fin = datetime.strptime(date_fin, "%d/%m/%Y")
        self.responsable = responsable
        self.statut = statut
        self.dependances = dependances or []


class Membre:
    def __init__(self, nom, role):
        self.nom = nom
        self.role = role


class Equipe:
    def __init__(self):
        self.membres = []

    def ajouter_membre(self, membre):
        self.membres.append(membre)


class Jalon:
    def __init__(self, nom, date):
        self.nom = nom
        self.date = datetime.strptime(date, "%d/%m/%Y")


class Risque:
    def __init__(self, description, probabilite, impact):
        self.description = description
        self.probabilite = float(probabilite)
        self.impact = int(impact)


class Changement:
    def __init__(self, description, version, date):
        self.description = description
        self.version = version
        self.date = datetime.strptime(date, "%d/%m/%Y")


class Projet:
    def __init__(self, nom, description, date_debut, date_fin, budget):
        self.nom = nom
        self.description = description
        self.date_debut = datetime.strptime(date_debut, "%d/%m/%Y")
        self.date_fin = datetime.strptime(date_fin, "%d/%m/%Y")
        self.budget = budget
        self.taches = []
        self.equipe = Equipe()
        self.risques = []
        self.jalons = []
        self.versions = []
        self.notification_context = None

    def ajouter_tache(
        self, nom, description, date_debut, date_fin, responsable, statut
    ):
        try:
            date_debut = datetime.strptime(date_debut, "%d/%m/%Y")
            date_fin = datetime.strptime(date_fin, "%d/%m/%Y")
        except ValueError:
            print("Format de date invalide. " "Veuillez utiliser le format jj/mm/aaaa.")
            return

        if date_debut > date_fin:
            print("La date de début ne peut pas être après la date de fin.")
            return

        tache = Tache(
            nom,
            description,
            date_debut.strftime("%d/%m/%Y"),
            date_fin.strftime("%d/%m/%Y"),
            responsable,
            statut,
        )
        self.taches.append(tache)
        self.notifier(f"Nouvelle tâche ajoutée: {tache.nom}")
        self.generer_rapport()

    def ajouter_membre_equipe(self, nom, role):
        membre = Membre(nom, role)
        self.equipe.ajouter_membre(membre)
        self.notifier(f"{membre.nom} a été ajouté à l'équipe")
        self.generer_rapport()

    def ajouter_risque(self, description, probabilite, impact):
        try:
            probabilite = float(probabilite)
            impact = int(impact)
            if not (0 <= probabilite <= 1 and 1 <= impact <= 10):
                raise ValueError
        except ValueError:
            print("Probabilité ou impact invalide.")
            return

        risque = Risque(description, probabilite, impact)
        self.risques.append(risque)
        self.notifier(f"Nouveau risque ajouté: {risque.description}")
        self.generer_rapport()

    def ajouter_jalon(self, nom, date):
        try:
            date = datetime.strptime(date, "%d/%m/%Y")
        except ValueError:
            print("Format de date invalide. " "Veuillez utiliser le format jj/mm/aaaa.")
            return

        jalon = Jalon(nom, date.strftime("%d/%m/%Y"))
        self.jalons.append(jalon)
        self.notifier(f"Nouveau jalon ajouté: {jalon.nom}")
        self.generer_rapport()

    def enregistrer_changement(self, description, version, date):
        try:
            date = datetime.strptime(date, "%d/%m/%Y")
        except ValueError:
            print("Format de date invalide. " "Veuillez utiliser le format jj/mm/aaaa.")
            return

        changement = Changement(description, version, date.strftime("%d/%m/%Y"))
        self.versions.append(changement)
        self.notifier(
            f"Changement enregistré: {changement.description} "
            f"(version {changement.version})"
        )
        self.generer_rapport()

    def notifier(self, message):
        if self.notification_context:
            for membre in self.equipe.membres:
                self.notification_context.envoyer(membre.nom, message)

    def definir_notification_context(self, context):
        self.notification_context = context

    def calculer_chemin_critique(self):
        chemins = []

        def parcourir(tache, chemin):
            chemin.append(tache)
            if not tache.dependances:
                chemins.append(chemin[:])
            else:
                for dependance in tache.dependances:
                    parcourir(dependance, chemin)
            chemin.pop()

        for tache in self.taches:
            if not any(tache in t.dependances for t in self.taches):
                parcourir(tache, [])

        chemin_critique = max(
            chemins,
            key=lambda ch: sum((t.date_fin - t.date_debut).days for t in ch),
            default=[],
        )
        return chemin_critique

    def generer_rapport(self):
        rapport = f"Rapport d'activités du Projet '{self.nom}':\n"
        rapport += f"Description: {self.description}\n"
        rapport += (
            f"Dates: "
            f"{self.date_debut.strftime('%d/%m/%Y')} "
            f"à {self.date_fin.strftime('%d/%m/%Y')}\n"
        )
        rapport += f"Budget: {self.budget}\n"
        rapport += "Équipe:\n"
        for membre in self.equipe.membres:
            rapport += f"- {membre.nom} ({membre.role})\n"
        rapport += "Tâches:\n"
        for tache in self.taches:
            rapport += (
                f"- {tache.nom} ({tache.date_debut.strftime('%d/%m/%Y')} "
                f"à {tache.date_fin.strftime('%d/%m/%Y')}), Responsable: "
                f"{tache.responsable}, Statut: {tache.statut}\n"
            )
        rapport += "Jalons:\n"
        for jalon in self.jalons:
            rapport += f"- {jalon.nom} ({jalon.date.strftime('%d/%m/%Y')})\n"
        rapport += "Risques:\n"
        for risque in self.risques:
            rapport += (
                f"- {risque.description} (Probabilité: "
                f"{risque.probabilite}, Impact: {risque.impact})\n"
            )
        rapport += "Chemin Critique:\n"
        chemin_critique = self.calculer_chemin_critique()
        for tache in chemin_critique:
            rapport += (
                f"- {tache.nom} "
                f"({tache.date_debut.strftime('%d/%m/%Y')} "
                f"à {tache.date_fin.strftime('%d/%m/%Y')})\n"
            )
        print(rapport)
        return rapport


class NotificationStrategy:
    def envoyer(self, destinataire, message):
        raise NotImplementedError


class EmailNotificationStrategy(NotificationStrategy):
    def envoyer(self, destinataire, message):
        print(f"Notification envoyée à {destinataire} par email: {message}")


class NotificationContext:
    def __init__(self, strategy):
        self.strategy = strategy

    def envoyer(self, destinataire, message):
        self.strategy.envoyer(destinataire, message)


if __name__ == "__main__":
    projet = Projet(
        "Linguere Service", "Agence de recrutement", "01/11/2023", "03/06/2024", 3000000
    )

    # Configuration du contexte de notification
    notification_strategy = EmailNotificationStrategy()
    notification_context = NotificationContext(notification_strategy)
    projet.definir_notification_context(notification_context)

    while True:
        print("\nMENU:")
        print("1. Ajouter une tâche")
        print("2. Ajouter un membre de l'équipe")
        print("3. Ajouter un risque")
        print("4. Ajouter un jalon")
        print("5. Enregistrer un changement")
        print("6. Générer un rapport")
        print("7. Quitter")
        choix = input("Entrez votre choix: ")

        if choix == "1":
            nom = input("Nom de la tâche: ")
            description = input("Description de la tâche: ")
            date_debut = input("Date de début de la tâche (jj/mm/aaaa): ")
            date_fin = input("Date de fin de la tâche (jj/mm/aaaa): ")
            responsable = input("Responsable de la tâche: ")
            statut = input("Statut de la tâche: ")
            projet.ajouter_tache(
                nom, description, date_debut, date_fin, responsable, statut
            )
        elif choix == "2":
            nom = input("Nom du membre: ")
            role = input("Rôle du membre: ")
            projet.ajouter_membre_equipe(nom, role)
        elif choix == "3":
            description = input("Description du risque: ")
            probabilite = input("Probabilité du risque (0-1): ")
            impact = input("Impact du risque (1-10): ")
            projet.ajouter_risque(description, probabilite, impact)
        elif choix == "4":
            nom = input("Nom du jalon: ")
            date = input("Date du jalon (jj/mm/aaaa): ")
            projet.ajouter_jalon(nom, date)
        elif choix == "5":
            description = input("Description du changement: ")
            version = input("Version du changement: ")
            date = input("Date du changement (jj/mm/aaaa): ")
            projet.enregistrer_changement(description, version, date)
        elif choix == "6":
            rapport = projet.generer_rapport()
            print(rapport)
        elif choix == "7":
            print("Programme terminé.")
            break
        else:
            print("Choix invalide. Veuillez réessayer.")
