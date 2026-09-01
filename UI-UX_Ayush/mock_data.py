"""
mock_data.py — VIDI Demo Mode Data
====================================
All mock/demo data is centralised here.
To connect a real AI backend, replace the functions in this file
with calls to your RAG pipeline or LLM API.
"""

# ---------------------------------------------------------------------------
# Dashboard metrics (replace with live backend counters)
# ---------------------------------------------------------------------------
DASHBOARD_METRICS = {
    "standards_indexed": "4,500+",
    "queries_answered": "1,280",
    "evidence_backed_pct": "94%",
    "avg_confidence": "89%",
}

# ---------------------------------------------------------------------------
# Sample query suggestions shown on the welcome screen
# ---------------------------------------------------------------------------
QUERY_SUGGESTIONS = [
    "What are the requirements for Portland cement under IS 269?",
    "Which Indian Standard applies to electrical safety testing?",
    "What does IS 456 Clause 5.2 require for concrete?",
    "Explain the BIS certification process for electronics.",
    "What are the labelling requirements for packaged drinking water?",
    "Which standard governs steel reinforcement bars in India?",
]

# ---------------------------------------------------------------------------
# Sample standards for the Standards Explorer
# ---------------------------------------------------------------------------
STANDARDS_LIBRARY = [
    {
        "id": "IS 269:2015",
        "title": "Ordinary Portland Cement — Specification",
        "category": "Cement & Building Materials",
        "year": 2015,
        "industry": "Construction",
        "description": "Specifies requirements for ordinary Portland cement covering composition, physical, and chemical requirements.",
    },
    {
        "id": "IS 456:2000",
        "title": "Plain and Reinforced Concrete — Code of Practice",
        "category": "Civil Engineering",
        "year": 2000,
        "industry": "Construction",
        "description": "Code of practice for structural use of plain and reinforced concrete.",
    },
    {
        "id": "IS 1646:1997",
        "title": "Code of Practice for Fire Safety of Buildings (General)",
        "category": "Fire Safety",
        "year": 1997,
        "industry": "Construction",
        "description": "General fire safety requirements for buildings and structures.",
    },
    {
        "id": "IS 13252:2010",
        "title": "Information Technology Equipment — Safety",
        "category": "Electronics & IT",
        "year": 2010,
        "industry": "Electronics",
        "description": "Safety requirements for IT and audio/video equipment intended for household use.",
    },
    {
        "id": "IS 14772:2000",
        "title": "Packaged Drinking Water — Specification",
        "category": "Food & Beverages",
        "year": 2000,
        "industry": "Food Processing",
        "description": "Specification covering quality, labelling, and testing of packaged drinking water.",
    },
    {
        "id": "IS 1786:2008",
        "title": "High Strength Deformed Steel Bars — Specification",
        "category": "Steel & Metals",
        "year": 2008,
        "industry": "Construction",
        "description": "Requirements for high strength deformed steel bars and wires for concrete reinforcement.",
    },
    {
        "id": "IS 732:1989",
        "title": "Code of Practice for Electrical Wiring Installations",
        "category": "Electrical",
        "year": 1989,
        "industry": "Electrical",
        "description": "Code for installation of electrical wiring systems in buildings.",
    },
    {
        "id": "IS 9000:1981",
        "title": "Basic Environmental Testing Procedures for Electronic Equipment",
        "category": "Electronics & IT",
        "year": 1981,
        "industry": "Electronics",
        "description": "Standard test procedures for environmental testing of electronic components.",
    },
    {
        "id": "IS 4031:1999",
        "title": "Methods of Physical Tests for Hydraulic Cement",
        "category": "Cement & Building Materials",
        "year": 1999,
        "industry": "Construction",
        "description": "Methods for determining physical properties of hydraulic cements.",
    },
    {
        "id": "IS 2062:2011",
        "title": "Hot Rolled Medium and High Tensile Structural Steel",
        "category": "Steel & Metals",
        "year": 2011,
        "industry": "Manufacturing",
        "description": "Specification for structural steel used in general construction and engineering purposes.",
    },
]

