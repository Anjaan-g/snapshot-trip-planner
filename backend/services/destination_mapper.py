# fmt: off
import random

from decouple import config
from openai import OpenAI

DESTINATIONS = {
    "beach": [
        {
            "name": "Bora Bora",
            "rank": 5,
            "explanation": "Experience the ultimate tropical escape at Bora Bora, where crystal-clear turquoise lagoons meet lush volcanic peaks. Ideal for snorkeling, overwater bungalows, and romantic getaways.",
            "activities": [
                "Snorkeling",
                "Scuba Diving",
                "Sunbathing",
                "Boat Tours",
                "Jet Skiing",
            ],
            "bestSeason": "May to October",
            "country": "French Polynesia",
            "image": "https://cdn.pixabay.com/photo/2017/01/20/00/30/bora-bora-1992219_1280.jpg",
        },
        {
            "name": "Bondi Beach",
            "rank": 4,
            "explanation": "Surf’s up at Bondi Beach, Australia’s world-famous coastal hotspot. Enjoy vibrant beach culture, great waves, and scenic coastal walks alongside bustling cafes.",
            "activities": [
                "Surfing",
                "Swimming",
                "Beach Volleyball",
                "Coastal Walks",
                "Dining",
            ],
            "bestSeason": "December to February",
            "country": "Australia",
            "image": "https://cdn.pixabay.com/photo/2016/11/21/15/46/australia-1846319_1280.jpg",
        },
        {
            "name": "Maui",
            "rank": 3,
            "explanation": "Maui offers a perfect blend of relaxing beaches and adventurous volcano hikes. Swim with sea turtles, explore waterfalls, or unwind on golden sands.",
            "activities": [
                "Snorkeling",
                "Hiking",
                "Whale Watching",
                "Beach Relaxation",
                "Helicopter Tours",
            ],
            "bestSeason": "April to May, September to November",
            "country": "USA (Hawaii)",
            "image": "https://cdn.pixabay.com/photo/2016/07/21/00/22/maui-1530551_1280.jpg",
        },
        {
            "name": "Phuket",
            "rank": 2,
            "explanation": "Phuket blends tropical beaches with vibrant nightlife and cultural experiences, offering both relaxation and lively entertainment.",
            "activities": [
                "Beach Parties",
                "Snorkeling",
                "Island Hopping",
                "Night Markets",
                "Thai Cooking Classes",
            ],
            "bestSeason": "November to April",
            "country": "Thailand",
            "image": "https://cdn.pixabay.com/photo/2016/11/29/05/09/phuket-1866734_1280.jpg",
        },
        {
            "name": "Zanzibar",
            "rank": 1,
            "explanation": "Zanzibar offers historic spice markets, pristine beaches, and turquoise waters perfect for swimming, diving, and cultural exploration.",
            "activities": [
                "Snorkeling",
                "Diving",
                "Cultural Tours",
                "Beach Relaxation",
                "Spice Tours",
            ],
            "bestSeason": "June to October",
            "country": "Tanzania",
            "image": "https://cdn.pixabay.com/photo/2018/01/18/11/42/zanzibar-3080104_1280.jpg",
        },
    ],
    "mountain": [
        {
            "name": "Swiss Alps",
            "rank": 5,
            "explanation": "The Swiss Alps offer breathtaking alpine views, world-class skiing, and charming mountain villages. Ideal for winter sports and summer hiking adventures.",
            "activities": [
                "Skiing",
                "Snowboarding",
                "Hiking",
                "Paragliding",
                "Mountain Biking",
            ],
            "bestSeason": "December to March (winter), June to September (summer)",
            "country": "Switzerland",
            "image": "https://cdn.pixabay.com/photo/2017/03/27/14/56/alps-2178718_1280.jpg",
        },
        {
            "name": "Rocky Mountains",
            "rank": 4,
            "explanation": "Explore vast wilderness with diverse wildlife and rugged terrain in the Rocky Mountains. Perfect for hiking, camping, and photography enthusiasts.",
            "activities": [
                "Hiking",
                "Wildlife Watching",
                "Camping",
                "Fishing",
                "Skiing",
            ],
            "bestSeason": "June to September",
            "country": "USA/Canada",
            "image": "https://cdn.pixabay.com/photo/2016/11/29/04/09/rocky-mountains-1868656_1280.jpg",
        },
        {
            "name": "Himalayas",
            "rank": 3,
            "explanation": "The Himalayas, home to Mount Everest, offer awe-inspiring trekking and spiritual experiences for adventurers and nature lovers alike.",
            "activities": [
                "Trekking",
                "Mountaineering",
                "Meditation",
                "Camping",
                "Cultural Tours",
            ],
            "bestSeason": "March to June, September to November",
            "country": "Nepal/India/Bhutan",
            "image": "https://cdn.pixabay.com/photo/2017/09/05/21/22/mountains-2716932_1280.jpg",
        },
        {
            "name": "Andes",
            "rank": 2,
            "explanation": "Stretching along South America’s spine, the Andes are rich with history, challenging hikes, and incredible landscapes from deserts to glaciers.",
            "activities": [
                "Hiking",
                "Cultural Visits",
                "Mountain Biking",
                "Bird Watching",
                "Camping",
            ],
            "bestSeason": "May to September",
            "country": "South America (Peru, Chile, Argentina, etc.)",
            "image": "https://cdn.pixabay.com/photo/2017/06/24/08/53/mountains-2430547_1280.jpg",
        },
        {
            "name": "Dolomites",
            "rank": 1,
            "explanation": "The Dolomites offer stunning limestone peaks, alpine meadows, and outdoor sports like climbing and skiing in a historic Italian setting.",
            "activities": [
                "Rock Climbing",
                "Hiking",
                "Skiing",
                "Mountain Biking",
                "Photography",
            ],
            "bestSeason": "June to September, December to March",
            "country": "Italy",
            "image": "https://cdn.pixabay.com/photo/2018/03/06/17/15/mountains-3207353_1280.jpg",
        },
    ],
    "forest": [
        {
            "name": "Amazon Rainforest",
            "rank": 5,
            "explanation": "Dive into the world’s largest tropical rainforest, abundant with wildlife and exotic plants. A paradise for eco-tourism and river adventures.",
            "activities": [
                "Wildlife Watching",
                "Boat Tours",
                "Jungle Trekking",
                "Bird Watching",
                "Photography",
            ],
            "bestSeason": "July to December",
            "country": "Brazil/Peru/Colombia",
            "image": "https://cdn.pixabay.com/photo/2016/06/24/10/47/amazon-1479033_1280.jpg",
        },
        {
            "name": "Black Forest",
            "rank": 4,
            "explanation": "The Black Forest enchants visitors with its dense evergreen trees, quaint villages, and rich folklore. Ideal for hiking and cultural exploration.",
            "activities": [
                "Hiking",
                "Cycling",
                "Cultural Tours",
                "Photography",
                "Wine Tasting",
            ],
            "bestSeason": "May to October",
            "country": "Germany",
            "image": "https://cdn.pixabay.com/photo/2017/05/31/19/10/black-forest-2369310_1280.jpg",
        },
        {
            "name": "Redwood National Park",
            "rank": 3,
            "explanation": "Stand among the tallest trees on Earth at Redwood National Park. Perfect for serene walks, wildlife spotting, and reconnecting with nature.",
            "activities": [
                "Hiking",
                "Camping",
                "Wildlife Watching",
                "Photography",
                "Picnicking",
            ],
            "bestSeason": "June to September",
            "country": "USA (California)",
            "image": "https://cdn.pixabay.com/photo/2017/06/23/20/18/redwood-2438876_1280.jpg",
        },
        {
            "name": "Yakushima",
            "rank": 2,
            "explanation": "Mystical ancient cedar forests and waterfalls define Yakushima, making it a magical destination for nature lovers and hikers.",
            "activities": [
                "Hiking",
                "Waterfall Visits",
                "Wildlife Watching",
                "Photography",
            ],
            "bestSeason": "April to November",
            "country": "Japan",
            "image": "https://cdn.pixabay.com/photo/2018/07/26/19/35/japan-3558370_1280.jpg",
        },
        {
            "name": "Białowieża Forest",
            "rank": 1,
            "explanation": "Białowieża is one of Europe’s last and largest remaining primeval forests, home to European bison and pristine ecosystems.",
            "activities": [
                "Wildlife Watching",
                "Hiking",
                "Nature Tours",
                "Photography",
            ],
            "bestSeason": "May to September",
            "country": "Poland/Belarus",
            "image": "https://cdn.pixabay.com/photo/2018/08/01/10/47/european-bison-3576648_1280.jpg",
        },
    ],
    "city": [
        {
            "name": "New York City",
            "rank": 5,
            "explanation": "The city that never sleeps offers iconic landmarks, vibrant culture, endless entertainment, and diverse culinary experiences.",
            "activities": [
                "Sightseeing",
                "Broadway Shows",
                "Museum Visits",
                "Shopping",
                "Dining",
            ],
            "bestSeason": "April to June, September to November",
            "country": "USA",
            "image": "https://cdn.pixabay.com/photo/2016/11/29/06/15/new-york-1866736_1280.jpg",
        },
        {
            "name": "Tokyo",
            "rank": 4,
            "explanation": "Tokyo blends futuristic innovation with deep-rooted tradition, bustling streets, and world-class food scenes.",
            "activities": [
                "Temple Visits",
                "Shopping",
                "Dining",
                "Tech Tours",
                "Cultural Events",
            ],
            "bestSeason": "March to May, October to November",
            "country": "Japan",
            "image": "https://cdn.pixabay.com/photo/2017/02/12/20/29/tokyo-2061211_1280.jpg",
        },
        {
            "name": "Paris",
            "rank": 3,
            "explanation": "Paris charms with romantic streets, iconic landmarks, museums, and gourmet cuisine that define European elegance.",
            "activities": [
                "Museum Tours",
                "Sightseeing",
                "Dining",
                "Shopping",
                "Cruise on Seine",
            ],
            "bestSeason": "April to June, September to November",
            "country": "France",
            "image": "https://cdn.pixabay.com/photo/2015/03/26/09/39/eiffel-tower-690293_1280.jpg",
        },
        {
            "name": "London",
            "rank": 2,
            "explanation": "London’s rich history, theaters, parks, and multicultural vibe make it a captivating global city to explore.",
            "activities": [
                "Sightseeing",
                "Museum Visits",
                "Theater",
                "Dining",
                "Shopping",
            ],
            "bestSeason": "May to September",
            "country": "UK",
            "image": "https://cdn.pixabay.com/photo/2015/03/30/12/37/london-698697_1280.jpg",
        },
        {
            "name": "Dubai",
            "rank": 1,
            "explanation": "Dubai dazzles with futuristic architecture, luxury shopping, desert adventures, and world-class entertainment.",
            "activities": [
                "Desert Safaris",
                "Shopping",
                "Sightseeing",
                "Beach Visits",
                "Dining",
            ],
            "bestSeason": "November to March",
            "country": "UAE",
            "image": "https://cdn.pixabay.com/photo/2015/01/03/10/49/dubai-587043_1280.jpg",
        },
    ],
    "desert": [
        {
            "name": "Sahara Desert",
            "rank": 5,
            "explanation": "The Sahara is the largest hot desert on Earth, offering vast dunes, camel treks, and starlit nights unlike any other.",
            "activities": [
                "Camel Trekking",
                "Camping",
                "Sandboarding",
                "Cultural Tours",
                "Photography",
            ],
            "bestSeason": "October to April",
            "country": "North Africa",
            "image": "https://cdn.pixabay.com/photo/2017/07/31/23/44/desert-2556663_1280.jpg",
        },
        {
            "name": "Namib Desert",
            "rank": 4,
            "explanation": "Namib Desert is known for towering red dunes and unique desert-adapted wildlife in an otherworldly landscape.",
            "activities": [
                "Dune Climbing",
                "Wildlife Tours",
                "Photography",
                "Sandboarding",
            ],
            "bestSeason": "May to September",
            "country": "Namibia",
            "image": "https://cdn.pixabay.com/photo/2016/02/19/10/00/namib-desert-1214327_1280.jpg",
        },
        {
            "name": "Gobi Desert",
            "rank": 3,
            "explanation": "The Gobi features dramatic dunes, ancient fossils, and vast steppe landscapes offering a raw and rugged adventure.",
            "activities": [
                "Camel Trekking",
                "Fossil Tours",
                "Cultural Visits",
                "Hiking",
            ],
            "bestSeason": "May to September",
            "country": "Mongolia/China",
            "image": "https://cdn.pixabay.com/photo/2016/02/22/23/37/desert-1216536_1280.jpg",
        },
        {
            "name": "Atacama Desert",
            "rank": 2,
            "explanation": "The Atacama is the driest non-polar desert, famous for stargazing, salt flats, and unique desert landscapes.",
            "activities": ["Stargazing", "Hiking", "Salt Flats Tours", "Photography"],
            "bestSeason": "March to May, September to November",
            "country": "Chile",
            "image": "https://cdn.pixabay.com/photo/2015/11/05/00/44/desert-1023313_1280.jpg",
        },
        {
            "name": "Mojave Desert",
            "rank": 1,
            "explanation": "Home to iconic Joshua Trees, the Mojave Desert offers unique flora, hiking trails, and proximity to Las Vegas excitement.",
            "activities": ["Hiking", "Wildlife Watching", "Camping", "Photography"],
            "bestSeason": "March to May, September to November",
            "country": "USA",
            "image": "https://cdn.pixabay.com/photo/2014/11/05/17/26/joshua-tree-518543_1280.jpg",
        },
    ],
    "waterfall": [
        {
            "name": "Niagara Falls",
            "rank": 5,
            "explanation": "Niagara Falls is one of the most famous waterfalls worldwide, offering powerful cascades and popular boat tours.",
            "activities": [
                "Boat Tours",
                "Sightseeing",
                "Photography",
                "Hiking",
                "Visiting Observation Decks",
            ],
            "bestSeason": "June to August",
            "country": "USA/Canada",
            "image": "https://cdn.pixabay.com/photo/2016/08/11/23/46/niagara-falls-1584895_1280.jpg",
        },
        {
            "name": "Iguazu Falls",
            "rank": 4,
            "explanation": "Located on the border of Argentina and Brazil, Iguazu Falls boasts a vast network of powerful waterfalls surrounded by rainforest.",
            "activities": ["Boat Tours", "Hiking", "Wildlife Watching", "Photography"],
            "bestSeason": "March to May, August to October",
            "country": "Argentina/Brazil",
            "image": "https://cdn.pixabay.com/photo/2017/04/15/11/24/iguazu-falls-2223989_1280.jpg",
        },
        {
            "name": "Victoria Falls",
            "rank": 3,
            "explanation": "Known locally as 'The Smoke That Thunders,' Victoria Falls impresses with its massive curtain of water and dramatic views.",
            "activities": [
                "Boat Tours",
                "Bungee Jumping",
                "Hiking",
                "Wildlife Viewing",
                "Helicopter Rides",
            ],
            "bestSeason": "February to May",
            "country": "Zambia/Zimbabwe",
            "image": "https://cdn.pixabay.com/photo/2018/04/18/22/01/victoria-falls-3339087_1280.jpg",
        },
        {
            "name": "Angel Falls",
            "rank": 2,
            "explanation": "Angel Falls is the world’s highest uninterrupted waterfall, located deep in Venezuela’s jungle offering a remote adventure.",
            "activities": ["Trekking", "Boat Trips", "Camping", "Photography"],
            "bestSeason": "December to April",
            "country": "Venezuela",
            "image": "https://cdn.pixabay.com/photo/2018/06/05/15/28/venezuela-3457814_1280.jpg",
        },
        {
            "name": "Plitvice Lakes",
            "rank": 1,
            "explanation": "Croatia’s Plitvice Lakes National Park features cascading waterfalls, turquoise lakes, and lush forest trails.",
            "activities": ["Hiking", "Photography", "Boat Rides", "Nature Watching"],
            "bestSeason": "April to October",
            "country": "Croatia",
            "image": "https://cdn.pixabay.com/photo/2015/11/07/11/49/plitvice-1028800_1280.jpg",
        },
    ],
    "lake": [
        {
            "name": "Lake Tahoe",
            "rank": 5,
            "explanation": "Nestled in the Sierra Nevada, Lake Tahoe offers crystal-clear waters, skiing, hiking, and vibrant lakeside towns.",
            "activities": ["Skiing", "Boating", "Hiking", "Swimming", "Fishing"],
            "bestSeason": "June to September (summer), December to March (winter)",
            "country": "USA",
            "image": "https://cdn.pixabay.com/photo/2016/11/18/19/43/lake-tahoe-1836036_1280.jpg",
        },
        {
            "name": "Lake Baikal",
            "rank": 4,
            "explanation": "Lake Baikal is the world’s deepest and oldest freshwater lake, renowned for its unique biodiversity and icy winter scenery.",
            "activities": ["Hiking", "Boating", "Ice Skating", "Wildlife Watching"],
            "bestSeason": "June to September",
            "country": "Russia",
            "image": "https://cdn.pixabay.com/photo/2017/02/28/10/38/lake-baikal-2109969_1280.jpg",
        },
        {
            "name": "Lake Como",
            "rank": 3,
            "explanation": "Famous for its scenic beauty, Lake Como is surrounded by mountains, charming villages, and luxurious villas.",
            "activities": ["Boating", "Sightseeing", "Dining", "Hiking", "Shopping"],
            "bestSeason": "April to June, September to October",
            "country": "Italy",
            "image": "https://cdn.pixabay.com/photo/2017/01/06/19/15/lake-como-1953569_1280.jpg",
        },
        {
            "name": "Crater Lake",
            "rank": 2,
            "explanation": "Located in Oregon, Crater Lake is known for its deep blue water, volcanic origins, and stunning surrounding cliffs.",
            "activities": ["Hiking", "Photography", "Boat Tours", "Camping"],
            "bestSeason": "July to September",
            "country": "USA",
            "image": "https://cdn.pixabay.com/photo/2015/03/26/10/02/crater-lake-690029_1280.jpg",
        },
        {
            "name": "Lake Victoria",
            "rank": 1,
            "explanation": "Africa’s largest lake, Lake Victoria supports diverse cultures and wildlife, making it a vital and scenic destination.",
            "activities": [
                "Fishing",
                "Boat Tours",
                "Wildlife Watching",
                "Cultural Visits",
            ],
            "bestSeason": "June to September",
            "country": "Tanzania/Uganda/Kenya",
            "image": "https://cdn.pixabay.com/photo/2017/08/02/10/47/lake-2569329_1280.jpg",
        },
    ],
}

