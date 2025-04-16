
import random

WOODCUTTER_COST = 3
EXCHANGE_VALUE = 1

class Player:
    def __init__(self):
        self.woodcutters = 1
        self.victory_points = 0
        self.harvested_trees = 0
        self.replanted = 0
        self.exchanges_this_round = 0
        self.has_harvested = False
        self.total_vp_gained = 0

    def to_dict(self):
        return {
            "woodcutters": self.woodcutters,
            "victory_points": self.victory_points,
            "harvested_trees": self.harvested_trees,
            "replanted": self.replanted,
            "exchanges_this_round": self.exchanges_this_round,
            "has_harvested": self.has_harvested,
            "total_vp_gained": self.total_vp_gained
        }

class GameModel:
    def __init__(self, variant=1):
        self.players = [Player(), Player()]
        self.forest = 100
        self.current_round = 0
        self.variant = variant
        self.current_player = 0
        self.game_over = False
        self.replant_buffer = 0

    def get_state(self):
        return {
            "forest": self.forest,
            "current_round": self.current_round,
            "current_player": self.current_player,
            "players": [p.to_dict() for p in self.players],
            "game_over": self.game_over
        }

    def harvest(self):
        player = self.players[self.current_player]
        harvest = sum(2 if roll >= 5 else 1 if roll >= 2 else 0 
                      for roll in [random.randint(1,6) for _ in range(player.woodcutters)])
        actual_harvest = min(harvest, self.forest)
        self.forest -= actual_harvest
        player.harvested_trees += actual_harvest
        player.has_harvested = True
        return actual_harvest

    def end_turn(self):
        self.players[self.current_player].has_harvested = False
        self.current_player = 1 - self.current_player
        if self.current_player == 0:
            self.current_round += 1
            self.end_round()
        if self.forest <= 0 or self.current_round >= 20:
            self.game_over = True

    def end_round(self):
        self.forest = min(self.forest + self.replant_buffer, 100)
        self.replant_buffer = 0
        for p in self.players:
            p.replanted = 0
            p.exchanges_this_round = 0
        if self.variant == 3 and self.current_round % 5 == 0:
            bonus = self.forest // 10
            for p in self.players:
                p.victory_points += bonus
                p.total_vp_gained += bonus

    def replant(self, amount):
        p = self.players[self.current_player]
        if amount <= p.harvested_trees:
            p.harvested_trees -= amount
            p.replanted += amount
            self.replant_buffer += amount * 3
            return True
        return False

    def buy_vp(self, amount):
        p = self.players[self.current_player]
        if amount * 2 <= p.harvested_trees:
            p.harvested_trees -= amount * 2
            p.victory_points += amount
            p.total_vp_gained += amount
            return True
        return False

    def buy_wc(self, amount):
        p = self.players[self.current_player]
        if amount * WOODCUTTER_COST <= p.harvested_trees:
            p.harvested_trees -= amount * WOODCUTTER_COST
            p.woodcutters += amount
            return True
        return False

    def exchange_wc(self):
        p = self.players[self.current_player]
        if p.woodcutters > 1 and p.exchanges_this_round < 2:
            p.woodcutters -= 1
            p.victory_points += EXCHANGE_VALUE
            p.total_vp_gained += EXCHANGE_VALUE
            p.exchanges_this_round += 1
            return True
        return False
