# competitors.py
# ─────────────────────────────────────────────────────
# THE ONLY FILE you edit to add, remove, or update
# competitor channels.
#
# Each entry is a dict with these fields:
#
#   name     : Display name shown in the UI
#   id       : YouTube channel ID (starts with UC...)
#   category : One or more of:
#              "JEE", "NEET", "Class 8-12", "Boards", "Foundation"
#   language : "Hindi", "English", "Tamil", "Telugu", "Bilingual"
#   priority : 1 = Tier 1 (direct competitor)
#              2 = Tier 2 (significant player)
#              3 = Tier 3 (niche / specialist)
#   active   : True = include in analysis
#              False = skip (but keep for record)
# ─────────────────────────────────────────────────────

COMPETITOR_REGISTRY = [

    # ── PHYSICS WALLAH NETWORK ────────────────────────
    {
        "name":     "Physics Wallah",
        "id":       "UCiGyWN6DEbnj2alu7iapuKQ",
        "category": ["JEE", "NEET", "Class 8-12"],
        "language": "Hindi",
        "priority": 1,
        "active":   True,
    },
    {
        "name":     "JEE Wallah",
        "id":       "UCVJU_IChPMOe8RWkdVQjtfQ",
        "category": ["JEE"],
        "language": "Hindi",
        "priority": 1,
        "active":   True,
    },
    {
        "name":     "PW JEE",
        "id":       "UCVf1jaub9qzp4rMvdKflZYA",
        "category": ["JEE"],
        "language": "Hindi",
        "priority": 1,
        "active":   True,
    },
    {
        "name":     "Competition Wallah",
        "id":       "UCD16eo98AXl-9T61Xd711kQ",
        "category": ["JEE", "NEET"],
        "language": "Hindi",
        "priority": 1,
        "active":   True,
    },
    {
        "name":     "PW NEET",
        "id":       "UCGw8iWmsw1cPlfcrww-3C0g",
        "category": ["NEET"],
        "language": "Hindi",
        "priority": 1,
        "active":   True,
    },

    # ── UNACADEMY NETWORK ─────────────────────────────
    {
        "name":     "Yakeen NEET",
        "id":       "UCk19x9BG23f5xkHOzihhclA",
        "category": ["NEET"],
        "language": "Hindi",
        "priority": 1,
        "active":   True,
    },
    {
        "name":     "Unacademy JEE",
        "id":       "UCcMU5NE1Lmf4Fqpx7n9F3Sw",
        "category": ["JEE"],
        "language": "Hindi",
        "priority": 1,
        "active":   True,
    },
    {
        "name":     "Unacademy JEE English",
        "id":       "UCGcukk3AUT_ebF3jRcsdQLg",
        "category": ["JEE"],
        "language": "English",
        "priority": 2,
        "active":   True,
    },
    {
        "name":     "JEEfinity by Unacademy",
        "id":       "UCVGJz1j0N7Gk2qayiideOUg",
        "category": ["JEE"],
        "language": "Hindi",
        "priority": 2,
        "active":   True,
    },
    {
        "name":     "NEET Alchemy by Unacademy",
        "id":       "UCvSE2vW71NVLqh5IwjhxLBA",
        "category": ["NEET"],
        "language": "Hindi",
        "priority": 2,
        "active":   True,
    },
    {
        "name":     "Unacademy NEET",
        "id":       "UCdQwYksctqqiRwqp3PiJMWA",
        "category": ["NEET"],
        "language": "Hindi",
        "priority": 1,
        "active":   True,
    },
    {
        "name":     "IITian Explains",
        "id":       "UCvjRa2jVhKVSbVDG85vKGww",
        "category": ["JEE"],
        "language": "Hindi",
        "priority": 2,
        "active":   True,
    },

    # ── ALLEN ─────────────────────────────────────────
    {
        "name":     "ALLEN NEET",
        "id":       "UCySvBtI4jMLXp0BT9osvASw",
        "category": ["NEET"],
        "language": "Hindi",
        "priority": 1,
        "active":   True,
    },
    {
        "name":     "ALLEN JEE",
        "id":       "UCkUI45drrKTWLxy3q3voJRw",
        "category": ["JEE"],
        "language": "Hindi",
        "priority": 1,
        "active":   True,
    },

    # ── MOTION KOTA ───────────────────────────────────
    {
        "name":     "Motion JEE & NEET",
        "id":       "UCfl4OhoOv8xF64D5KzJinnA",
        "category": ["JEE", "NEET"],
        "language": "Hindi",
        "priority": 2,
        "active":   True,
    },
    {
        "name":     "Motion Kota JEE",
        "id":       "UCd7OIpmiEXf3iu1cir6-PrA",
        "category": ["JEE"],
        "language": "Hindi",
        "priority": 2,
        "active":   True,
    },
    {
        "name":     "Motion NEET",
        "id":       "UC8UzfGlCDh-Q8WDJfrJ6XoA",
        "category": ["NEET"],
        "language": "Hindi",
        "priority": 2,
        "active":   True,
    },

    # ── NEW LIGHT ─────────────────────────────────────
    {
        "name":     "New Light NEET",
        "id":       "UC-NUWDDbu7Yy6dL2YMx2Biw",
        "category": ["NEET"],
        "language": "Hindi",
        "priority": 2,
        "active":   True,
    },
    {
        "name":     "New Light PRAYAAS",
        "id":       "UCPWH5p6qAl7fewEzX1iwRFw",
        "category": ["NEET"],
        "language": "Hindi",
        "priority": 2,
        "active":   True,
    },

    # ── AAKASH ────────────────────────────────────────
    {
        "name":     "Aakash NEET",
        "id":       "UCAPDuc6Kfpe1mKjMX367qmA",
        "category": ["NEET", "JEE"],
        "language": "Hindi",
        "priority": 1,
        "active":   True,
    },

    # ── KHAN SIR ──────────────────────────────────────
    {
        "name":     "Khan Sir Patna",
        "id":       "UCL77mMHDQV_D2DixeqD1Tyg",
        "category": ["Class 8-12", "Boards", "Foundation"],
        "language": "Hindi",
        "priority": 1,
        "active":   True,
    },

    # ── COACHING INSTITUTIONS ─────────────────────────
    {
        "name":     "Competishun Mohit Tyagi",
        "id":       "UCpyc1eTpM1cA3P0ZWym4clw",
        "category": ["JEE"],
        "language": "Hindi",
        "priority": 2,
        "active":   True,
    },
    {
        "name":     "Competishun+",
        "id":       "UC6ieIswHA9WInRsa2r88hRw",
        "category": ["JEE"],
        "language": "Hindi",
        "priority": 2,
        "active":   True,
    },
    {
        "name":     "eSaral JEE & NEET",
        "id":       "UCddnJhXMUxzHoH8AZkZSd8w",
        "category": ["JEE", "NEET", "Class 8-12"],
        "language": "Hindi",
        "priority": 2,
        "active":   True,
    },
    {
        "name":     "eSaral NEET",
        "id":       "UCD7O0ABXcFzKPTAuUTNCE3A",
        "category": ["NEET"],
        "language": "Hindi",
        "priority": 2,
        "active":   True,
    },
    {
        "name":     "Resonance Eduventures",
        "id":       "UC_bdItm01JN2xXRz5hXJwTQ",
        "category": ["JEE", "NEET"],
        "language": "Hindi",
        "priority": 2,
        "active":   True,
    },
    {
        "name":     "Etoos Education",
        "id":       "UCa2dTDY1WDY2xWO8pRSES2g",
        "category": ["JEE", "NEET"],
        "language": "Hindi",
        "priority": 2,
        "active":   True,
    },
    {
        "name":     "Vora Classes",
        "id":       "UCDG_YP69cl42ly3pPy8-Liw",
        "category": ["JEE", "NEET"],
        "language": "Hindi",
        "priority": 2,
        "active":   True,
    },
    {
        "name":     "Career Point Kota",
        "id":       "UCLNYhA7rnXfdaFh-W6hJTSg",
        "category": ["JEE", "NEET"],
        "language": "Hindi",
        "priority": 2,
        "active":   True,
    },
    {
        "name":     "Matrix JEE Academy",
        "id":       "UC1qTGuS_gRjKRburf9i1izg",
        "category": ["JEE"],
        "language": "Hindi",
        "priority": 2,
        "active":   True,
    },

    # ── PHYSICS SPECIALISTS ───────────────────────────
    {
        "name":     "Physics Galaxy",
        "id":       "UCgBmfNILAlXmGv3CsJ8oFJA",
        "category": ["JEE"],
        "language": "English",
        "priority": 2,
        "active":   True,
    },
    {
        "name":     "Eduniti Physics",
        "id":       "UC7px6OmooQLmsJlYACR_n-A",
        "category": ["JEE"],
        "language": "Hindi",
        "priority": 3,
        "active":   True,
    },
    {
        "name":     "JeePhyX",
        "id":       "UCR91PnmVpl3YO3f0ToCQrig",
        "category": ["JEE"],
        "language": "Hindi",
        "priority": 3,
        "active":   True,
    },
    {
        "name":     "Physics Sir JEE",
        "id":       "UC8Z_fpEYLtBu3-OuhJGqLZg",
        "category": ["JEE"],
        "language": "Hindi",
        "priority": 3,
        "active":   True,
    },
    {
        "name":     "Vinay Uppal Physics",
        "id":       "UC5byrHGQwlhfUanp_ubKwdg",
        "category": ["JEE"],
        "language": "Hindi",
        "priority": 3,
        "active":   True,
    },
    {
        "name":     "NMS Sir Physics",
        "id":       "UC-ub6TMPCDj4lxuoZh_ZL8g",
        "category": ["JEE"],
        "language": "Hindi",
        "priority": 3,
        "active":   True,
    },
    {
        "name":     "Sachin Sir Physics",
        "id":       "UCwkhjRhv6CHkQa6EiQmcX0g",
        "category": ["NEET", "JEE"],
        "language": "Hindi",
        "priority": 3,
        "active":   True,
    },

    # ── CHEMISTRY SPECIALISTS ─────────────────────────
    {
        "name":     "Pankaj Sir Chemistry",
        "id":       "UCMMlYN-EhNrt0eoEDUK0bdg",
        "category": ["JEE", "NEET"],
        "language": "Hindi",
        "priority": 2,
        "active":   True,
    },
    {
        "name":     "Canvas Classes Chemistry",
        "id":       "UCWGjJvI_6gX-RACsZ6KZyrw",
        "category": ["JEE", "NEET"],
        "language": "Hindi",
        "priority": 3,
        "active":   True,
    },
    {
        "name":     "Sachin Rana Chemistry",
        "id":       "UC1-ZdFLBukC6fTZ8QRWvpDw",
        "category": ["JEE"],
        "language": "Hindi",
        "priority": 3,
        "active":   True,
    },

    # ── MATHEMATICS SPECIALISTS ───────────────────────
    {
        "name":     "MathonGo",
        "id":       "UCNn75PJi2J5OmZGuLCZGJPg",
        "category": ["JEE"],
        "language": "Hindi",
        "priority": 2,
        "active":   True,
    },
    {
        "name":     "Bhannat Maths",
        "id":       "UCDSP-sZ5khlym4MucLh77Jw",
        "category": ["JEE"],
        "language": "Hindi",
        "priority": 2,
        "active":   True,
    },
    {
        "name":     "Best Approach Manoj Chauhan",
        "id":       "UCr_h4xhYBLawp5bdObn0hbA",
        "category": ["JEE"],
        "language": "Hindi",
        "priority": 3,
        "active":   True,
    },
    {
        "name":     "Mathsmerizing",
        "id":       "UCO0s78XLuof9HKSMpUsxMsg",
        "category": ["JEE"],
        "language": "Hindi",
        "priority": 3,
        "active":   True,
    },
    {
        "name":     "Maths Unplugged",
        "id":       "UCHWna16c7Ff0mY_QBVF2rXQ",
        "category": ["JEE"],
        "language": "Hindi",
        "priority": 3,
        "active":   True,
    },
    {
        "name":     "RZ Maths",
        "id":       "UCvZCNCHoOINkG24aRruHtcQ",
        "category": ["JEE"],
        "language": "Hindi",
        "priority": 3,
        "active":   True,
    },
    {
        "name":     "GB Sir Maths",
        "id":       "UCjILZDfCFrqeU1EQrAm_ZPw",
        "category": ["JEE"],
        "language": "Hindi",
        "priority": 3,
        "active":   True,
    },
    {
        "name":     "Factorial Academy",
        "id":       "UCeSAnGvh_0SXg53on-NQDzQ",
        "category": ["JEE"],
        "language": "Hindi",
        "priority": 3,
        "active":   True,
    },

    # ── NEET SPECIALISTS ──────────────────────────────
    {
        "name":     "NEETprep NCERT",
        "id":       "UC4BjX3BqigeWAOp0kLkKSIA",
        "category": ["NEET"],
        "language": "Hindi",
        "priority": 2,
        "active":   True,
    },
    {
        "name":     "Biomentors Classes Online",
        "id":       "UCwMNVCXcSWNMS0C8rcRCWxA",
        "category": ["NEET"],
        "language": "Hindi",
        "priority": 2,
        "active":   True,
    },
    {
        "name":     "Careerwill NEET",
        "id":       "UCGJJPZRf7mhHqp0X3fpVdyg",
        "category": ["NEET"],
        "language": "Hindi",
        "priority": 2,
        "active":   True,
    },
    {
        "name":     "NEET Adda247",
        "id":       "UC9v_KhFxEX6D4f3oDd9_LIQ",
        "category": ["NEET"],
        "language": "Hindi",
        "priority": 2,
        "active":   True,
    },
    {
        "name":     "Anmol Sharma Biology",
        "id":       "UCoSQ_RjcoEnkAtYCVvX7tfA",
        "category": ["NEET"],
        "language": "Hindi",
        "priority": 3,
        "active":   True,
    },
    {
        "name":     "Biofairy Ritu Rattewal",
        "id":       "UCBlHYBCoCmfqHnZNk5NyVvQ",
        "category": ["NEET"],
        "language": "Hindi",
        "priority": 3,
        "active":   True,
    },
    {
        "name":     "Biology at Ease",
        "id":       "UCYbFCdcMfA68ZvJO__zTUjg",
        "category": ["NEET"],
        "language": "Hindi",
        "priority": 3,
        "active":   True,
    },
    {
        "name":     "Dr. Rakshita Singh",
        "id":       "UCObWXIaGPPVjX_RJgYDbB1w",
        "category": ["NEET"],
        "language": "Hindi",
        "priority": 3,
        "active":   True,
    },
    {
        "name":     "Dr. Parth Goyal",
        "id":       "UCoh-C01mA3H32unyTAOF0NQ",
        "category": ["NEET"],
        "language": "Hindi",
        "priority": 3,
        "active":   True,
    },
    {
        "name":     "Tamanna Chaudhary",
        "id":       "UCLBo1sRUQzDdblEvsytdsig",
        "category": ["NEET"],
        "language": "Hindi",
        "priority": 3,
        "active":   True,
    },
    {
        "name":     "NEET Kaka JEE",
        "id":       "UC3wQ-HF4qpZVEUwWAzgRySw",
        "category": ["NEET", "JEE"],
        "language": "Hindi",
        "priority": 3,
        "active":   True,
    },
]
