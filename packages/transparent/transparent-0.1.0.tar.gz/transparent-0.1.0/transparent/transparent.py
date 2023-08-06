import os
import sys
import numpy as np
import pandas as pd


class TransparentAI:
    def __init__(self, model, data, labels):
        self.model = model
        self.data = data
        self.labels = labels

    def preprocess(self):
        pass
