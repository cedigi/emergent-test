import pytest
from store import DatabaseManager

@pytest.fixture
def db():
    return DatabaseManager("file::memory:?cache=shared")

def test_delete_team_removes_matches(db):
    tid = db.create_tournament("T", "doublette", 2)
    team1 = db.create_team(tid, "A", ["a","b"])
    team2 = db.create_team(tid, "B", ["c","d"])
    db.create_match(tid, 1, team1, team2)
    db.delete_team(team1)
    teams = db.get_teams_by_tournament(tid)
    assert all(t['id'] != team1 for t in teams)
    matches = db.get_matches_by_tournament_round(tid, 1)
    assert matches == []
