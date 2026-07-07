"""Major Australia series — Tests, ODIs & T20s — trophies, opponents, demo fixtures."""

from dataclasses import dataclass, field


FORMAT_TEST = "test"
FORMAT_ODI = "odi"
FORMAT_T20 = "t20"
ALL_FORMATS = (FORMAT_TEST, FORMAT_ODI, FORMAT_T20)

FORMAT_LABELS = {
    FORMAT_TEST: "Test",
    FORMAT_ODI: "ODI",
    FORMAT_T20: "T20",
}

FORMAT_INTROS = {
    FORMAT_TEST: "Test cricket at its finest",
    FORMAT_ODI: "One Day International cricket — fifty overs of pure drama!",
    FORMAT_T20: "T20 cricket — buckle up, it's going to be fast and furious!",
}

FORMAT_STAKES_SUFFIX = {
    FORMAT_TEST: "",
    FORMAT_ODI: " in this ODI series",
    FORMAT_T20: " in this T20 series",
}


@dataclass
class TestSeries:
    id: str
    name: str
    trophy: str
    opponent: str
    opponent_aliases: list[str]
    emoji: str
    intro_line: str
    stakes_line: str


# All major Test opponents for Australia
AUSTRALIA_TEST_SERIES: dict[str, TestSeries] = {
    "ashes": TestSeries(
        id="ashes",
        name="The Ashes",
        trophy="The Ashes urn",
        opponent="England",
        opponent_aliases=["england", "eng"],
        emoji="🏴󠁧󠁢󠁥󠁮󠁧󠁿",
        intro_line="The NRMA Insurance Men's Ashes — what a series!",
        stakes_line="The urn is on the line!",
    ),
    "border_gavaskar": TestSeries(
        id="border_gavaskar",
        name="Border-Gavaskar Trophy",
        trophy="Border-Gavaskar Trophy",
        opponent="India",
        opponent_aliases=["india", "ind"],
        emoji="🇮🇳",
        intro_line="Border-Gavaskar Trophy cricket — Sunil Haveascar and the boys are in town!",
        stakes_line="The Border-Gavaskar Trophy hangs in the balance!",
    ),
    "trans_tasman": TestSeries(
        id="trans_tasman",
        name="Trans-Tasman Trophy",
        trophy="Trans-Tasman Trophy",
        opponent="New Zealand",
        opponent_aliases=["new zealand", "nz"],
        emoji="🇳🇿",
        intro_line="Australia versus New Zealand — the Trans-Tasman Trophy is up for grabs!",
        stakes_line="Trans-Tasman bragging rights on the line!",
    ),
    "south_africa": TestSeries(
        id="south_africa",
        name="Australia v South Africa",
        trophy="Freedom Trophy",
        opponent="South Africa",
        opponent_aliases=["south africa", "sa"],
        emoji="🇿🇦",
        intro_line="Australia against South Africa — Test cricket at its fiercest!",
        stakes_line="The Freedom Trophy is at stake!",
    ),
    "pakistan": TestSeries(
        id="pakistan",
        name="Australia v Pakistan",
        trophy="Test series honours",
        opponent="Pakistan",
        opponent_aliases=["pakistan", "pak"],
        emoji="🇵🇰",
        intro_line="Australia versus Pakistan — spin, pace, and everything in between!",
        stakes_line="A massive series for both nations!",
    ),
    "sri_lanka": TestSeries(
        id="sri_lanka",
        name="Australia v Sri Lanka",
        trophy="Test series honours",
        opponent="Sri Lanka",
        opponent_aliases=["sri lanka", "sl"],
        emoji="🇱🇰",
        intro_line="Australia take on Sri Lanka — spin-friendly conditions expected!",
        stakes_line="Series honours up for grabs in the island nation!",
    ),
    "west_indies": TestSeries(
        id="west_indies",
        name="Australia v West Indies",
        trophy="Frank Worrell Trophy",
        opponent="West Indies",
        opponent_aliases=["west indies", "wi"],
        emoji="🏝️",
        intro_line="Australia versus the West Indies — the Frank Worrell Trophy!",
        stakes_line="Caribbean flair meets Aussie grit!",
    ),
    "bangladesh": TestSeries(
        id="bangladesh",
        name="Australia v Bangladesh",
        trophy="Test series honours",
        opponent="Bangladesh",
        opponent_aliases=["bangladesh", "ban"],
        emoji="🇧🇩",
        intro_line="Australia face Bangladesh — a Test series full of surprises!",
        stakes_line="Bangladesh looking to upset the Aussies on home soil!",
    ),
}

