import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from agent.graph import run_question


class GraphTest(unittest.TestCase):
    def test_gmv_last_7_days(self):
        result = run_question("最近7天GMV是多少？")
        self.assertEqual(result["metric_name"], "gmv")
        self.assertEqual(result["time_range"], "last_7_days")
        self.assertIn("SUM(order_amount)", result["generated_sql"])
        self.assertEqual(result["final_answer"], "最近7天GMV为125430元。")
        self.assertEqual(len(result["messages"]), 2)

    def test_last_week_followup_inherits_gmv(self):
        result1 = run_question("最近7天GMV是多少？")
        result2 = run_question("上周呢？", result1)
        self.assertEqual(result2["metric_name"], "gmv")
        self.assertEqual(result2["time_range"], "last_week")
        self.assertIn("current_week", result2["generated_sql"])
        self.assertNotIn("-- need context", result2["generated_sql"])
        self.assertIn("上周GMV为118200元", result2["final_answer"])

    def test_channel_followup_inherits_gmv_and_time_range(self):
        result1 = run_question("最近7天GMV是多少？")
        result2 = run_question("按渠道拆一下？", result1)
        self.assertEqual(result2["metric_name"], "gmv")
        self.assertEqual(result2["time_range"], "last_7_days")
        self.assertEqual(result2["dimensions"], ["channel"])
        self.assertIn("GROUP BY channel", result2["generated_sql"])
        self.assertIn("app 62300元", result2["final_answer"])

    def test_chinese_delete_is_blocked_before_execution(self):
        result = run_question("删除订单表。")
        self.assertIn("安全拦截", result["final_answer"])
        self.assertEqual(result["generated_sql"], "")
        self.assertIsNone(result["query_result"])

    def test_english_drop_is_blocked_before_execution(self):
        result = run_question("DROP TABLE orders;")
        self.assertIn("安全拦截", result["final_answer"])
        self.assertEqual(result["generated_sql"], "")
        self.assertIsNone(result["query_result"])


if __name__ == "__main__":
    unittest.main()
