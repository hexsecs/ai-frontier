import unittest
from chatgpt_charts import convert, to_vega

class ChartTests(unittest.TestCase):
    def test_bar(self):
        source = {"chartType":"bar","xKey":"method","series":[{"dataKey":"rate","label":"Success","valueSuffix":"%"}],"yAxisMin":0,"data":[{"method":"Native","rate":15.24},{"method":"ANGLER","rate":20.36}]}
        result = to_vega(source)
        self.assertEqual(result["mark"]["type"], "bar")
        self.assertEqual([r["value"] for r in result["data"]["values"]], [15.24, 20.36])
        self.assertEqual(result["encoding"]["y"]["scale"]["domainMin"], 0)
    def test_inline(self):
        raw = '<Chart content={{"chartType":"bar","xKey":"x","series":[{"dataKey":"y"}],"data":[{"x":"a","y":3}]}}/>'
        self.assertIn("```vega-lite", convert(raw))
        self.assertNotIn("<Chart", convert(raw))
    def test_invalid(self):
        with self.assertRaises(ValueError):
            to_vega({"chartType":"unknown","xKey":"x","series":[],"data":[]})

if __name__ == "__main__":
    unittest.main()
