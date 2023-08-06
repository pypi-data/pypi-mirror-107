#!/usr/bin/env python3

class ModelCard:
    """Machine Learning Model Card"""
    
    def __init__(self, name, date, version):
            self.name = name
            self.date = date 
            self.version = version

    def print(self):
        print("Model name is", self.name)
        print("Model date is", self.date)
        print("Model version is", self.version)