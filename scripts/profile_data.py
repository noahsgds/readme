"""Contenu du profil — source unique, reprise de https://www.noahsegonds.fr/.

Modifie ce fichier puis lance `python scripts/generate.py` pour régénérer les visuels.
"""

LOGIN = "noahsgds"
NAME_FIRST = "Noah"
NAME_LAST = "Segonds"
SITE = "https://www.noahsegonds.fr/"
LINKEDIN = "https://www.linkedin.com/in/noah-segonds/"
EMAIL = "noah47300@gmail.com"

ROLES = [
    "Data Analyst @ Decathlon",
    "Business Analyst",
    "Chef de Projet IA",
    "5x vainqueur de hackathon",
]

HIGHLIGHTS = [
    # (valeur, libellé, couleur)
    ("8", "hackathons IA", "#88C0D0"),
    ("5", "victoires 1ère place", "#EBCB8B"),
    ("#1", "major de promo", "#A3BE8C"),
    ("+500K€", "générés en campagnes", "#B48EAD"),
    ("14", "pays · Next Best Sport", "#BF616A"),
]

# rank: 1, 2 ou 3 — cover: dégradé repris du site
HACKATHONS = [
    {
        "title": "Hackathon Match Group",
        "period": "Juin 2026",
        "rank": 3,
        "icon": "💬",
        "categories": ["HACKATHON", "IA", "ENTREPRISE"],
        "cover": ("#EB6F92", "#B4637A"),
        "desc": "3 jours chez Match Group (Tinder, Hinge, Meetic) : former leurs équipes à "
                "l'IA générative (Claude) et pitcher un produit devant le CEO Spencer Rascoff.",
        "tags": ["IA générative", "Claude", "Pitch"],
        "url": None,
    },
    {
        "title": "Dust Customer Hackathon — Signal",
        "period": "Juin 2026",
        "rank": 3,
        "icon": "📡",
        "categories": ["HACKATHON", "IA", "GTM"],
        "cover": ("#5E81AC", "#3B4A6B"),
        "desc": "Seule équipe étudiante face à Alan, PayFit, Mirakl et 30+ boîtes tech : "
                "un pipeline GTM multi-agents en production sur Dust, buildé en une journée.",
        "tags": ["Dust", "Multi-agents", "GTM"],
        "url": None,
    },
    {
        "title": "Hackathon Mirakl x OpenAI",
        "period": "Mai 2026",
        "rank": 1,
        "icon": "🤖",
        "categories": ["HACKATHON", "IA", "AGENTS"],
        "cover": ("#A3BE8C", "#5E8B6A"),
        "desc": "Jugé par des experts OpenAI : architecture d'agents autonomes qui automatise "
                "toute la prospection commerciale, orchestrée sur Dust, Make et n8n.",
        "tags": ["Dust", "Make", "n8n", "Agents IA"],
        "url": "https://github.com/noahsgds/mirakl",
    },
    {
        "title": "Hackathon PayFit x Dust x Lovable",
        "period": "Mars 2026",
        "rank": 1,
        "icon": "🔍",
        "categories": ["HACKATHON", "IA", "SEO"],
        "cover": ("#7A6FF0", "#4C4BA8"),
        "desc": "Direction d'une équipe de 8 sur 4 jours : agents IA d'automatisation SEO "
                "(rédaction, veille, simulation) via Dust, Make et Lovable.",
        "tags": ["Dust", "Make", "Lovable", "SEO"],
        "url": "https://payfit-pied.vercel.app/",
    },
    {
        "title": "MichiMichi — SaaS Santé Mentale",
        "period": "Oct. 2025",
        "rank": 2,
        "icon": "🧠",
        "categories": ["HACKATHON", "IA", "SANTÉ"],
        "cover": ("#88C0D0", "#4E8FA6"),
        "desc": "Matching psychologue-patient avec suivi IA et garde-fous adaptatifs selon la "
                "sensibilité des sujets : une IA responsable à fort impact social.",
        "tags": ["IA responsable", "Lovable", "Framer"],
        "url": "https://michimichi.lovable.app/",
    },
    {
        "title": "Aura Agency — Lovable x Dust x Wesype",
        "period": "Mai 2025",
        "rank": 1,
        "icon": "🎵",
        "categories": ["HACKATHON", "IA", "SAAS"],
        "cover": ("#B48EAD", "#7A5C87"),
        "desc": "Un label de musique indépendant 100 % automatisé : 12 agents spécialisés "
                "(juridique, com, admin) orchestrés sur Dust, interface en vibecoding.",
        "tags": ["Dust", "Lovable", "Multi-agents"],
        "url": "https://www.loom.com/share/6ddc6ae5dc204aa585975148c1657361",
    },
    {
        "title": "Hackathon Go Fusion — RSE / CSRD",
        "period": "Mars 2025",
        "rank": 1,
        "icon": "🌱",
        "categories": ["HACKATHON", "BUSINESS", "RSE"],
        "cover": ("#8FBF7F", "#4F8A55"),
        "desc": "Stratégie business B2B et SEO pour une startup de mesure d'impact carbone, "
                "avec plan de développement commercial RSE / CSRD.",
        "tags": ["Stratégie B2B", "SEO", "CSRD"],
        "url": "https://github.com/noahsgds/green-challenge-hub",
    },
    {
        "title": "Hackathon des 3M — Malt x Make x Mistral",
        "period": "Fév. 2025",
        "rank": 1,
        "icon": "✉️",
        "categories": ["HACKATHON", "IA", "AUTOMATISATION"],
        "cover": ("#EB9B5B", "#C46E38"),
        "desc": "Personnalisation d'emails à grande échelle pour Malt : pipeline IA no-code "
                "complet conçu en 3 jours avec Make et Mistral AI.",
        "tags": ["Make", "Mistral AI", "No-code"],
        "url": None,
    },
]

