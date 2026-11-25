from voice_registry import REAL_VOICES

CATEGORY_PLAN = [
    ("Girl", 45),
    ("Woman", 35),
    ("Boy", 45),
    ("Man", 35),
    ("Cartoon", 20),
    ("Horror", 20),
]

US_VOICE_SEEDS = [
    ("liva", "Liva", "Soft & Sweet", "Girl", "hi_female_sweet", 1.04),
    ("kai", "Kai", "Energetic Youth", "Boy", "en_male_warm", 1.08),
    ("teny", "Teny", "Cute & Bubbly", "Girl", "en_female_clear", 1.12),
    ("rex", "Rex", "Deep Alpha", "Man", "hi_male_deep", 0.90),
    ("aria", "Aria", "Warm Natural", "Woman", "en_female_clear", 0.98),
    ("axel", "Axel", "Cool Gamer", "Boy", "en_male_warm", 1.05),
    ("luna", "Luna", "Dreamy Story", "Girl", "hi_female_sweet", 0.94),
    ("damon", "Damon", "Dark Villain", "Horror", "hi_male_deep", 0.85),
    ("nova", "Nova", "Trending Reels", "Girl", "en_female_clear", 1.10),
    ("leo", "Leo", "Funny Creator", "Cartoon", "en_male_warm", 1.16),
    ("zora", "Zora", "Bold & Classy", "Woman", "hi_female_sweet", 0.96),
    ("zane", "Zane", "Smooth Podcast", "Man", "en_male_warm", 0.95),
    ("chloe", "Chloe", "Sassy Bestie", "Girl", "en_female_clear", 1.08),
    ("blaze", "Blaze", "Action Hero", "Man", "hi_male_deep", 0.96),
    ("maya", "Maya", "Calm Narrator", "Woman", "mr_female_natural", 0.95),
    ("milo", "Milo", "Playful Kid", "Cartoon", "hi_male_deep", 1.18),
    ("bella", "Bella", "Gentle Whisper", "Girl", "hi_female_sweet", 0.92),
    ("knox", "Knox", "True Crime", "Man", "en_male_warm", 0.88),
    ("nori", "Nori", "Anime Star", "Cartoon", "en_female_clear", 1.20),
    ("orion", "Orion", "Shadow Ghost", "Horror", "en_male_warm", 0.82),
    ("skyla", "Skyla", "Bright Morning", "Girl", "en_female_clear", 1.05),
    ("jace", "Jace", "Street Vlog", "Boy", "hi_male_deep", 1.04),
    ("elena", "Elena", "Elegant Host", "Woman", "en_female_clear", 0.97),
    ("raven", "Raven", "Cursed Witch", "Horror", "hi_female_sweet", 0.84),
    ("clara", "Clara", "British Charm", "Woman", "en_female_clear", 0.99),
    ("julian", "Julian", "Tech Reviewer", "Man", "en_male_warm", 1.02),
    ("ruby", "Ruby", "Cheerful Vibe", "Girl", "hi_female_sweet", 1.09),
    ("atlas", "Atlas", "Heavy Trailer", "Man", "hi_male_deep", 0.88),
    ("ivy", "Ivy", "Mystic Fairy", "Cartoon", "hi_female_sweet", 1.15),
    ("drake", "Drake", "Midnight Fear", "Horror", "hi_male_deep", 0.83),
    ("hazel", "Hazel", "Cozy Evening", "Woman", "mr_female_natural", 0.96),
    ("finn", "Finn", "Fast Comedy", "Boy", "en_male_warm", 1.14),
    ("sienna", "Sienna", "Luxury Ad", "Woman", "en_female_clear", 0.95),
    ("cole", "Cole", "Chill Buddy", "Boy", "mr_male_natural", 1.00),
    ("freya", "Freya", "Nordic Queen", "Woman", "en_female_clear", 0.93),
    ("ryder", "Ryder", "Turbo Racer", "Boy", "en_male_warm", 1.11),
    ("stella", "Stella", "Pop Star", "Girl", "en_female_clear", 1.07),
    ("vance", "Vance", "Grim Reaper", "Horror", "en_male_warm", 0.80),
    ("naomi", "Naomi", "News Anchor", "Woman", "hi_female_sweet", 1.00),
    ("troy", "Troy", "Stadium Hype", "Man", "hi_male_deep", 1.06),
]

STYLE_SUFFIXES = [
    ("Lite", 0.00),
    ("Pro", -0.04),
    ("Vibe", 0.05),
    ("Max", -0.07),
    ("Studio", 0.02),
]

def build_200_categories():
    presets = []
    used_ids = set()

    for suffix_label, speed_delta in STYLE_SUFFIXES:
        for base_slug, display_name, tagline, category, base_id, base_speed in US_VOICE_SEEDS:
            if len(presets) >= 200:
                break
            preset_id = f"{base_slug}_{suffix_label.lower()}"
            if preset_id in used_ids:
                continue

            base = REAL_VOICES[base_id]
            final_name = display_name if suffix_label == "Lite" else f"{display_name} {suffix_label}"
            final_speed = round(max(0.78, min(1.28, base_speed + speed_delta)), 2)

            presets.append({
                "id": preset_id,
                "name": final_name,
                "tagline": f"{tagline} • {category}",
                "category": category,
                "base_voice": base_id,
                "language": base["language"],
                "gender": base["gender"],
                "speed": final_speed,
                "is_preset": True,
            })
            used_ids.add(preset_id)

    return presets

ALL_PRESETS = {p["id"]: p for p in build_200_categories()}