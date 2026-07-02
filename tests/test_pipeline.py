import sqlite3, tempfile, unittest
from pathlib import Path
from src.build_database import build
from src.evaluate import evaluate
from src.generate_data import generate


class PipelineTests(unittest.TestCase):
    def test_pipeline_protects_high_risk_cases(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp); raw=root/"raw"; db=root/"test.db"
            generate(raw, n=600, seed=4)
            build(raw/"tickets.csv", db, Path(__file__).parents[1]/"sql")
            result=evaluate(db)
            self.assertEqual(result["high_risk_escaped"], 0)

    def test_all_tickets_reach_decision(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp); raw=root/"raw"; db=root/"test.db"
            generate(raw, n=400, seed=8); build(raw/"tickets.csv", db, Path(__file__).parents[1]/"sql")
            with sqlite3.connect(db) as conn:
                total, decided=conn.execute("SELECT COUNT(*),SUM(automated IN (0,1)) FROM tickets").fetchone()
            self.assertEqual(total, decided)


if __name__ == "__main__": unittest.main()

