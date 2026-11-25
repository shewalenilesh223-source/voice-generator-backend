from voice_registry import REAL_VOICES

CATEGORY_PLAN = [
    ("Natural", 20),
    ("Comedy", 10),
    ("Cinematic", 5),
    ("Storytelling", 5),
    ("International", 5),
    ("Special", 5),
]

FEATURED_PRESETS = [
    {"id": "lira_natural", "name": "Lira", "tagline": "Sweet & Clear", "category": "Natural", "base_id": "hi_female_sweet", "speed": 1.0},
    {"id": "lucas_natural", "name": "Lucas", "tagline": "Warm Podcast", "category": "Natural", "base_id": "en_male_warm", "speed": 0.98},
    {"id": "damon_cinema", "name": "Damon", "tagline": "True Crime", "category": "Cinematic", "base_id": "en_male_warm", "speed": 0.90},
    {"id": "marcus_cinema", "name": "Marcus", "tagline": "Motivational", "category": "Cinematic", "base_id": "hi_male_deep", "speed": 0.95},
    {"id": "leo_comedy", "name": "Leo", "tagline": "Aussie Creator", "category": "Comedy", "base_id": "en_male_warm", "speed": 1.12},
    {"id": "julian_natural", "name": "Julian", "tagline": "Tech Reviewer", "category": "Natural", "base_id": "en_male_warm", "speed": 1.05},
    {"id": "oliver_story", "name": "Oliver", "tagline": "Heartfelt Story", "category": "Storytelling", "base_id": "hi_male_deep", "speed": 0.92},
    {"id": "atlas_cinema", "name": "Atlas", "tagline": "Bold Alpha", "category": "Cinematic", "base_id": "hi_male_deep", "speed": 0.92},
    {"id": "clara_intl", "name": "Clara", "tagline": "British Elegance", "category": "International", "base_id": "en_female_clear", "speed": 0.98},
    {"id": "chloe_comedy", "name": "Chloe", "tagline": "Trending Reels", "category": "Comedy", "base_id": "hi_female_sweet", "speed": 1.15},
    {"id": "elena_story", "name": "Elena", "tagline": "Calm & Soothing", "category": "Storytelling", "base_id": "hi_female_sweet", "speed": 0.90},
    {"id": "maya_natural", "name": "Maya", "tagline": "Smart Explainer", "category": "Natural", "base_id": "mr_female_natural", "speed": 1.02},
]

def build_50_categories():
    presets = []
    used_ids = set()

    for item in FEATURED_PRESETS:
        base = REAL_VOICES[item["base_id"]]
        presets.append({
            "id": item["id"],
            "name": item["name"],
            "tagline": item["tagline"],
            "category": item["category"],
            "base_voice": item["base_id"],
            "language": base["language"],
            "gender": base["gender"],
            "speed": item["speed"],
            "is_preset": True,
        })
        used_ids.add(item["id"])

    base_keys = list(REAL_VOICES.keys())
    counter = 1
    for cat_name, target_count in CATEGORY_PLAN:
        current_count = sum(1 for p in presets if p["category"] == cat_name)
        while current_count < target_count:
            base_id = base_keys[counter % len(base_keys)]
            base = REAL_VOICES[base_id]
            preset_id = f"{cat_name.lower()}_voice_{counter:02d}"
            if preset_id not in used_ids:
                presets.append({
                    "id": preset_id,
                    "name": f"{cat_name} Voice {current_count + 1}",
                    "tagline": f"{cat_name} • {base['gender']}",
                    "category": cat_name,
                    "base_voice": base_id,
                    "language": base["language"],
                    "gender": base["gender"],
                    "speed": round(0.92 + (counter % 4) * 0.06, 2),
                    "is_preset": True,
                })
                used_ids.add(preset_id)
                current_count += 1
            counter += 1

    return presets

ALL_PRESETS = {p["id"]: p for p in build_50_categories()}