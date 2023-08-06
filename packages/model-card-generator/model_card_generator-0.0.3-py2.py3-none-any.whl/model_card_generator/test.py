#!/usr/bin/env python3

from .env import get_env
from .model_card import ModelCard

env_dict = {
    # Model card
    'name':                  'MODEL_NAME',
    'date':                  'MODEL_DATE',
    'version':               'MODEL_VERSION',

    # Dataset
    'aroeira_images':       'DATASET_AROEIRA_IMAGES',
    'capororoca_images':    'DATASET_CAPOROROCA_IMAGES',
    'embauba_images':       'DATASET_EMBAUBA_IMAGES',
    'jeriva_images':        'DATASET_JERIVA_IMAGES',
    'mulungu_images':       'DATASET_MULUNGU_IMAGES',
    'pitangueira_images':   'DATASET_PITANGUEIRA_IMAGES'
}

mc = ModelCard(
    get_env(env_dict['name']), 
    get_env(env_dict['date']), 
    get_env(env_dict['version']),
)