INDUSTRY_CATEGORIES = sorted({s["industry"] for s in STANDARDS_LIBRARY})
STANDARD_CATEGORIES = sorted({s["category"] for s in STANDARDS_LIBRARY})

# ---------------------------------------------------------------------------
# BIS Services Directory
# ---------------------------------------------------------------------------
BIS_SERVICES = [
    {
        "id": "isi_mark",
        "title": "Product Certification Scheme (ISI Mark)",
        "subtitle": "Scheme-I (Domestic Manufacturers)",
        "badge": "Mandatory & Voluntary",
        "badge_variant": "high",
        "icon": "🛡️",
        "description": "Enables manufacturers to use the prestigious ISI Standard Mark confirming products satisfy Indian Standards. Over 450 products fall under mandatory certification.",
        "key_features": [
            "Factory quality audits and production process evaluation",
            "Mandatory independent sample testing at BIS laboratories",
            "Continuous surveillance through random market audits",
            "Direct licensing with simplified digital submission on Manakonline"
        ],
        "applicable_sectors": ["Cement", "Steel", "Food & Drinking Water", "Automotive Parts", "Electrical Appliances"],
        "portal_link": "https://www.manakonline.in"
    },
    {
        "id": "crs_scheme",
        "title": "Compulsory Registration Scheme (CRS)",
        "subtitle": "Scheme-II (MeitY & MNRE Goods)",
        "badge": "Mandatory Electronic",
        "badge_variant": "blue",
        "icon": "💻",
        "description": "Self-declaration of conformity based on testing from BIS recognized laboratories for electronic, IT goods, and solar photo-voltaic components.",
        "key_features": [
            "Covers 80+ electronic & IT product categories (Laptops, Mobile phones, LED lamps)",
            "Test report validity from BIS-recognized labs (under 90 days)",
            "Quick digital registration without mandatory prior factory inspection",
            "QR code-based Unique Registration Number (URN) label"
        ],
        "applicable_sectors": ["Information Technology", "Consumer Electronics", "Solar Energy", "Telecom Equipment"],
        "portal_link": "https://www.crsbis.in"
    },
    {
        "id": "hallmarking",
        "title": "Hallmarking Scheme",
        "subtitle": "Precious Metals (Gold & Silver)",
        "badge": "Mandatory HUID",
        "badge_variant": "amber",
        "icon": "✨",
        "description": "Guarantees the purity and fineness of gold and silver articles sold in India, authenticated by a 6-digit alphanumeric Hallmark Unique Identification (HUID).",
        "key_features": [
            "Mandatory 6-digit HUID laser engraved on every jewellery piece",
            "Assaying and Hallmarking Centers (AHC) accredited nationwide",
            "Consumer verification via the official 'BIS CARE' mobile app",
            "Standard purity grades: 14K (585), 18K (750), 20K (833), 22K (916), 24K (999)"
        ],
        "applicable_sectors": ["Gold Jewellery", "Silver Artefacts", "Bullion & Coins"],
        "portal_link": "https://www.manakonline.in"
    },
    {
        "id": "mscs",
        "title": "Management Systems Certification (MSCS)",
        "subtitle": "ISO Compliance Certification",
        "badge": "Enterprise Quality",
        "badge_variant": "high",
        "icon": "🏢",
        "description": "BIS certifies organizations for compliance with international and Indian management standards covering Quality, Environment, Safety, and Food Security.",
        "key_features": [
            "IS/ISO 9001 (Quality Management Systems - QMS)",
            "IS/ISO 14001 (Environmental Management Systems - EMS)",
            "IS/ISO 45001 (Occupational Health & Safety - OHSMS)",
            "IS/ISO 22000 & IS/ISO 27001 (Information Security Management)"
        ],
        "applicable_sectors": ["Manufacturing", "Healthcare", "IT Services", "Government Bodies"],
        "portal_link": "https://www.bis.gov.in"
    },
    {
        "id": "lrs",
        "title": "Laboratory Recognition Scheme (LRS)",
        "subtitle": "Testing & Calibration Network",
        "badge": "Accreditation",
        "badge_variant": "blue",
        "icon": "🔬",
        "description": "Maintains a comprehensive network of Central, Regional, and recognized third-party laboratories to test consumer and industrial samples against standard specifications.",
        "key_features": [
            "Central Laboratory in Sahibabad + 4 Regional & 3 Branch Labs",
            "Over 200+ NABL-accredited recognized private & government laboratories",
            "Inter-laboratory proficiency testing programs (PT)",
            "Online Laboratory Information Management System (LIMS)"
        ],
        "applicable_sectors": ["Chemical", "Mechanical", "Electrical", "Microbiological", "Civil Testing"],
        "portal_link": "https://www.bis.gov.in"
    },
    {
        "id": "standards_formulation",
        "title": "Standard Formulation (Know Your Standards)",
        "subtitle": "Technical Committees & Public Consultation",
        "badge": "National Consensus",
        "badge_variant": "high",
        "icon": "📐",
        "description": "The open, consensus-driven process through which new Indian Standards are proposed, drafted, scrutinized by 15 Division Councils, and published for national adoption.",
        "key_features": [
            "15 Division Councils covering Civil, Electrotechnical, Food, Transport, etc.",
            "Public consultation and open draft review mechanism",
            "Harmonization with International Standards (ISO / IEC)",
            "Standards Portal: Free access to read all Indian Standards online"
        ],
        "applicable_sectors": ["All National Industries", "Academia", "Research Institutions"],
        "portal_link": "https://www.standardsbis.in"
    }
]

