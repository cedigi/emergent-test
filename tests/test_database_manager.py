import sqlite3
import os
from store import DatabaseManager


def test_database_crud_operations(tmp_path):
    db_file = tmp_path / "test.db"
    dbm = DatabaseManager(db_path=str(db_file))

    # Tournament CRUD
    tid = dbm.create_tournament("Test", "doublette", 2)
    tournament = dbm.get_tournament(tid)
    assert tournament["name"] == "Test"
    assert tournament["type"] == "doublette"

    dbm.update_tournament(tid, current_round=1)
    assert dbm.get_tournament(tid)["current_round"] == 1

    # Team CRUD
    team_id = dbm.create_team(tid, "Team A", ["A", "B"])
    teams = dbm.get_teams_by_tournament(tid)
    assert len(teams) == 1
    assert teams[0]["id"] == team_id
    assert teams[0]["players"] == ["A", "B"]

    dbm.update_team_stats(team_id, wins=1, losses=0, points_for=13, points_against=7)
    teams = dbm.get_teams_by_tournament(tid)
    assert teams[0]["wins"] == 1
    assert teams[0]["points_for"] == 13
    assert teams[0]["points_against"] == 7

    # Match CRUD
    match_id = dbm.create_match(tid, 1, team_id, team_id, court_number=1)
    matches = dbm.get_matches_by_tournament_round(tid, 1)
    assert len(matches) == 1
    assert matches[0]["id"] == match_id

    dbm.update_match_score(match_id, 13, 7)
    matches = dbm.get_matches_by_tournament_round(tid, 1)
    assert matches[0]["team1_score"] == 13
    assert matches[0]["team2_score"] == 7
    assert matches[0]["status"] == "finished"

    # Standings
    standings = dbm.get_team_standings(tid)
    assert len(standings) == 1
    assert standings[0]["name"] == "Team A"
