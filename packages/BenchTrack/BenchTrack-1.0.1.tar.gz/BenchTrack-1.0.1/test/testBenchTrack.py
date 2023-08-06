import unittest
import BenchTrack.tools as tl
import BenchTrack.structureBench as bt

class TestMathFunc(unittest.TestCase):
    """Test BenchTrack.py"""
    def test_construct(self):
        bench = bt.BenchTrack("../../infrastructures/PGM", "")
        self.assertEqual("PGM",bench.getName())
        string = "PGM:list Themes[inference[BIFreading[pyAgrumTest ]]]"
        self.assertEqual(string,bench.__str__())

    def test_structure(self):
        bench = bt.BenchTrack("../../infrastructures/PGM", "")
        structure = bench.get_structure_tasks()
        theme = structure['inference']
        task = theme['BIFreading']
        self.assertEqual(task[0],'pyAgrumTest.py')

    def test_filter_target(self):
        bench = bt.BenchTrack("../../infrastructures/PGM", "")
        number = bench.filter_target(['pyAgrumTest'],False)
        self.assertEqual(number,0)
        number = bench.filter_target(['pyAgrumTest'], True)
        self.assertEqual(number,1)

    def test_filter_task(self):
        bench = bt.BenchTrack("../../infrastructures/PGM", "")
        number = bench.filter_task(['BIFreading'],False)
        self.assertEqual(number,0)
        number = bench.filter_task(['BIFreading'], True)
        self.assertEqual(number,1)

    def test_filter_task(self):
        bench = bt.BenchTrack("../../infrastructures/PGM", "")
        number = bench.filter_task(['BIFreading'],False)
        self.assertEqual(number,0)
        number = bench.filter_task(['BIFreading'], True)
        self.assertEqual(number,1)

    def test_execute(self):
        self.assertTrue(tl.exeCmd("../../infrastructures/PGM/tasks/inference/BIFreading", "asia.bif", "python {script} {arg}", "python", "pyAgrumTest"))

    def text_To_Csv(self):
        bench = bt.BenchTrack("../../infrastructures/PGM", "")
        bench.ToCsv()


if __name__ == '__main__':
    unittest.main()
