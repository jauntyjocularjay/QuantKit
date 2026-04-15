
import unittest
import stats

class TestMedianIndex(unittest.TestCase):

	def test_median_index_odd_length(self):
		# Should return the correct median index for sorted odd-length list
		self.assertEqual(stats.median_index([1, 2, 3, 4, 5]), (2,), "median_index should return (2,) for sorted odd-length list")
		# Should return the correct median index for unsorted odd-length list
		self.assertEqual(stats.median_index([5, 4, 3, 2, 1]), (2,), "median_index should return (2,) for unsorted odd-length list")
		# Should return (0,) for single-element list
		self.assertEqual(stats.median_index([10]), (0,), "median_index should return (0,) for single-element list")

	def test_median_index_even_length(self):
		# Should return the correct median indices for sorted even-length list
		self.assertEqual(stats.median_index([1, 2, 3, 4, 5, 6]), (2, 3), "median_index should return (2, 3) for sorted even-length list")
		# Should return the correct median indices for unsorted even-length list
		self.assertEqual(stats.median_index([6, 5, 4, 3, 2, 1]), (2, 3), "median_index should return (2, 3) for unsorted even-length list")
		# Should return (0, 1) for two-element list
		self.assertEqual(stats.median_index([10, 20]), (0, 1), "median_index should return (0, 1) for two-element list")

	def test_median_index_empty_list(self):
		# Should return () for empty list
		self.assertEqual(stats.median_index([]), (), "median_index should return () for empty list")

	def test_median_index_none(self):
		# Should return () for None input
		self.assertEqual(stats.median_index(None), (), "median_index should return () for None input")

	def test_median_index_duplicates(self):
		# Should return correct median index for odd-length list with duplicates
		self.assertEqual(stats.median_index([1, 2, 2, 3, 4]), (2,), "median_index should return (2,) for odd-length list with duplicates")
		# Should return correct median indices for even-length list with duplicates
		self.assertEqual(stats.median_index([1, 2, 2, 3, 4, 4]), (2, 3), "median_index should return (2, 3) for even-length list with duplicates")



class TestIqrSlice(unittest.TestCase):
	def test_iqr_slice_typical(self):
		# Should return correct slice for odd-length list
		self.assertEqual(stats.iqr_slice([1, 2, 3, 4, 5, 6, 7, 8, 9]), [3, 4, 5, 6, 7], "iqr_slice should return [3, 4, 5, 6, 7] for odd-length list")
		# Should return correct slice for even-length list
		self.assertEqual(stats.iqr_slice([1, 2, 3, 4, 5, 6, 7, 8]), [3, 4, 5, 6], "iqr_slice should return [3, 4, 5, 6] for even-length list")

	def test_iqr_slice_empty(self):
		# Should return None for empty list
		result = stats.iqr_slice([])
		self.assertIsNone(result, f"iqr_slice([]) returned {result} instead of None. iqr_slice should return None for empty list.")

	def test_iqr_slice_none(self):
		# Should return None for None input
		result = stats.iqr_slice(None)
		self.assertIsNone(result, f"iqr_slice(None) returned {result} instead of None. iqr_slice should return None for None input.")

	def test_iqr_slice_non_numeric(self):
		# Should raise TypeError for non-numeric input
		with self.assertRaises(TypeError, msg="iqr_slice should raise TypeError for non-numeric input (iqr_slice)"):
			stats.iqr_slice([1, 'a', 3])


class TestCheckListItemsAreNumbers(unittest.TestCase):

	def test_check_list_items_are_numbers_all_numbers(self):
		# Should not raise error for all-numeric input
		try:
			stats.check_list_items_are_numbers([1, 2, 3.5])
		except Exception as e:
			self.fail(f"check_list_items_are_numbers raised {type(e).__name__} unexpectedly on all-numeric input: {e}. check_list_items_are_numbers should not raise any error for all-numeric input.")

	def test_check_list_items_are_numbers_empty(self):
		# Should not raise error for empty list
		try:
			stats.check_list_items_are_numbers([])
		except Exception as e:
			self.fail(f"check_list_items_are_numbers raised {type(e).__name__} unexpectedly on empty list: {e}. check_list_items_are_numbers should not raise any error for empty list.")

	def test_check_list_items_are_numbers_none(self):
		# Should not raise error for None input
		try:
			stats.check_list_items_are_numbers(None)
		except Exception as e:
			self.fail(f"check_list_items_are_numbers raised {type(e).__name__} unexpectedly on None input: {e}. check_list_items_are_numbers should not raise any error for None input.")

	def test_check_list_items_are_numbers_non_number(self):
		# Should raise TypeError for non-numeric input
		with self.assertRaises(TypeError, msg="check_list_items_are_numbers should raise TypeError for non-numeric input (check_list_items_are_numbers)"):
			stats.check_list_items_are_numbers([1, 'b', 3])

if __name__ == "__main__":
	unittest.main()