EXPERIENCES = [
    {
        "title": "Data Analyst — Growth Customer United",
        "company": "DECATHLON",
        "type": "Alternance",
        "period": "Août 2024 — Présent",
        "current": True,
        "color": "#BF616A",
        "line": "BP Digital 2035 · Next Best Sport (ML sur Databricks) présenté devant 14 pays · KYC 4 marchés",
        "tags": ["Databricks", "SQL", "Power BI", "ML", "Python"],
    },
    {
        "title": "Bras droit CEO / CSM (20 clients)",
        "company": "SIMIO",
        "type": "Alternance",
        "period": "Sept. 2024 — Août 2025",
        "current": False,
        "color": "#88C0D0",
        "line": "Campagnes WhatsApp +500K€ · automatisation Make & n8n (40 % de clic) · 20 nouveaux clients",
        "tags": ["Make", "n8n", "WhatsApp API", "CRM"],
    },
    {
        "title": "Assistant Commercial & Marketing",
        "company": "YOC AntiGaspi",
        "type": "Stage",
        "period": "Avr. — Juin 2024",
        "current": False,
        "color": "#81A1C1",
        "line": "Programme Ambassadeurs : +1300 utilisateurs · stratégie marketing · clients Elior, API Restauration",
        "tags": ["Growth", "Marketing", "Analytics"],
    },
    {
        "title": "Business Developer",
        "company": "DOMY",
        "type": "Alternance",
        "period": "Août — Nov. 2023",
        "current": False,
        "color": "#B48EAD",
        "line": "250 psychologues en SAV · stratégie B2B / B2C · +80 psychologues et 10 partenaires",
        "tags": ["Business Dev", "B2B", "B2C"],
    },
    {
        "title": "Président — BDE GACORIZON",
        "company": "GACO",
        "type": "Associatif",
        "period": "2021 — 2023",
        "current": False,
        "color": "#A3BE8C",
        "line": "Équipe de 12 · 18 projets tuteurés (35 000 € de fonds de roulement) · soirées +200 personnes",
        "tags": ["Leadership", "Management"],
    },
]

SKILLS = [
    ("LANGUAGES", [("Python", 80), ("SQL", 85), ("JavaScript", 65), ("TypeScript", 60)]),
    ("DATA & ANALYTICS", [("Excel", 90), ("Power BI", 80), ("Databricks", 75), ("Dataiku", 74),
                          ("Google Analytics", 72), ("Tableau", 70)]),
    ("MACHINE LEARNING", [("Data Analysis", 80), ("Statistical Modeling", 70),
                          ("ML Algorithms", 65), ("scikit-learn", 62)]),
    ("BUSINESS & MARKETING", [("Business Dev.", 85), ("Marketing Digital", 80),
                              ("CRM / KPIs", 78), ("Growth Hacking", 72)]),
    ("AUTOMATION & TOOLS", [("Notion", 85), ("Make", 72), ("Git", 70), ("n8n", 68)]),
    ("FRONTEND", [("React", 65), ("TypeScript", 60), ("Vite", 58)]),
]
