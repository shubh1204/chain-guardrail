class DetectedPIISchema:
    def __init__(self, pii, category, score):
        self.pii = pii
        self.category = category
        self.score = score
