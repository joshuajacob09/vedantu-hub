# utils/registry.py
# ─────────────────────────────────────────────────────
# Dynamic registry loader.
# All modules query this instead of raw dicts.
# Filters are applied here — never in the UI layer.
# ─────────────────────────────────────────────────────

from competitors import COMPETITOR_REGISTRY

# Valid values for reference
VALID_CATEGORIES = ["JEE", "NEET", "Class 8-12", "Boards", "Foundation"]
VALID_LANGUAGES  = ["Hindi", "English", "Tamil", "Telugu", "Bilingual"]
VALID_PRIORITIES = [1, 2, 3]


def get_all_competitors(active_only: bool = True) -> list[dict]:
    """Return full competitor list. active_only=True skips inactive channels."""
    if active_only:
        return [c for c in COMPETITOR_REGISTRY if c["active"]]
    return COMPETITOR_REGISTRY


def get_competitors_by_category(category: str, active_only: bool = True) -> list[dict]:
    """
    Return competitors matching a category.
    e.g. get_competitors_by_category("JEE")
    """
    pool = get_all_competitors(active_only)
    return [c for c in pool if category in c["category"]]


def get_competitors_by_priority(priority: int, active_only: bool = True) -> list[dict]:
    """
    Return competitors at a given priority tier.
    1 = Tier 1 direct competitors
    2 = Tier 2 significant players
    3 = Tier 3 niche/specialist
    """
    pool = get_all_competitors(active_only)
    return [c for c in pool if c["priority"] == priority]


def get_competitors_by_language(language: str, active_only: bool = True) -> list[dict]:
    """Return competitors in a specific language."""
    pool = get_all_competitors(active_only)
    return [c for c in pool if c["language"] == language]


def get_top_competitors(n: int = 5, active_only: bool = True) -> list[dict]:
    """Return top N competitors sorted by priority (1 first)."""
    pool = get_all_competitors(active_only)
    sorted_pool = sorted(pool, key=lambda c: c["priority"])
    return sorted_pool[:n]


def as_name_id_dict(competitors: list[dict]) -> dict:
    """
    Convert a list of competitor dicts to a simple {name: id} dict.
    Used anywhere that needs the old-style flat dict format.
    e.g. for st.selectbox options.
    """
    return {c["name"]: c["id"] for c in competitors}


def get_categories_available() -> list[str]:
    """Return all unique categories present in the active registry."""
    active = get_all_competitors()
    cats = set()
    for c in active:
        for cat in c["category"]:
            cats.add(cat)
    return sorted(cats)


def get_registry_stats() -> dict:
    """Return summary stats about the registry — used in UI."""
    all_c   = get_all_competitors(active_only=False)
    active  = get_all_competitors(active_only=True)
    return {
        "total":    len(all_c),
        "active":   len(active),
        "inactive": len(all_c) - len(active),
        "tier1":    len(get_competitors_by_priority(1)),
        "tier2":    len(get_competitors_by_priority(2)),
        "tier3":    len(get_competitors_by_priority(3)),
        "by_category": {
            cat: len(get_competitors_by_category(cat))
            for cat in get_categories_available()
        },
    }
