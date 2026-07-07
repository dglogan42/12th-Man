"""Classic Twelfth Man (Billy Birmingham) spoof commentary lines and templates."""

import random

# Commentator IDs
RICHHIE = "richie"
BILL = "bill"
TONY = "tony"
IAN = "ian"
GREG = "greg"
MAX = "max"
DARRELL = "darrell"
SLATS = "slats"

COMMENTATORS = {
    RICHHIE: {"name": "Richie Benaud", "color": "#f5e6c8", "style": "calm, measured"},
    BILL: {"name": "Bill Lawry", "color": "#ff6b6b", "style": "nasally, Victorian"},
    TONY: {"name": "Tony Greig", "color": "#4ecdc4", "style": "South African accent"},
    IAN: {"name": "Ian Chappell", "color": "#95e1d3", "style": "dry, analytical"},
    GREG: {"name": "Greg Chappell", "color": "#a8d8ea", "style": "calm"},
    MAX: {"name": "Max Walker", "color": "#ffd93d", "style": "manic"},
    DARRELL: {"name": "Darrell Eastlake", "color": "#ff9ff3", "style": "over-the-top"},
    SLATS: {"name": "Michael Slater", "color": "#54a0ff", "style": "enthusiastic"},
}

# Parodied English player names (Twelfth Man style — affectionate, not mean)
ENGLISH_NAME_PARODIES = {
    "joe root": ["Joe Rude", "Joe Shoot", "Joe Boot"],
    "ben stokes": ["Ben Croaks", "Ben Jokes", "Ben Pokes"],
    "zak crawley": ["Zak Crawly", "Zak Scrawley", "Zak Gnawley"],
    "harry brook": ["Harry Crook", "Harry Brook-lyn", "Harry Look"],
    "jonny bairstow": ["Jonny Bearstow", "Jonny Hairstow", "Jonny Warestow"],
    "ollie pope": ["Ollie Mope", "Ollie Hope", "Ollie Dope"],
    "jamie smith": ["Jamie Smyth", "Jamie Smirk", "Jamie Plinth"],
    "chris woakes": ["Chris Soaks", "Chris Croaks", "Chris Brokes"],
    "jofra archer": ["Jofra Marcher", "Jofra Larcher", "Jofra Par cher"],
    "mark wood": ["Mark Would", "Mark Good", "Mark Hood"],
    "james anderson": ["James Handerson", "James Sanderson", "James Granderson"],
    "stuart broad": ["Stuart Proud", "Stuart Loud", "Stuart Crowd"],
    "jos buttler": ["Jos Muttler", "Jos Cutter", "Jos Flutter"],
}

AUSSIE_NAME_PARODIES = {
    "travis head": ["Travis Red", "Travis Lead", "Travis Bread"],
    "steve smith": ["Steve Smyth", "Steve Smirk", "Steve Plinth"],
    "mitchell starc": ["Mitchell Stark", "Mitchell Spark", "Mitchell Shark"],
    "pat cummins": ["Pat Cummings", "Pat Muffins", "Pat Crumpets"],
    "nathan lyon": ["Nathan Lion", "Nathan Fly-on", "Nathan Crying"],
    "alex carey": ["Alex Scary", "Alex Hairy", "Alex Dairy"],
    "usman khawaja": ["Usman Kawaja", "Usman Khawadja", "Usman Khawanger"],
    "mitchell marsh": ["Mitchell Mash", "Mitchell Marshmallow", "Mitchell Gnash"],
    "josh hazlewood": ["Josh Hazelwould", "Josh Mazelwood", "Josh Dazzlewood"],
    "scott boland": ["Scott Poland", "Scott Rolled", "Scott Bowled"],
    "marnus labuschagne": ["Marnus Labooschagn", "Marnus Labooshayne", "Marnus La-boo-shane"],
}

