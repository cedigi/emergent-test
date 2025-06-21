from store import DatabaseManager


def test_update_team_changes_fields():
    db = DatabaseManager("file::memory:?cache=shared")
    tid = db.create_tournament("T", "doublette", 2)
    team_id = db.create_team(tid, "Old", ["a","b"])
    db.update_team(team_id, name="New", players=["c","d"])
    team = db.get_teams_by_tournament(tid)[0]
    assert team['name'] == "New"
    assert team['players'] == ["c","d"]
