from flask import Flask, render_template, request, redirect, url_for, session, flash,jsonify
from flask_mail import Mail, Message
import pyodbc
import time
from datetime import datetime
import secrets
from flask_cors import CORS


app = Flask(__name__)
app.secret_key = secrets.token_hex(16)  # Generates a 32-character hexadecimal secret key

DB_CONNECTION = "Driver={SQL Server};Server=WLI223X8;Database=TravelDB;Trusted_Connection=yes;"

def get_db_connection():
    return pyodbc.connect(DB_CONNECTION)

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'violahencel2002@gmail.com'
app.config['MAIL_PASSWORD'] = 'rogc peyn utgr oeww'
mail = Mail(app)

login_attempts = {}
place_details = {
    1: {
        "name": "Kashmir",
        "details": """Kashmir, known as 'Paradise on Earth,' offers scenic landscapes, pristine valleys, serene lakes, and snow-capped mountains.""",
        "image": "kashmir.jpg",
        "pricing": "₹20,000 for budget travelers, ₹40,000 for mid-range travelers, and ₹70,000 for luxury travelers (per person for 5 days).",
        "itinerary": {
            "low": [
                "Day 1: Arrival in Srinagar and budget houseboat stay.",
                "Day 2: Day trip to Gulmarg with local transport.",
                "Day 3: Visit Pahalgam and Betaab Valley on a shared cab.",
                "Day 4: Stroll through Mughal Gardens.",
                "Day 5: Departure."
            ],
            "medium": [
                "Day 1: Arrival in Srinagar with a stay in a premium houseboat.",
                "Day 2: Private tour to Gulmarg with a cable car ride.",
                "Day 3: Visit Pahalgam and Lidder River in a guided tour.",
                "Day 4: Explore Dal Lake and Shankaracharya Temple.",
                "Day 5: Departure."
            ],
            "high": [
                "Day 1: Arrival with luxury accommodation in Srinagar.",
                "Day 2: Private guided tour to Gulmarg and gondola ride.",
                "Day 3: Visit Aru Valley and enjoy leisure time at Lidder River.",
                "Day 4: Private shikara ride on Dal Lake.",
                "Day 5: Departure."
            ]
        }
    },
    2: {
        "name": "Udaipur",
        "details": """Udaipur, the City of Lakes, is renowned for its royal palaces, serene lakes, and vibrant culture.""",
        "image": "udaipur.jpg",
        "pricing": "₹15,000 for budget travelers, ₹35,000 for mid-range travelers, and ₹60,000 for luxury travelers (per person for 5 days).",
        "itinerary": {
            "low": [
                "Day 1: Arrival and local sightseeing on public transport.",
                "Day 2: Explore City Palace and Fateh Sagar Lake.",
                "Day 3: Visit Jagdish Temple and Saheliyon Ki Bari.",
                "Day 4: Day trip to Haldighati using budget transport.",
                "Day 5: Departure."
            ],
            "medium": [
                "Day 1: Arrival with a mid-range hotel stay.",
                "Day 2: Guided tour of City Palace and Lake Pichola.",
                "Day 3: Visit Kumbhalgarh Fort with a group.",
                "Day 4: Explore Shilpgram and local bazaars.",
                "Day 5: Departure."
            ],
            "high": [
                "Day 1: Arrival with luxury hotel stay near Lake Pichola.",
                "Day 2: Private boat ride on Lake Pichola and dinner at a heritage hotel.",
                "Day 3: Visit Eklingji Temple and Nathdwara with a private chauffeur.",
                "Day 4: Private cultural evening at Bagore Ki Haveli.",
                "Day 5: Departure."
            ]
        }
    },
    3: {
        "name": "Kerala",
        "details": """Kerala, known as 'God's Own Country,' is famous for its backwaters, lush greenery, and unique culture.""",
        "image": "kerala.jpg",
        "pricing": "₹18,000 for budget travelers, ₹40,000 for mid-range travelers, and ₹75,000 for luxury travelers (per person for 5 days).",
        "itinerary": {
            "low": [
                "Day 1: Arrival in Cochin and stay in a budget homestay.",
                "Day 2: Alleppey backwaters day cruise.",
                "Day 3: Explore Munnar and tea plantations via shared transport.",
                "Day 4: Visit Periyar Wildlife Sanctuary with a group.",
                "Day 5: Departure."
            ],
            "medium": [
                "Day 1: Arrival with a stay in a premium hotel in Cochin.",
                "Day 2: Overnight houseboat stay in Alleppey.",
                "Day 3: Private tour of Munnar's attractions.",
                "Day 4: Guided tour of Periyar Wildlife Sanctuary.",
                "Day 5: Departure."
            ],
            "high": [
                "Day 1: Arrival with a stay in a luxury resort in Cochin.",
                "Day 2: Private luxury houseboat experience in Alleppey.",
                "Day 3: Explore Munnar's tea gardens with a private guide.",
                "Day 4: Exclusive wildlife tour at Periyar Sanctuary.",
                "Day 5: Departure."
            ]
        }
    },
    4: {
        "name": "Shimla",
        "details": """Shimla, the Queen of Hills, is known for its colonial architecture, pleasant weather, and scenic beauty.""",
        "image": "shimla.jpg",
        "pricing": "₹10,000 for budget travelers, ₹25,000 for mid-range travelers, and ₹50,000 for luxury travelers (per person for 5 days).",
        "itinerary": {
            "low": [
                "Day 1: Arrival and explore Mall Road on foot.",
                "Day 2: Visit Kufri and Jakhoo Temple using shared transport.",
                "Day 3: Day trip to Mashobra and Naldehra.",
                "Day 4: Stroll through Lakkar Bazaar and Ridge Road.",
                "Day 5: Departure."
            ],
            "medium": [
                "Day 1: Arrival with a stay in a mid-range resort.",
                "Day 2: Guided tour of Kufri and Jakhoo Temple.",
                "Day 3: Visit Narkanda and enjoy scenic views.",
                "Day 4: Explore Annandale and Shimla State Museum.",
                "Day 5: Departure."
            ],
            "high": [
                "Day 1: Arrival with luxury accommodation in Shimla.",
                "Day 2: Private guided tour of Kufri and apple orchards.",
                "Day 3: Visit Chail Palace with a private guide.",
                "Day 4: Exclusive cultural experience at Himachal Art Gallery.",
                "Day 5: Departure."
            ]
        }
    },
    5: {
        "name": "Bali",
        "details": """Bali, the Island of Gods, is renowned for its beaches, temples, and vibrant nightlife.""",
        "image": "bali.jpg",
        "pricing": "₹25,000 for budget travelers, ₹60,000 for mid-range travelers, and ₹1,00,000 for luxury travelers (per person for 5 days).",
        "itinerary": {
            "low": [
                "Day 1: Arrival and budget stay in Kuta.",
                "Day 2: Explore Uluwatu Temple and nearby beaches using public transport.",
                "Day 3: Day trip to Ubud with shared transport.",
                "Day 4: Visit Tanah Lot Temple and Seminyak Beach.",
                "Day 5: Departure."
            ],
            "medium": [
                "Day 1: Arrival with a mid-range villa stay.",
                "Day 2: Guided tour of Uluwatu Temple and Kecak Dance show.",
                "Day 3: Explore Ubud and Monkey Forest with a private guide.",
                "Day 4: Visit Nusa Penida for snorkeling and beaches.",
                "Day 5: Departure."
            ],
            "high": [
                "Day 1: Arrival with a luxury beachfront villa.",
                "Day 2: Private helicopter ride and Uluwatu Temple visit.",
                "Day 3: Exclusive spa day and Ubud cultural tour.",
                "Day 4: Luxury yacht tour to Nusa Penida.",
                "Day 5: Departure."
            ]
        }
    },
        6: {
        "name": "Vietnam",
        "details": """Vietnam offers a perfect blend of natural wonders, historical landmarks, and rich cultural experiences. Explore its vibrant cities, scenic beaches, and tranquil countryside.""",
        "image": "vietnam.jpg",
        "pricing": "₹30,000 for budget travelers, ₹55,000 for mid-range travelers, and ₹90,000 for luxury travelers (per person for 5 days).",
        "itinerary": {
            "low": [
                "Day 1: Arrival in Hanoi and explore Old Quarter on foot.",
                "Day 2: Budget cruise on Halong Bay.",
                "Day 3: Visit Hoi An's ancient town using local transport.",
                "Day 4: Explore Cu Chi Tunnels near Ho Chi Minh City.",
                "Day 5: Departure."
            ],
            "medium": [
                "Day 1: Arrival and stay in a mid-range hotel in Hanoi.",
                "Day 2: Halong Bay overnight cruise.",
                "Day 3: Fly to Da Nang and visit Hoi An with a guided tour.",
                "Day 4: Explore Ho Chi Minh City's War Remnants Museum and Cu Chi Tunnels.",
                "Day 5: Departure."
            ],
            "high": [
                "Day 1: Arrival and stay in a luxury resort in Hanoi.",
                "Day 2: Exclusive private Halong Bay cruise.",
                "Day 3: Guided luxury tour of Hoi An and My Son Sanctuary.",
                "Day 4: Private city tour of Ho Chi Minh City and Mekong Delta excursion.",
                "Day 5: Departure."
            ]
        }
    },
    7: {
        "name": "Malaysia",
        "details": """Malaysia is a cultural melting pot with modern cities, beautiful beaches, and lush rainforests. Enjoy its blend of tradition and modernity.""",
        "image": "malaysia.jpg",
        "pricing": "₹25,000 for budget travelers, ₹50,000 for mid-range travelers, and ₹80,000 for luxury travelers (per person for 5 days).",
        "itinerary": {
            "low": [
                "Day 1: Arrival in Kuala Lumpur and explore using public transport.",
                "Day 2: Visit Batu Caves and Petronas Towers.",
                "Day 3: Explore Malacca city on a budget tour.",
                "Day 4: Free time at Langkawi beaches.",
                "Day 5: Departure."
            ],
            "medium": [
                "Day 1: Arrival and stay in a mid-range hotel in Kuala Lumpur.",
                "Day 2: Guided tour of Batu Caves and city landmarks.",
                "Day 3: Visit Langkawi Island and enjoy a guided beach tour.",
                "Day 4: Explore George Town in Penang.",
                "Day 5: Departure."
            ],
            "high": [
                "Day 1: Arrival and stay at a luxury hotel in Kuala Lumpur.",
                "Day 2: Private guided tour of Batu Caves and city landmarks.",
                "Day 3: Fly to Langkawi for a luxury beach stay.",
                "Day 4: Explore Penang with a private guide and fine dining.",
                "Day 5: Departure."
            ]
        }
    },
    8: {
        "name": "Singapore",
        "details": """Singapore, a modern city-state, is renowned for its futuristic skyline, vibrant nightlife, and cultural diversity. It offers a mix of urban attractions and lush gardens.""",
        "image": "singapore.jpg",
        "pricing": "₹35,000 for budget travelers, ₹65,000 for mid-range travelers, and ₹1,00,000 for luxury travelers (per person for 5 days).",
        "itinerary": {
            "low": [
                "Day 1: Arrival and explore Chinatown and Little India.",
                "Day 2: Visit Gardens by the Bay and Marina Bay Sands (free observation deck).",
                "Day 3: Explore Sentosa Island using public transport.",
                "Day 4: Walk along Orchard Road and Clarke Quay.",
                "Day 5: Departure."
            ],
            "medium": [
                "Day 1: Arrival and stay in a mid-range hotel near Marina Bay.",
                "Day 2: Visit Universal Studios and Sentosa Island attractions.",
                "Day 3: Guided tour of Gardens by the Bay and Marina Bay Sands SkyPark.",
                "Day 4: Explore Jurong Bird Park and enjoy a river cruise.",
                "Day 5: Departure."
            ],
            "high": [
                "Day 1: Arrival and stay at a luxury hotel near Marina Bay Sands.",
                "Day 2: Private tour of Gardens by the Bay and Universal Studios.",
                "Day 3: Exclusive yacht tour to Sentosa Island.",
                "Day 4: Gourmet dining experience and private cultural tour.",
                "Day 5: Departure."
            ]
        }
    },
    9: {
        "name": "Thailand",
        "details": """Thailand is a vibrant destination known for its tropical beaches, royal palaces, ancient ruins, and bustling markets.""",
        "image": "thailand.jpg",
        "pricing": "₹30,000 for budget travelers, ₹60,000 for mid-range travelers, and ₹1,00,000 for luxury travelers (per person for 5 days).",
        "itinerary": {
            "low": [
                "Day 1: Arrival in Bangkok and explore temples like Wat Arun using public transport.",
                "Day 2: Visit Chatuchak Market and enjoy street food.",
                "Day 3: Day trip to Ayutthaya with local transport.",
                "Day 4: Explore Pattaya and its beaches.",
                "Day 5: Departure."
            ],
            "medium": [
                "Day 1: Arrival with a stay in a mid-range hotel in Bangkok.",
                "Day 2: Guided tour of Grand Palace and floating markets.",
                "Day 3: Visit Ayutthaya with a guided tour.",
                "Day 4: Fly to Phuket for beach exploration.",
                "Day 5: Departure."
            ],
            "high": [
                "Day 1: Arrival and stay in a luxury hotel in Bangkok.",
                "Day 2: Private tour of Bangkok’s temples and cultural landmarks.",
                "Day 3: Exclusive yacht tour of Ayutthaya.",
                "Day 4: Private villa stay in Phuket with spa services.",
                "Day 5: Departure."
            ]
        }
    },
    10: {
        "name": "Dubai",
        "details": """Dubai is a city of luxury and innovation, featuring iconic skyscrapers, man-made islands, and world-class shopping experiences.""",
        "image": "dubai.jpg",
        "pricing": "₹40,000 for budget travelers, ₹80,000 for mid-range travelers, and ₹1,50,000 for luxury travelers (per person for 5 days).",
        "itinerary": {
            "low": [
                "Day 1: Arrival and visit Dubai Mall using local transport.",
                "Day 2: View Burj Khalifa from outside and explore Old Dubai.",
                "Day 3: Visit Dubai Marina and JBR beach.",
                "Day 4: Desert safari with shared transport.",
                "Day 5: Departure."
            ],
            "medium": [
                "Day 1: Arrival and stay in a mid-range hotel in Downtown Dubai.",
                "Day 2: Burj Khalifa observation deck and Dubai Mall guided tour.",
                "Day 3: Private desert safari and cultural show.",
                "Day 4: Explore Palm Jumeirah and Atlantis.",
                "Day 5: Departure."
            ],
            "high": [
                "Day 1: Arrival and stay at a luxury hotel near Burj Khalifa.",
                "Day 2: Exclusive access to Burj Khalifa Sky Lounge and VIP Dubai Mall tour.",
                "Day 3: Private desert safari and luxury camp experience.",
                "Day 4: Helicopter tour of Dubai and fine dining.",
                "Day 5: Departure."
            ]
        }
    },
        11: {
        "name": "Japan",
        "details": """Japan is a land of contrasts, where ancient traditions coexist with cutting-edge technology. Experience its historic temples, serene gardens, and bustling urban centers.""",
        "image": "japan.jpg",
        "pricing": "₹70,000 for budget travelers, ₹1,20,000 for mid-range travelers, and ₹2,00,000 for luxury travelers (per person for 5 days).",
        "itinerary": {
            "low": [
                "Day 1: Arrival in Tokyo and explore Shinjuku and Asakusa on foot.",
                "Day 2: Visit Meiji Shrine and enjoy street food at Harajuku.",
                "Day 3: Day trip to Mount Fuji using public transport.",
                "Day 4: Explore Osaka Castle and Dotonbori district.",
                "Day 5: Departure."
            ],
            "medium": [
                "Day 1: Arrival and stay in a mid-range hotel in Tokyo.",
                "Day 2: Guided tour of Meiji Shrine and Harajuku.",
                "Day 3: Private transport to Mount Fuji and Hakone.",
                "Day 4: Visit Kyoto's temples and bamboo forests.",
                "Day 5: Departure."
            ],
            "high": [
                "Day 1: Arrival and stay in a luxury hotel in Tokyo.",
                "Day 2: Private guided tours of Tokyo’s landmarks.",
                "Day 3: Exclusive trip to Mount Fuji with fine dining.",
                "Day 4: Private cultural tour of Kyoto and Osaka.",
                "Day 5: Departure."
            ]
        }
    },
    12: {
        "name": "South Korea",
        "details": """South Korea is a fascinating blend of ancient traditions and modern advancements. Discover its historic palaces, K-pop culture, and scenic landscapes.""",
        "image": "southkorea.jpg",
        "pricing": "₹60,000 for budget travelers, ₹1,00,000 for mid-range travelers, and ₹1,80,000 for luxury travelers (per person for 5 days).",
        "itinerary": {
            "low": [
                "Day 1: Arrival in Seoul and explore Gyeongbokgung Palace.",
                "Day 2: Visit Bukchon Hanok Village and local markets.",
                "Day 3: Day trip to Nami Island using public transport.",
                "Day 4: Explore Myeongdong shopping district.",
                "Day 5: Departure."
            ],
            "medium": [
                "Day 1: Arrival and stay in a mid-range hotel in Seoul.",
                "Day 2: Guided tour of Gyeongbokgung Palace and Insadong.",
                "Day 3: Day trip to Nami Island with guided transport.",
                "Day 4: Explore Gangnam and COEX Mall.",
                "Day 5: Departure."
            ],
            "high": [
                "Day 1: Arrival and stay in a luxury hotel in Seoul.",
                "Day 2: Private guided tours of Seoul’s cultural landmarks.",
                "Day 3: Exclusive day trip to Nami Island and Petite France.",
                "Day 4: Personalized K-pop experience and fine dining.",
                "Day 5: Departure."
            ]
        }
    },
    13: {
        "name": "Paris",
        "details": """Paris, the City of Love, is known for its iconic landmarks, romantic ambiance, and rich art and culture. Experience the Eiffel Tower, Louvre Museum, and Seine River.""",
        "image": "paris.jpg",
        "pricing": "₹80,000 for budget travelers, ₹1,40,000 for mid-range travelers, and ₹2,50,000 for luxury travelers (per person for 5 days).",
        "itinerary": {
            "low": [
                "Day 1: Arrival in Paris and explore Montmartre and Sacré-Cœur.",
                "Day 2: Visit the Eiffel Tower and stroll along the Seine.",
                "Day 3: Free day to explore local markets and parks.",
                "Day 4: Walk through Champs-Élysées and Arc de Triomphe.",
                "Day 5: Departure."
            ],
            "medium": [
                "Day 1: Arrival and stay in a mid-range hotel near the Eiffel Tower.",
                "Day 2: Guided tour of the Louvre and Notre Dame Cathedral.",
                "Day 3: Explore Versailles Palace with a guided tour.",
                "Day 4: Enjoy a Seine River cruise and Montmartre district.",
                "Day 5: Departure."
            ],
            "high": [
                "Day 1: Arrival and stay in a luxury hotel with Eiffel Tower views.",
                "Day 2: Exclusive private tour of the Louvre and Seine River cruise.",
                "Day 3: Helicopter tour of Versailles Palace and fine dining.",
                "Day 4: Personalized shopping experience and cultural tour.",
                "Day 5: Departure."
            ]
        }
    },
    14: {
        "name": "New York",
        "details": """New York City, the City That Never Sleeps, is famous for its towering skyscrapers, vibrant neighborhoods, and cultural landmarks.""",
        "image": "newyork.jpg",
        "pricing": "₹90,000 for budget travelers, ₹1,60,000 for mid-range travelers, and ₹2,80,000 for luxury travelers (per person for 5 days).",
        "itinerary": {
            "low": [
                "Day 1: Arrival and explore Times Square and Central Park.",
                "Day 2: Visit the Statue of Liberty using public ferry.",
                "Day 3: Walk through Brooklyn Bridge and DUMBO.",
                "Day 4: Free day to explore museums on discount passes.",
                "Day 5: Departure."
            ],
            "medium": [
                "Day 1: Arrival and stay in a mid-range hotel in Manhattan.",
                "Day 2: Guided tour of Statue of Liberty and Ellis Island.",
                "Day 3: Explore Central Park and Metropolitan Museum of Art.",
                "Day 4: Visit Top of the Rock and Brooklyn neighborhoods.",
                "Day 5: Departure."
            ],
            "high": [
                "Day 1: Arrival and stay at a luxury hotel near Central Park.",
                "Day 2: Private helicopter tour of New York City landmarks.",
                "Day 3: Exclusive Broadway show and fine dining.",
                "Day 4: Private tours of museums and Brooklyn Bridge.",
                "Day 5: Departure."
            ]
        }
    },
    15: {
        "name": "Australia",
        "details": """Australia, the Land Down Under, is known for its unique wildlife, vibrant cities, and stunning natural wonders like the Great Barrier Reef.""",
        "image": "australia.jpg",
        "pricing": "₹1,20,000 for budget travelers, ₹2,00,000 for mid-range travelers, and ₹3,50,000 for luxury travelers (per person for 5 days).",
        "itinerary": {
            "low": [
                "Day 1: Arrival in Sydney and explore local beaches.",
                "Day 2: Walk through Darling Harbour and Bondi Beach.",
                "Day 3: Visit Blue Mountains using public transport.",
                "Day 4: Free day to explore local attractions.",
                "Day 5: Departure."
            ],
            "medium": [
                "Day 1: Arrival and stay in a mid-range hotel in Sydney.",
                "Day 2: Guided tour of the Sydney Opera House and Harbour Bridge.",
                "Day 3: Day trip to the Great Barrier Reef.",
                "Day 4: Explore Melbourne’s laneways and culture.",
                "Day 5: Departure."
            ],
            "high": [
                "Day 1: Arrival and stay at a luxury hotel in Sydney.",
                "Day 2: Exclusive guided tours of Sydney landmarks.",
                "Day 3: Private Great Barrier Reef tour with snorkeling.",
                "Day 4: Luxury helicopter tour of Melbourne’s attractions.",
                "Day 5: Departure."
            ]
        }
    },
        16: {
        "name": "Switzerland",
        "details": """Switzerland, known as 'Heaven on Earth,' is famous for its breathtaking alpine scenery, pristine lakes, and charming villages. It offers a perfect mix of adventure and relaxation.""",
        "image": "switzerland.jpg",
        "pricing": "₹1,50,000 for budget travelers, ₹2,50,000 for mid-range travelers, and ₹4,00,000 for luxury travelers (per person for 5 days).",
        "itinerary": {
            "low": [
                "Day 1: Arrival in Zurich and explore Old Town.",
                "Day 2: Day trip to Lucerne using public transport.",
                "Day 3: Visit Interlaken and enjoy local hiking trails.",
                "Day 4: Explore local markets and enjoy Swiss chocolate tours.",
                "Day 5: Departure."
            ],
            "medium": [
                "Day 1: Arrival and stay in a mid-range Zurich hotel.",
                "Day 2: Guided tour of Lucerne and Mount Titlis.",
                "Day 3: Scenic train ride to Interlaken and Jungfrau region.",
                "Day 4: Explore Geneva and Lake Geneva on a guided tour.",
                "Day 5: Departure."
            ],
            "high": [
                "Day 1: Arrival and stay in a luxury Zurich hotel.",
                "Day 2: Private guided tour of Lucerne and Mount Pilatus.",
                "Day 3: Helicopter tour of Interlaken and Jungfraujoch.",
                "Day 4: Exclusive wine and cheese tour in Geneva.",
                "Day 5: Departure."
            ]
        }
    },
    17: {
        "name": "Maldives",
        "details": """The Maldives, a tropical paradise, is renowned for its crystal-clear waters, luxurious overwater villas, and vibrant marine life. Perfect for couples and beach lovers.""",
        "image": "maldives.jpg",
        "pricing": "₹80,000 for budget travelers, ₹1,50,000 for mid-range travelers, and ₹3,00,000 for luxury travelers (per person for 5 days).",
        "itinerary": {
            "low": [
                "Day 1: Arrival and check-in at a budget island resort.",
                "Day 2: Snorkeling and exploring local islands.",
                "Day 3: Day trip to Male and visit cultural sites.",
                "Day 4: Relaxation at the beach and sunset photography.",
                "Day 5: Departure."
            ],
            "medium": [
                "Day 1: Arrival and stay in a mid-range beachfront resort.",
                "Day 2: Guided snorkeling tour and dolphin watching.",
                "Day 3: Visit nearby islands with guided transport.",
                "Day 4: Spa treatments and water sports.",
                "Day 5: Departure."
            ],
            "high": [
                "Day 1: Arrival and stay in a luxury overwater villa.",
                "Day 2: Private scuba diving session and fine dining.",
                "Day 3: Luxury yacht trip to nearby islands.",
                "Day 4: Exclusive spa treatments and gourmet meals.",
                "Day 5: Departure."
            ]
        }
    },
    18: {
        "name": "Iceland",
        "details": """Iceland, the 'Land of Fire and Ice,' is known for its dramatic landscapes, including glaciers, volcanoes, and geysers. It offers a unique and awe-inspiring travel experience.""",
        "image": "iceland.jpg",
        "pricing": "₹1,50,000 for budget travelers, ₹2,50,000 for mid-range travelers, and ₹4,00,000 for luxury travelers (per person for 5 days).",
        "itinerary": {
            "low": [
                "Day 1: Arrival in Reykjavik and explore the city center.",
                "Day 2: Visit the Golden Circle (Thingvellir, Geysir, Gullfoss).",
                "Day 3: Explore South Coast waterfalls and black sand beaches.",
                "Day 4: Relax at local thermal baths.",
                "Day 5: Departure."
            ],
            "medium": [
                "Day 1: Arrival and stay in a mid-range Reykjavik hotel.",
                "Day 2: Guided tour of the Golden Circle with transport.",
                "Day 3: Explore South Coast highlights with a guided tour.",
                "Day 4: Visit Blue Lagoon and relax.",
                "Day 5: Departure."
            ],
            "high": [
                "Day 1: Arrival and stay in a luxury Reykjavik hotel.",
                "Day 2: Private tour of the Golden Circle with fine dining.",
                "Day 3: Helicopter tour of glaciers and volcanoes.",
                "Day 4: Exclusive Blue Lagoon experience with spa treatments.",
                "Day 5: Departure."
            ]
        }
    },
    19: {
        "name": "Egypt",
        "details": """Egypt, the 'Land of the Pharaohs,' is famous for its ancient pyramids, temples, and rich cultural heritage. It's a must-visit for history enthusiasts.""",
        "image": "egypt.jpg",
        "pricing": "₹70,000 for budget travelers, ₹1,20,000 for mid-range travelers, and ₹2,50,000 for luxury travelers (per person for 5 days).",
        "itinerary": {
            "low": [
                "Day 1: Arrival in Cairo and visit the Pyramids of Giza from outside.",
                "Day 2: Explore the Egyptian Museum on a budget tour.",
                "Day 3: Day trip to Alexandria using public transport.",
                "Day 4: Walk through local markets and mosques.",
                "Day 5: Departure."
            ],
            "medium": [
                "Day 1: Arrival and stay in a mid-range Cairo hotel.",
                "Day 2: Guided tour of Pyramids of Giza and Sphinx.",
                "Day 3: Visit Egyptian Museum and Citadel of Cairo.",
                "Day 4: Day trip to Alexandria with guided transport.",
                "Day 5: Departure."
            ],
            "high": [
                "Day 1: Arrival and stay at a luxury hotel near the Pyramids.",
                "Day 2: Private guided tour of Pyramids with camel ride.",
                "Day 3: Exclusive tour of Egyptian Museum and Nile cruise.",
                "Day 4: Helicopter tour of Alexandria and fine dining.",
                "Day 5: Departure."
            ]
        }
    },
    20: {
        "name": "South Africa",
        "details": """South Africa, the 'Rainbow Nation,' is known for its diverse culture, wildlife safaris, and breathtaking landscapes. It's an adventurer's paradise.""",
        "image": "southafrica.jpg",
        "pricing": "₹80,000 for budget travelers, ₹1,50,000 for mid-range travelers, and ₹3,00,000 for luxury travelers (per person for 5 days).",
        "itinerary": {
            "low": [
                "Day 1: Arrival in Cape Town and explore Table Mountain.",
                "Day 2: Visit Cape Point and Boulders Beach using public transport.",
                "Day 3: Safari at a local game reserve.",
                "Day 4: Explore local markets and museums.",
                "Day 5: Departure."
            ],
            "medium": [
                "Day 1: Arrival and stay in a mid-range hotel in Cape Town.",
                "Day 2: Guided tour of Cape Point and Boulders Beach.",
                "Day 3: Safari experience at Kruger National Park.",
                "Day 4: Explore wine regions in Stellenbosch.",
                "Day 5: Departure."
            ],
            "high": [
                "Day 1: Arrival and stay at a luxury hotel in Cape Town.",
                "Day 2: Private guided tour of Cape Town and beaches.",
                "Day 3: Exclusive safari experience at a private game reserve.",
                "Day 4: Helicopter tour of wine regions and fine dining.",
                "Day 5: Departure."
            ]
        }
    }
    }

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    if username not in login_attempts:
        login_attempts[username] = {'attempts': 0, 'lock_time': 0}

    if time.time() < login_attempts[username]['lock_time']:
        flash("Too many login attempts. Try again later.")
        return redirect(url_for('index'))

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
    user = cursor.fetchone()
    conn.close()

    if user is not None:
        session['user_id'] = user[0]
        session['username'] = username
        login_attempts[username] = {'attempts': 0, 'lock_time': 0}
        return redirect(url_for('home'))
    else:
        login_attempts[username]['attempts'] += 1
        if login_attempts[username]['attempts'] >= 3:
            login_attempts[username]['lock_time'] = time.time() + 60
            flash("Too many failed attempts. Try again in 1 minute.")
        else:
            flash("Invalid credentials. Please try again.")
        return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        fullname = request.form['fullname']
        phone = request.form['phone']
        dob = request.form['dob']
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (fullname, phone, dob, email, username, password) VALUES (?, ?, ?, ?, ?, ?)",
                       (fullname, phone, dob, email, username, password))
        conn.commit()
        conn.close()
        flash("Registration successful. Please login.")
        return redirect(url_for('index'))
    return render_template('register.html')

