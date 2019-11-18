import unittest
from docker_pull import command_parser, DEFAULT_REPO, DEFAULT_URL, DEFAULT_TAG


class TestDockerPull(unittest.TestCase):
    def test_command_parser(self):
        test1 = 'hello-world'
        results1 = (
            DEFAULT_URL,
            DEFAULT_REPO,
            test1,
            DEFAULT_TAG
        )
        self.assertEqual(command_parser(test1), results1)

        test2 = 'abc/hello-world'
        results2 = (
            DEFAULT_URL,
            'abc',
            'hello-world',
            DEFAULT_TAG
        )
        self.assertEqual(command_parser(test2), results2)

        test3 = 'mcr.microsoft.com/test-lib/hello-world'
        results3 = (
            'mcr.microsoft.com',
            'test-lib',
            'hello-world',
            DEFAULT_TAG
        )
        self.assertEqual(command_parser(test3), results3)

        test4 = 'mcr.microsoft.com/test-lib/hello-world:123'
        results4 = (
            'mcr.microsoft.com',
            'test-lib',
            'hello-world',
            '123'
        )
        self.assertEqual(command_parser(test4), results4)

        test5 = 'mcr.microsoft.com/test-lib/hello-world@sha1:123'
        results5 = (
            'mcr.microsoft.com',
            'test-lib',
            'hello-world',
            'sha1:123'
        )
        self.assertEqual(command_parser(test5), results5)

        test6 = 'test-lib/hello-world@sha1:123'
        results6 = (
            DEFAULT_URL,
            'test-lib',
            'hello-world',
            'sha1:123'
        )
        self.assertEqual(command_parser(test6), results6)

        test7 = 'test-lib/hello-world:123'
        results7 = (
            DEFAULT_URL,
            'test-lib',
            'hello-world',
            '123'
        )
        self.assertEqual(command_parser(test7), results7)

        test8 = 'hello-world@sha1:123'
        results8 = (
            DEFAULT_URL,
            DEFAULT_REPO,
            'hello-world',
            'sha1:123'
        )
        self.assertEqual(command_parser(test8), results8)

        test9 = 'hello-world:123'
        results9 = (
            DEFAULT_URL,
            DEFAULT_REPO,
            'hello-world',
            '123'
        )
        self.assertEqual(command_parser(test9), results9)


if __name__ == '__main__':
    unittest.main()
