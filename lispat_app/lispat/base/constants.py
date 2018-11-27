import nltk
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

DESIRED_TERMS = [
    "asset",
    "authentication",
    "authenticity",
    "authorization",
    "availability",
    "confidentiality",
    "configuration",
    "cryptographically strong",
    "cybersecurity",
    "cybersecurity bill of materials",
    "cbom",
    "denial of service",
    "encryption",
    "end of support",
    "integrity",
    "jitter",
    "life-cycle",
    "malware",
    "patchability",
    "updatability",
    "patient harm",
    "privileged user",
    "quality of service",
    "risk",
    "risk analysis",
    "trustworthy device",
    "regulations",
    "regulatory",
    "regulation"
]

DESIRED_PHRASE = [
    "shall",
    "required",
    "requires",
    "must",
    "need",
    "has"
]