# fmt: on


def get_destination(scene_type: str) -> dict:
    """
    Randomly returns a destination for the detected scene type
    """
    if scene_type not in DESTINATIONS:
        return {
            "name": "Unknown",
            "rank": 0,
            "explanation": "No destination available.",
        }

    return random.choice(DESTINATIONS[scene_type])


def get_similar_destinations(scene_type: str, exclude: str = None):
    candidates = DESTINATIONS.get(scene_type, [])

    # Exclude the top destination by name
    filtered = [
        dest for dest in candidates if dest["name"].lower() != (exclude or "").lower()
    ]

    # Optional: shuffle or re-rank
    return sorted(filtered, key=lambda d: d["rank"])[:3]


def get_all_destinations():
    all_destinations = []
    for scene_type, destinations in DESTINATIONS.items():
        for dest in destinations:
            all_destinations.append({**dest, "scene_type": scene_type})
    return all_destinations


def generate_scene_explanation(
    scene_type: str, detected_scenes: list, use_api: bool = False
) -> str:
    """
    Generate a basic or AI-generated explanation for a travel scene.

    If use_api is True, tries to call OpenAI-compatible API (future support).
    """
    if not detected_scenes:
        return "No scenes detected to describe."

    scene_objects = ", ".join(detected_scenes[0:5])

    if use_api:
        try:
            # Placeholder for OpenAI or OpenRouter integration
            client = OpenAI(api_key=config("OPENAI_API_KEY"))
            prompt = f"""
                Scene type: {scene_type}
                Detected objects: {scene_objects}

                Explain in 2–3 sentences why this image suggests a travel destination like {scene_type}.
                Be descriptive and connect the visual elements to the destination choice.
            """
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": "You are an intelligent travel assistant.",
                    },
                    {"role": "user", "content": prompt},
                ],
                temperature=0.7,
                max_tokens=120,
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            return f"AI explanation unavailable: {str(e)}"

    # 🔁 Local Fallback (Basic Template-Based Logic)
    template = (
        f"This image suggests a travel destination related to {scene_type} "
        f"because it contains elements like {scene_objects}. "
        f"These features are typically found in places known for {scene_type.lower()} experiences."
    )

    return template
