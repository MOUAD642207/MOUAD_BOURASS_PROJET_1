from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
import json
import uuid
from datetime import datetime
import os
import re

# ========== CONFIGURATION ==========
DATA_FILE = "subscribers.json"

# ========== MODÈLES ==========
class SubscriberCreate(BaseModel):
    email: EmailStr
    phone: str
    newsletter: bool = False

# ========== BASE DE DONNÉES ==========
def read_subscribers():
    """Lit le fichier JSON"""
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return []

def write_subscribers(subscribers):
    """Écrit dans le fichier JSON"""
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(subscribers, f, indent=2, default=str, ensure_ascii=False)

def add_subscriber(email, phone, newsletter):
    """Ajoute un abonné"""
    subscribers = read_subscribers()
    
    # Vérifier si l'email existe déjà
    for sub in subscribers:
        if sub['email'].lower() == email.lower():
            raise ValueError("Cet email est déjà inscrit")
    
    # Nettoyer le téléphone
    phone_clean = re.sub(r'[^0-9+]', '', phone)
    
    new_subscriber = {
        "id": str(uuid.uuid4()),
        "email": email.lower(),
        "phone": phone_clean,
        "newsletter": newsletter,
        "subscribed_at": datetime.now().isoformat()
    }
    
    subscribers.append(new_subscriber)
    write_subscribers(subscribers)
    return new_subscriber

def get_newsletter_emails():
    """Récupère les emails des abonnés à la newsletter"""
    subscribers = read_subscribers()
    return [sub['email'] for sub in subscribers if sub.get('newsletter', False)]

def get_stats():
    """Statistiques"""
    subscribers = read_subscribers()
    total = len(subscribers)
    newsletter_yes = sum(1 for s in subscribers if s.get('newsletter', False))
    return {"total": total, "newsletter": newsletter_yes}

