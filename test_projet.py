"""
Projet de MQPL de Mame Diarra Beye et Oumy Lo

"""

import unittest
from projet import Projet, EmailNotificationStrategy, NotificationContext


class TestProjet(unittest.TestCase):


    def setUp(self):
        
        self.projet = Projet(
            "Linguere Service", "Agence de recrutement",
            "1/11/2023", "3/6/2024", 3000000
        )
        self.notification_strategy = EmailNotificationStrategy()
        self.notification_context = (
            NotificationContext(self.notification_strategy))
        self.projet.definir_notification_context(self.notification_context)

    def test_ajouter_tache(self):
        
        self.projet.ajouter_tache(
            "Tache1", "Description de la tâche 1", "1/11/2023",
            "3/6/2024", "Responsable1", "en cours"
        )
        self.assertEqual(len(self.projet.taches), 1)
        self.assertEqual(self.projet.taches[0].nom, "Tache1")

    def test_ajouter_membre_equipe(self):
        
        self.projet.ajouter_membre_equipe("Membre1", "Role1")
        self.assertEqual(len(self.projet.equipe.membres), 1)
        self.assertEqual(self.projet.equipe.membres[0].nom, "Membre1")

    def test_ajouter_risque(self):
        
        self.projet.ajouter_risque("Risque1", "élevée", "fort")
        self.assertEqual(len(self.projet.risques), 1)
        self.assertEqual(self.projet.risques[0].description, "Risque1")

    def test_ajouter_jalon(self):
        
        self.projet.ajouter_jalon("Jalon1", "15/11/2023")
        self.assertEqual(len(self.projet.jalons), 1)
        self.assertEqual(self.projet.jalons[0].nom, "Jalon1")

    def test_enregistrer_changement(self):
        
        self.projet.enregistrer_changement("Changement1", "1.0", "01/12/2023")
        self.assertEqual(len(self.projet.versions), 1)
        self.assertEqual(self.projet.versions[0].description, "Changement1")

    def test_generer_rapport(self):
    
        self.projet.ajouter_tache(
            "Tache1", "Description de la tâche 1",
            "1/11/2023", "3/6/2024", "Responsable1", "en cours"
        )
        self.projet.ajouter_membre_equipe("Membre1", "Role1")
        self.projet.ajouter_risque("Risque1", "élevée", "fort")
        self.projet.ajouter_jalon("Jalon1", "15/11/2023")
        self.projet.enregistrer_changement("Changement1", "1.0", "01/12/2023")
        rapport = self.projet.generer_rapport()
        self.assertIn("Tache1", rapport)
        self.assertIn("Membre1", rapport)
        self.assertIn("Risque1", rapport)
        self.assertIn("Jalon1", rapport)
        self.assertIn("Changement1", rapport)


if __name__ == "_main_":
    unittest.main()