@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form['email']

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT username FROM users WHERE email = ?", (email,))
        user = cursor.fetchone()
        conn.close()

        if user:
            new_password = "Temp1234"
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("UPDATE users SET password = ? WHERE email = ?", (new_password, email))
            conn.commit()
            conn.close()

            msg = Message("Password Reset", recipients=[email])
            msg.body = f"Your new temporary password is: {new_password}. Please change it after logging in."
            mail.send(msg)

            flash("A temporary password has been sent to your email.")
            return redirect(url_for('index'))
        else:
            flash("Email not found.")
    return render_template('forgot_password.html')

@app.route('/home')
def home():
    if 'user_id' not in session:
        return redirect(url_for('index'))

    places = [
        {"id": 1, "name": "Kashmir", "description": "The Heaven is Here", "image": "kashmir.jpg"},
        {"id": 2, "name": "Udaipur", "description": "Royal Heritage Delight", "image": "udaipur.jpg"},
        {"id": 3, "name": "Kerala", "description": "Backwaters & Beaches", "image": "kerala.jpg"},
        {"id": 4, "name": "Shimla", "description": "largest city of the northern Indian state", "image": "shimla.jpg"},
        {"id": 5, "name": "Bali", "description": "Island of the Gods", "image": "bali.jpg"},
        {"id": 6, "name": "Vietnam", "description": "Land of Natural Wonders", "image": "vietnam.jpg"},
        {"id": 7, "name": "Malaysia", "description": "Truly Asia", "image": "malaysia.jpg"},
        {"id": 8, "name": "Singapore", "description": "The Lion City", "image": "singapore.jpg"},
        {"id": 9, "name": "Thailand", "description": "The Land of Smiles", "image": "thailand.jpg"},
        {"id": 10, "name": "Dubai", "description": "Luxury & Skyscrapers", "image": "dubai.jpg"},
        {"id": 11, "name": "Japan", "description": "Land of the Rising Sun", "image": "japan.jpg"},
        {"id": 12, "name": "South Korea", "description": "Tradition Meets Technology", "image": "southkorea.jpg"},
        {"id": 13, "name": "Paris", "description": "The City of Love", "image": "paris.jpg"},
        {"id": 14, "name": "New York", "description": "The City That Never Sleeps", "image": "newyork.jpg"},
        {"id": 15, "name": "Australia", "description": "The Land Down Under", "image": "australia.jpg"},
        {"id": 16, "name": "Switzerland", "description": "Heaven on Earth", "image": "switzerland.jpg"},
        {"id": 17, "name": "Maldives", "description": "Tropical Paradise", "image": "maldives.jpg"},
        {"id": 18, "name": "Iceland", "description": "Land of Fire and Ice", "image": "iceland.jpg"},
        {"id": 19, "name": "Egypt", "description": "Land of the Pharaohs", "image": "egypt.jpg"},
        {"id": 20, "name": "South Africa", "description": "Wildlife & Adventure", "image": "southafrica.jpg"},
    ]
    return render_template('home.html', places=places)