# ---------------------------------------------------------------------------
# Saved Standards (for sidebar bookmark view)
# ---------------------------------------------------------------------------
SAVED_STANDARDS = [
    {"id": "IS 456:2000", "title": "Plain and Reinforced Concrete", "category": "Civil Engineering"},
    {"id": "IS 269:2015", "title": "Ordinary Portland Cement", "category": "Cement & Building Materials"},
    {"id": "IS 13252:2010", "title": "IT Equipment — Safety", "category": "Electronics & IT"}
]


# ---------------------------------------------------------------------------
# Recent query history (sidebar) — mock
# ---------------------------------------------------------------------------
RECENT_QUERIES = [
    "Cement testing requirements — IS 269",
    "BIS certification process overview",
    "IS 456 concrete — Clause 5 details",
    "Electrical safety standards",
    "Packaged water labelling rules",
    "Steel bar grading under IS 1786",
]

# ---------------------------------------------------------------------------
# Role-specific answer prefixes
# ---------------------------------------------------------------------------
ROLE_PREFIXES = {
    "Manufacturer": "As a **manufacturer**, here is what you need to comply with:",
    "Engineer": "As an **engineer**, the relevant technical specifications are:",
    "Quality Control Professional": "From a **quality control** perspective, the key requirements are:",
    "Industry Representative": "For **industry compliance** purposes, the following applies:",
    "Consumer": "Here is a **plain-language explanation** of what this standard means for you:",
    "Student / Researcher": "Here is an **academic overview** of the standard and its implications:",
    "Other": "Based on the available documentation, here is the relevant information:",
}

# ---------------------------------------------------------------------------
# Demo responses
# ---------------------------------------------------------------------------

