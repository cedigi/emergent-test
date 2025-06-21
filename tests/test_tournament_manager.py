import importlib
from store import DatabaseManager
import store
import tournament


def test_generate_next_round(monkeypatch, tmp_path):
    db_file = tmp_path / "test.db"
    test_db = DatabaseManager(db_path=str(db_file))

    # Patch global db_manager in store and tournament modules
    monkeypatch.setattr(store, "db_manager", test_db)
    importlib.reload(tournament)
    monkeypatch.setattr(tournament, "db_manager", test_db)

    tm = tournament.TournamentManager()

    tid = test_db.create_tournament("Test", "doublette", 2)
    for i in range(4):
        test_db.create_team(tid, f"Team {i}", [f"P{i}a", f"P{i}b"])

    matches = tm.generate_next_round(tid)

    assert len(matches) == 2
    assert test_db.get_tournament(tid)["current_round"] == 1

    stored_matches = test_db.get_matches_by_tournament_round(tid, 1)
    assert len(stored_matches) == 2
