try:
    from ragas import evaluate
    from ragas.metrics import faithfulness
except ImportError:
    evaluate = None
    faithfulness = None