#!/usr/bin/env python3

from .model_card import ModelCard
from .pdf_elements import first_page_elements
from fpdf import Template
from PyPDF2 import PdfFileMerger
from os import remove
from typing import List

first_page_filename = './pag_1.pdf'
final_filename='./cartao_de_modelo.pdf'

def merge_pdfs(final_filename: str, *filenames: List[str]):
    """Merge multiples PDF into one"""

    pdf_merger = PdfFileMerger()

    for f in filenames:
        pdf_merger.append(f)

    pdf_merger.write(final_filename)

    for f in filenames:
        remove(f)

def write_first_page(model_card: ModelCard, filename: str):
    t = Template(format='A4', elements=first_page_elements, title='Cartão de Modelo', author='')
    t.add_page()

    t['model_name'] = model_card.model_name
    t['model_date'] = model_card.model_date
    t['model_version'] = model_card.model_version
    t['dataset_total_images'] = 'Total de {} imagens'.format(model_card.dataset_total_images)
    t['dataset_augmentation_type'] = model_card.dataset_augmentation_type
    t['dataset_batch_size'] = model_card.dataset_batch_size

    dataset_training_percentage = 1 - model_card.dataset_validation_percentage
    t['dataset_validation_percentage'] = \
        '{}% para treinamento ({} imagens), {}% para validação ({} imagens)'.format(
        int(dataset_training_percentage * 100), 
        int(model_card.dataset_total_images * dataset_training_percentage),
        int(model_card.dataset_validation_percentage * 100),
        int(model_card.dataset_total_images * model_card.dataset_validation_percentage))

    t.render(filename)

def write_pdf(model_card: ModelCard): 
    """Generates Model Card PDF"""

    write_first_page(model_card, first_page_filename)
    merge_pdfs(final_filename, first_page_filename)