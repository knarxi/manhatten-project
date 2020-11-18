"""Recognize table"""
import cv2
from PIL import Image

from screen_operations import take_screenshot, crop_screenshot_with_topleft_corner, \
    is_template_in_search_area, binary_pil_to_cv2, ocr

CARD_VALUES = "23456789TJQKA"
CARD_SUITES = "CDHS"

class TableScraper:
    def __init__(self, table_dict):
        self.table_dict = table_dict
        self.screenshot = None
        self.total_players = 3
        self.my_cards = None
        self.table_cards = None
        self.current_round_pot = None
        self.total_pot = None
        self.dealer_position = None
        self.players_in_game = None
        self.player_funds = None
        self.player_pots = None
        self.call_value = None
        self.raise_value = None
        self.call_button = None
        self.raise_button = None
        self.players_names = None
        self.game_number = None

    def take_screenshot2(self):
        """Take a screenshot"""
        self.screenshot = take_screenshot()

    def crop_from_top_left_corner(self):
        """Crop top left corner based on the current selected table dict and replace self.screnshot with it"""
        self.screenshot = crop_screenshot_with_topleft_corner(self.screenshot,
                                                                        self.table_dict['topleft_corner'])

        return self.screenshot

    def get_my_cards2(self):
        """Get my cards"""
        my_cards = []
        for value in CARD_VALUES:
            for suit in CARD_SUITES:
                if is_template_in_search_area(self.table_dict, self.screenshot,
                                              value.upper() + suit.upper(), 'mycards'):
                    my_cards.append(value + suit)
        if len(self.my_cards) != 2:
            print("My cards not recognized")
        return True

    def get_table_cards2(self):
        """Get the cards on the table"""
        table_cards = []
        for value in CARD_VALUES:
            for suit in CARD_SUITES:
                if is_template_in_search_area(self.table_dict, self.screenshot,
                                              value.upper() + suit.upper(), 'boardcards'):
                    table_cards.append(value + suit)

        assert len(self.table_cards) != 1, "Table cards can never be 1"
        assert len(self.table_cards) != 2, "Table cards can never be 2"
        return True

    def get_game_number_on_screen2(self):
        """Game number"""
        self.game_number = ocr(self.screenshot, 'game_number', self.table_dict)


    def get_dealer_position2(self):
        """Determines position of dealer, where 0=myself, continous counter clockwise"""
        for i in range(1,self.total_players):
            if is_template_in_search_area(self.table_dict,self.screenshot,'button', 'button'+str(i)):

                self.dealer_position = i
                return True

    def get_pots(self):
        """Get current and total pot"""
        self.current_round_pot = float(ocr(self.screenshot, 'current_round_pot', self.table_dict))
        self.total_pot = float(ocr(self.screenshot, 'total_pot_area', self.table_dict))

    def get_players_in_game(self):
        """
        Get players in the game by checking for covered cards.
        Return: list of ints
        """
        self.players_in_game = [0]  # assume myself in game
        for i in range(1, self.total_players):
            if is_template_in_search_area(self.table_dict, self.screenshot,
                                          'covered_card', 'covered_card_area'+str(i)):
                self.players_in_game.append(i)
        return True

    def other_players_names(self):
        self.players_names = []
        for i in range(1, self.total_players-1):
            ocr(self.screenshot, 'player'+str(i), self.table_dict, player=True)


    def get_raise_value(self):
        """Read the value of the raise button"""
        self.raise_value = ocr(self.screenshot, 'raise_value', self.table_dict)
        return self.raise_value


    def get_call_value(self):
        """Read the call value from the call button"""
        self.call_value = ocr(self.screenshot, 'call_value', self.table_dict)
        return self.call_value


    def get_my_funds2(self):
        self.get_players_funds(my_funds_only=True)


    def get_players_funds(self, my_funds_only=False ):
        """
        Get funds of players
        Returns: list of floats
        """
        if my_funds_only:
            counter = 1
        else:
            counter = self.total_players
            print(counter)
        self.player_funds = []
        for i in range(1,counter):
            funds = ocr(self.screenshot, 'player_funds'+str(i), self.table_dict)
            self.player_funds.append(funds)

        return True



if __name__ == "__main__":
    from templates import table_dict

    filename = 'savedImage.jpg'
    s2 = Image.open("spin pp2.png")
    a= TableScraper(table_dict)

    a.screenshot=Image.open("spin pp2.png")
    a.get_pots()
    print(type(a.total_pot))




