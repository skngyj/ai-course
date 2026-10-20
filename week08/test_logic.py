import unittest
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from week08.logic import calculate_fee

class TestCalculateFee(unittest.TestCase):
    def test_1_hour_parking(self):
        """1시간 주차: 10:00 -> 11:00 = 1시간 0분, 1,500원"""
        # 60분 - 30분(무료) = 30분 -> 3개 구간 (30/10 = 3) -> 3 * 500 = 1500
        # wait, let's check logic: (60-30+9)//10 = 39//10 = 3. 3*500=1500. Correct.
        result = calculate_fee("10:00", "11:00")
        self.assertEqual(result["status"], "success")
        self.assertEqual(result["duration_min"], 60)
        self.assertEqual(result["display_time"], "1시간 0분")
        self.assertEqual(result["fee"], 1500)

    def test_2_midnight_crossing(self):
        """자정 넘김: 23:00 -> 01:00 = 2시간 0분, 4,500원"""
        # 120분 - 30분 = 90분 -> 9개 구간 -> 9 * 500 = 4500. Correct.
        result = calculate_fee("23:00", "01:00")
        self.assertEqual(result["status"], "success")
        self.assertEqual(result["duration_min"], 120)
        self.assertEqual(result["display_time"], "2시간 0분")
        self.assertEqual(result["fee"], 4500)

    def test_3_free_period(self):
        """30분 무료: 10:00 -> 10:30 = 0원"""
        result = calculate_fee("10:00", "10:30")
        self.assertEqual(result["status"], "success")
        self.assertEqual(result["duration_min"], 30)
        self.assertEqual(result["display_time"], "0시간 30분")
        self.assertEqual(result["fee"], 0)

    def test_4_31_min_parking(self):
        """31분 주차: 10:00 -> 10:31 = 500원"""
        # 31분 - 30분 = 1분 -> 1개 구간 -> 500. Correct.
        result = calculate_fee("10:00", "10:31")
        self.assertEqual(result["status"], "success")
        self.assertEqual(result["duration_min"], 31)
        self.assertEqual(result["fee"], 500)

    def test_5_35_min_parking(self):
        """35분 주차: 10:00 -> 10:35 = 500원"""
        # 35분 - 30분 = 5분 -> 1개 구간 -> 500. Correct.
        result = calculate_fee("10:00", "10:35")
        self.assertEqual(result["status"], "success")
        self.assertEqual(result["duration_min"], 35)
        self.assertEqual(result["fee"], 500)

    def test_6_max_fee(self):
        """최대 요금: 10:00 -> 20:00 = 20,000원"""
        result = calculate_fee("10:00", "20:00")
        self.assertEqual(result["status"], "success")
        self.assertEqual(result["fee"], 20000)

    def test_7_empty_input(self):
        """빈 입력 오류"""
        result = calculate_fee("", "10:00")
        self.assertEqual(result["status"], "error")
        self.assertIn("비어 있습니다", result["message"])

    def test_8_invalid_time_format(self):
        """잘못된 시간 오류"""
        result = calculate_fee("25:00", "10:00")
        self.assertEqual(result["status"], "error")
        self.assertIn("형식", result["message"])

    def test_9_same_time_error(self):
        """동일 시각 오류"""
        result = calculate_fee("10:00", "10:00")
        self.assertEqual(result["status"], "error")
        self.assertIn("동일할 수 없습니다", result["message"])

    def test_10_return_dict_format(self):
        """성공 결과의 반환 dict 형식 확인"""
        result = calculate_fee("10:00", "11:00")
        self.assertIsInstance(result, dict)
        self.assertIn("status", result)
        self.assertIn("duration_min", result)
        self.assertIn("display_time", result)
        self.assertIn("fee", result)

if __name__ == "__main__":
    import sys
    
    # Run tests manually to control output format as requested
    suite = unittest.TestLoader().loadTestsFromTestCase(TestCalculateFee)
    runner = unittest.TextTestRunner(stream=sys.stdout, verbosity=2)
    result = runner.run(suite)

    print()
    passed = result.testsRun - len(result.failures) - len(result.errors)
    failed = len(result.failures) + len(result.errors)
    
    print(f"Passed: {passed}, Failed: {failed}")
    
    if failed > 0:
        sys.exit(1)
    else:
        sys.exit(0)