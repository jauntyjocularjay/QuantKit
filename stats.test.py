import unittest, console
import stats

console.clear()

class TestMedianIndex(unittest.TestCase):

	def test_odd_length(self):
		# Verifies that a sorted odd-length list returns a single-element tuple with the correct median index
		self.assertEqual(stats.median_index([1, 2, 3, 4, 5]), (2,), "Failed on sorted odd-length list")
		# Verifies that an unsorted odd-length list returns a single-element tuple with the correct median index
		self.assertEqual(stats.median_index([5, 4, 3, 2, 1]), (2,), "Failed on unsorted odd-length list")
		# Verifies that a single-element list returns a tuple with index 0
		self.assertEqual(stats.median_index([10]), (0,), "Failed on single-element list")

	def test_even_length(self):
		# Verifies that a sorted even-length list returns a tuple with the two correct median indices
		self.assertEqual(stats.median_index([1, 2, 3, 4, 5, 6]), (2, 3), "Failed on sorted even-length list")
		# Verifies that an unsorted even-length list returns a tuple with the two correct median indices
		self.assertEqual(stats.median_index([6, 5, 4, 3, 2, 1]), (2, 3), "Failed on unsorted even-length list")
		# Verifies that a two-element list returns a tuple with indices 0 and 1
		self.assertEqual(stats.median_index([10, 20]), (0, 1), "Failed on two-element list")

	def test_empty_lists(self):
		# Verifies that an empty list returns an empty tuple
		self.assertEqual(stats.median_index([]), (), "Failed on empty list")
  
	def test_none(self):
		# Verifies that None input returns an empty tuple
		self.assertEqual(stats.median_index(None), (), "Failed on None input")

	def test_duplicates(self):
		# Verifies that an odd-length list with duplicate values returns the correct median index
		self.assertEqual(stats.median_index([1, 2, 2, 3, 4]), (2,), "Failed on odd-length list with duplicates")
		# Verifies that an even-length list with duplicate values returns the correct median indices
		self.assertEqual(stats.median_index([1, 2, 2, 3, 4, 4]), (2, 3), "Failed on even-length list with duplicates")



class TestIqrSlice(unittest.TestCase):
	def test_typical(self):
		# Verifies correct slice for odd-length list
		self.assertEqual(stats.iqr_slice([1, 2, 3, 4, 5, 6, 7, 8, 9]), [3, 4, 5, 6, 7], "Failed on odd-length list")
		# Verifies correct slice for even-length list
		self.assertEqual(stats.iqr_slice([1, 2, 3, 4, 5, 6, 7, 8]), [3, 4, 5, 6], "Failed on even-length list")

	def test_empty(self):
		# Verifies None for empty list
		self.assertIsNone(stats.iqr_slice([]), "Failed on empty list")

	def test_none(self):
		# Verifies None for None input
		self.assertIsNone(stats.iqr_slice(None), "Failed on None input")

	def test_non_numeric(self):
		# Verifies TypeError for non-numeric input
		with self.assertRaises(TypeError):
			stats.iqr_slice([1, 'a', 3])


class TestCheckListItemsAreNumbers(unittest.TestCase):
	def test_all_numbers(self):
		# Should not raise
		stats.check_list_items_are_numbers([1, 2, 3.5])

	def test_empty(self):
		# Should not raise
		stats.check_list_items_are_numbers([])

	def test_none(self):
		# Should not raise
		stats.check_list_items_are_numbers(None)

	def test_non_number(self):
		# Should raise TypeError
		with self.assertRaises(TypeError):
			stats.check_list_items_are_numbers([1, 'b', 3])

if __name__ == "__main__":
	unittest.main()
