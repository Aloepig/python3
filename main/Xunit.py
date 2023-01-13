class TestCase:
    def __init__(self, name):
        self.name = name
        self.wasRun = None
        self.log = None

    def setup(self):
        pass

    def teardown(self):
        pass

    def run(self):
        result = TestResult()
        result.test_started()
        self.setup()
        method = getattr(self, self.name)
        method()
        self.teardown()
        return result


class TestResult:
    def __init__(self):
        self.runCount = 0
        self.failedCount = 0

    def test_started(self):
        self.runCount = self.runCount + 1

    def test_failed(self):
        self.failedCount = self.failedCount + 1

    def summary(self):
        return "%d run, %d failed" % (self.runCount, self.failedCount)


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
    def test_result(self):
        test = WasRun("testmethod")
        result = test.run()
        assert ("1 run, 0 failed" == result.summary())

    def test_failed_result(self):
        test = WasRun("testmethod")
        result = test.run()
        assert ("1 run, 1 failed" == result.summary())

    def test_template_method(self):
        self.test = WasRun("testmethod")
        self.test.run()
        assert ("setUp testMethod tearDown " == self.test.log)

    def test_failed_result_formatting(self):
        result = TestResult()
        result.test_started()
        result.test_failed()
        assert ("1 run, 1 failed" == result.summary())


TestCaseTest("test_template_method").run()
TestCaseTest("test_result").run()
TestCaseTest("test_failed_result_formatting").run()
TestCaseTest("test_failed_result").run()
