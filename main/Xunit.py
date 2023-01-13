class TestCase:
    def __init__(self, name):
        self.name = name
        self.wasRun = None
        self.log = None
        self.suite = TestSuite()

    def setup(self):
        pass

    def teardown(self):
        pass

    def run(self, result):
        result.test_started()
        try:
            self.setup()
        except:
            result.test_setup_error()
        try:
            method = getattr(self, self.name)
            method()
        except:
            result.test_failed()
        self.teardown()


class TestSuite:
    def __init__(self):
        self.tests = []

    def add(self, test):
        self.tests.append(test)

    def run(self, result):
        for test in self.tests:
            test.run(result)


class TestResult:
    def __init__(self):
        self.runCount = 0
        self.failedCount = 0
        self.setup_error = ""

    def test_started(self):
        self.runCount = self.runCount + 1

    def test_failed(self):
        self.failedCount = self.failedCount + 1

    def test_setup_error(self):
        self.setup_error = "[setup error]"

    def summary(self):
        return "%d run, %d failed%s" % (self.runCount, self.failedCount, self.setup_error)


class WasRun(TestCase):
    def setup(self):
        self.wasRun = None
        self.log = "setUp "

    def testmethod(self):
        self.wasRun = 1
        self.log = self.log + "testMethod "

    def teardown(self):
        self.log = self.log + "tearDown "

    def test_broken_method(self):
        raise Exception


class TestCaseTest(TestCase):
    def setup(self):
        self.result = TestResult()
        # assert (1 == 2)

    def test_template_method(self):
        self.test = WasRun("testmethod")
        self.test.run(self.result)
        assert ("setUp testMethod tearDown " == self.test.log)

    def test_result(self):
        test = WasRun("testmethod")
        test.run(self.result)
        assert ("1 run, 0 failed" == self.result.summary())

    def test_failed_result(self):
        test = WasRun("testmethod")
        test.run(self.result)
        assert (not "1 run, 1 failed" == self.result.summary())

    def test_failed_result_formatting(self):
        self.result.test_started()
        self.result.test_failed()
        assert ("1 run, 1 failed" == self.result.summary())

    def test_suite(self):
        testsuite = TestSuite()
        testsuite.add(WasRun("testmethod"))
        testsuite.add(WasRun("test_broken_method"))
        testsuite.run(self.result)
        assert ("2 run, 1 failed" == self.result.summary())

    def test_make_suite(self):
        self.suite.add(WasRun("testmethod"))
        self.suite.add(WasRun("test_broken_method"))
        self.suite.run(self.result)
        assert ("2 run, 1 failed" == self.result.summary())

    def test_setup_failed(self):
        self.result.test_setup_error()
        assert ("[setup error]" == self.result.setup_error)


suite = TestSuite()
suite.add(TestCaseTest("test_template_method"))
suite.add(TestCaseTest("test_result"))
suite.add(TestCaseTest("test_failed_result_formatting"))
suite.add(TestCaseTest("test_failed_result"))
suite.add(TestCaseTest("test_suite"))
suite.add(TestCaseTest("test_make_suite"))
suite.add(TestCaseTest("test_setup_failed"))
testResult = TestResult()
suite.run(testResult)
print(testResult.summary())
