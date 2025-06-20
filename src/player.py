import src.deck as deck


class Player:
  def __init__(self, name):
    self.name = name
    self.hand = []
  
  def show_hand(self):
    print("Hand:")
    i = 1
    for card in self.hand:
      print(str(i) + ". ", end = "")
      card.peek()
      i += 1

  def draw_card(self, deck):
    self.hand.append(deck.draw_card())

  def num_cards(self):
    return len(self.hand)
    
  def remove_cards(self, cards):
    for card in cards:
      self.hand.remove(card)

  def low_card(self):
    #output the users lowest card
    #2 of hearts is the highest card in the game
    low_card = deck.Card("Hearts", 2)
    for card in self.hand:
      low_card = deck.compare_cards(low_card, card) 
    return low_card

  def valid_single(self, player_card, card_stack, prev_move):
    #sigle is valid if card stack is empty or if it is higher than the card
    #stack
    if card_stack == []:
      return True
    if prev_move == 1:
      if deck.compare_cards(player_card, card_stack[0]) == card_stack[0]:
        return True
    return False
  
  def play_single(self, card, card_stack, prev_move):
    player_card = self.hand[card]
    if self.valid_single(player_card, card_stack, prev_move):
      self.remove_cards([player_card])
      return [player_card]
    return False

  def valid_multi(self, player_cards, card_stack):
    # Validate a set of cards where all cards share the same value
    # Works for pairs, triples and quads
    card_value_set = {card.value for card in player_cards}
    if len(card_value_set) == 1 and len(player_cards) in [2, 3, 4]:
      if card_stack == []:
        return True
      elif len(player_cards) == len(card_stack):
        player_high_card = deck.high_card(player_cards)
        card_stack_high_card = deck.high_card(card_stack)
        high_card = deck.compare_cards(player_high_card, card_stack_high_card)
        if high_card == card_stack_high_card:
          return True
    return False

  def play_multi(self, cards, card_stack):
    player_cards = [self.hand[card] for card in cards]
    if self.valid_multi(player_cards, card_stack):
      self.remove_cards(player_cards)
      return player_cards
    return False

  def valid_run(self, player_cards, card_stack, prev_move):
    #run is valid if previous move was a run or a pass
    #if previous move was a run, the run played but be higher order
    #get card values
    card_values = [card.value for card in player_cards]
    #must be minimum of 3 cards in run
    if len(card_values) < 3:
      return False
    if 2 in card_values:
      return False
    #check to make sure cards in run are consecutive
    if 1 in card_values:
      one_index = card_values.index(1)
      card_values[one_index] = 14
    if sorted(card_values) == list(range(min(card_values), max(card_values)+1)):
      if card_stack == []:
        return True
      #verify run is higher order than previous run played
      elif prev_move == 4 and len(player_cards) == len(card_stack):
        player_high_card = deck.high_card(player_cards)
        card_stack_high_card = deck.high_card(card_stack)
        low_card = deck.compare_cards(player_high_card, card_stack_high_card)
        if low_card == card_stack_high_card:
          return True
    return False
  
  def play_run(self, cards, card_stack, prev_move):
    player_cards = [self.hand[card] for card in cards]
    if self.valid_run(player_cards, card_stack, prev_move):
      self.remove_cards(player_cards)
      return player_cards
    return False

  def valid_double_run(self, player_cards, card_stack, prev_move):
    # Validate runs made up of consecutive pairs
    if len(player_cards) < 6 or len(player_cards) % 2 != 0:
      return False

    # sort cards by value for easier checking
    values = [card.value for card in player_cards]
    # convert Ace to high value for sequence comparison
    values = [14 if v == 1 else v for v in values]
    pairs = []
    for i in range(0, len(values), 2):
      if values[i] != values[i+1]:
        return False
      pairs.append(values[i])

    if 2 in pairs:
      return False
    if pairs != list(range(min(pairs), max(pairs)+1)):
      return False

    if card_stack == []:
      return True
    elif prev_move == 6 and len(player_cards) == len(card_stack):
      player_high_card = deck.high_card(player_cards)
      card_stack_high_card = deck.high_card(card_stack)
      low_card = deck.compare_cards(player_high_card, card_stack_high_card)
      if low_card == card_stack_high_card:
        return True
    return False

  def play_double_run(self, cards, card_stack, prev_move):
    player_cards = [self.hand[card] for card in cards]
    if self.valid_double_run(player_cards, card_stack, prev_move):
      self.remove_cards(player_cards)
      return player_cards
    return False
      

if __name__ == "__main__":
  d = deck.Deck()
  player = Player("Gajan")
  player.draw_card(d)
  player.show_hand()
  player_low_card = player.low_card()
  player_low_card.peek()
