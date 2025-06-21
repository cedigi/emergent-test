from store import DatabaseManager

def test_delete_tournament_cascades():
    db = DatabaseManager("file::memory:?cache=shared")
    tid = db.create_tournament("T", "doublette", 2)
    t1 = db.create_team(tid, "A", ["a","b"])
    t2 = db.create_team(tid, "B", ["c","d"])
    db.create_match(tid, 1, t1, t2)
    db.delete_tournament(tid)
    assert db.get_tournament(tid) is None
    assert db.get_teams_by_tournament(tid) == []
    assert db.get_matches_by_tournament_round(tid, 1) == []
