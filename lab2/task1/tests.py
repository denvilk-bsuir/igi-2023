import unittest
import utils


class Unit(unittest.TestCase):

    def test_sentences(self):
        text = "Hello Mr.Pliska. How are your Mrs.Tushinskaya? "
        sentences = utils.divide_all_sentences(text)
        self.assertEqual(len(sentences), 2)
        self.assertEqual(sentences[0][1], '.')
        self.assertEqual(sentences[1][1], '?')

    def test_check_number(self):
        self.assertEqual(utils.check_not_number('C12'), True)
        self.assertEqual(utils.check_not_number('@'), True)
        self.assertEqual(utils.check_not_number('12213'), False)

    def test_get_top_n_grams(self):
        d = {
            "abced": 123,
            "sfd": 1,
            "fas": 432,
            "twer": 0
        }
        ans = [
            ("fas", 432),
            ("abced", 123),
            ("sfd", 1),
            ("twer", 0),
        ]
        self.assertListEqual(utils.get_top_n_grams(d), ans)


if __name__ == '__main__':
    unittest.main()
