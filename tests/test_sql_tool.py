import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from tools.sql_tool import generate_sql


class SqlToolTest(unittest.TestCase):
    def test_generates_gmv_sql(self):
        sql = generate_sql("最近7天GMV是多少？")
        self.assertIn("SUM(order_amount)", sql)
        self.assertIn("order_status = 'paid'", sql)

    def test_followup_last_week_uses_gmv_context(self):
        messages = [
            {"role": "user", "content": "最近7天GMV是多少？"},
            {"role": "assistant", "content": "最近7天GMV为125430元。"},
        ]
        sql = generate_sql("上周呢？", messages)
        self.assertIn("current_week", sql)
        self.assertIn("last_week", sql)
        self.assertNotIn("-- need context", sql)

    def test_followup_channel_uses_structured_context(self):
        state = {
            "metric_name": "gmv",
            "time_range": "last_7_days",
            "dimensions": ["channel"],
        }
        sql = generate_sql("按渠道拆一下？", state=state)
        self.assertIn("GROUP BY channel", sql)
        self.assertIn("ORDER BY gmv DESC", sql)

    def test_delete_question_is_not_order_count_sql(self):
        sql = generate_sql("删除订单表。")
        self.assertIn("-- blocked", sql)
        self.assertNotIn("COUNT", sql)


if __name__ == "__main__":
    unittest.main()
