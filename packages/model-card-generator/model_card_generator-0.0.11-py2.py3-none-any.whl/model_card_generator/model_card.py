#!/usr/bin/env python3

class ModelCard:
    """Machine Learning Model Card"""
    
    def __init__(self, 
                model_name: str, 
                model_date: str, 
                model_version: str, 
                dataset_total_images: int, 
                dataset_augmentation_type: str, 
                dataset_batch_size: int, 
                dataset_validation_percentage: float):
        self.model_name = str(model_name)
        self.model_date = str(model_date)
        self.model_version = str(model_version)

        self.dataset_total_images = int(dataset_total_images)
        self.dataset_augmentation_type = str(dataset_augmentation_type)
        self.dataset_batch_size = int(dataset_batch_size)
        self.dataset_validation_percentage = float(dataset_validation_percentage)