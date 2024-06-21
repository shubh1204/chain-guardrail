from typing import List

from presidio_analyzer import AnalyzerEngine
from presidio_anonymizer import AnonymizerEngine, EngineResult


def parse_text(text: str) -> EngineResult:
    # TODO: handle names with "'"
    # text = text.replace("' ", "")
    # text = text.replace("'", "")
    analyzer = AnalyzerEngine()
    engine = AnonymizerEngine()

    results = analyzer.analyze(text=text, language="en", score_threshold=0.4)
    engine.anonymize(text=text, analyzer_results=results)

    return engine.anonymize(text=text, analyzer_results=results)