# Classic Twelfth Man Indian parodies
INDIAN_NAME_PARODIES = {
    "virat kohli": ["Virat Goatee", "Virat Bowly", "Virat Slowly"],
    "rohit sharma": ["Rohit Sharma-rama-ding-dong", "No-hit Sharma", "Rohit Sharmeleon"],
    "sunil gavaskar": ["Sunil Haveascar", "Sunil Gaveascar", "Sunil Nocar"],
    "mohinder amarnath": ["Cuthis Arminhalf", "Mohinder Amarmuff", "Mohinder Alarm-bath"],
    "sachin tendulkar": ["Sachin Bendulkar", "Sachin Pretendulkar", "Sachin Mendulkar"],
    "kapil dev": ["Kapil Rev", "Kapil Nev", "Kapil Bev"],
    "kl rahul": ["KL Rahool", "KL Ra-haha-haha", "KL Rahul-rahul-rahul"],
    "rishabh pant": ["Rishabh Can't", "Rishabh Rant", "Rishabh Plant"],
    "jasprit bumrah": ["Jasprit Bumbler", "Jasprit Humrah", "Jasprit Tumrah"],
    "ravindra jadeja": ["Ravindra Jade-jar", "Ravindra Spadeja", "Ravindra Fadeja"],
    "mohammed shami": ["Mohammed Shammy", "Mohammed Jammy", "Mohammed Cammy"],
    "cheteshwar pujara": ["Cheteshwar Poojara", "Cheteshwar Fujara", "Cheteshwar Lujara"],
    "ajinkya rahane": ["Ajinkya Rahoney", "Ajinkya Rahini", "Ajinkya Rahaha"],
    "shubman gill": ["Shubman Chill", "Shubman Bill", "Shubman Fill"],
    "hardik pandya": ["Hardik Panda", "Hardik Bandya", "Hardik Sandya"],
}

PAKISTANI_NAME_PARODIES = {
    "babar azam": ["Babar Azham", "Babar A-zap", "Babar Blazam"],
    "mohammad rizwan": ["Mohammad Riz-one", "Mohammad Fizzwan", "Mohammad Wizwan"],
    "shaheen afridi": ["Shaheen Afridi-dle-dee", "Shaheen Safidi", "Shaheen Taffy"],
    "imran khan": ["Imran Can", "Imran Shan", "Imran Pan"],
    "wasim akram": ["Wasim Akram-bo", "Wasim Bakram", "Wasim Macram"],
    "javed miandad": ["Javed Me-and-ad", "Javed Me-on-dad", "Javed Me-under-dad"],
    "abdullah shafique": ["Abdullah Sha-freak", "Abdullah Sha-flick", "Abdullah Sha-stick"],
    "naseem shah": ["Naseem Shh", "Naseem Shah-rah", "Naseem Blah"],
}

NEW_ZEALAND_NAME_PARODIES = {
    "kane williamson": ["Kane Will-I-am-son", "Kane Stilliamson", "Kane Milliamson"],
    "tom latham": ["Tom Batham", "Tom Lathem", "Tom Patham"],
    "daryl mitchell": ["Daryl Mismatch", "Daryl Kitchen", "Daryl Stitch-ell"],
    "tim southee": ["Tim Southie", "Tim Mouthy", "Tim Shouty"],
    "mitchell santner": ["Mitchell Santana", "Mitchell Canner", "Mitchell Planner"],
    "trent boult": ["Trent Bolt", "Trent Volt", "Trent Molt"],
}

SOUTH_AFRICA_NAME_PARODIES = {
    "kagiso rabada": ["Kagiso Rabada-da", "Kagiso Grabada", "Kagiso Tabada"],
    "quinton de kock": ["Quinton De Clock", "Quinton De Sock", "Quinton De Rock"],
    "ab de villiers": ["AB De Pillagers", "AB De Fillers", "AB De Spillers"],
    "dale steyn": ["Dale Stay-in", "Dale Spray-in", "Dale Slay-in"],
    "temba bavuma": ["Temba Ba-vroom-a", "Temba Ba-hum-a", "Temba Ba-drum-a"],
    "aiden markram": ["Aiden Mark-rum", "Aiden Barkram", "Aiden Sparkram"],
    "anrich nortje": ["Anrich Naughty", "Anrich Sporty", "Anrich Forty"],
}

SRI_LANKA_NAME_PARODIES = {
    "kumar sangakkara": ["Kumar Sangamuffin", "Kumar Sangabacker", "Kumar Sangasnacker"],
    "mahela jayawardene": ["Mahela Jay-were-dead", "Mahela Jay-award-win", "Mahela Jay-awkward"],
    "muttiah muralitharan": ["Muttiah Murali-three-ran", "Muttiah Murali-spin", "Muttiah Murali-grin"],
    "angelo mathews": ["Angelo Math-ews", "Angelo Mat-hose", "Angelo Cat-hews"],
    "dimuth karunaratne": ["Dimuth Karuna-rat", "Dimuth Karuna-bat", "Dimuth Karuna-splat"],
}

