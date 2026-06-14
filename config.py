# config.py
# ─────────────────────────────────────────────────────
# App-wide settings and channel registries.
# To add/edit COMPETITOR channels → edit competitors.py
# To add/edit VEDANTU channels → edit VEDANTU_CHANNELS below
# ─────────────────────────────────────────────────────

from utils.registry import as_name_id_dict, get_all_competitors, get_top_competitors

# ── App metadata ──────────────────────────────────────
APP_TITLE    = "Vedantu Content Intelligence Hub"
APP_ICON     = "🎯"
FOOTER_TEXT  = "Built by Joshua Jacob | YouTube Intern @ Vedantu"
GROQ_MODEL   = "llama-3.3-70b-versatile"
MAX_RESULTS  = 10

# ── Vedantu channels ──────────────────────────────────
VEDANTU_CHANNELS = {
    # JEE
    "Vedantu JEE Made Ejee":        "UC91RZv71f8p0VV2gaFI07pg",
    "Vedantu JEE English":          "UCwBfgxcxKUzlhpEMJxWEmdg",
    "Vedantu JEE Vaathi":           "UCUfK8KOu9IygDWI8O3_Vb0Q",
    # NEET
    "Vedantu NEET Made Ejee":       "UCqaq3Cwa7m_EsqlvfZh6uyw",
    "Vedantu NEET English":         "UCt8OFYyeXWmu8jiLU3hUwjw",
    "Vedantu NEET Tamil":           "UCTvn7dytna9k1xIlPAzqprw",
    "Vedantu NEET Vettri":          "UC6f7NHfiJK5GdgY4SumBHng",
    "Sankalp NEET Vedantu":         "UCWFXoexcMI1jQrHH2N-SJzQ",
    # Boards & Commerce
    "Vedantu Commerce":             "UC4sfE23vp1PaO740hhhqpig",
    "Vedantu CBSE 10th":            "UCMY7ZvLB6-DnuSis_2s37_A",
    "Vedantu 9&10 English":         "UCOZZbzNiwvj308Vt-ndesKA",
    "Vedantu Class 6 7 & 8":        "UCi-J9CCaQ8w427GPHmoQGHA",
    # Regional
    "Vedantu Telugu":               "UCsq4gc-EDXqxZZbaRjqFeTw",
    "Vedantu Master Tamil":         "UCo7S5qgzt1H66Qlepl90c1g",
    # Olympiad & Young
    "Vedantu Young Wonders":        "UCK85zyie3OYa7rU494QjPbw",
    "Vedantu Olympiad School":      "UCPFn447O8-X7UdcW3AmIydQ",
    # Specialty
    "Catalysis by Vedantu":         "UCYIET4VzyU9-vIJhDYNzHPg",
    "Spectrum by Vedantu":          "UC0G5Qkp7bJfHKOCemS3fPAw",
    "Elementary Chemistry Vedantu": "UCG8eg2aeXrKOpcr6fvMX-lQ",
}

# ── Competitor channels (loaded from competitors.py) ──
# These are computed once at import time.
# All modules should use utils/registry.py for filtered queries.
COMPETITOR_CHANNELS = as_name_id_dict(get_all_competitors())

# Combined — used by search, export, trend detection
ALL_CHANNELS = {**VEDANTU_CHANNELS, **COMPETITOR_CHANNELS}

# Top 5 for quota-sensitive operations (weekly report, AI strategist)
TOP_COMPETITORS = as_name_id_dict(get_top_competitors(5))