def _cement_response(role: str) -> dict:
    prefix = ROLE_PREFIXES.get(role, ROLE_PREFIXES["Other"])
    return {
        "answer": (
            f"{prefix}\n\n"
            "Based on **IS 269:2015** (*Ordinary Portland Cement — Specification*), "
            "the standard specifies the following core requirements:\n\n"
            "**Composition Requirements:**\n"
            "- Clinker content and permissible additions are strictly regulated.\n"
            "- Fly ash and slag additions must not exceed prescribed limits.\n\n"
            "**Physical Property Requirements (Clause 5):**\n"
            "- Fineness (specific surface): >= 225 m2/kg (Blaine)\n"
            "- Soundness: Le Chatelier expansion <= 10 mm\n"
            "- Setting time (initial): >= 30 minutes\n"
            "- Compressive strength (28-day): >= 33 N/mm2\n\n"
            "**Chemical Requirements (Clause 6):**\n"
            "- MgO content <= 6.0%\n"
            "- SO3 content <= 3.5%\n"
            "- Loss on ignition <= 5.0%\n\n"
            "All testing must be conducted as per **IS 4031** (Methods of Physical Tests for Hydraulic Cement)."
        ),
        "confidence": 92,
        "confidence_label": "High Confidence",
        "standard": {
            "id": "IS 269:2015",
            "title": "Ordinary Portland Cement — Specification",
            "category": "Cement & Building Materials",
            "year": 2015,
            "relevance": "High",
            "source": "BIS Standards Database",
        },
        "evidence": [
            {
                "clause": "Clause 5",
                "page": 8,
                "snippet": (
                    '"The cement shall conform to the physical requirements specified in Table 1. '
                    'Fineness shall be determined in accordance with IS 4031 (Part 2)."'
                ),
                "standard": "IS 269:2015",
                "relevance_score": 96,
            },
            {
                "clause": "Clause 6.1",
                "page": 11,
                "snippet": (
                    '"The chemical composition of Portland cement shall satisfy the limits given in Table 2, '
                    'including limits on MgO, SO3, and loss on ignition."'
                ),
                "standard": "IS 269:2015",
                "relevance_score": 91,
            },
        ],
        "related_standards": ["IS 4031:1999", "IS 455:2015", "IS 8112:2013"],
        "topic": "Cement",
        "sources_count": 5,
    }


def _electrical_response(role: str) -> dict:
    prefix = ROLE_PREFIXES.get(role, ROLE_PREFIXES["Other"])
    return {
        "answer": (
            f"{prefix}\n\n"
            "Electrical safety testing in India is governed by several key standards:\n\n"
            "**IS 13252:2010** — *Safety of Information Technology Equipment*:\n"
            "- Covers insulation, creepage distances, and protective earthing.\n"
            "- Requires thermal safety cutoffs for heat-generating components.\n\n"
            "**IS 732:1989** — *Electrical Wiring Installations*:\n"
            "- Governs installation quality for wiring within buildings.\n"
            "- Mandates earth leakage protection (ELCB/RCD) in wet areas.\n\n"
            "**IS 9000** series — *Environmental Testing for Electronic Equipment*:\n"
            "- Defines test methods for temperature cycling, humidity, vibration.\n\n"
            "**BIS Certification (IS Mark):** Products covered under mandatory BIS certification "
            "must demonstrate compliance before market entry."
        ),
        "confidence": 88,
        "confidence_label": "High Confidence",
        "standard": {
            "id": "IS 13252:2010",
            "title": "Information Technology Equipment — Safety",
            "category": "Electronics & IT",
            "year": 2010,
            "relevance": "High",
            "source": "BIS Standards Database",
        },
        "evidence": [
            {
                "clause": "Clause 2.6",
                "page": 14,
                "snippet": (
                    '"Equipment shall be provided with means of protection against electric shock, '
                    'including adequate insulation and protective earthing arrangements."'
                ),
                "standard": "IS 13252:2010",
                "relevance_score": 89,
            },
        ],
        "related_standards": ["IS 732:1989", "IS 9000:1981", "IS 694:2010"],
        "topic": "Electrical Safety",
        "sources_count": 4,
    }