WEST_INDIES_NAME_PARODIES = {
    "brian lara": ["Brian Lava", "Brian Lara-dee-da", "Brian Laramb"],
    "viv richards": ["Viv Richard-son", "Viv Stichards", "Viv Kitchens"],
    "kraigg brathwaite": ["Kraigg Bath-wait", "Kraigg Rath-waite", "Kraigg Math-waite"],
    "jason holder": ["Jason Folder", "Jason Bolder", "Jason Colder"],
    "shamarh brooks": ["Shamarh Crooks", "Shamarh Hooks", "Shamarh Nooks"],
}

BANGLADESH_NAME_PARODIES = {
    "shakib al hasan": ["Shakib Al Hassle", "Shakib Al Hasson", "Shakib Al Hazzard"],
    "mushfiqur rahim": ["Mushfiqur Rake-him", "Mushfiqur Bake-him", "Mushfiqur Take-him"],
    "tamim iqbal": ["Tamim Equal", "Tamim Sequel", "Tamim Prequel"],
    "litton das": ["Litton Dashes", "Litton Splashes", "Litton Crashes"],
}

OPPONENT_PARODIES: dict[str, dict] = {
    "england": ENGLISH_NAME_PARODIES,
    "australia": AUSSIE_NAME_PARODIES,
    "india": INDIAN_NAME_PARODIES,
    "pakistan": PAKISTANI_NAME_PARODIES,
    "new_zealand": NEW_ZEALAND_NAME_PARODIES,
    "south_africa": SOUTH_AFRICA_NAME_PARODIES,
    "sri_lanka": SRI_LANKA_NAME_PARODIES,
    "west_indies": WEST_INDIES_NAME_PARODIES,
    "bangladesh": BANGLADESH_NAME_PARODIES,
}

TEAM_ALIASES: dict[str, str] = {
    "aus": "australia", "aussie": "australia", "australian": "australia",
    "eng": "england", "english": "england",
    "ind": "india", "indian": "india",
    "pak": "pakistan", "pakistani": "pakistan",
    "nz": "new_zealand", "kiwi": "new_zealand",
    "sa": "south_africa", "protea": "south_africa",
    "sl": "sri_lanka", "lankan": "sri_lanka",
    "wi": "west_indies", "windies": "west_indies",
    "ban": "bangladesh", "bengal": "bangladesh",
}

VENUES = {
    "gabba": "the Gabba",
    "brisbane": "the Gabba",
    "adelaide": "Adelaide Oval",
    "perth": "the WACA",
    "waca": "the WACA",
    "melbourne": "the MCG",
    "mcg": "the MCG",
    "sydney": "the SCG",
    "scg": "the SCG",
    "lords": "Lord's",
    "oval": "the Oval",
    "old trafford": "Old Trafford",
    "headingley": "Headingley",
    "edgbaston": "Edgbaston",
}

# Event-triggered classic lines
WICKET_LINES = [
    ("Got him, yes! Piss off! You're out!", BILL),
    ("He's gone! Got him! Yes! Piss off!", BILL),
    ("Marvellous bowling! He's out!", RICHHIE),
    ("I don't believe it! What a delivery!", DARRELL),
    ("That's plumb! No doubt about it!", TONY),
    ("He's walking! Well, he's not walking, but he's out!", IAN),
]

FOUR_LINES = [
    ("That's raced away to the fence! Four runs!", TONY),
    ("Beautifully timed! Four!", RICHHIE),
    ("The crowd loves it! Four runs to the boundary!", BILL),
    ("CRACKING SHOT! FOUR RUNS!", DARRELL),
    ("That's a magnificent stroke!", RICHHIE),
]

SIX_LINES = [
    ("OH MY GOODNESS! INTO THE CROWD! SIX RUNS!", DARRELL),
    ("That's gone all the way! Six!", TONY),
    ("What a hit! That's sailed into the stands!", BILL),
    ("Maximum! He's absolutely nailed that!", SLATS),
    ("I don't believe it! That's out of the ground!", MAX),
]

DOT_LINES = [
    ("Good line and length. Nothing doing.", RICHHIE),
    ("Well bowled. Dot ball.", IAN),
    ("The batsman can't get it away.", GREG),
    ("Tight bowling. No run.", RICHHIE),
]

TWO_LINES = [
    ("Chew runs! They've come back for chew!", RICHHIE),
    ("Chew! They'll get chew for that.", RICHHIE),
    ("A comfortable chew. Good running.", RICHHIE),
]

