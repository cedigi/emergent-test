from store import DatabaseManager


def test_update_match_court():
    db = DatabaseManager("file::memory:?cache=shared")
    tid = db.create_tournament("T", "doublette", 2)
    t1 = db.create_team(tid, "A", ["a","b"])
    t2 = db.create_team(tid, "B", ["c","d"])
    mid = db.create_match(tid, 1, t1, t2, court_number=1)
    db.update_match_court(mid, 5)
    match = db.get_matches_by_tournament_round(tid, 1)[0]
    assert match['court_number'] == 5