def _concrete_response(role: str) -> dict:
    prefix = ROLE_PREFIXES.get(role, ROLE_PREFIXES["Other"])
    return {
        "answer": (
            f"{prefix}\n\n"
            "**IS 456:2000** (*Plain and Reinforced Concrete — Code of Practice*) is the primary standard.\n\n"
            "**Clause 5 — Materials:**\n"
            "- Clause 5.1: Cement must conform to IS 269, IS 8112, or IS 455.\n"
            "- Clause 5.2: Aggregates shall meet IS 383; maximum aggregate size <= 20 mm for slabs.\n"
            "- Clause 5.4: Water used in mixing shall be clean and free from injurious amounts of oils, acids, alkalis.\n\n"
            "**Clause 6 — Concrete Mix Design:**\n"
            "- Minimum cement content and maximum w/c ratio defined by exposure condition.\n"
            "- Moderate exposure: min cement 300 kg/m3, max w/c = 0.50.\n\n"
            "**Durability Provisions (Clause 8):**\n"
            "- Cover requirements range from 20 mm (mild) to 75 mm (extreme) exposure."
        ),
        "confidence": 95,
        "confidence_label": "High Confidence",
        "standard": {
            "id": "IS 456:2000",
            "title": "Plain and Reinforced Concrete — Code of Practice",
            "category": "Civil Engineering",
            "year": 2000,
            "relevance": "High",
            "source": "BIS Standards Database",
        },
        "evidence": [
            {
                "clause": "Clause 5.2",
                "page": 8,
                "snippet": (
                    '"Aggregate shall comply with the requirements of IS 383. '
                    'The maximum size of coarse aggregate shall not exceed one-fourth of the minimum thickness of the member."'
                ),
                "standard": "IS 456:2000",
                "relevance_score": 97,
            },
        ],
        "related_standards": ["IS 383:2016", "IS 10262:2019", "IS 1786:2008"],
        "topic": "Concrete",
        "sources_count": 6,
    }


def _low_confidence_response(role: str) -> dict:
    return {
        "answer": None,
        "confidence": 48,
        "confidence_label": "Low Confidence",
        "standard": None,
        "evidence": [],
        "related_standards": [],
        "topic": "Unknown",
        "sources_count": 0,
    }


def _bis_certification_response(role: str) -> dict:
    prefix = ROLE_PREFIXES.get(role, ROLE_PREFIXES["Other"])
    return {
        "answer": (
            f"{prefix}\n\n"
            "**BIS Certification (IS Mark Scheme)** is governed under the Bureau of Indian Standards Act, 2016.\n\n"
            "**Process Overview:**\n"
            "1. **Application** — Submit Form-I along with product details and test reports to the relevant BIS office.\n"
            "2. **Factory Assessment** — BIS inspects manufacturing premises and quality control systems.\n"
            "3. **Sample Testing** — Product samples are tested at BIS-recognised laboratories.\n"
            "4. **Grant of Licence** — Licence granted upon satisfactory testing and factory assessment.\n"
            "5. **Surveillance** — Periodic factory inspections and market sample testing ensure continued compliance.\n\n"
            "**Key Documents Required:**\n"
            "- Test reports from BIS-recognised laboratory\n"
            "- Quality control plan\n"
            "- Factory layout and process flow\n\n"
            "The process typically takes **4-12 weeks** depending on product category and test complexity."
        ),
        "confidence": 90,
        "confidence_label": "High Confidence",
        "standard": {
            "id": "BIS Act 2016",
            "title": "Bureau of Indian Standards Act, 2016",
            "category": "Regulatory Framework",
            "year": 2016,
            "relevance": "High",
            "source": "BIS Regulatory Database",
        },
        "evidence": [
            {
                "clause": "Section 17",
                "page": 22,
                "snippet": (
                    '"Any manufacturer or producer who desires to use the Standard Mark on any article or process '
                    'shall make an application to the Bureau in such form as may be specified."'
                ),
                "standard": "BIS Act 2016",
                "relevance_score": 93,
            },
        ],
        "related_standards": ["IS 10220:2002", "BIS Scheme-I", "CRS Scheme"],
        "topic": "BIS Certification",
        "sources_count": 4,
    }


