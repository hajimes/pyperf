import glob
import os.path
import sys

from perf import tests
from perf.tests import unittest


ROOT_DIR = os.path.realpath(os.path.join(os.path.dirname(__file__), '..', '..'))
EXAMPLES_DIR = os.path.join(ROOT_DIR, 'doc', 'examples')


class ExampleTests(unittest.TestCase):
    TESTED = set()
    # It's not easy to test a GUI
    IGNORED = {'hist_scipy.py', 'plot.py'}

    @classmethod
    def tearDownClass(cls):
        scripts = glob.glob(os.path.join(EXAMPLES_DIR, '*.py'))
        scripts = list(map(os.path.basename, scripts))
        not_tested = set(scripts) - cls.IGNORED - cls.TESTED
        if not_tested:
            raise Exception("not tested scripts: %s" % sorted(not_tested))

    def check_command(self, script, args, nproc=3):
        self.TESTED.add(script)
        script = os.path.join(EXAMPLES_DIR, script)

        cmd = [sys.executable] + [script] + args + ["--inherit-env=PYTHONPATH"]
        proc = tests.get_output(cmd)

        self.assertRegex(proc.stdout,
                         r'Mean \+- std dev: [0-9.]+ [mun]s '
                         r'\+- [0-9.]+ [mun]s\n')
        self.assertEqual(proc.returncode, 0)

    def test_bench_func(self):
        script = 'bench_func.py'
        # Use -w1 --min-time=0.001 to reduce the duration of the test
        args = ['-p2', '-w1', '--min-time=0.001']
        self.check_command(script, args)

    def test_bench_func_no_warmup(self):
        script = 'bench_func.py'
        args = ['-p2', '-w0', '--min-time=0.001']
        self.check_command(script, args)

    def test_bench_time_func(self):
        script = 'bench_time_func.py'
        args = ['-p2', '-w1', '--min-time=0.001']
        self.check_command(script, args)

    def test_bench_command(self):
        script = 'bench_command.py'
        args = ['-p2', '-w1', '--min-time=0.001']
        self.check_command(script, args)

    def test_bench_timeit(self):
        script = 'bench_timeit.py'
        args = ['-p2', '-w1', '--min-time=0.001']
        self.check_command(script, args)


if __name__ == "__main__":
    unittest.main()
