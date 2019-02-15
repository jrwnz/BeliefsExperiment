import random
import math
import json
import numpy as np

## Seed is 1234 + session number
session = 1234 + 1 
random.seed(session)

## Sets payoff info
payoff_info = {
    'a': {'action': {'number': 1, 'amount': 10}},
    'b': {'action': {'number': 2, 'amount': 10},
          'belief': {'number': 2, 'amount': 5}},
}
with open('payoff_info.json','w') as f:
    json.dump(payoff_info,f)


## Define sections
section_names = ['actions','beliefs','matrix_training','actions_practice','beliefs_practice']

## Define games
base_games = [
    {
    'Type': 'Base_x',
    'Index': str(x),
    'Payoffs': {
        "U": {"L": [x, 0], "R": [0, 20]},
        "D": {"L": [0, 20], "R": [20, 0]}
        }
    } for x in [1,2,5,10,40,80]
] + [
    {
    'Type': 'Base_y',
    'Index': str(y),
    'Payoffs': {
        "U": {"L": [y, 0], "R": [0, 2]},
        "D": {"L": [0, 2], "R": [2, 0]}
        }
    } for y in [8]
]

target_games = [
    {
    'Type': 'Target',
    'Index': str(1),
    'Payoffs': {
        "U": {"L": [6, 0], "R": [0, 20]},
        "D": {"L": [0, 10], "R": [20, 0]}
        }
    },
    {
    'Type': 'Target',
    'Index': str(2),
    'Payoffs': {
         "U": {"L": [6, 0], "R": [0, 20]},
        "D": {"L": [0, 40], "R": [20, 0]}
        }
    }
]
    
dominance_games = [
    {
    'Type': 'Dominance',
    'Index': 'blue',
    'Payoffs': {
        "U": {"L": [6, 0], "R": [0, 20]},
        "D": {"L": [8, 20], "R": [20, 4]}
        }
    },
    {
    'Type': 'Dominance',
    'Index': 'red',
    'Payoffs': {
        "U": {"L": [20, 0], "R": [4, 20]},
        "D": {"L": [0, 6], "R": [20, 8]}
        }
    },
    {
    'Type': 'Dominance',
    'Index': 'both',
    'Payoffs': {
        "U": {"L": [2, 0], "R": [20, 4]},
        "D": {"L": [0, 8], "R": [8, 20]}
        }
    }
]


matrix_training_games = [
    {
    'Payoffs': {
                "U": {"L": [39, 5], "R": [22, 11]},
                "D": {"L": [16, 27], "R": [50, 6]}
                },
    'Type': 'Matrix_Training',
    'Index': str(1),
    'Question_Actions': 'U,R',
    'Question_Player': 'red'
    },
        {
    'Payoffs': {
                "U": {"L": [40, 6], "R": [23, 12]},
                "D": {"L": [17, 28], "R": [51, 7]}
                },
    'Type': 'Matrix_Training',
    'Index': str(2),
    'Question_Actions': 'U,L',
    'Question_Player': 'blue'
    },
        {
    'Payoffs': {
                "U": {"L": [41, 7], "R": [24, 13]},
                "D": {"L": [18, 29], "R": [52, 8]}
                },
    'Type': 'Matrix_Training',
    'Index': str(3),
    'Question_Actions': 'D,R',
    'Question_Player': 'red'
    },
        {
    'Payoffs': {
                "U": {"L": [42, 8], "R": [25, 14]},
                "D": {"L": [19, 30], "R": [53, 9]}
                },
    'Type': 'Matrix_Training',
    'Index': str(4),
    'Question_Actions': 'D,L',
    'Question_Player': 'blue'
    },
]

practice_games = [
    {
    'Type': 'Practice',
    'Index': str(1),
    'Payoffs': {
        "U": {"L": [30, 0], "R": [0, 30]},
        "D": {"L": [0, 30], "R": [30, 0]}
        }
    },
    {
    'Type': 'Practice',
    'Index': str(2),
    'Payoffs': {
        "U": {"L": [20, 0], "R": [0, 30]},
        "D": {"L": [0, 30], "R": [30, 0]}
        }
    },     
    {
    'Type': 'Practice',
    'Index': str(3),
    'Payoffs': {
        "U": {"L": [45, 0], "R": [0, 30]},
        "D": {"L": [0, 30], "R": [30, 0]}
        }
    },     
    {
    'Type': 'Practice',
    'Index': str(4),
    'Payoffs': {
        "U": {"L": [75, 0], "R": [0, 30]},
        "D": {"L": [0, 30], "R": [30, 0]}
        }
    }, 
]