AUSTRALIA_ALIASES = {"australia", "aus", "aussie", "australian"}


def detect_format(title: str, match_type: str = "") -> str:
    """Detect match format from title or API match type field."""
    text = (title + " " + match_type).lower()
    if any(k in text for k in ("t20", "t20i", "twenty20", "20-over")):
        return FORMAT_T20
    if any(k in text for k in ("odi", "one day", "50 over", "50-over")):
        return FORMAT_ODI
    if "test" in text or "ashes" in text:
        return FORMAT_TEST
    # Default shorter formats if ambiguous but international
    return FORMAT_ODI


def detect_series(title: str, teams: list[str]) -> str | None:
    """Return series id if this is an Australia international match."""
    text = (title + " " + " ".join(str(t) for t in teams)).lower()
    has_australia = any(a in text for a in AUSTRALIA_ALIASES)
    if not has_australia:
        return None
    for sid, series in AUSTRALIA_TEST_SERIES.items():
        if any(alias in text for alias in series.opponent_aliases):
            return sid
    if "ashes" in text:
        return "ashes"
    return None


def roster_key(series_id: str, fmt: str) -> str:
    return f"{series_id}_{fmt}"


def get_roster(series_id: str, fmt: str = FORMAT_TEST) -> dict:
    key = roster_key(series_id, fmt)
    if key in DEMO_ROSTERS:
        return DEMO_ROSTERS[key]
    base_key = roster_key(series_id, FORMAT_TEST)
    return DEMO_ROSTERS.get(base_key, DEMO_ROSTERS["ashes_test"])


def get_series(series_id: str) -> TestSeries | None:
    return AUSTRALIA_TEST_SERIES.get(series_id)


def opponent_team_key(series_id: str) -> str:
    """Key used for name parody lookups."""
    mapping = {
        "ashes": "england",
        "border_gavaskar": "india",
        "trans_tasman": "new_zealand",
        "south_africa": "south_africa",
        "pakistan": "pakistan",
        "sri_lanka": "sri_lanka",
        "west_indies": "west_indies",
        "bangladesh": "bangladesh",
    }
    return mapping.get(series_id, "england")


