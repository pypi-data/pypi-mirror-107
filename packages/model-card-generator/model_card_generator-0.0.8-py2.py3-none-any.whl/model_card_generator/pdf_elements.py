#!/usr/bin/env python3

# x1 -> left
# y1 -> top
# x2 -> right
# y2 -> bottom

# General consts
frame_x1 = 15.0
frame_x2 = 195.0
offset = 3.0
left_text_x1 = frame_x1 + offset
vertical_divider_x = 80.0
right_text_x1 = vertical_divider_x + offset
highlight_color = 0x2A97DF
text_size = 11.0

first_page_elements = [
    # Header
    { 
        'name': 'card_logo', 'type': 'I', 
        'x1': 137.0, 'y1': 19.0, 
        'x2': 195.0, 'y2': 37.0, 
        'font': None, 'size': 0.0, 'bold': 0, 'italic': 0, 'underline': 0, 
        'foreground': 0, 'background': 0, 
 #       'align': 'R', 'text': './logo.png', 'priority': 2, 
    },
    { 
        'name': 'card_name', 'type': 'T', 
        'x1': left_text_x1, 'y1': 20.0, 
        'x2': 115.0, 'y2': 37.5, 
        'font': 'Arial', 'size': 20.0, 'bold': 1, 'italic': 0, 'underline': 0, 
        'foreground': highlight_color, 'background': 0, 
        'align': 'L', 'text': 'Cartão de Modelo', 'priority': 2, 
    },

    # Document frame
    { 
        'name': 'frame', 'type': 'B', 
        'x1': frame_x1, 'y1': 15.0, 
        'x2': 195.0, 'y2': 282.0, 
        'font': 'Arial', 'size': 0.0, 'bold': 0, 'italic': 0, 'underline': 0, 
        'foreground': 0, 'background': 0, 
        'align': 'I', 'text': None, 'priority': 1, 
    },
    { 
        'name': 'line_1', 'type': 'L', 
        'x1': frame_x1, 'y1': 40.0, 
        'x2': frame_x2, 'y2': 40.0, 
        'font': 'Arial', 'size': 0, 'bold': 0, 'italic': 0, 'underline': 0, 
        'foreground': 0, 'background': 0, 
        'align': 'I', 'text': None, 'priority': 3, 
    },
    { 
        'name': 'vertical_divider_1', 'type': 'L', 
        'x1': vertical_divider_x, 'y1': 40.0, 
        'x2': vertical_divider_x, 'y2': 70.0, 
        'font': 'Arial', 'size': 0, 'bold': 0, 'italic': 0, 'underline': 0, 
        'foreground': 0, 'background': 0, 
        'align': 'I', 'text': None, 'priority': 3, 
    },

    # Nome do modelo
    { 
        'name': 'text_1', 'type': 'T', 
        'x1': left_text_x1, 'y1': 40.0, 
        'x2': frame_x2, 'y2': 50.0, 
        'font': 'Arial', 'size': text_size, 'bold': 1, 'italic': 0, 'underline': 0, 
        'foreground': 0, 'background': 0, 
        'align': 'L', 'text': 'Nome do modelo', 'priority': 0, 'multiline': False,
    },
    { 
        'name': 'model_name', 'type': 'T', 
        'x1': right_text_x1, 'y1': 40.0, 
        'x2': frame_x2, 'y2': 50.0, 
        'font': 'Arial', 'size': text_size, 'bold': 0, 'italic': 0, 'underline': 0, 
        'foreground': 0, 'background': 0, 
        'align': 'L', 'text': '', 'priority': 0, 
    },
    { 
        'name': 'line_2', 'type': 'L', 
        'x1': frame_x1, 'y1': 50.0, 
        'x2': frame_x2, 'y2': 50.0, 
        'font': 'Arial', 'size': 0, 'bold': 0, 'italic': 0, 'underline': 0, 
        'foreground': 0, 'background': 0, 
        'align': 'I', 'text': None, 'priority': 3, 
    },

    # Data
    { 
        'name': 'text_3', 'type': 'T', 
        'x1': left_text_x1, 'y1': 50.0, 
        'x2': frame_x2, 'y2': 60.0, 
        'font': 'Arial', 'size': text_size, 'bold': 1, 'italic': 0, 'underline': 0, 
        'foreground': 0, 'background': 0, 
        'align': 'L', 'text': 'Data', 'priority': 0, 
    },
    { 
        'name': 'model_date', 'type': 'T', 
        'x1': right_text_x1, 'y1': 50.0, 
        'x2': frame_x2, 'y2': 60.0, 
        'font': 'Arial', 'size': text_size, 'bold': 0, 'italic': 0, 'underline': 0, 
        'foreground': 0, 'background': 0, 
        'align': 'L', 'text': '', 'priority': 0, 'multiline': False,
    },
    { 
        'name': 'line_3', 'type': 'L', 
        'x1': frame_x1, 'y1': 60.0, 
        'x2': frame_x2, 'y2': 60.0, 
        'font': 'Arial', 'size': 0, 'bold': 0, 'italic': 0, 'underline': 0, 
        'foreground': 0, 'background': 0, 
        'align': 'I', 'text': None, 'priority': 3, 
    },

    # Versão
    { 
        'name': 'text_5', 'type': 'T', 
        'x1': left_text_x1, 'y1': 60.0, 
        'x2': frame_x2, 'y2': 70.0, 
        'font': 'Arial', 'size': text_size, 'bold': 1, 'italic': 0, 'underline': 0, 
        'foreground': 0, 'background': 0, 
        'align': 'L', 'text': 'Versão', 'priority': 0, 
    },
    { 
        'name': 'model_version', 'type': 'T', 
        'x1': right_text_x1, 'y1': 60.0, 
        'x2': frame_x2, 'y2': 70.0, 
        'font': 'Arial', 'size': text_size, 'bold': 0, 'italic': 0, 'underline': 0, 
        'foreground': 0, 'background': 0, 
        'align': 'L', 'text': '', 'priority': 0, 'multiline': False,
    },
    { 
        'name': 'line_4', 'type': 'L', 
        'x1': frame_x1, 'y1': 70.0, 
        'x2': frame_x2, 'y2': 70.0, 
        'font': 'Arial', 'size': 0, 'bold': 0, 'italic': 0, 'underline': 0, 
        'foreground': 0, 'background': 0, 
        'align': 'I', 'text': None, 'priority': 3, 
    },

    # Objetivo do modelo de ML
    { 
        'name': 'text_7', 'type': 'T', 
        'x1': left_text_x1, 'y1': 70.0, 
        'x2': frame_x2, 'y2': 80.0, 
        'font': 'Arial', 'size': text_size, 'bold': 1, 'italic': 0, 'underline': 0, 
        'foreground': highlight_color, 'background': 0, 
        'align': 'L', 'text': 'Objetivo do modelo de ML', 'priority': 0, 
    },
    { 
        'name': 'line_5', 'type': 'L', 
        'x1': frame_x1, 'y1': 80.0, 
        'x2': frame_x2, 'y2': 80.0, 
        'font': 'Arial', 'size': 0, 'bold': 0, 'italic': 0, 'underline': 0, 
        'foreground': 0, 'background': 0, 
        'align': 'I', 'text': None, 'priority': 3, 
    },
    { 
        'name': 'vertical_divider_2', 'type': 'L', 
        'x1': vertical_divider_x, 'y1': 80.0, 
        'x2': vertical_divider_x, 'y2': 190.0, 
        'font': 'Arial', 'size': 0, 'bold': 0, 'italic': 0, 'underline': 0, 
        'foreground': 0, 'background': 0, 
        'align': 'I', 'text': None, 'priority': 3, 
    },

    # Tarefa
    { 
        'name': 'text_9', 'type': 'T', 
        'x1': left_text_x1, 'y1': 80.0, 
        'x2': frame_x2, 'y2': 90.0, 
        'font': 'Arial', 'size': text_size, 'bold': 1, 'italic': 0, 'underline': 0, 
        'foreground': 0, 'background': 0, 
        'align': 'L', 'text': 'Tarefa', 'priority': 0, 
    },
    { 
        'name': 'text_10', 'type': 'T', 
        'x1': right_text_x1, 'y1': 82.5, 
        'x2': frame_x2, 'y2': 87.5, 
        'font': 'Arial', 'size': text_size, 'bold': 0, 'italic': 0, 'underline': 0, 
        'foreground': 0, 'background': 0, 
        'align': 'L', 'text': 'Classificar/predizer a espécie de árvore de uma imagem de árvore (tipicamente a vista da árvore toda ou partes dentro do habitat natural (rua, praça, parque, etc.) capturada de um aplicativo Android em relação a 10 categorias de árvores', 'priority': 0, 'multiline': True, 
    },
    { 
        'name': 'line_6', 'type': 'L', 
        'x1': frame_x1, 'y1': 105.0, 
        'x2': frame_x2, 'y2': 105.0, 
        'font': 'Arial', 'size': 0, 'bold': 0, 'italic': 0, 'underline': 0, 
        'foreground': 0, 'background': 0, 
        'align': 'I', 'text': None, 'priority': 3, 
    },

    # Contexto de uso
    { 
        'name': 'text_10', 'type': 'T', 
        'x1': left_text_x1, 'y1': 105.0, 
        'x2': frame_x2, 'y2': 115.0, 
        'font': 'Arial', 'size': text_size, 'bold': 1, 'italic': 0, 'underline': 0, 
        'foreground': 0, 'background': 0, 
        'align': 'L', 'text': 'Contexto de uso', 'priority': 0, 
    },
    { 
        'name': 'text_11', 'type': 'T', 
        'x1': right_text_x1, 'y1': 107.5, 
        'x2': frame_x2, 'y2': 112.5, 
        'font': 'Arial', 'size': text_size, 'bold': 0, 'italic': 0, 'underline': 0, 
        'foreground': 0, 'background': 0, 
        'align': 'L', 'text': 'O modelo é utilizado como exemplo no contexto de ensino de ML na Educação Básica. Este modelo não foi treinado para ser utilizado em pesquisa na área de botânica', 'priority': 0, 'multiline': True, 
    },
    { 
        'name': 'line_7', 'type': 'L', 
        'x1': frame_x1, 'y1': 125.0, 
        'x2': frame_x2, 'y2': 125.0, 
        'font': 'Arial', 'size': 0, 'bold': 0, 'italic': 0, 'underline': 0, 
        'foreground': 0, 'background': 0, 
        'align': 'I', 'text': None, 'priority': 3, 
    },

    # Público alvo
    { 
        'name': 'text_12', 'type': 'T', 
        'x1': left_text_x1, 'y1': 125.0, 
        'x2': frame_x2, 'y2': 135.0, 
        'font': 'Arial', 'size': text_size, 'bold': 1, 'italic': 0, 'underline': 0, 
        'foreground': 0, 'background': 0, 
        'align': 'L', 'text': 'Público alvo', 'priority': 0, 
    },
    { 
        'name': 'text_13', 'type': 'T', 
        'x1': right_text_x1, 'y1': 127.5, 
        'x2': frame_x2, 'y2': 132.5, 
        'font': 'Arial', 'size': text_size, 'bold': 0, 'italic': 0, 'underline': 0, 
        'foreground': 0, 'background': 0, 
        'align': 'L', 'text': 'Cidadãos (8+ anos)\nFoco em alunos do Ensino Médio', 'priority': 0, 'multiline': True, 
    },
    { 
        'name': 'line_8', 'type': 'L', 
        'x1': frame_x1, 'y1': 140.0, 
        'x2': frame_x2, 'y2': 140.0, 
        'font': 'Arial', 'size': 0, 'bold': 0, 'italic': 0, 'underline': 0, 
        'foreground': 0, 'background': 0, 
        'align': 'I', 'text': None, 'priority': 3, 
    },

    # Riscos
    { 
        'name': 'text_14', 'type': 'T', 
        'x1': left_text_x1, 'y1': 140.0, 
        'x2': frame_x2, 'y2': 150.0, 
        'font': 'Arial', 'size': text_size, 'bold': 1, 'italic': 0, 'underline': 0, 
        'foreground': 0, 'background': 0, 
        'align': 'L', 'text': 'Riscos', 'priority': 0, 
    },
    { 
        'name': 'text_15', 'type': 'T', 
        'x1': right_text_x1, 'y1': 142.5, 
        'x2': frame_x2, 'y2': 147.5, 
        'font': 'Arial', 'size': text_size, 'bold': 0, 'italic': 0, 'underline': 0, 
        'foreground': 0, 'background': 0, 
        'align': 'L', 'text': 'Risco de classificar erroneamente as espécies de árvores, porém se refere a classificação de árvores sem riscos à saúde dos usuários', 'priority': 0, 'multiline': True, 
    },
    { 
        'name': 'line_9', 'type': 'L', 
        'x1': frame_x1, 'y1': 160.0, 
        'x2': frame_x2, 'y2': 160.0, 
        'font': 'Arial', 'size': 0, 'bold': 0, 'italic': 0, 'underline': 0, 
        'foreground': 0, 'background': 0, 
        'align': 'I', 'text': None, 'priority': 3, 
    },

    # Tipo da tarefa
    { 
        'name': 'text_15', 'type': 'T', 
        'x1': left_text_x1, 'y1': 160.0, 
        'x2': frame_x2, 'y2': 170.0, 
        'font': 'Arial', 'size': text_size, 'bold': 1, 'italic': 0, 'underline': 0, 
        'foreground': 0, 'background': 0, 
        'align': 'L', 'text': 'Tipo da tarefa', 'priority': 0, 
    },
    { 
        'name': 'text_16', 'type': 'T', 
        'x1': right_text_x1, 'y1': 160.0, 
        'x2': frame_x2, 'y2': 170.0, 
        'font': 'Arial', 'size': text_size, 'bold': 0, 'italic': 0, 'underline': 0, 
        'foreground': 0, 'background': 0, 
        'align': 'L', 'text': 'Single-label classificação de imagens', 'priority': 0, 'multiline': True, 
    },
    { 
        'name': 'line_10', 'type': 'L', 
        'x1': frame_x1, 'y1': 170.0, 
        'x2': frame_x2, 'y2': 170.0, 
        'font': 'Arial', 'size': 0, 'bold': 0, 'italic': 0, 'underline': 0, 
        'foreground': 0, 'background': 0, 
        'align': 'I', 'text': None, 'priority': 3, 
    },  

    # Categorias
    { 
        'name': 'text_17', 'type': 'T', 
        'x1': left_text_x1, 'y1': 170.0, 
        'x2': frame_x2, 'y2': 180.0, 
        'font': 'Arial', 'size': text_size, 'bold': 1, 'italic': 0, 'underline': 0, 
        'foreground': 0, 'background': 0, 
        'align': 'L', 'text': 'Categorias', 'priority': 0, 
    },
    { 
        'name': 'text_18', 'type': 'T', 
        'x1': right_text_x1, 'y1': 172.5, 
        'x2': frame_x2, 'y2': 177.5, 
        'font': 'Arial', 'size': text_size, 'bold': 0, 'italic': 0, 'underline': 0, 
        'foreground': 0, 'background': 0, 
        'align': 'L', 'text': '10 categorias de espécies de árvores nativas/endêmicas de SC/Brasil: aroeira-vermelha, jerivá, ipê-amarelo, ipê-roxo, mulungu, capororoca, embaúba, olandi, pitangueira e tanheiro', 'priority': 0, 'multiline': True, 
    },
    { 
        'name': 'line_11', 'type': 'L', 
        'x1': frame_x1, 'y1': 190.0, 
        'x2': frame_x2, 'y2': 190.0, 
        'font': 'Arial', 'size': 0, 'bold': 0, 'italic': 0, 'underline': 0, 
        'foreground': 0, 'background': 0, 
        'align': 'I', 'text': None, 'priority': 3, 
    },  

    # Conjunto de dados
    { 
        'name': 'text_19', 'type': 'T', 
        'x1': left_text_x1, 'y1': 190.0, 
        'x2': frame_x2, 'y2': 200.0, 
        'font': 'Arial', 'size': text_size, 'bold': 1, 'italic': 0, 'underline': 0, 
        'foreground': highlight_color, 'background': 0, 
        'align': 'L', 'text': 'Conjunto de dados', 'priority': 0, 
    },
    { 
        'name': 'line_12', 'type': 'L', 
        'x1': frame_x1, 'y1': 200.0, 
        'x2': frame_x2, 'y2': 200.0, 
        'font': 'Arial', 'size': 0, 'bold': 0, 'italic': 0, 'underline': 0, 
        'foreground': 0, 'background': 0, 
        'align': 'I', 'text': None, 'priority': 3, 
    },
    { 
        'name': 'vertical_divider_3', 'type': 'L', 
        'x1': vertical_divider_x, 'y1': 200.0, 
        'x2': vertical_divider_x, 'y2': 282.0, 
        'font': 'Arial', 'size': 0, 'bold': 0, 'italic': 0, 'underline': 0, 
        'foreground': 0, 'background': 0, 
        'align': 'I', 'text': None, 'priority': 3, 
    },

    # Descrição dos dados
    { 
        'name': 'text_20', 'type': 'T', 
        'x1': left_text_x1, 'y1': 200.0, 
        'x2': frame_x2, 'y2': 210.0, 
        'font': 'Arial', 'size': text_size, 'bold': 1, 'italic': 0, 'underline': 0, 
        'foreground': 0, 'background': 0, 
        'align': 'L', 'text': 'Descrição dos dados', 'priority': 0, 
    },
    { 
        'name': 'text_21', 'type': 'T', 
        'x1': right_text_x1, 'y1': 202.5, 
        'x2': frame_x2, 'y2': 207.5, 
        'font': 'Arial', 'size': text_size, 'bold': 0, 'italic': 0, 'underline': 0, 
        'foreground': 0, 'background': 0, 
        'align': 'L', 'text': 'Conjunto de imagens de árvores (tipicamente a vista da árvore toda ou partes dentro do habitat natural (rua, praça, parque, etc.) capturada por um aplicativo Android', 'priority': 0, 'multiline': True, 
    },
    { 
        'name': 'line_13', 'type': 'L', 
        'x1': frame_x1, 'y1': 220.0, 
        'x2': frame_x2, 'y2': 220.0, 
        'font': 'Arial', 'size': 0, 'bold': 0, 'italic': 0, 'underline': 0, 
        'foreground': 0, 'background': 0, 
        'align': 'I', 'text': None, 'priority': 3, 
    },  

    # Origem dos dados
    { 
        'name': 'text_22', 'type': 'T', 
        'x1': left_text_x1, 'y1': 220.0, 
        'x2': frame_x2, 'y2': 230.0, 
        'font': 'Arial', 'size': text_size, 'bold': 1, 'italic': 0, 'underline': 0, 
        'foreground': 0, 'background': 0, 
        'align': 'L', 'text': 'Origem dos dados', 'priority': 0, 
    },
    { 
        'name': 'text_23', 'type': 'T', 
        'x1': right_text_x1, 'y1': 220.0, 
        'x2': frame_x2, 'y2': 230.0, 
        'font': 'Arial', 'size': text_size, 'bold': 0, 'italic': 0, 'underline': 0, 
        'foreground': 0, 'background': 0, 
        'align': 'L', 'text': 'Coleta própria via app \"Coleta de imagens CnE\"', 'priority': 0,
    },
    { 
        'name': 'line_14', 'type': 'L', 
        'x1': frame_x1, 'y1': 230.0, 
        'x2': frame_x2, 'y2': 230.0, 
        'font': 'Arial', 'size': 0, 'bold': 0, 'italic': 0, 'underline': 0, 
        'foreground': 0, 'background': 0, 
        'align': 'I', 'text': None, 'priority': 3, 
    },  

    # Quantidade de dados
    { 
        'name': 'text_24', 'type': 'T', 
        'x1': left_text_x1, 'y1': 230.0, 
        'x2': frame_x2, 'y2': 240.0, 
        'font': 'Arial', 'size': text_size, 'bold': 1, 'italic': 0, 'underline': 0, 
        'foreground': 0, 'background': 0, 
        'align': 'L', 'text': 'Quantidade de dados', 'priority': 0, 
    },
    { 
        'name': 'dataset_total_images', 'type': 'T', 
        'x1': right_text_x1, 'y1': 230.0, 
        'x2': frame_x2, 'y2': 240.0, 
        'font': 'Arial', 'size': text_size, 'bold': 0, 'italic': 0, 'underline': 0, 
        'foreground': 0, 'background': 0, 
        'align': 'L', 'text': '', 'priority': 0, 'multiline': False,
    },
    { 
        'name': 'line_15', 'type': 'L', 
        'x1': frame_x1, 'y1': 240.0, 
        'x2': frame_x2, 'y2': 240.0, 
        'font': 'Arial', 'size': 0, 'bold': 0, 'italic': 0, 'underline': 0, 
        'foreground': 0, 'background': 0, 
        'align': 'I', 'text': None, 'priority': 3, 
    },  

    # Tipos de aumento de dados aplicados
    { 
        'name': 'text_26', 'type': 'T', 
        'x1': left_text_x1, 'y1': 242.5, 
        'x2': right_text_x1, 'y2': 247.5, 
        'font': 'Arial', 'size': text_size, 'bold': 1, 'italic': 0, 'underline': 0, 
        'foreground': 0, 'background': 0, 
        'align': 'L', 'text': 'Tipos de aumento de dados aplicados', 'priority': 0, 'multiline': True,
    },
    { 
        'name': 'dataset_augmentation_type', 'type': 'T', 
        'x1': right_text_x1, 'y1': 240.0, 
        'x2': frame_x2, 'y2': 250.0, 
        'font': 'Arial', 'size': text_size, 'bold': 0, 'italic': 0, 'underline': 0, 
        'foreground': 0, 'background': 0, 
        'align': 'L', 'text': '', 'priority': 0, 'multiline': False,
    },
    { 
        'name': 'line_16', 'type': 'L', 
        'x1': frame_x1, 'y1': 255.0, 
        'x2': frame_x2, 'y2': 255.0, 
        'font': 'Arial', 'size': 0, 'bold': 0, 'italic': 0, 'underline': 0, 
        'foreground': 0, 'background': 0, 
        'align': 'I', 'text': None, 'priority': 3, 
    },  

    # Tamanho do batch
    { 
        'name': 'text_28', 'type': 'T', 
        'x1': left_text_x1, 'y1': 255.0, 
        'x2': frame_x2, 'y2': 265.0, 
        'font': 'Arial', 'size': text_size, 'bold': 1, 'italic': 0, 'underline': 0, 
        'foreground': 0, 'background': 0, 
        'align': 'L', 'text': 'Tamanho do batch', 'priority': 0, 
    },
    { 
        'name': 'dataset_batch_size', 'type': 'T', 
        'x1': right_text_x1, 'y1': 255.0, 
        'x2': frame_x2, 'y2': 265.0, 
        'font': 'Arial', 'size': text_size, 'bold': 0, 'italic': 0, 'underline': 0, 
        'foreground': 0, 'background': 0, 
        'align': 'L', 'text': '', 'priority': 0, 'multiline': False,
    },
    { 
        'name': 'line_16', 'type': 'L', 
        'x1': frame_x1, 'y1': 265.0, 
        'x2': frame_x2, 'y2': 265.0, 
        'font': 'Arial', 'size': 0, 'bold': 0, 'italic': 0, 'underline': 0, 
        'foreground': 0, 'background': 0, 
        'align': 'I', 'text': None, 'priority': 3, 
    },  
    
    # Divisão do conjunto de dados
    { 
        'name': 'text_30', 'type': 'T', 
        'x1': left_text_x1, 'y1': 267.5, 
        'x2': right_text_x1, 'y2': 272.5, 
        'font': 'Arial', 'size': text_size, 'bold': 1, 'italic': 0, 'underline': 0, 
        'foreground': 0, 'background': 0, 
        'align': 'L', 'text': 'Divisão do conjunto de dados', 'priority': 0, 'multiline': True,
    },
    { 
        'name': 'dataset_validation_percentage', 'type': 'T', 
        'x1': right_text_x1, 'y1': 267.5, 
        'x2': frame_x2, 'y2': 272.5, 
        'font': 'Arial', 'size': text_size, 'bold': 0, 'italic': 0, 'underline': 0, 
        'foreground': 0, 'background': 0, 
        'align': 'L', 'text': '', 'priority': 0, 'multiline': True,
    },
]