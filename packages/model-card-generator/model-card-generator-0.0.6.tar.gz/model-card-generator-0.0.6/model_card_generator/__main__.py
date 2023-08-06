#!/usr/bin/env python3

from .env import get_env
from .model_card import ModelCard
from .pdf import write_pdf

mc = ModelCard(
    get_env('MODEL_NAME'), 
    get_env('MODEL_DATE'), 
    get_env('MODEL_VERSION'),
    get_env('DATASET_TOTAL_IMAGES'),
    get_env('DATASET_AUGMENTATION_TYPE'),
    get_env('DATASET_BATCH_SIZE'),
    get_env('DATASET_VALIDATION_PERCENTAGE'),
)

write_pdf(mc)