# Demo rosters — keyed by series_format (e.g. ashes_odi, border_gavaskar_t20)
DEMO_ROSTERS: dict[str, dict] = {
    "ashes_test": {
        "batting_team": "england",
        "batting_abbr": "ENG",
        "opponent_abbr": "ENG",
        "batsmen": ["Joe Root", "Harry Brook", "Zak Crawley", "Ben Stokes",
                    "Jamie Smith", "Ollie Pope", "Chris Woakes"],
        "bowlers": ["Mitchell Starc", "Pat Cummins", "Josh Hazlewood",
                    "Nathan Lyon", "Scott Boland"],
        "fielders": ["Alex Carey", "Travis Head", "Usman Khawaja", "Steve Smith"],
        "venue": "Sydney Cricket Ground",
        "runs": 287, "wickets": 6, "overs": 78, "balls": 4,
        "lead_text": "England lead by 42 runs",
        "format": FORMAT_TEST, "max_overs": 999,
    },
    "ashes_odi": {
        "batting_team": "england", "batting_abbr": "ENG", "opponent_abbr": "ENG",
        "batsmen": ["Jos Buttler", "Jonny Bairstow", "Harry Brook", "Joe Root",
                    "Liam Livingstone", "Chris Woakes", "Jofra Archer"],
        "bowlers": ["Mitchell Starc", "Pat Cummins", "Josh Hazlewood",
                    "Adam Zampa", "Travis Head"],
        "fielders": ["Alex Carey", "Glenn Maxwell", "Travis Head", "Steve Smith"],
        "venue": "Melbourne Cricket Ground",
        "runs": 245, "wickets": 4, "overs": 42, "balls": 3,
        "lead_text": "England need 86 runs from 45 balls",
        "format": FORMAT_ODI, "max_overs": 50,
    },
    "ashes_t20": {
        "batting_team": "england", "batting_abbr": "ENG", "opponent_abbr": "ENG",
        "batsmen": ["Jos Buttler", "Phil Salt", "Harry Brook", "Liam Livingstone",
                    "Will Jacks", "Chris Jordan", "Adil Rashid"],
        "bowlers": ["Mitchell Starc", "Pat Cummins", "Adam Zampa",
                    "Josh Hazlewood", "Glenn Maxwell"],
        "fielders": ["Tim David", "Glenn Maxwell", "Travis Head", "Matthew Wade"],
        "venue": "Perth Stadium",
        "runs": 98, "wickets": 3, "overs": 14, "balls": 2,
        "lead_text": "England need 52 from 34 balls — get on with it!",
        "format": FORMAT_T20, "max_overs": 20,
    },
    "border_gavaskar_test": {
        "batting_team": "india",
        "batting_abbr": "IND",
        "opponent_abbr": "IND",
        "batsmen": ["Virat Kohli", "Rohit Sharma", "KL Rahul", "Rishabh Pant",
                    "Ravindra Jadeja", "Jasprit Bumrah", "Mohammed Shami"],
        "bowlers": ["Pat Cummins", "Mitchell Starc", "Nathan Lyon",
                    "Josh Hazlewood", "Travis Head"],
        "fielders": ["Alex Carey", "Steve Smith", "Usman Khawaja", "Marnus Labuschagne"],
        "venue": "Melbourne Cricket Ground",
        "runs": 312, "wickets": 4, "overs": 85, "balls": 2,
        "lead_text": "India trail by 18 runs",
        "format": FORMAT_TEST, "max_overs": 999,
    },
    "border_gavaskar_odi": {
        "batting_team": "india", "batting_abbr": "IND", "opponent_abbr": "IND",
        "batsmen": ["Virat Kohli", "Rohit Sharma", "Shubman Gill", "Hardik Pandya",
                    "Rishabh Pant", "Ravindra Jadeja", "Jasprit Bumrah"],
        "bowlers": ["Pat Cummins", "Mitchell Starc", "Adam Zampa",
                    "Josh Hazlewood", "Glenn Maxwell"],
        "fielders": ["Alex Carey", "Glenn Maxwell", "Travis Head", "Steve Smith"],
        "venue": "Sydney Cricket Ground",
        "runs": 278, "wickets": 5, "overs": 47, "balls": 4,
        "lead_text": "India need 34 runs from 14 balls",
        "format": FORMAT_ODI, "max_overs": 50,
    },
    "border_gavaskar_t20": {
        "batting_team": "india", "batting_abbr": "IND", "opponent_abbr": "IND",
        "batsmen": ["Rohit Sharma", "Virat Kohli", "Suryakumar Yadav", "Hardik Pandya",
                    "Rishabh Pant", "Ravindra Jadeja", "Arshdeep Singh"],
        "bowlers": ["Pat Cummins", "Mitchell Starc", "Adam Zampa",
                    "Josh Hazlewood", "Glenn Maxwell"],
        "fielders": ["Tim David", "Glenn Maxwell", "Matthew Wade", "Travis Head"],
        "venue": "Melbourne Cricket Ground",
        "runs": 112, "wickets": 2, "overs": 11, "balls": 5,
        "lead_text": "India need 67 from 50 balls — carnage incoming!",
        "format": FORMAT_T20, "max_overs": 20,
    },
    "trans_tasman_test": {
        "batting_team": "new_zealand",
        "batting_abbr": "NZ",
        "opponent_abbr": "NZ",
        "batsmen": ["Kane Williamson", "Tom Latham", "Daryl Mitchell", "Tom Blundell",
                    "Glenn Phillips", "Mitchell Santner", "Tim Southee"],
        "bowlers": ["Pat Cummins", "Mitchell Starc", "Scott Boland",
                    "Nathan Lyon", "Travis Head"],
        "fielders": ["Alex Carey", "Steve Smith", "Travis Head", "Marnus Labuschagne"],
        "venue": "Perth Stadium",
        "runs": 198, "wickets": 5, "overs": 62, "balls": 3,
        "lead_text": "New Zealand trail by 87 runs",
        "format": FORMAT_TEST, "max_overs": 999,
    },
    "trans_tasman_odi": {
        "batting_team": "new_zealand", "batting_abbr": "NZ", "opponent_abbr": "NZ",
        "batsmen": ["Kane Williamson", "Devon Conway", "Daryl Mitchell", "Glenn Phillips",
                    "Tom Latham", "Mitchell Santner", "Trent Boult"],
        "bowlers": ["Mitchell Starc", "Pat Cummins", "Adam Zampa",
                    "Josh Hazlewood", "Travis Head"],
        "fielders": ["Alex Carey", "Glenn Maxwell", "Travis Head", "Steve Smith"],
        "venue": "Hagley Oval, Christchurch",
        "runs": 198, "wickets": 6, "overs": 38, "balls": 2,
        "lead_text": "New Zealand need 112 from 72 balls",
        "format": FORMAT_ODI, "max_overs": 50,
    },
    "trans_tasman_t20": {
        "batting_team": "new_zealand", "batting_abbr": "NZ", "opponent_abbr": "NZ",
        "batsmen": ["Finn Allen", "Devon Conway", "Glenn Phillips", "Daryl Mitchell",
                    "Jimmy Neesham", "Mitchell Santner", "Tim Southee"],
        "bowlers": ["Mitchell Starc", "Pat Cummins", "Adam Zampa",
                    "Josh Hazlewood", "Glenn Maxwell"],
        "fielders": ["Tim David", "Glenn Maxwell", "Matthew Wade", "Travis Head"],
        "venue": "Eden Park, Auckland",
        "runs": 89, "wickets": 4, "overs": 12, "balls": 3,
        "lead_text": "New Zealand need 78 from 45 balls",
        "format": FORMAT_T20, "max_overs": 20,
    },
    "south_africa_test": {
        "batting_team": "south_africa",
        "batting_abbr": "SA",
        "opponent_abbr": "SA",
        "batsmen": ["Temba Bavuma", "Aiden Markram", "Quinton de Kock", "Keshav Maharaj",
                    "Kagiso Rabada", "Anrich Nortje", "Marco Jansen"],
        "bowlers": ["Mitchell Starc", "Pat Cummins", "Josh Hazlewood",
                    "Nathan Lyon", "Scott Boland"],
        "fielders": ["Alex Carey", "Steve Smith", "Travis Head", "Usman Khawaja"],
        "venue": "Gabba, Brisbane",
        "runs": 245, "wickets": 7, "overs": 71, "balls": 5,
        "lead_text": "South Africa trail by 56 runs",
        "format": FORMAT_TEST, "max_overs": 999,
    },
    "south_africa_odi": {
        "batting_team": "south_africa", "batting_abbr": "SA", "opponent_abbr": "SA",
        "batsmen": ["Quinton de Kock", "Temba Bavuma", "Aiden Markram", "Heinrich Klaasen",
                    "David Miller", "Kagiso Rabada", "Anrich Nortje"],
        "bowlers": ["Mitchell Starc", "Pat Cummins", "Adam Zampa",
                    "Josh Hazlewood", "Travis Head"],
        "fielders": ["Alex Carey", "Glenn Maxwell", "Travis Head", "Steve Smith"],
        "venue": "Wanderers, Johannesburg",
        "runs": 231, "wickets": 5, "overs": 44, "balls": 1,
        "lead_text": "South Africa need 89 from 35 balls",
        "format": FORMAT_ODI, "max_overs": 50,
    },
    "south_africa_t20": {
        "batting_team": "south_africa", "batting_abbr": "SA", "opponent_abbr": "SA",
        "batsmen": ["Quinton de Kock", "Aiden Markram", "David Miller", "Heinrich Klaasen",
                    "Tristan Stubbs", "Kagiso Rabada", "Anrich Nortje"],
        "bowlers": ["Mitchell Starc", "Pat Cummins", "Adam Zampa",
                    "Josh Hazlewood", "Glenn Maxwell"],
        "fielders": ["Tim David", "Glenn Maxwell", "Matthew Wade", "Travis Head"],
        "venue": "Newlands, Cape Town",
        "runs": 105, "wickets": 3, "overs": 13, "balls": 4,
        "lead_text": "South Africa need 61 from 38 balls",
        "format": FORMAT_T20, "max_overs": 20,
    },
    "pakistan_test": {
        "batting_team": "pakistan",
        "batting_abbr": "PAK",
        "opponent_abbr": "PAK",
        "batsmen": ["Babar Azam", "Mohammad Rizwan", "Abdullah Shafique", "Saud Shakeel",
                    "Agha Salman", "Shaheen Afridi", "Naseem Shah"],
        "bowlers": ["Mitchell Starc", "Pat Cummins", "Nathan Lyon",
                    "Josh Hazlewood", "Travis Head"],
        "fielders": ["Alex Carey", "Steve Smith", "Usman Khawaja", "Marnus Labuschagne"],
        "venue": "Adelaide Oval",
        "runs": 267, "wickets": 5, "overs": 74, "balls": 1,
        "lead_text": "Pakistan lead by 23 runs",
        "format": FORMAT_TEST, "max_overs": 999,
    },
    "pakistan_odi": {
        "batting_team": "pakistan", "batting_abbr": "PAK", "opponent_abbr": "PAK",
        "batsmen": ["Babar Azam", "Mohammad Rizwan", "Fakhar Zaman", "Iftikhar Ahmed",
                    "Shadab Khan", "Shaheen Afridi", "Haris Rauf"],
        "bowlers": ["Mitchell Starc", "Pat Cummins", "Adam Zampa",
                    "Josh Hazlewood", "Glenn Maxwell"],
        "fielders": ["Alex Carey", "Glenn Maxwell", "Travis Head", "Steve Smith"],
        "venue": "Gaddafi Stadium, Lahore",
        "runs": 256, "wickets": 4, "overs": 43, "balls": 5,
        "lead_text": "Pakistan need 67 from 37 balls",
        "format": FORMAT_ODI, "max_overs": 50,
    },
    "pakistan_t20": {
        "batting_team": "pakistan", "batting_abbr": "PAK", "opponent_abbr": "PAK",
        "batsmen": ["Mohammad Rizwan", "Babar Azam", "Iftikhar Ahmed", "Shadab Khan",
                    "Shaheen Afridi", "Haris Rauf", "Naseem Shah"],
        "bowlers": ["Mitchell Starc", "Pat Cummins", "Adam Zampa",
                    "Josh Hazlewood", "Glenn Maxwell"],
        "fielders": ["Tim David", "Glenn Maxwell", "Matthew Wade", "Travis Head"],
        "venue": "Adelaide Oval",
        "runs": 94, "wickets": 5, "overs": 15, "balls": 1,
        "lead_text": "Pakistan need 71 from 29 balls — hold onto your hats!",
        "format": FORMAT_T20, "max_overs": 20,
    },
    "sri_lanka_test": {
        "batting_team": "sri_lanka",
        "batting_abbr": "SL",
        "opponent_abbr": "SL",
        "batsmen": ["Dimuth Karunaratne", "Kusal Mendis", "Angelo Mathews", "Dhananjaya de Silva",
                    "Dinesh Chandimal", "Prabath Jayasuriya", "Kasun Rajitha"],
        "bowlers": ["Nathan Lyon", "Pat Cummins", "Mitchell Starc",
                    "Travis Head", "Josh Hazlewood"],
        "fielders": ["Alex Carey", "Steve Smith", "Travis Head", "Marnus Labuschagne"],
        "venue": "Galle International Stadium",
        "runs": 156, "wickets": 8, "overs": 55, "balls": 4,
        "lead_text": "Sri Lanka trail by 134 runs",
        "format": FORMAT_TEST, "max_overs": 999,
    },
    "sri_lanka_odi": {
        "batting_team": "sri_lanka", "batting_abbr": "SL", "opponent_abbr": "SL",
        "batsmen": ["Pathum Nissanka", "Kusal Mendis", "Charith Asalanka", "Dhananjaya de Silva",
                    "Wanindu Hasaranga", "Maheesh Theekshana", "Dilshan Madushanka"],
        "bowlers": ["Adam Zampa", "Pat Cummins", "Mitchell Starc",
                    "Josh Hazlewood", "Glenn Maxwell"],
        "fielders": ["Alex Carey", "Glenn Maxwell", "Travis Head", "Steve Smith"],
        "venue": "R. Premadasa Stadium, Colombo",
        "runs": 187, "wickets": 7, "overs": 39, "balls": 3,
        "lead_text": "Sri Lanka need 134 from 63 balls",
        "format": FORMAT_ODI, "max_overs": 50,
    },
    "sri_lanka_t20": {
        "batting_team": "sri_lanka", "batting_abbr": "SL", "opponent_abbr": "SL",
        "batsmen": ["Pathum Nissanka", "Kusal Mendis", "Wanindu Hasaranga", "Charith Asalanka",
                    "Dasun Shanaka", "Maheesh Theekshana", "Dilshan Madushanka"],
        "bowlers": ["Adam Zampa", "Mitchell Starc", "Pat Cummins",
                    "Josh Hazlewood", "Glenn Maxwell"],
        "fielders": ["Tim David", "Glenn Maxwell", "Matthew Wade", "Travis Head"],
        "venue": "Pallekele International Stadium",
        "runs": 76, "wickets": 6, "overs": 11, "balls": 2,
        "lead_text": "Sri Lanka need 89 from 52 balls",
        "format": FORMAT_T20, "max_overs": 20,
    },
    "west_indies_test": {
        "batting_team": "west_indies",
        "batting_abbr": "WI",
        "opponent_abbr": "WI",
        "batsmen": ["Kraigg Brathwaite", "Shamarh Brooks", "Jermaine Blackwood", "Jason Holder",
                    "Roston Chase", "Gudakesh Motie", "Alzarri Joseph"],
        "bowlers": ["Mitchell Starc", "Pat Cummins", "Josh Hazlewood",
                    "Nathan Lyon", "Scott Boland"],
        "fielders": ["Alex Carey", "Steve Smith", "Travis Head", "Usman Khawaja"],
        "venue": "Perth Stadium",
        "runs": 223, "wickets": 6, "overs": 68, "balls": 2,
        "lead_text": "West Indies trail by 45 runs",
        "format": FORMAT_TEST, "max_overs": 999,
    },
    "west_indies_t20": {
        "batting_team": "west_indies", "batting_abbr": "WI", "opponent_abbr": "WI",
        "batsmen": ["Shai Hope", "Nicholas Pooran", "Andre Russell", "Shimron Hetmyer",
                    "Jason Holder", "Alzarri Joseph", "Romario Shepherd"],
        "bowlers": ["Mitchell Starc", "Pat Cummins", "Adam Zampa",
                    "Josh Hazlewood", "Glenn Maxwell"],
        "fielders": ["Tim David", "Glenn Maxwell", "Matthew Wade", "Travis Head"],
        "venue": "Kensington Oval, Barbados",
        "runs": 118, "wickets": 4, "overs": 14, "balls": 5,
        "lead_text": "West Indies need 84 from 31 balls — Russell at the crease!",
        "format": FORMAT_T20, "max_overs": 20,
    },
    "bangladesh_test": {
        "batting_team": "bangladesh",
        "batting_abbr": "BAN",
        "opponent_abbr": "BAN",
        "batsmen": ["Najmul Hossain Shanto", "Mushfiqur Rahim", "Litton Das", "Shakib Al Hasan",
                    "Mehidy Hasan", "Taijul Islam", "Taskin Ahmed"],
        "bowlers": ["Nathan Lyon", "Pat Cummins", "Mitchell Starc",
                    "Josh Hazlewood", "Travis Head"],
        "fielders": ["Alex Carey", "Steve Smith", "Marnus Labuschagne", "Travis Head"],
        "venue": "Shere Bangla National Stadium, Dhaka",
        "runs": 189, "wickets": 9, "overs": 58, "balls": 1,
        "lead_text": "Bangladesh trail by 211 runs",
        "format": FORMAT_TEST, "max_overs": 999,
    },
    "bangladesh_odi": {
        "batting_team": "bangladesh", "batting_abbr": "BAN", "opponent_abbr": "BAN",
        "batsmen": ["Litton Das", "Najmul Hossain Shanto", "Shakib Al Hasan", "Mushfiqur Rahim",
                    "Mahmudullah", "Mehidy Hasan", "Mustafizur Rahman"],
        "bowlers": ["Adam Zampa", "Mitchell Starc", "Pat Cummins",
                    "Josh Hazlewood", "Glenn Maxwell"],
        "fielders": ["Alex Carey", "Glenn Maxwell", "Travis Head", "Steve Smith"],
        "venue": "Shere Bangla National Stadium, Dhaka",
        "runs": 212, "wickets": 8, "overs": 46, "balls": 0,
        "lead_text": "Bangladesh need 98 from 24 balls",
        "format": FORMAT_ODI, "max_overs": 50,
    },
}