WIDE_LINES = [
    ("Wide! The umpire's got his arms out like a scarecrow!", BILL),
    ("That's a wide. Down the leg side.", RICHHIE),
    ("Wide ball. Extra run to the batting side.", IAN),
]

NO_BALL_LINES = [
    ("No ball! He's overstepped! Free hit coming up!", TONY),
    ("The umpire's called no ball. Too many on the crease.", RICHHIE),
]

MAIDEN_LINES = [
    ("A maiden over! Excellent bowling!", RICHHIE),
    ("Six balls, no runs. A maiden. Marvellous.", RICHHIE),
]

DRINKS_LINES = [
    ("And it's drinks. Time for a cup of tea and a chat about Richie's jacket collection.",
     RICHHIE),
    ("Drinks break. Bill's checking on his racing pigeons.", BILL),
    ("Drinks! Tony's trying to get his car keys out of the pitch.", TONY),
]

RAIN_LINES = [
    ("The covers are coming on. Typical English weather... oh wait, we're in Australia.",
     IAN),
    ("Rain stops play. Richie's cream jacket will get ruined.", RICHHIE),
]

SESSION_LINES = [
    ("And welcome back to the SCG or the MCG or the Gabba or the WACA or wherever the hell we are.",
     BILL),
    ("We work as a team, and we do it my way.", RICHHIE),
    ("The tension, the drama, the buzz, the crowd, the atmosphere!", BILL),
    ("It's a beautiful day for cricket. Or is it? Hard to tell from up here.", IAN),
]

PITCH_REPORT_LINES = [
    ("Tony's sticking his car keys into the pitch again... and they're stuck. Tony, for heaven's sake.",
     RICHHIE),
    ("The pitch looks dry. Tony's buried his Italian loafers in it. We'll never get those back.",
     BILL),
    ("Good pitch for batting. Or bowling. One of the two.", IAN),
]

ODI_POWERPLAY_LINES = [
    ("Powerplay! Field up, batsmen attacking — this is ODI cricket!", SLATS),
    ("First ten overs — Bill's already yelling about the run rate!", BILL),
    ("New ball, new innings. Let's see some aggression!", TONY),
]

ODI_DEATH_OVERS_LINES = [
    ("Death overs! This is where legends are made!", DARRELL),
    ("Final five overs — the crowd is on its feet!", BILL),
    ("Yorkers and bouncers — hold onto your hats!", TONY),
    ("They need chew an over! Chew an over! It's getting tight!", RICHHIE),
]

T20_POWERPLAY_LINES = [
    ("Powerplay! Maximum six fielders out — let 'em hit it!", SLATS),
    ("T20 cricket — no time to waste, get on with it!", BILL),
    ("Twenty overs. That's it. Buckle up!", DARRELL),
]

T20_DEATH_OVERS_LINES = [
    ("Last over! THIS IS ABSOLUTELY CHAOTIC!", DARRELL),
    ("Death overs in a T20 — I don't believe what I'm seeing!", MAX),
    ("They need 18 off the last over — it's anyone's game!", SLATS),
    ("Get on with it! Get on with it! What are you waiting for?!", BILL),
]

T20_SIX_LINES = [
    ("MAXIMUM! INTO THE STANDS! T20 CARNAGE!", DARRELL),
    ("That's out of the ground! Six runs! Unbelievable!", SLATS),
    ("He's absolutely smoked that! Six!", TONY),
]

ODI_BANTER = [
    ("Fifty overs each. Richie's calculated that's approximately chew hundred balls.", RICHHIE),
    ("ODI cricket — Bill's brought his racing pigeons to the ground again.", BILL),
    ("The white ball's doing funny things. Or maybe it's Tony's car keys in the pitch.", IAN),
]

T20_BANTER = [
    ("Twenty overs. Richie reckons we'll be done before Bill finds a park.", RICHHIE),
    ("T20! Max Walker has already commentated three sixes that haven't happened yet!", MAX),
    ("Get on with it! That's the beauty of T20 — no time for Bill's pigeon stories!", BILL),
]

BANTER_LINES = [
    ("Bill, you're late again for the team meeting.", RICHHIE),
    ("I'm not late, Richie. The Victorian crowd held me up.", BILL),
    ("Richie, is that you or Darrell Eastlake? I can never tell.", TONY),
    ("I am NOT Darrell Eastlake!", RICHHIE),
    ("Max Walker has hijacked the commentary box again!", MAX),
    ("Let me back in, Richie! I promise I won't mention my deodorant ads!", MAX),
]


