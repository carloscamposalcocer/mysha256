import hashlib
import unittest
import hash


class MyTestCase(unittest.TestCase):
    def test_sha256_FirstDigits_CompareWithHaslib(self):

        for i in range(3):
            expected_result = hashlib.sha256(str(i).encode()).hexdigest()
            result = hash.my_sha256(str(i))

            self.assertEqual(result, expected_result)


if __name__ == '__main__':
    unittest.main()
