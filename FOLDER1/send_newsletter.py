import requests
import json

# Récupérer les emails des abonnés
response = requests.get("http://localhost:8000/api/newsletter-emails")
emails = response.json().get("emails", [])

print(f"📧 Envoi à {len(emails)} abonnés...")

# Contenu de la newsletter
message = """
Bonjour,

Notre nouvelle version est disponible !
Découvrez les nouveautés sur notre site.

Merci de votre confiance !
L'équipe
"""

# Ici tu peux ajouter le code d'envoi d'email
# Pour l'instant on affiche juste
for email in emails:
    print(f"📨 Envoi à {email}")

print("✅ Fini !")