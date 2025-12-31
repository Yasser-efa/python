import numpy as np
import re

# Données d'entraînement (exemples créés par DeepSeek)
emails_entrainement = [
    # SPAM
    ("Félicitations ! Vous avez été sélectionné pour gagner un voyage gratuit aux Bahamas", "spam"),
    ("Offre limitée : iPhone 15 à 99€ seulement, cliquez vite avant épuisement", "spam"),
    ("Augmentez vos revenus depuis chez vous, méthode garantie 5000€/mois", "spam"),
    ("Prêt personnel express, sans enquête de crédit, argent en 24h", "spam"),
    ("Pharmacie en ligne, Viagra à prix cassé, livraison discrète", "spam"),
    ("URGENT : Votre compte bancaire nécessite une vérification immédiate", "spam"),
    ("Vous avez gagné un bon d'achat de 500€ chez Amazon, cliquez ici", "spam"),
    ("Réduction exceptionnelle de 80/100 sur toutes les montres de luxe", "spam"),
    ("Travaillez 2h par jour depuis votre canapé, revenus garantis", "spam"),
    ("Alerte sécurité : votre mot de passe a été compromis", "spam"),
    
    # HAM (emails légitimes)
    ("Bonjour, la réunion de l'équipe projet est prévue jeudi à 14h", "ham"),
    ("Pierre, tu peux me passer le dossier client Dupont pour demain ?", "ham"),
    ("Rappel : ton rendez-vous chez le dentiste est confirmé pour vendredi", "ham"),
    ("La facture n°2024-587 est disponible dans votre espace client", "ham"),
    ("Merci pour ton retour, je transmets l'info à l'équipe technique", "ham"),
    ("CV joint : candidature pour le poste de développeur web", "ham"),
    ("Compte-rendu de la réunion du 15 mars avec les actionnaires", "ham"),
    ("Invitation : séminaire annuel de l'entreprise le 25 juin", "ham"),
    ("Projet de budget 2024 à valider avant le 30 novembre", "ham"),
    ("Demande de congés du 10 au 20 août pour approbation", "ham")
]
emails_test = [
    ("Gagnez iPhone gratuit cliquer maintenant", "spam"),
    ("Réunion projet jeudi 14h salle conférence", "ham"),
    ("Votre compte nécessite vérification urgente", "spam"),
    ("Merci pour votre retour bonne journée", "ham"),
    ("Bitcoin gratuit investissement rapide", "spam"),
    ("Dossier client à signer avant vendredi", "ham"),
]

def nettoyeur(texte):
    texte = texte.lower()
    texte = re.sub(r'[^\w\s]',' ',texte)
    texte = [str(car) for car in texte.split()]
    return texte

class DetecteurSpamNaif:
    def __init__(self):
        self.vocabulaire = {}
        self.categories = ["spam", "ham"]
        self.total_spam = 0
        self.total_ham = 0
    
    def entrainer(self, emails_etiquetes):
        for email in emails_etiquetes:
            texte, categorie = email
            mots = nettoyeur(texte)
            
            mots_filtres = []
            for mot in mots:
                if len(mot) > 2:
                    mots_filtres.append(mot)
            
            if categorie == "spam":
                self.total_spam += len(mots_filtres)
            else:
                self.total_ham += len(mots_filtres)
            
            for mot in mots_filtres:
                if mot not in self.vocabulaire:
                    self.vocabulaire[mot] = {"spam": 0, "ham": 0}
                self.vocabulaire[mot][categorie] += 1
                    
                
    
    def analyser_vocabulaire(self):
        score = []
        for mot, comptes in self.vocabulaire.items():
            if self.total_ham > 0 and self.total_spam > 0:
                freq_mot = (comptes["spam"] / self.total_spam) - (comptes["ham"] / self.total_ham)
                score.append((freq_mot, mot))
        score_trie = sorted(score, reverse=True)
        for i, (score_i, mot) in enumerate(score_trie[:10], 1):
            print(f"{i}. {mot} avec une fréquence de: {score_i}")
        for i, (score_i, mot) in enumerate(score_trie[-10:], 1):
            print(f"{i}. {mot} avec une fréquence de: {score_i}")
    
    def predire(self, texte, score_inconnu=0.0005):
            txt_nettoye = nettoyeur(texte)
            txt_filtre = []
            score_total = 0
            for mot in txt_nettoye:
                if len(mot)>2:
                    txt_filtre.append(mot)
            for mot in txt_filtre:
                if mot in self.vocabulaire:
                    score_mot_spam = (self.vocabulaire[mot]["spam"] / self.total_spam)
                    score_mot_ham = ((self.vocabulaire[mot]["ham"] / self.total_ham))
                    freq_mot = score_mot_spam - score_mot_ham
                    score_total += freq_mot
                else:
                    score_total+=score_inconnu
            if score_total > 0:
                return "spam"
            else:
                return "ham"
    def evaluer(self, emails_test):
        correct = 0
        for emails in emails_test:
            txt, vrai_categorie = emails
            predi = self.predire(txt)
            if predi == vrai_categorie:
                correct += 1
        precision = correct / len(emails_test)
        print(f"Précision: {precision:.1%} ({correct}/{len(emails_test)})")

        


    
detecteur = DetecteurSpamNaif()
detecteur.entrainer(emails_entrainement)
print("Total spam mots:", detecteur.total_spam)
print("Total ham mots:", detecteur.total_ham)
print("Taille vocabulaire:", len(detecteur.vocabulaire))
detecteur.analyser_vocabulaire()

print("////////////////////////////////////////")

# Teste ta prédiction
test_emails = [
    ("Gagnez un iPhone gratuit immédiatement", "Devrait être spam"),
    ("Réunion du projet demain à 10h en salle B", "Devrait être ham"),
    ("Cliquez ici pour votre bonus exclusif", "Devrait être spam"),
    ("Merci pour votre email, je reviens vers vous lundi", "Devrait être ham")
]

for texte, attendu in test_emails:
    prediction = detecteur.predire(texte)
    print(f"'{texte[:30]}...' → Prédit: {prediction} | Attendu: {attendu}")

print("////////////////////////////////////////")

test_etrange = [
    ("Xylophonium zibzab flurp gratz", "Mot inventés - quel effet ?"),
    ("Cryptocurrency bitcoin million free", "Anglais - mots inconnus"),
]

for texte, description in test_etrange:
    for score_val in [0.005, -0.005, 0.0]:
        prediction = detecteur.predire(texte, score_inconnu=score_val)
        print(f"Score {score_val}: '{texte}' → {prediction} | {description}")

print("////////////////////////////////////////")

print("ÉVALUATION SUR LE JEU DE TEST:")
precision = detecteur.evaluer(emails_test)