for games in [base_games,dominance_games,target_games]:
    for game in games:
        game['Code'] = '{}_{}'.format(game['Type'],game['Index'])
        game['Section_Rounds'] = {section: {} for section in section_names}
                                     
for games in [matrix_training_games,practice_games]:
    for game in games:
        game['Code'] = '{}_{}'.format(game['Type'],game['Index'])
        game['Section_Rounds'] = {section: {} for section in section_names}
            
games = {
         game['Code']: game for game in 
         base_games 
         + dominance_games
         + target_games
         + practice_games
         + matrix_training_games
        }

all_game_codes = {
    'base': [code for code in games if code.startswith('Base')],
    'dominance': [code for code in games if code.startswith('Dominance')],
    'target': [code for code in games if code.startswith('Target')],
    'matrix_training': [code for code in games if code.startswith('Matrix_Training')],
    'actions_practice': [code for code in games if code.startswith('Practice')],
    'beliefs_practice': [code for code in games if code.startswith('Practice')][:3],
}


## Define game orders
orders = {}
for section in section_names:
    orders[section] = []

def get_buffered_sample(codes,buffer_codes):
    buffer_length = len(buffer_codes)
    non_buffer_codes = [code for code in codes if code not in buffer_codes]
    new_sample = random.sample(non_buffer_codes,buffer_length)
    reamaining_codes = [code for code in codes if code not in new_sample]
    new_sample += random.sample(reamaining_codes,len(reamaining_codes))
    return new_sample

def add_section_info(order_codes,section):
    for (index, round_codes) in enumerate(order_codes):
        blue_code = round_codes['blue']
        red_code = round_codes['red']
        blue_rounds = [i+1 for i, x in enumerate(order_codes) if x['blue'] == blue_code]
        red_rounds = [i+1 for i, x in enumerate(order_codes) if x['red'] == red_code]
        orders[section].append({
            'blue': {
                'Code': blue_code,
                'Rounds': blue_rounds,
                'Iteration': blue_rounds.index(index+1)+1,
                'Type': games[blue_code]['Type'],
                'Index': games[blue_code]['Index'],
            },
            'red': {
                'Code': red_code,
                'Rounds': red_rounds,
                'Iteration': red_rounds.index(index+1)+1,
                'Type': games[red_code]['Type'],
                'Index': games[red_code]['Index'],
            },                    
        })
        rounds_name = (
            'Belief_Rounds' if section == 'beliefs' else
            'Action_Rounds' if section == 'actions' else
            'Rounds'
        )
        games[blue_code]['Section_Rounds'][section]['blue'] = blue_rounds
        games[red_code]['Section_Rounds'][section]['red'] = red_rounds 

## Action orders
buffer_length = 2
num_blocks = 2
block_codes = all_game_codes['base'] + all_game_codes['target']
block_length = len(block_codes)

order_codes = random.sample(block_codes,block_length)
for block in range(num_blocks-1):
    order_codes += get_buffered_sample(block_codes,order_codes[-buffer_length:])

if random.random() < 0.5:
    insert_codes = ['Dominance_red','Dominance_blue']
else:
    insert_codes = ['Dominance_blue','Dominance_red']
for index, code in enumerate(insert_codes):
    order_codes.insert(round((index+1)*len(order_codes+insert_codes)/(len(insert_codes)+1)),code)
    
order_codes = [
    {'red':code,'blue':code}
    for code in order_codes
]

add_section_info(order_codes,'actions') 


## Belief orders
buffer_length = 2
num_blocks = 5
block_codes = all_game_codes['base']
block_length = len(block_codes)

order_codes = random.sample(block_codes,block_length)
for block in range(num_blocks-1):
    order_codes += get_buffered_sample(block_codes,order_codes[-buffer_length:])

insert_codes = ['self','other','self','other','self']
for index, code in enumerate(insert_codes):
    order_codes.insert(round((index+1)*len(order_codes+insert_codes)/(len(insert_codes)+1)),code)

order_codes = [
    {'red':'Dominance_red','blue':'Dominance_blue'} if code == 'self' else
    {'red':'Dominance_blue','blue':'Dominance_red'} if code == 'other' else
    {'red':code,'blue':code}
    for code in order_codes
]

add_section_info(order_codes,'beliefs')  


## Other section orders
for section in ['actions_practice','matrix_training','beliefs_practice',]:
    order_codes = [{'red':code,'blue':code} for code in all_game_codes[section]]
    add_section_info(order_codes,section)


## Save games and orders
with open('games.json','w') as f:
    json.dump(games,f)
with open('orders.json','w') as f:
    json.dump(orders,f)    