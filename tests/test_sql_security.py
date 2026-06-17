import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from tools.sql_security import validate_sql, validate_user_question


class SqlSecurityTest(unittest.TestCase):
    def test_blocks_dangerous_chinese_question(self):
        error = validate_user_question("删除订单表。")
        self.assertIsNotNone(error)
        self.assertIn("安全拦截", error)

    def test_blocks_dangerous_english_question(self):
        error = validate_user_question("DROP TABLE orders;")
        self.assertIsNotNone(error)
        self.assertIn("安全拦截", error)

    def test_allows_safe_select(self):
        error = validate_sql("SELECT order_id FROM orders;")
        self.assertIsNone(error)

    def test_blocks_non_select_sql(self):
        error = validate_sql("DROP TABLE orders;")
        self.assertIsNotNone(error)
        self.assertIn("只允许执行 SELECT", error)

    def test_blocks_multi_statement_sql(self):
        error = validate_sql("SELECT order_id FROM orders; SELECT user_id FROM users;")
        self.assertIsNotNone(error)
        self.assertIn("禁止多语句", error)

    def test_blocks_select_star(self):
        error = validate_sql("SELECT * FROM orders;")
        self.assertIsNotNone(error)
        self.assertIn("禁止 SELECT *", error)


if __name__ == "__main__":
    unittest.main()