# Demo & upcoming fixtures — Tests, ODIs, T20s
DEMO_FIXTURES: list[dict] = [
    # Tests
    {"id": "demo-ashes-test", "series": "ashes", "format": FORMAT_TEST, "status": "live",
     "title": "DEMO: 5th Test — England vs Australia (The Ashes)"},
    {"id": "demo-border-gavaskar-test", "series": "border_gavaskar", "format": FORMAT_TEST, "status": "live",
     "title": "DEMO: 3rd Test — India vs Australia (Border-Gavaskar)"},
    {"id": "demo-trans-tasman-test", "series": "trans_tasman", "format": FORMAT_TEST, "status": "live",
     "title": "DEMO: 2nd Test — New Zealand vs Australia"},
    {"id": "demo-south-africa-test", "series": "south_africa", "format": FORMAT_TEST, "status": "live",
     "title": "DEMO: 1st Test — South Africa vs Australia"},
    {"id": "demo-pakistan-test", "series": "pakistan", "format": FORMAT_TEST, "status": "live",
     "title": "DEMO: 2nd Test — Pakistan vs Australia"},
    {"id": "demo-sri-lanka-test", "series": "sri_lanka", "format": FORMAT_TEST, "status": "live",
     "title": "DEMO: 1st Test — Sri Lanka vs Australia"},
    {"id": "demo-west-indies-test", "series": "west_indies", "format": FORMAT_TEST, "status": "live",
     "title": "DEMO: 2nd Test — West Indies vs Australia (Frank Worrell)"},
    {"id": "demo-bangladesh-test", "series": "bangladesh", "format": FORMAT_TEST, "status": "live",
     "title": "DEMO: 1st Test — Bangladesh vs Australia"},
    # ODIs
    {"id": "demo-ashes-odi", "series": "ashes", "format": FORMAT_ODI, "status": "live",
     "title": "DEMO: 3rd ODI — England vs Australia"},
    {"id": "demo-border-gavaskar-odi", "series": "border_gavaskar", "format": FORMAT_ODI, "status": "live",
     "title": "DEMO: 2nd ODI — India vs Australia (Border-Gavaskar)"},
    {"id": "demo-trans-tasman-odi", "series": "trans_tasman", "format": FORMAT_ODI, "status": "live",
     "title": "DEMO: 1st ODI — New Zealand vs Australia (Chappell-Hadlee)"},
    {"id": "demo-south-africa-odi", "series": "south_africa", "format": FORMAT_ODI, "status": "live",
     "title": "DEMO: 3rd ODI — South Africa vs Australia"},
    {"id": "demo-pakistan-odi", "series": "pakistan", "format": FORMAT_ODI, "status": "live",
     "title": "DEMO: 1st ODI — Pakistan vs Australia"},
    {"id": "demo-sri-lanka-odi", "series": "sri_lanka", "format": FORMAT_ODI, "status": "live",
     "title": "DEMO: 2nd ODI — Sri Lanka vs Australia"},
    {"id": "demo-bangladesh-odi", "series": "bangladesh", "format": FORMAT_ODI, "status": "live",
     "title": "DEMO: 3rd ODI — Bangladesh vs Australia"},
    # T20s
    {"id": "demo-ashes-t20", "series": "ashes", "format": FORMAT_T20, "status": "live",
     "title": "DEMO: 2nd T20I — England vs Australia"},
    {"id": "demo-border-gavaskar-t20", "series": "border_gavaskar", "format": FORMAT_T20, "status": "live",
     "title": "DEMO: 3rd T20I — India vs Australia"},
    {"id": "demo-trans-tasman-t20", "series": "trans_tasman", "format": FORMAT_T20, "status": "live",
     "title": "DEMO: 1st T20I — New Zealand vs Australia"},
    {"id": "demo-south-africa-t20", "series": "south_africa", "format": FORMAT_T20, "status": "live",
     "title": "DEMO: 2nd T20I — South Africa vs Australia"},
    {"id": "demo-pakistan-t20", "series": "pakistan", "format": FORMAT_T20, "status": "live",
     "title": "DEMO: 3rd T20I — Pakistan vs Australia"},
    {"id": "demo-sri-lanka-t20", "series": "sri_lanka", "format": FORMAT_T20, "status": "live",
     "title": "DEMO: 1st T20I — Sri Lanka vs Australia"},
    {"id": "demo-west-indies-t20", "series": "west_indies", "format": FORMAT_T20, "status": "live",
     "title": "DEMO: 2nd T20I — West Indies vs Australia"},
    # Upcoming
    {"id": "fixture-ashes-2027-test", "series": "ashes", "format": FORMAT_TEST, "status": "upcoming",
     "title": "1st Test: England vs Australia — Ashes 2027", "venue": "Edgbaston, Birmingham"},
    {"id": "fixture-ashes-2027-odi", "series": "ashes", "format": FORMAT_ODI, "status": "upcoming",
     "title": "1st ODI: England vs Australia — 2027", "venue": "Lord's, London"},
    {"id": "fixture-border-gavaskar-t20", "series": "border_gavaskar", "format": FORMAT_T20, "status": "upcoming",
     "title": "1st T20I: India vs Australia — 2026", "venue": "Optus Stadium, Perth"},
    {"id": "fixture-world-cup-odi", "series": "border_gavaskar", "format": FORMAT_ODI, "status": "upcoming",
     "title": "ICC Cricket World Cup: India vs Australia", "venue": "Narendra Modi Stadium, Ahmedabad"},
    {"id": "fixture-t20-world-cup", "series": "ashes", "format": FORMAT_T20, "status": "upcoming",
     "title": "ICC T20 World Cup: England vs Australia", "venue": "Kensington Oval, Barbados"},
]


def fixture_lookup(match_id: str) -> dict | None:
    for fix in DEMO_FIXTURES:
        if fix["id"] == match_id:
            return fix
    return None