def normalize_team(team: str) -> str:
    t = team.lower().strip().replace(" ", "_")
    return TEAM_ALIASES.get(t, t)


def parody_name(name: str, team: str = "") -> str:
    """Return a Twelfth Man-style parodied player name."""
    key = name.lower().strip()
    team_key = normalize_team(team)
    # Australians get less name parody in the original — only use pool if present
    if team_key == "australia":
        pool = AUSSIE_NAME_PARODIES
        if key in pool:
            return random.choice(pool[key])
        return name
    pool = OPPONENT_PARODIES.get(team_key, ENGLISH_NAME_PARODIES)
    if key in pool:
        return random.choice(pool[key])
    parts = name.split()
    if len(parts) >= 2:
        suffixes = ["ington", "sworth", "bottom", "crumble", "fumble", "wobble", "nobble"]
        return f"{parts[0]} {parts[-1][:-1]}{random.choice(suffixes)}" if len(parts[-1]) > 3 else name
    return name


def pick_line(pool: list[tuple[str, str]]) -> tuple[str, str]:
    return random.choice(pool)


def welcome_line(venue: str = "", series_intro: str = "") -> tuple[str, str]:
    venue_name = "wherever the hell we are"
    for key, v in VENUES.items():
        if key in venue.lower():
            venue_name = v
            break
    intro = series_intro or "Test cricket at its finest"
    templates = [
        (f"And welcome back to {venue_name}. {intro}", BILL),
        (f"Good morning from {venue_name}. We work as a team, and we do it my way.", RICHHIE),
        (f"The tension, the drama, the buzz, the crowd, the atmosphere! {venue_name} is rocking!",
         BILL),
    ]
    return random.choice(templates)


def series_banter(series_id: str) -> list[tuple[str, str]]:
    """Extra banter lines specific to each major series."""
    extra: dict[str, list[tuple[str, str]]] = {
        "border_gavaskar": [
            ("Sunil Haveascar and Cuthis Arminhalf — what a batting lineup!", BILL),
            ("The Indians are here! Bill's trying to pronounce the team sheet.", TONY),
            ("I've got the Indian names on flashcards. Still not helping.", RICHHIE),
        ],
        "ashes": [
            ("The Poms are here! Bill's already complaining about the weather.", BILL),
            ("England are batting. Tony's sticking his keys in the pitch again.", RICHHIE),
        ],
        "pakistan": [
            ("The Pakistanis are here! Tony's practising his pronunciation.", TONY),
            ("Wasim Akram-bo and the boys — what a lineup!", BILL),
        ],
        "trans_tasman": [
            ("The Kiwis are here! No one's pronouncing Wellington correctly.", IAN),
            ("New Zealand versus Australia — Bill's backing the Victorians, naturally.", BILL),
        ],
        "south_africa": [
            ("South Africa! Tony's feeling patriotic about his homeland.", TONY),
            ("The Proteas are in town. Richie's wearing his cream jacket.", RICHHIE),
        ],
        "west_indies": [
            ("The Windies! Brian Lava and the boys from the Caribbean!", DARRELL),
            ("West Indian cricket — now THAT'S atmosphere!", SLATS),
        ],
        "sri_lanka": [
            ("Sri Lanka! Muttiah Murali-three-ran territory!", BILL),
            ("Spin-friendly conditions. Tony's keys are stuck in the pitch again.", RICHHIE),
        ],
        "bangladesh": [
            ("Bangladesh! Shakib Al Hassle leading the charge!", BILL),
            ("The Tigers are here — this could be a ripper!", SLATS),
        ],
    }
    return extra.get(series_id, [])


def format_banter(fmt: str) -> list[tuple[str, str]]:
    if fmt == "odi":
        return ODI_BANTER
    if fmt == "t20":
        return T20_BANTER
    return []


def phase_line(fmt: str, phase: str) -> tuple[str, str] | None:
    """Return a commentary line for powerplay/death phase, or None."""
    if phase == "powerplay":
        pool = T20_POWERPLAY_LINES if fmt == "t20" else ODI_POWERPLAY_LINES
        return pick_line(pool)
    if phase == "death":
        pool = T20_DEATH_OVERS_LINES if fmt == "t20" else ODI_DEATH_OVERS_LINES
        return pick_line(pool)
    return None