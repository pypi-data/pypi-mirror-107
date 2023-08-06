#!/usr/bin/env python3

import os

def get_env(name: str):
    """Get environment variable value"""
    
    return os.environ[name]