def _water_response(role: str) -> dict:
    prefix = ROLE_PREFIXES.get(role, ROLE_PREFIXES["Other"])
    return {
        "answer": (
            f"{prefix}\n\n"
            "**IS 14772:2000** (*Packaged Drinking Water — Specification*) governs labelling requirements.\n\n"
            "**Mandatory Label Information (Clause 10):**\n"
            "- Name of product: 'Packaged Drinking Water'\n"
            "- Name and address of manufacturer\n"
            "- Net volume\n"
            "- Batch/lot number\n"
            "- Date of manufacture and best-before date\n"
            "- IS Mark (BIS licence number)\n"
            "- Storage instructions\n\n"
            "**Water Quality Requirements (Clause 5):**\n"
            "- pH: 6.5-8.5\n"
            "- TDS: <= 500 mg/L\n"
            "- Turbidity: <= 1 NTU\n"
            "- No detectable coliform bacteria\n\n"
            "BIS certification is **mandatory** for packaged drinking water under the IS Mark scheme."
        ),
        "confidence": 94,
        "confidence_label": "High Confidence",
        "standard": {
            "id": "IS 14772:2000",
            "title": "Packaged Drinking Water — Specification",
            "category": "Food & Beverages",
            "year": 2000,
            "relevance": "High",
            "source": "BIS Standards Database",
        },
        "evidence": [
            {
                "clause": "Clause 10.1",
                "page": 7,
                "snippet": (
                    '"Every container of packaged drinking water shall carry a label with the following information: '
                    'name of product, name and address of manufacturer, net volume, and BIS licence number."'
                ),
                "standard": "IS 14772:2000",
                "relevance_score": 95,
            },
        ],
        "related_standards": ["IS 1239:2004", "FSSAI Regulations", "IS 12711:1999"],
        "topic": "Packaged Drinking Water",
        "sources_count": 3,
    }


def get_demo_response(query: str, role: str) -> dict:
    """
    Returns a mock response dict for a given query and user role.

    REPLACE THIS FUNCTION with your actual AI backend call, e.g.:
        response = rag_pipeline.query(query, user_role=role)
        return format_response(response)

    The returned dict must have keys:
        answer, confidence, confidence_label, standard, evidence,
        related_standards, topic, sources_count
    """
    q = query.lower()

    if any(k in q for k in ["cement", "is 269", "portland"]):
        return _cement_response(role)
    elif any(k in q for k in ["electrical", "electric", "is 13252", "safety test", "it equipment"]):
        return _electrical_response(role)
    elif any(k in q for k in ["concrete", "is 456", "reinforced", "clause 5.2"]):
        return _concrete_response(role)
    elif any(k in q for k in ["certification", "bis certif", "is mark", "licence"]):
        return _bis_certification_response(role)
    elif any(k in q for k in ["water", "packaged", "is 14772", "drinking"]):
        return _water_response(role)
    elif any(k in q for k in ["unknown", "random", "test low", "insufficient"]):
        return _low_confidence_response(role)
    else:
        prefix = ROLE_PREFIXES.get(role, ROLE_PREFIXES["Other"])
        return {
            "answer": (
                f"{prefix}\n\n"
                "Based on the available BIS documentation, VIDI has identified the following relevant information. "
                "Please refine your query with a specific standard number or clause for a more precise answer.\n\n"
                "**General Guidance:**\n"
                "- Indian Standards are published by the Bureau of Indian Standards (BIS).\n"
                "- Standards can be searched at the BIS website (www.bis.gov.in).\n"
                "- For product-specific requirements, specify the product name or IS number.\n\n"
                "_Tip: Try asking about IS 269 (cement), IS 456 (concrete), or IS 13252 (IT safety) for detailed responses._"
            ),
            "confidence": 72,
            "confidence_label": "Moderate Confidence",
            "standard": {
                "id": "BIS General",
                "title": "Bureau of Indian Standards — General Information",
                "category": "Regulatory Framework",
                "year": 2024,
                "relevance": "Moderate",
                "source": "BIS Knowledge Base",
            },
            "evidence": [
                {
                    "clause": "General",
                    "page": 1,
                    "snippet": (
                        '"BIS is the national standards body of India working under the aegis of the '
                        'Ministry of Consumer Affairs, Food & Public Distribution."'
                    ),
                    "standard": "BIS Overview",
                    "relevance_score": 74,
                }
            ],
            "related_standards": ["IS 269:2015", "IS 456:2000", "IS 13252:2010"],
            "topic": "General",
            "sources_count": 2,
        }
