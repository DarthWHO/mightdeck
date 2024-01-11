from might_decks import Deck
from might_decks import *
import visuals as v
from visuals import DrawCard
from functools import partial

def update_status(draw):
    v.update_status(Deck.decks_status(draw))

def end_draw():
    state_update = True
    if Deck.get_num_cards() != 0:
        for item in data:
            data[item]['deck'].end_draw()
            if len(data[item]['deck'].stored_discards) == 18:
                shuffle(data[item])
                state_update = False
        if state_update:
            v.update_status(Deck.decks_status(False))       
    reset()
        

def shuffle(deck_dict):
     deck_dict["deck"].shuffle()
     deck_dict["deck"].remaining_cards()
     update_status(False)
     v.update_deck_status(deck_dict["play_area"], deck_dict["deck"].remaining_cards())

def draw_all():
    for item in data:            
        if data[item]['play_area'].spin.get() != "":
                if int(data[item]['play_area'].spin.get()) > 0:
                    draw(data[item], int(data[item]['play_area'].spin.get()))
        data[item]['play_area'].spin.set(0)

# def success_chance():
#     for item in data:            
#         if data[item]['play_area'].spin.get() != "":
#                 if int(data[item]['play_area'].spin.get()) > 0:
#                     if int(data[item]['play_area'].spin.get()) > data[item]['deck'].cards_left():
#                         current_deck_size += data[item]['deck'].cards_left()
#                         total_cards_discard += data[item]['deck'].cards_left_stored()
#                         known_misses_current += data[item]['deck'].misses_left()
#                         known_misses_discard += data[item]['deck'].misses_left_stored()
#                         num_draws_current += data[item]['deck'].cards_left()
#                         num_draws_discard += (int(data[item]['play_area'].spin.get()) - data[item]['deck'].cards_left())
#                     else:
#                         current_deck_size += data[item]['deck'].cards_left()
#                         total_cards_discard += data[item]['deck'].cards_left_stored()
#                         num_draws_current += data[item]['deck'].cards_left()

#     probability = simulate_draws(num_draws_current, known_misses_current, current_deck_size, 
#                                  num_draws_discard, known_misses_discard, total_cards_discard, 
#                                  num_simulations)
#     probability = 1 - probability
#     v.result_text.configure(text=f"Success Chance:\n     {format(probability, '.0%')}")

def draw(deck_dict, count=1, crit=False):

    
    if deck_dict["deck"].draw(count, crit) == 0:
        v.update_deck_status(deck_dict["play_area"], deck_dict["deck"].remaining_cards())
        update_status(True)
        v.result_text.configure(text=f"Total:  {Deck.hits()}\nCrits:  {Deck.crits()}\nMisses: {Deck.misses()}")
        draw_cards()
        if v.get_game_state() == "oathsworn":
            if deck_dict["deck"].deck_crits() > 0:
                deck_dict["play_area"].btn_draw.configure(state= 'normal', text=f"Crits ({deck_dict['deck'].deck_crits()})")
            else:
                deck_dict["play_area"].btn_draw.configure(state= 'disabled', text=f"No Crits")
    else:
        update_status(True)

def draw_cards():
    for item in data:            
        for widget in data[item]['play_area'].card_area.winfo_children():
            widget.destroy()
        data[item]['deck'].reset_cards_drawn()

        for i in range(len(data[item]['deck'].current_discards)):
            if data[item]['deck'].cards_drawn() == 9:
                for j in range(len(data[item]['deck'].current_discards) - 9):
                    DrawCard(data[item]['play_area'].card_area, j, 1, data[item]['colour'], data[item]['colour'], text=data[item]['deck'].current_discards[j+i][5])
            else:
                DrawCard(data[item]['play_area'].card_area, i, 0, data[item]['colour'], data[item]['colour'], text=data[item]['deck'].current_discards[i][5])
            data[item]['deck'].set_cards_drawn(1)

        data[item]['play_area'].spin.configure(to=(18-len(data[item]['deck'].current_discards)))

def reset():
    v.result_text.configure(text="")

    for item in data:           
        for widget in data[item]['play_area'].card_area.winfo_children():
            widget.destroy()
        data[item]['play_area'].spin.set(0)
        data[item]['play_area'].spin.configure(to=18)
        action_with_arg = partial(draw, data[item], crit=True)
        data[item]['play_area'].btn_draw.configure(state='disabled', text=f"No Crits", command=action_with_arg)

def switch_state():
    end_draw()
    data.clear()
    v.update_game_state()    

    if v.get_game_state() == "oathsworn":
        white_o = {"deck": white_deck_o, "play_area": v.white_area, "colour": "white"}
        data['white_o'] = white_o
        yellow_o = {"deck": yellow_deck_o, "play_area": v.yellow_area, "colour": "yellow"}
        data['yellow_o'] = yellow_o
        red_o = {"deck": red_deck_o,"play_area": v.red_area, "colour": "red"}
        data['red_o'] = red_o
        black_o = {"deck": black_deck_o,"play_area": v.black_area, "colour": "black"}
        data['black_o'] = black_o

    else:
        white_e = {"deck": white_deck_e, "play_area": v.white_area, "colour": "white"}
        data['white_e'] = white_e
        yellow_e = {"deck": yellow_deck_e, "play_area": v.yellow_area, "colour": "yellow"}
        data['yellow_e'] = yellow_e
        red_e = {"deck": red_deck_e,"play_area": v.red_area, "colour": "red"}
        data['red_e'] = red_e
        black_e = {"deck": black_deck_e,"play_area": v.black_area, "colour": "black"}
        data['black_e'] = black_e
        

    for item in data:
        v.update_deck_status(data[item]['play_area'], data[item]['deck'].remaining_cards())
        action_with_arg = partial(shuffle, data[item])
        data[item]['play_area'].btn_shuffle.configure(command=action_with_arg)
        v.update_deck_status(data[item]["play_area"], data[item]["deck"].remaining_cards())
        data[item]["play_area"].update_styles()
    
    reset()

data = {}
v.btn_draw_all.configure(command=draw_all)
v.btn_end_draw.configure(command=end_draw)
v.btn_switch.configure(command=switch_state)
# v.btn_chance.configure(command=success_chance)
switch_state()
switch_state()
switch_state()
update_status(False)

v.root.mainloop()