@app.route('/place/<int:place_id>')
def place_detail(place_id):
    place = place_details.get(place_id)
    if not place:
        return "Place not found", 404

    # Default to medium-budget itinerary
    itinerary = place["itinerary"]["medium"] if "medium" in place["itinerary"] else []

    # Pass `place_id` to the template explicitly
    return render_template('place_detail.html', place=place, itinerary=itinerary, place_id=place_id)



@app.route('/itinerary/<int:place_id>')
def itinerary_page(place_id):
    place = place_details.get(place_id)
    if not place:
        return "Place not found", 404

    # Fetch itineraries for all budgets
    itineraries = {
        "low": place["itinerary"].get("low", []),
        "medium": place["itinerary"].get("medium", []),
        "high": place["itinerary"].get("high", [])
    }

    return render_template('itinerary.html', place=place, itineraries=itineraries, place_id=place_id)





@app.route('/search', methods=['POST'])
def search():
    search_query = request.form.get('search_query').strip().lower()
    
    # List of available places (can be moved to a database for scalability)
    available_places = [
        {"id": 1, "name": "Kashmir", "description": "The Heaven is Here", "image": "kashmir.jpg"},
        {"id": 2, "name": "Udaipur", "description": "Royal Heritage Delight", "image": "udaipur.jpg"},
        {"id": 3, "name": "Kerala", "description": "Backwaters & Beaches", "image": "kerala.jpg"},
        {"id": 4, "name": "North East", "description": "Himalayan Heaven", "image": "northeast.jpg"},
        {"id": 5, "name": "Bali", "description": "Island of the Gods", "image": "bali.jpg"},
        {"id": 6, "name": "Vietnam", "description": "Land of Natural Wonders", "image": "vietnam.jpg"},
        {"id": 7, "name": "Malaysia", "description": "Truly Asia", "image": "malaysia.jpg"},
        {"id": 8, "name": "Singapore", "description": "The Lion City", "image": "singapore.jpg"},
        {"id": 9, "name": "Thailand", "description": "The Land of Smiles", "image": "thailand.jpg"},
        {"id": 10, "name": "Dubai", "description": "Luxury & Skyscrapers", "image": "dubai.jpg"},
        {"id": 11, "name": "Japan", "description": "Land of the Rising Sun", "image": "japan.jpg"},
        {"id": 12, "name": "South Korea", "description": "Tradition Meets Technology", "image": "southkorea.jpg"},
        {"id": 13, "name": "Paris", "description": "The City of Love", "image": "paris.jpg"},
        {"id": 14, "name": "New York", "description": "The City That Never Sleeps", "image": "newyork.jpg"},
        {"id": 15, "name": "Australia", "description": "The Land Down Under", "image": "australia.jpg"},
        {"id": 16, "name": "Switzerland", "description": "Heaven on Earth", "image": "switzerland.jpg"},
        {"id": 17, "name": "Maldives", "description": "Tropical Paradise", "image": "maldives.jpg"},
        {"id": 18, "name": "Iceland", "description": "Land of Fire and Ice", "image": "iceland.jpg"},
        {"id": 19, "name": "Egypt", "description": "Land of the Pharaohs", "image": "egypt.jpg"},
        {"id": 20, "name": "South Africa", "description": "Wildlife & Adventure", "image": "southafrica.jpg"},
    ]

    # Filter places matching the search query
    matching_places = [
        place for place in available_places if search_query in place['name'].lower()
    ]

    if matching_places:
        # Render results for matching places
        return render_template('search_results.html', places=matching_places)
    else:
        # If no match, show feedback message
        feedback_message = f"The place you are looking for is not available, but we are ready to take your feedback to include '{search_query.capitalize()}' in the future!"
        return render_template('search_results.html', places=[], feedback=feedback_message)


@app.route('/book', methods=['POST'])
def book():
    if 'user_id' not in session:
        return redirect(url_for('index'))

    destination = request.form['destination']
    budget = request.form['budget']

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO bookings (user_id, destination, budget, booking_date) VALUES (?, ?, ?, ?)",
                   (session['user_id'], destination, budget, datetime.now()))
    conn.commit()

    cursor.execute("SELECT email FROM users WHERE id = ?", (session['user_id'],))
    user_email = cursor.fetchone()[0]
    conn.close()

    msg = Message("Booking Confirmation", recipients=[user_email])
    msg.body = f"You have successfully booked a package to {destination} with a budget of {budget}.\nThank you!"
    mail.send(msg)

    flash("Booking successful! Confirmation email sent.")
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)