# ========== APPLICATION FASTAPI ==========
app = FastAPI(title="Maroc Invest - API Newsletter", version="1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ========== HTML + CSS + JS ==========
HTML_PAGE = """
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Newsletter</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 20px;
        }
        
        .container {
            width: 100%;
            max-width: 480px;
        }
        
        .card {
            background: white;
            border-radius: 20px;
            padding: 40px;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
            animation: fadeIn 0.5s ease;
        }
        
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(-20px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        h1 {
            color: #333;
            font-size: 28px;
            margin-bottom: 8px;
            text-align: center;
        }
        
        .subtitle {
            color: #666;
            text-align: center;
            margin-bottom: 30px;
            font-size: 14px;
        }
        
        .form-group {
            margin-bottom: 20px;
        }
        
        label {
            display: block;
            color: #333;
            font-weight: 600;
            margin-bottom: 6px;
            font-size: 14px;
        }
        
        input[type="email"],
        input[type="tel"] {
            width: 100%;
            padding: 12px 15px;
            border: 2px solid #e0e0e0;
            border-radius: 10px;
            font-size: 16px;
            transition: all 0.3s;
        }
        
        input[type="email"]:focus,
        input[type="tel"]:focus {
            border-color: #667eea;
            outline: none;
            box-shadow: 0 0 0 4px rgba(102, 126, 234, 0.1);
        }
        
        input.error {
            border-color: #e74c3c;
        }
        
        small {
            color: #888;
            font-size: 12px;
            display: block;
            margin-top: 4px;
        }
        
        .checkbox-group {
            margin: 15px 0;
        }
        
        .checkbox-label {
            display: flex;
            align-items: center;
            gap: 10px;
            cursor: pointer;
            font-weight: normal;
            font-size: 14px;
        }
        
        .checkbox-label input[type="checkbox"] {
            width: 18px;
            height: 18px;
            flex-shrink: 0;
        }
        
        .btn-submit {
            width: 100%;
            padding: 14px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 10px;
            font-size: 18px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s;
            margin-top: 10px;
        }
        
        .btn-submit:hover:not(:disabled) {
            transform: translateY(-2px);
            box-shadow: 0 10px 30px rgba(102, 126, 234, 0.4);
        }
        
        .btn-submit:disabled {
            opacity: 0.7;
            cursor: not-allowed;
        }
        
        .btn-submit.loading {
            position: relative;
            color: transparent;
        }
        
        .btn-submit.loading::after {
            content: '';
            position: absolute;
            left: 50%;
            top: 50%;
            width: 24px;
            height: 24px;
            border: 3px solid white;
            border-top-color: transparent;
            border-radius: 50%;
            animation: spin 0.6s linear infinite;
            transform: translate(-50%, -50%);
        }
        
        @keyframes spin {
            to { transform: translate(-50%, -50%) rotate(360deg); }
        }
        
        .message {
            padding: 12px 16px;
            border-radius: 10px;
            margin: 15px 0;
            display: none;
        }
        
        .message.success {
            display: block;
            background: #d4edda;
            color: #155724;
            border: 1px solid #c3e6cb;
        }
        
        .message.error {
            display: block;
            background: #f8d7da;
            color: #721c24;
            border: 1px solid #f5c6cb;
        }
        
        .info {
            margin-top: 20px;
            padding-top: 20px;
            border-top: 1px solid #e0e0e0;
            color: #888;
            font-size: 13px;
            text-align: center;
        }
        
        .info p {
            margin: 4px 0;
        }
        
        .stats {
            margin-top: 20px;
            padding: 15px;
            background: #f8f9fa;
            border-radius: 10px;
            text-align: center;
            font-size: 14px;
            color: #666;
        }
        
        .stats span {
            font-weight: 700;
            color: #333;
        }
        
        @media (max-width: 600px) {
            .card {
                padding: 24px;
            }
            h1 {
                font-size: 24px;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="card">
            <h1>📬 Newsletter</h1>
            <p class="subtitle">Recevez nos actualités et offres exclusives</p>
            
            <form id="subscribeForm">
                <div class="form-group">
                    <label for="email">Email *</label>
                    <input type="email" id="email" placeholder="votre@email.com" required>
                </div>
                
                <div class="form-group">
                    <label for="phone">Téléphone *</label>
                    <input type="tel" id="phone" placeholder="0612345678" required>
                    <small>Format: 10 chiffres</small>
                </div>
                
                <div class="checkbox-group">
                    <label class="checkbox-label">
                        <input type="checkbox" id="newsletter" checked>
                        <span>Je souhaite recevoir les nouveautés</span>
                    </label>
                </div>
                
                <div id="message" class="message"></div>
                
                <button type="submit" class="btn-submit" id="submitBtn">S'inscrire</button>
            </form>
            
            <div class="info">
                <p>🔒 Vos données sont sécurisées</p>
                <p>📧 Un email de confirmation vous sera envoyé</p>
            </div>
            
            <div class="stats" id="stats">
                Chargement des statistiques...
            </div>
        </div>
    </div>
    
    <script>
        // ===== STATISTIQUES =====
        async function loadStats() {
            try {
                const response = await fetch('/api/stats');
                const data = await response.json();
                document.getElementById('stats').innerHTML = `
                    📊 <span>${data.total}</span> abonnés · 
                    <span>${data.newsletter}</span> à la newsletter
                `;
            } catch (error) {
                document.getElementById('stats').innerHTML = '📊 Statistiques indisponibles';
            }
        }
        loadStats();
        
        // ===== FORMULAIRE =====
        const form = document.getElementById('subscribeForm');
        const messageDiv = document.getElementById('message');
        const submitBtn = document.getElementById('submitBtn');
        const emailInput = document.getElementById('email');
        const phoneInput = document.getElementById('phone');
        const newsletterCheck = document.getElementById('newsletter');
        
        // Nettoyer le téléphone en temps réel
        phoneInput.addEventListener('input', function() {
            this.value = this.value.replace(/[^0-9+]/g, '');
            if (this.value.length === 10) {
                this.classList.remove('error');
            }
        });
        
        // Validation email
        emailInput.addEventListener('input', function() {
            const emailRegex = /^[^\\s@]+@[^\\s@]+\\.[^\\s@]+$/;
            if (emailRegex.test(this.value)) {
                this.classList.remove('error');
            }
        });
        
        form.addEventListener('submit', async function(e) {
            e.preventDefault();
            
            // Reset
            messageDiv.className = 'message';
            messageDiv.style.display = 'none';
            submitBtn.disabled = true;
            submitBtn.classList.add('loading');
            
            // Récupérer les données
            const email = emailInput.value.trim();
            const phone = phoneInput.value.trim();
            const newsletter = newsletterCheck.checked;
            
            // Validation
            if (!email || !phone) {
                showMessage('Veuillez remplir tous les champs', 'error');
                submitBtn.disabled = false;
                submitBtn.classList.remove('loading');
                return;
            }
            
            if (phone.length < 10) {
                showMessage('Le téléphone doit contenir 10 chiffres', 'error');
                phoneInput.classList.add('error');
                submitBtn.disabled = false;
                submitBtn.classList.remove('loading');
                return;
            }
            
            try {
                const response = await fetch('/api/subscribe', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ email, phone, newsletter })
                });
                
                const data = await response.json();
                
                if (response.ok) {
                    showMessage('✅ Inscription réussie ! Vérifiez vos emails.', 'success');
                    form.reset();
                    newsletterCheck.checked = true;
                    loadStats(); // Mettre à jour les stats
                } else {
                    showMessage('❌ ' + (data.detail || 'Erreur'), 'error');
                }
            } catch (error) {
                showMessage('❌ Erreur de connexion au serveur', 'error');
            } finally {
                submitBtn.disabled = false;
                submitBtn.classList.remove('loading');
            }
        });
        
        function showMessage(text, type) {
            messageDiv.textContent = text;
            messageDiv.className = 'message ' + type;
            messageDiv.style.display = 'block';
            
            setTimeout(() => {
                messageDiv.style.display = 'none';
            }, 6000);
        }
    </script>
</body>
</html>
"""

# ========== ROUTES ==========

@app.get("/", response_class=HTMLResponse)
async def home():
    """Page d'accueil avec le formulaire"""
    return HTMLResponse(content=HTML_PAGE)

@app.post("/api/subscribe")
async def subscribe(subscriber: SubscriberCreate):
    """Inscription à la newsletter"""
    try:
        new_sub = add_subscriber(
            subscriber.email,
            subscriber.phone,
            subscriber.newsletter
        )
        return {
            "success": True,
            "message": "Inscription réussie !",
            "subscriber": new_sub
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Erreur interne")

@app.get("/api/stats")
async def stats():
    """Statistiques des abonnés"""
    return get_stats()

@app.get("/api/subscribers")
async def list_subscribers():
    """Liste tous les abonnés (pour admin)"""
    return read_subscribers()

@app.get("/api/newsletter-emails")
async def newsletter_emails():
    """Liste des emails des abonnés à la newsletter"""
    return {"emails": get_newsletter_emails()}

# ========== LANCEMENT ==========
if __name__ == "__main__":
    import uvicorn
    print("🚀 Serveur démarré sur http://localhost:8000")
    print("📊 Stats disponibles sur /api/stats")
    print("📧 Liste des emails newsletter sur /api/newsletter-emails")
    print("📬 Inscription newsletter sur /api/subscribe")
    uvicorn.run(app, host="0.0.0.0", port=8000)