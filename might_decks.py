import random

global_status = ""
global_status_counter = 0
global_current_draw = 0
global_miss_counter = 0
global_crit_count = 0
global_num_cards_drawn = 0

class Deck():
   def __init__(self, colour, type, card_definitions):
      self.current_cards = []
      self.current_discards = []
      self.stored_discards = []
      
      self.colour = colour
      self.type = type
      self.cards = []
      self.card_definitions = card_definitions
      self.name = f"{colour} - {type}"
      self.current_cards = []
      self.cards_drew = 0
      self.crits = 0
      self.build_deck(self.card_definitions)      
      self.status_update(f"Init {self.colour} - {self.type}!")
      self.shuffle()

   def build_deck(self, card_definitions):
      for card_def in card_definitions:
         for i in range(card_def[3]):
            self.cards.append([card_def[0], card_def[1], card_def[2], card_def[3], card_def[4], card_def[5]])

   def end_draw(self):
      global global_current_draw
      global global_miss_counter
      global global_crit_count
      global global_num_cards_drawn
      global_miss_counter = 0
      global_current_draw = 0
      global_crit_count = 0
      global_num_cards_drawn = 0
      self.crits = 0
      self.cards_drew = 0

      for card in self.current_discards:
         self.stored_discards.append(card)
      self.current_discards.clear()

   def remaining_cards(self):
      values = set(map(lambda x:x[4], self.current_cards))
      grouped_cards = [[y[1] for y in self.current_cards if y[4]==x] for x in values]
      remaining_cards = ""
      for i in range(len(grouped_cards)):
         percent = round((len(grouped_cards[i]) / len(self.current_cards)) * 100)       
         remaining_cards += f"{grouped_cards[i][0]}: {str(len(grouped_cards[i]))} - {percent}%\n"
      if len(self.current_cards) == 0:
         remaining_cards = "Deck empty!\nDeck will shuffle\nautomatically."
      return remaining_cards
    
   def status_update(self, status):
      global global_status
      global_status = f"{status}\n" + global_status      

   def decks_status(draw):
      global global_status
      if draw:
         pass
      else:
         global_status = f"\n-------------------\n\n" + global_status
      return global_status

   def shuffle(self):      
      self.current_cards.clear()
      self.current_cards = list(self.cards)
      for card in self.current_discards:
         self.current_cards.remove(card)
      self.stored_discards.clear()
      random.shuffle(self.current_cards)
      self.status_update(f"Shuffling {self.colour}...")

   def draw(self, count, crit=False):
      try:
         global global_miss_counter
         global global_current_draw
         global global_crit_count
         global global_num_cards_drawn

         self.count = count   
         for i in range(self.count):
            if len(self.current_cards) == 0:
               self.shuffle()
            if crit == True:
               self.crits -= 1
            random_card = random.choice(self.current_cards)
            self.current_cards.remove(random_card)
            global_current_draw += random_card[2]
            if random_card[0] == 'miss' and crit == False:
               global_miss_counter += 1
            if random_card[0] == 'crit':
               global_crit_count += 1
               self.crits += 1
            self.current_discards.append(random_card)
            global_num_cards_drawn += 1
            random.shuffle(self.current_cards)
            self.status_update(f"Drew {self.colour} - {random_card[1].strip()}!")
         return 0
      except IndexError:
         self.status_update(f"{self.colour} deck is empty!")
         return 1

   def cards_left(self):
      return(len(self.current_cards))
   
   def reset_cards_drawn(self):
      self.cards_drew = 0

   def set_cards_drawn(self, count):
      self.cards_drew += count
   
   def cards_drawn(self):
      return self.cards_drew

   def misses():
      return global_miss_counter
   
   def hits():
      return global_current_draw
   
   def crits():
      return global_crit_count
   
   def deck_crits(self):
      return self.crits
   
   def get_num_cards():
      return global_num_cards_drawn
   
   def get_name(self):
      return self.name

# setup decks - provide colour, type (enemy or oathsworn), 
# and card details ("type", "friendly name", hit value, # of cards and sort order)
# white_deck_o = Deck("white", "oathsworn", (("miss", "Miss   ", 0, 6, 0), 
#                                            ("hit", "Hit(1) ", 1, 6, 1), 
#                                            ("hit", "Hit(2) ", 2, 3, 2), 
#                                            ("crit", "Crit(2)", 2, 3, 3)))
# yellow_deck_o = Deck("yellow", "oathsworn", (("miss", "Miss   ", 0, 6, 0), 
#                                              ("hit", "Hit(1) ", 1, 3, 1), 
#                                              ("hit", "Hit(2) ", 2, 3, 2), 
#                                              ("hit", "Hit(3) ", 3, 3, 3), 
#                                              ("crit", "Crit(3)", 3, 3, 4)))
# red_deck_o = Deck("red", "oathsworn", (("miss", "Miss   ", 0, 6, 0), 
#                                        ("hit", "Hit(2) ", 2, 3, 1), 
#                                        ("hit", "Hit(3) ", 3, 6, 2), 
#                                        ("crit", "Crit(4)", 4, 3, 3)))
# black_deck_o = Deck("black", "oathsworn", (("miss", "Miss   ", 0, 6, 0), 
#                                        ("hit", "Hit(3) ", 3, 6, 1), 
#                                        ("hit", "Hit(4) ", 4, 3, 2), 
#                                        ("crit", "Crit(5)", 5, 3, 3)))
white_deck_e = Deck("white", "enemy", (("miss", "Miss   ", 0, 6, 0, "0"), 
                                           ("hit", "Hit(1) ", 1, 6, 1, "1"), 
                                           ("hit", "Hit(2) ", 2, 3, 2, "2"), 
                                           ("crit", "Crit(2)", 2, 3, 3, "{ 2 }")))
yellow_deck_e = Deck("yellow", "enemy", (("miss", "Miss   ", 0, 6, 0, "0"), 
                                             ("hit", "Hit(1) ", 1, 3, 1, "1"), 
                                             ("hit", "Hit(2) ", 2, 3, 2, "2"), 
                                             ("hit", "Hit(3) ", 3, 3, 3, "3"), 
                                             ("crit", "Crit(3)", 3, 3, 4, "{ 3 }")))
red_deck_e = Deck("red", "enemy", (("miss", "Miss   ", 0, 6, 0, "0"), 
                                       ("hit", "Hit(2) ", 2, 3, 1, "2"), 
                                       ("hit", "Hit(3) ", 3, 6, 2, "3"), 
                                       ("crit", "Crit(4)", 4, 3, 3, "{ 4 }")))
black_deck_e = Deck("black", "enemy", (("miss", "Miss   ", 0, 6, 0, "0"), 
                                       ("hit", "Hit(3) ", 3, 6, 1, "3"), 
                                       ("hit", "Hit(4) ", 4, 3, 2, "4"), 
                                       ("crit", "Crit(5)", 5, 3, 3, "{ 5 }")))
