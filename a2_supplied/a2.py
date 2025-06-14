from __future__ import annotations
from collections import UserString
from math import floor
#from tkinter.constants import FALSE, TRUE
from typing import Dict, List, Optional, Tuple
from a2_support import *
import copy


# Replace these <strings> with your name, student number and email address.
__author__ = "Cheng-Yu Wu, s4623099"
__email__ = "s4623099@student.uq.edu.au"

# Before submission, update this tag to reflect the latest version of the
# that you implemented, as per the blackbaord changelog. 
__version__ = 1.0

# Implement your classes here.
class PokemonStats(object):
    """
    #A class modelling the stats of a pokemon. These stats must be non-negative.
    """
    def __init__(self, stats: Tuple[float, int, int, int]) -> None:
        """
        Constructs an instance of PokemonStats.
        The format of the incoming stats are: (hit_chance, health, attack, defense) with the indices given by constants in the support code.
        
        Parameters
        stats: The base list of stats to encapsulate. These values can be assumed to be non-negative
            hit_chance = the chance for the pokemon to hit the enemy's pokemon
            max_health = the max health that the pokemon can get.
            attack     = the value related to damage.
            defense    = the value related to defense.
        """    
        self._hit_chance, self._max_health, self._attack, self._defense = stats
    
    def level_up(self) -> None:
        """
        Grows the PokemonStats instance after the pokemon has levelled up.
        On leveling up, the base hit chance should always be = 1, while the remaining stats grow by 5% and are rounded down.
        """
        self._hit_chance = 1
        self._max_health = int(self._max_health   * LEVEL_UP_STAT_GROWTH)
        self._attack     = int(self._attack       * LEVEL_UP_STAT_GROWTH)
        self._defense    = int(self._defense      * LEVEL_UP_STAT_GROWTH)
    
    def get_hit_chance(self) -> float:
        """Return the pokemon's current chance at making a successful attack."""
        return self._hit_chance

    def get_max_health(self) -> int:
        """Return the pokemon's max health"""
        return self._max_health

    def get_attack(self) -> int:
        """Return the pokemon's attack stat"""
        return self._attack

    def get_defense(self) -> int:
        """Return the pokemon's defense stat"""
        return self._defense

    def apply_modifier(self, modifier: Tuple[float, int, int, int])-> PokemonStats:
        """
        Applies a stat modifier and returns the newly constructed, modified pokemon stats.
        The resulting pokemon stats are the elementwise sum of the current stats and incoming modification and should be bound by 0.
        
        Parameter:
        modifier        : A list of stat modifications to apply, of the same structure as the initial supplied pokemon stats.
        current_stats   : A list of pokemon stats
        modified_stats  : A list of pokemon stats after modifiiers applied on
        """
        current_stats   = [self.get_hit_chance() ,self.get_max_health(),self.get_attack(),self.get_defense()]
        modified_stats  = list()

        """Method : create current_stats"""
        for i,j in enumerate(modifier):
            stat = current_stats[i] + j
            if stat <= 0:
                stat = 0 
            modified_stats.append(stat)

        return PokemonStats(tuple(modified_stats))

    def __str__(self) -> str:
        """Returns the string representation of this class."""
        return str(f'PokemonStats(({self.get_hit_chance()}, {self.get_max_health()}, {self.get_attack()}, {self.get_defense()}))')

    def __repr__(self) -> str:
        """Returns the string representation of this class."""
        return str(self)


class Pokemon(object):
    """
    A class which represents a Pokemon.
    A pokemon's level is determined by its experience points, through the formula: level = floor(experience ^ (1/3)).
    A pokemon can learn a maximum of 4 moves.
    """
    def __init__(self, name: str, stats: PokemonStats, element_type: str, moves: List[ForwardRef('Move')], level: int = 1) -> None:
        """
        Creates a Pokemon instance.

        Parameters
        name            : The name of this pokemon
        stats           : The pokemon's stats
        element_type    : The name of the type of this pokemon.
        moves           : A list of containing the moves that this pokemon will have learned after it is instantiated.
        level           : The pokemon's level.
        _current_health : pokemon's health during battle.
        _move_uses      : A dictionary of uses related to each move.
        _experience     : The experience this pokemon owns. At the begining, it would be level^3
        _modifier       : A list of modifiers working on this pokemon.
        _stats_unmod    : The pokemon's stats not effected by modifiers
        """
        self._name          = name
        self._stats         = copy.deepcopy(stats)
        self._element_type  = element_type
        self._moves         = moves
        self._level         = level

        self._current_health = -1
        self._move_uses      = dict()
        self._experience     = pow(self.get_level(), 3)
        self._modifier       = list()
        self._stats_unmod    = copy.deepcopy(stats)

    def get_name(self) -> str:
        """Get this pokemon's name."""
        return self._name

    def get_health(self) -> int:
        """Get the remaining health of this pokemon."""
        """Method : Health would be the maximum health if it is undefined or greater than the maximum health"""
        if (self._current_health == -1) or (self._current_health > self.get_max_health()):
            self._current_health = self.get_max_health()

        return self._current_health

    def get_max_health(self) -> int:
        """Get the maximum health of this pokemon before stat modifiers are applied."""
        return self._stats.get_max_health()

    def get_element_type(self) -> str:
        """Get the name of the type of this pokemon."""
        return self._element_type

    def get_remaining_move_uses(self, move: Move) -> int:
        """Gets the number of moves left for the supplied move, or 0 if the pokemon doesn't know the move."""
        """Method : Check if move is learnt by this pokemon and if the uses is not record before, make it as max uses of the move."""
        if move in self._move_uses:
            return self._move_uses.get(move)
        elif move in self._moves:
            self._move_uses[move] = move.get_max_uses()
            return  self._move_uses.get(move)
        else:
            return 0

    def get_level(self) -> int:
        """Get the level of this pokemon."""
        return self._level

    def get_experience(self) ->int:
        """Return the current pokemon's experience."""
        return self._experience

    def get_next_level_experience_requirement(self) -> int:
        """Return the total experience required for the pokemon to be one level higher."""
        level_update =  self.get_level() + 1
        experience_need = pow(level_update, 3)
        return experience_need

    def get_move_info(self) -> List[Tuple[Move, int]]: 
        """
        Return a list of the pokemon's known moves and their remaining uses.
        This list should be sorted by the name of the moves.
        """
        moves_info = []
        move_sorted = sorted(self._moves, key =lambda x : x.get_name())
        """Method : Add movs and their uses into the list."""
        for move in move_sorted:
            uses = self.get_remaining_move_uses(move)
            moves_info.append((move, uses))          

        return moves_info

    def has_fainted(self) -> bool:
        """Return true iff the pokemon has fainted."""
        if self.get_health() == 0:
            return True
        else:
            return False
    
    def modify_health(self, change: int) -> None:
        """
        Modify the pokemons health by the supplied amount.
        The resulting health is clamped between 0 and the max health of this pokemon after stat modifiers are applied.

        Parameters
        change : The health change to be applied to the pokemon.
        """
        self._current_health = self.get_health() + change
        """Method : Check resulting health is clamped between 0 and the max health of this pokemon after stat modifiers are applied."""
        if self._current_health > self.get_max_health():
            self._current_health = self.get_max_health()
        elif self._current_health < 0:
            self._current_health = 0

    def gain_experience(self, experience: int) -> None:
        """
        Increase the experience of this pokemon by the supplied amount, and level up if necessary.

        Parameters
        experience : The amount of experience points to increase.
        """
        self._experience = self._experience + experience
        """Method : Level up until the experience is not enough."""
        while self._experience >= self.get_next_level_experience_requirement():
            self.level_up()

    def level_up(self) -> None:
        """
        Increase the level of this pokemon.
        leveling up grows the pokemon's stats, and increase its current health by the amount that the maximum hp increased.
        """
        self._stats = copy.deepcopy(self._stats_unmod)
        health_reduced = self.get_max_health() - self.get_health()
        self._level = self.get_level() + 1
        self._stats.level_up()
        self._stats_unmod = copy.deepcopy(self._stats)
        """Method : Increase its current health by the amount that the maximum hp increased."""
        if self.get_health() != 0:
            self._current_health = self._stats.get_max_health() - health_reduced

    def experience_on_death(self) -> int:
        """
        The experience awarded to the victorious pokemon if this pokemon faints.
        This is calculated through the formula: 200 * level / 7 and rounded down to the nearest integer, where level: the level of the pokemon who fainted.
        """
        return floor(200 * self.get_level() / 7)

    def can_learn_move(self, move: Move) -> bool:
        """
        Returns true iff the pokemon can learn the given move. 
        i.e. they have learned less than the maximum number of moves for a pokemon and they haven't already learned the supplied move.
        """
        """Method : Check that moves learned are less than the maximum number of moves for a pokemon and they haven't already learned the supplied move."""
        if len(self._moves) < MAXIMUM_MOVE_SLOTS:
            for move_learned in self._moves:
                if move_learned == move:
                    return False
        else:
            return False

        return True

    def learn_move(self, move: Move) -> None:
        """
        Learns the given move, assuming the pokemon is able to.
        After learning this move, this Pokemon can use this move for max_uses times. See Move.

        Parameters
        move : move for pokemon to learn"""
        self._moves.append(move)
        self._move_uses[move] = move.get_max_uses()

    def forget_move(self, move: Move) -> None:
        """Forgets the supplied move, if the pokemon knows it."""
        for index, m in enumerate(self._moves):
            if move == m:
                self._moves.pop(index)
                del self._move_uses[move]
    
    def has_moves_left(self) -> bool:
        """Returns true iff the pokemon has any moves they can use"""
        """Method : Check the sum of all uses is zero or not."""
        if sum(self._move_uses.values()) == 0:
            return False
        else:
            return True

    def reduce_move_count(self, move: Move) -> None:
        """Reduce the move count of the move if the pokemon has learnt it."""
        if move in self._moves:
            self.get_remaining_move_uses(move)
            self._move_uses[move] -= 1

    def add_stat_modifier(self, modifier: Tuple[float, int, int, int], rounds: int) -> None:
        """
        Adds a stat modifier for a supplied number of rounds.

        Parameters
        modifier : A stat modifier to be applied to the pokemon.
        rounds   : The number of rounds that the stat modifier will be in effect for.
        """
        self._modifier.append((modifier,rounds))
        self._stats = self.get_stats()
        
    def get_stats(self) -> PokemonStats:
        """Return the pokemon stats after applying all current modifications."""
        self._stats = copy.deepcopy(self._stats_unmod)
        """Method : Apply all current codifications."""
        for mod in self._modifier:
            self._stats = self._stats.apply_modifier(mod[0])

        return self._stats

    def post_round_actions(self) -> None:
        """
        Update the stat modifiers by decrementing the remaining number of rounds they are in effect for.
        Hint: students should make sure that the pokemon's health is updated appropriately after status modifiers are removed, 
              i.e. the pokemon's health should never exceed its max health.
        """
        round_index = 1
        modifier_changed = list()
        
        """Method : Decrement the remaining number of rounds they are in effect for or delete them if rounds are 1."""
        for mod_index in range(len(self._modifier)-1,-1,-1):
            if self._modifier[mod_index][round_index] == 1:
                self._modifier.pop(mod_index)
            else:
                modifier_used, round_decreased = self._modifier[mod_index]
                round_decreased = round_decreased - 1
                modifier_changed.append((modifier_used, round_decreased))

        self._modifier = modifier_changed
        self._stats = self.get_stats()
        self._current_health = self.get_health()

    def rest(self) -> None:
        """Returns this pokemon to max health, removes any remaining status modifiers, and resets all move uses to their maximums."""
        self._current_health = self.get_max_health()
        self._stats          = self._stats_unmod
        self._modifier       = []
        for move in self._moves:
            self._move_uses[move] = move.get_max_uses()
        
    def __str__(self) -> str:
        """Returns a simple representation of this pokemons name and level."""
        return str(f'{self.get_name()} (lv{self.get_level()})')

    def __repr__(self) -> str:
        """Returns a string representation of this pokemon"""
        return str(self)   


class Trainer(object):
    """A class representing a pokemon trainer. A trainer can have 6 Pokemon at maximum."""
    def __init__(self, name: str) -> None:
        """
        Create an instance of the Trainer class.

        Parameters
        name            : The name of the trainer.
        item            : A dictionary of items that this trainer owns.
        pokemon         : A list of pokemons that this trainer owns.
        current_pokemon : The pokemon that facing the battle.
        """
        self._trainer_name = name
        self._item = dict()
        self._pokemon = list()
        self._current_pokemon = Pokemon

    def get_name(self) -> str:
        """Return the trainer's name."""
        return self._trainer_name

    def get_inventory(self) -> Dict[Item, int]:
        """Returns the trainer's inventory as a dictionary mapping items to the count of that item remaining in the dictionary."""
        return self._item

    def get_current_pokemon(self) -> Pokemon:
        """Gets the current pokemon, or raises a NoPokemonException if the trainer doesn't have a single pokemon."""
        if self._pokemon == []:
            raise NoPokemonException()
        else:
            return self._current_pokemon

    def get_all_pokemon(self) -> List[Pokemon]:
        """
        Returns the trainer's pokemon.
        The order of the pokemon in the list should be the order in which they were added to the roster.
        Modifying the list returned by this method should not affect the state of this instance.
        """
        return self._pokemon

    def rest_all_pokemon(self) -> None:
        """Rests all pokemon in the party"""
        for pokemon in self._pokemon:
            pokemon._stats = pokemon._stats_unmod
            pokemon.rest()

    def all_pokemon_fainted(self) -> bool:
        """Return true iff all the trainer's pokemon have fainted."""
        for index in range(len(self._pokemon)):
            if self._pokemon[index].get_health() != 0:
                return False
        
        return True

    def can_add_pokemon(self, pokemon: Pokemon) -> bool:
        """
        Returns true iff the supplied pokemon can be added to this trainer's roster.
        You shouldn't be able to add the same pokemon instance twice or more than the maximum amount of pokemon for a trainer.
        """
        if (len(self._pokemon) < MAXIMUM_POKEMON_ROSTER) and not(pokemon in self._pokemon):
            return True
        else:
            return False

    def add_pokemon(self, pokemon: Pokemon) -> None:
        """
        Adds a new pokemon into the roster, assuming that doing so would be valid.
        If there were no Pokemon in the roster prior to calling this method, set the current pokemon to the one that was added.
        """
        self._pokemon.append(pokemon)
        if self._current_pokemon == Pokemon:
            self._current_pokemon = pokemon

    def can_switch_pokemon(self, index: int) -> bool:
        """
        Determines if the pokemon index would be valid to switch to, and returns true iff the switch would be valid.
        You cannot swap to a pokemon which is currently out on battle, or which has fainted.

        Parameters
        index : The index of the next pokemon in the roster.
        """
        """Method : Check that the index is fit the list."""
        if (index > (len(self._pokemon)-1)):
            return False
        """Method : Check that a pokemon which is currently out on battle, or which has fainted."""
        if (self._pokemon[index] == self._current_pokemon) or (self._pokemon[index].has_fainted()):
            return False
        else:
            return True

    def switch_pokemon(self, index: int) -> None:
        """
        Switches pokemon to the one at the supplied index, assuming that the switch is valid.

        Parameters
        index : The index of the pokemon to switch to.
        """
        self._current_pokemon = self._pokemon[index]

    def add_item(self, item: Item, uses: int) -> None:
        """
        Adds an item to the trainer's inventory and increments its uses by the supplied amount.

        Parameters
        item : The item to add.
        uses : The quantity of the item to be added to the inventory.
        """
        if self._item.get(item) == None:
            self._item[item] = uses
        else:
            self._item[item] += uses

    def has_item(self, item: Item) -> bool:
        """Returns true if the item is in the trainer's inventory and has uses."""
        if self._item.get(item, 0) > 0:
            return True
        else:
            return False

    def use_item(self, item: Item) -> None:
        """If the item is present in the trainer's inventory, decrement its count. Removes the item from the inventory entirely if its count hits 0."""
        item.decrement_item_count(self._trainer_name)

        if self._item.get(self) == 0:
            del self._item[self]

    def __str__(self) -> str:
        """Returns a string representation of a Trainer"""
        return str(f"Trainer('{self.get_name()}')")

    def __repr__(self) -> str:
        """Returns a string representation of a Trainer"""
        return str(self)  


class Battle(object):
    """
    A class which represents a pokemon battle. A battle can be between trainers or between a trainer and a wild pokemon. 
    In this assignment, non-trainer battles are represented by a battle between 2 trainers, namely a regular trainer and a 'dummy' trainer whose only pokemon is the wild pokemon.
    The main state-components of the battle are the action queue, and the turn:
    1.  Pokemon battles aren't strictly turn-based, because the priority of each Action must be evaluated before they are performed. 
        To make this happen, each round, each trainer adds their desired action to an action queue, and then the actions are performed in order of priority. 
        In our implementation, the trainers cannot add an action to the queue unless it is valid for them to do so, based on the turn, and if the action would be valid.
    2.  The turn is the battle's way of determining who should be allowed to add actions to the action queue. Each round, the turn starts as None. 
        The first time an action is performed by a trainer that round, the turn is set to the opposite trainer, becoming a boolean value which is True if the opposite trainer is the player, and False if they are the enemy. 
        When the turn is a boolean, it means that only the trainer who it points to can add actions to the queue/enact them. When both trainers have enacted a valid action, the round is considered over, and the turn should be set to None.
    """
    def __init__(self, player: Trainer, enemy: Trainer, is_trainer_battle: bool) -> None:
        """
        Creates an instance of a trainer battle.

        Parameters
        player            : The trainer corresponding to the player character.
        enemy             : The enemy trainer.
        is_trainer_battle : True iff the battle takes place between trainers.
        trainer_action    : The action of the player.
        enemy_action      : The action of the enemy.
        end_early         : The bool value represents that if the battle ends early.
        performed         : The action situation -> 0: Sction queue is empty 1: Action of player is performed.  2: Action of enemy is performed. 
        """
        self._no_action         = Attack('None', 'None', 0, 0, 0, 0)
        self._player            = player
        self._enemy             = enemy
        self._is_trainer_battle = is_trainer_battle
        self._trainer_action    = self._no_action
        self._enemy_action      = self._no_action
        self._end_early         = False
        self._performed         = 0 

    def get_turn(self) -> Optional[bool]:
        """Get whose turn it currently is"""
        if self.is_over() or self.is_action_queue_empty() or not(self.is_ready()):
            return None

        if self.is_action_queue_full():
            if (self._trainer_action.get_priority() <= self._enemy_action.get_priority()):
                return True
            else:
                return False
        elif self.trainer_has_action_queued(True):
            return True
        else:
            return False
        
    def get_trainer(self, is_player: bool) -> Trainer:
        """
        Gets the trainer corresponding to the supplied parameter.

        Parameters
        is_player : True iff the trainer we want is the player.
        """
        if is_player:
            return self._player
        else:
            return self._enemy
    
    def attempt_end_early(self) -> None:
        """Ends the battle early if it's not a trainer battle"""
        if not(self.is_trainer_battle()):
            self._end_early = True

    def is_trainer_battle(self) -> bool:
        """Returns true iff the battle is between trainers"""
        return self._is_trainer_battle

    def is_action_queue_full(self) -> bool:
        """Returns true if both trainers have an action queued."""
        if self.trainer_has_action_queued(True) and self.trainer_has_action_queued(False):
            return True
        else:
            return False

    def is_action_queue_empty(self) -> bool:
        """Returns true if neither trainer have an action queued."""
        if self.trainer_has_action_queued(True) or self.trainer_has_action_queued(False):
            return False
        else:
            return True

    def trainer_has_action_queued(self, is_player: bool) -> bool:
        """
        Returns true iff the supplied trainer has an action queued

        Parameters
        is_player : True iff the trainer we want to check for is the player.
        """
        if is_player and (self._trainer_action != self._no_action):
            return True
        elif not(is_player) and (self._enemy_action != self._no_action):
            return True
        else:
            return False

    def is_ready(self) -> bool:
        """
        Returns true iff the next action is ready to be performed.
        The battle is deemed ready if neither trainer has performed an action this round and the action queue is full, 
        or if one trainer has performed an action, and the other trainer is in the queue.
        """
        if self.is_action_queue_full():
            return True
        elif not(self.is_action_queue_empty()) and (self._performed != 0):
            return True
        else:
            return False        

    def queue_action(self, action: Action, is_player: bool) -> None:  
        """
        Attempts to queue the supplied action if it's valid given the battle state, and came from the right trainer.
        An action is unable to be added to the queue if: The trainer is already in the queue; The queue is ready; The action is invalid given the game state;

        Parameters
        action    : The action we are attempting to queue
        is_player : True iff we're saying the action is going to be performed by the player.
        """
        if not(self.trainer_has_action_queued(is_player)) and action.is_valid(self,is_player) and not(self.is_ready()):
            if is_player:
                self._trainer_action = action
            else:
                self._enemy_action = action

        self.trainer_has_action_queued(is_player)

    def enact_turn(self) -> Optional[ActionSummary]:
        """
        Attempts to perform the next action in the queue, and returns a summary of its effects if it was valid.

        Notes
        1. If the next action in the queue is invalid, it should still be removed from the queue.
        2. If this was the last turn to be performed that round, perform the post round actions.
        """
        #self._performed check the action situation -> 0: Sction queue is empty 1: Action of player is performed.  2: Action of enemy is performed.
        player_turn = self.get_turn()
        if (player_turn == None) or (self.is_ready() == False):
            return ActionSummary("The round is not ready!")

        if player_turn:
            action_enact = copy.deepcopy(self._trainer_action)
            self._trainer_action = self._no_action
            self._performed = 1
            """Method : If this was the last turn to be performed that round, perform the post round actions."""
            if self.is_action_queue_empty():
                self._player._current_pokemon.post_round_actions()
                self._enemy._current_pokemon.post_round_actions()
                self._performed = 0
        else:
            action_enact = copy.deepcopy(self._enemy_action)
            self._enemy_action = self._no_action
            self._performed = 2
            """Method : If this was the last turn to be performed that round, perform the post round actions."""
            if self.is_action_queue_empty():
                self._player._current_pokemon.post_round_actions()
                self._enemy._current_pokemon.post_round_actions()
                self._performed = 0

        return action_enact.apply(self, player_turn)

    def is_over(self) -> bool:
        """
        Returns true iff the battle is over.
        A battle is over if all of the pokemon have fainted for either trainer, or if it ended early.
        """
        if self._player.all_pokemon_fainted() or self._enemy.all_pokemon_fainted() or self._end_early:
            return True
        else:
            return False
        

class ActionSummary(object):
    """
    A class containing messages about actions and their effects.
    These messages are handled by the view to display information about the flow of the game.
    Constructs a new ActionSummary with an optional message.
    """
    def __init__(self, message: Optional[str] = None) -> None:
        """
        Constructs a new ActionSummary with an optional message.

        Parameters
        message  : An optional message to be included.
        _message : A list of message.
        """
        self._message = list()
        self._message.append(message)
        
        if message == None:
            self._message.remove(None)

    def get_messages(self) -> List[str]:
        """Returns a list of the messages contained within this summary."""
        return self._message

    def add_message(self, message: str) -> None:
        """
        Adds the supplied message to the ActionSummary instance.

        Parameters
        message : The message to add.
        """
        self._message.append(message) 
        if message == None:
            self._message.remove(None)

    def combine(self, summary: ActionSummary) -> None:
        """
        Combines two ActionSummaries.
        The messages contained in the supplied summary should be added after those currently contained.

        Parameters
        summary : A summary containing the messages to add.
        """
        for string in summary.get_messages():
            self._message.append(string)


class Action(object):
    """
    An abstract class detailing anything which takes up a turn in battle.
    Applying an action can be thought of as moving the game from one state to the next.

    Subclasses: Flee, Item, Move, SwitchPokemon
    """
    def get_priority(self) -> int:
        """
        Returns the priority of this action, which is used to determine which action is performed first each round in the battle.
        Lower values of priority are 'quicker' than higher values, e.g. an Action with priority 0 happens before one with priority 1.
        You might want to take a look at the support code for a hint here.
        """
        return DEFAULT_ACTION_PRIORITY

    def is_valid(self, battle: Battle, is_player: bool) -> bool:
        """
        Determines if the action would be valid for the given trainer and battle state. Returns true iff it would be valid.
        By default, no action is valid if the game is over, or if it's not the trainer's turn.

        Parameters
        battle    : The ongoing pokemon battle
        is_player : True iff the player is using this action.
        """
        if battle.is_over() or ((is_player != battle.get_turn()) and not(battle.get_turn() == None)):
            return False
        else:
            return True

    def apply(self, battle: Battle, is_player: bool) -> ActionSummary:
        """
        Applies the action to the game state and returns a summary of the effects of doing so.
        On the base Action class, this method should raise a NotImplementedError.

        Parameters
        battle    : The ongoing pokemon battle
        is_player : True iff the player is using this action.
        """
        raise NotImplementedError()

    def __str__(self) -> str:
        """Return a string representation of this class."""
        return 'Action()'

    def __repr__(self) -> str:
        """Return a string representation of this class"""
        return str(self)  


class Flee(Action):
    """
    An action where the trainer attempts to run away from the battle.

    Notes
    1. While it may still be valid, it has no effect in trainer battles.
    2. If successful, this should end the battle early.

    Ancestors : Action
    
    Inherited members
    Action: __repr__, get_priority
    """
    def is_valid(self, battle: Battle, is_player: bool) -> bool:
        """
        Determines if an attempt to flee would be valid for a given battle state. Returns true iff it would be valid.
        Fleeing is considered a valid action if the base action validity checks pass, and the trainer's current pokemon has not fainted. This does not mean, however, that a trainer can flee trainer battles. In that case, fleeing is considered wasting a turn.

        Parameters
        battle    : The ongoing pokemon battle
        is_player : True iff the player is using this item.
        """
        player = battle.get_trainer(is_player)

        if battle.is_over() or ((is_player != battle.get_turn()) and not(battle.get_turn() == None)):
            return False
            
        if player._current_pokemon.has_fainted():
            return False
        else:
            return True

    def apply(self, battle: Battle, is_player: bool) -> ActionSummary:
        """
        The trainer attempts to flee the battle.
        The resulting message depends on whether or not the action was successful. See the support code for a hint.

        Parameters
        battle    : The ongoing pokemon battle
        is_player : True iff the player is using this item.
        """
        battle.attempt_end_early()
        if is_player and battle._end_early:
            return ActionSummary(FLEE_SUCCESS)

        return ActionSummary(FLEE_INVALID)

    def __str__(self) -> str:
        """Return a string representation of this class."""
        return "Flee()"

class SwitchPokemon(Action):
    """
    An action representing the trainer's intention to switch pokemon.

    Ancestors : Action

    Inherited members
    Action: __repr__, get_priority
    """
    def __init__(self, next_pokemon_index: int) -> None:
        """
        Creates an instance of the SwitchPokemon class.

        Parameters
        next_pokemon_index : The index of the pokemon the trainer wants to switch to.
        """
        self._next_pokemon_index = next_pokemon_index

    def is_valid(self, battle: Battle, is_player: bool) -> bool:
        """
        Determines if switching pokemon would be valid for a given trainer and battle state. Returns true iff it would be valid.
        After checking the validity requirements specified on the base Action class, switching delegates validity checking to the Trainer class.

        Parameters
        battle    : The ongoing pokemon battle
        is_player : True iff the player is using this item.
        """
        if battle.is_over() or ((is_player != battle.get_turn()) and not(battle.get_turn() == None)):
            return False

        if (is_player and battle._player.can_switch_pokemon(self._next_pokemon_index)) or (not(is_player) and battle._enemy.can_switch_pokemon(self._next_pokemon_index)):
            return True
        else:
            return False

    def apply(self, battle: Battle, is_player: bool) -> ActionSummary:
        """
        The trainer switches pokemon, assuming that the switch would be valid.
        If the trainer using this action is the player, and their pokemon has not yet fainted, a message should be added to the action summary, in the form: '{pokemon_name}, return!'.

        Parameters
        battle    : The ongoing pokemon battle
        is_player : True iff the player is using this action.
        """
        pokemon_alive_return_msg = ActionSummary()
        player = battle.get_trainer(is_player)

        if not(player._current_pokemon.has_fainted()):
            pokemon_alive_return_msg = ActionSummary(f"{player._current_pokemon.get_name()}, return!")

        player.switch_pokemon(self._next_pokemon_index)
        pokemon_alive_return_msg.add_message(f"{player.get_name()} switched to {player._pokemon[self._next_pokemon_index].get_name()}.")
        return pokemon_alive_return_msg

    def __str__(self) -> str:
        """Return a string representation of this class."""
        return f"SwitchPokemon({self._next_pokemon_index})"


class Item(Action):
    """
    An abstract class representing an Item, which a trainer may attempt to use to influence the battle.
    Creates an Item.

    Parameters
    name : The name of this item
    
    Ancestors : Action
    
    Subclasses : Food, Pokeball

    Inherited members
    Action: __repr__, apply, get_priority
    """
    def __init__(self, name: str) -> None:
        """
        Creates an Item.

        Parameters
        name: The name of this item
        """
        self._item_name = name

    def get_name(self) -> str:
        """Return the name of this item"""
        return self._item_name

    def is_valid(self, battle: Battle, is_player: bool) -> bool:
        """
        Determines if using the item would be a valid action for the given trainer and battle state. Returns true iff it would be valid.
        In addition to the validity requirements specified on the base Action class, Item and its subclasses are considered valid if: 
        1. The trainer's current pokemon has not fainted. 
        2. The item exists in the inventory of the trainer attempting to use it.

        Parameters
        battle    : The ongoing pokemon battle
        is_player : True iff the player is using this item.
        """
        player = battle.get_trainer(is_player)

        if battle.is_over() or ((is_player != battle.get_turn()) and not(battle.get_turn() == None)):
            return False

        """Method : Cheak that 1. The trainer's current pokemon has not fainted. 2. The item exists in the inventory of the trainer attempting to use it."""
        if not(player._current_pokemon.has_fainted()) and (self in player.get_inventory()):
            return True
        else:
            return False

    def decrement_item_count(self, trainer: Trainer) -> None:
        """
        Decrease the count of this item by one in the trainer's inventory

        Parameters
        trainer : The trainer attempting to use this item.
        """
        if self in trainer.get_inventory():
            trainer.get_inventory()[self] -= 1

            if trainer.get_inventory()[self] == 0:
                del trainer.get_inventory()[self]

    def __str__(self) -> str:
        """Return a string representation of this class."""
        return "Item()"


class Pokeball(Item):
    """
    An item which a trainer can use to attempt to catch wild pokemon.

    Ancestors:Item, Action

    Inherited members
    Item: __repr__, decrement_item_count, get_name, get_priority, is_valid
    """
    def __init__(self, name, catch_chance) -> None:
        """
        Creates a pokeball instance, used to catch pokemon in wild battles

        Parameters
        name         : The name of this pokeball
        catch_chance : The chance this pokeball has of catching a pokemon.
        """
        super().__init__(name)
        self._catch_chance      = catch_chance

    def __eq__(self, pokeball: Pokeball):
        """ Define the equality logic for comparing two objects using the equal operator (==)"""
        if not isinstance(pokeball, Pokeball):
            return False
        return (self._item_name == pokeball._item_name) and (self._catch_chance == pokeball._catch_chance)

    def __hash__(self):
        """Make the class to be properly hashable."""
        return 0

    def apply(self, battle: Battle, is_player: bool) -> ActionSummary:
        """
        Attempt to catch the enemy pokemon and returns an ActionSummary containing information about the catch attempt.
        The returned summary will contain a different message based on the results of attempting to use the pokeball. See the support code for some hints as to what these messages might be.

        Notes
        1. No matter the result of the catch attempt, a pokeball will be used.
        2. Catching pokemon is impossible in trainer battles.
        3. The did_succeed method from the support code must be used to determine if a catch attempt was successful.
        4. The wild pokemon will be added to the trainers roster if there is room
        5. In a wild battle, catching the enemy pokemon will end the battle.
        
        Parameters
        battle    : The ongoing pokemon battle
        is_player : True iff the player is using this item.
        """
        catch_msg   = ActionSummary()
        player      = battle.get_trainer(is_player)
        enemy       = battle.get_trainer(not(is_player))
        """Method : No matter the result of the catch attempt, a pokeball will be used."""
        self.decrement_item_count(player)

        """Method : Catching pokemon is impossible in trainer battles."""
        if battle._is_trainer_battle:
            return ActionSummary(POKEBALL_INVALID_BATTLE_TYPE)
        """
        Method :
        The did_succeed method from the support code must be used to determine if a catch attempt was successful.
        The wild pokemon will be added to the trainers roster if there is room
        """
        if did_succeed(self._catch_chance):
            #In a wild battle, catching the enemy pokemon will end the battle.
            battle._end_early = 1
            catch_msg = ActionSummary(POKEBALL_SUCCESSFUL_CATCH.format(enemy._current_pokemon.get_name()))
            if not(player.can_add_pokemon(enemy._current_pokemon.get_name())):
                catch_msg = ActionSummary(POKEBALL_FULL_TEAM.format(enemy._current_pokemon.get_name()))
            else:
                battle._player.add_pokemon(enemy._current_pokemon)
        else:
            catch_msg = ActionSummary(POKEBALL_UNSUCCESSFUL_CATCH.format(enemy._current_pokemon.get_name()))

        return catch_msg

    def __str__(self) -> str:
        """Return a string representation of this class."""
        return "Pokeball('{}')".format(self._item_name)

class Food(Item):
    """
    An Item which restores HP to the pokemon whose trainer uses it.

    Ancestors : Item, Action

    Inherited members
    Item : __repr__, decrement_item_count,, get_name, get_priority, is_valid
    """
    def __init__(self, name: str, health_restored: int) -> None:
        """
        Create a Food instance.

        Parameters
        name            : The name of this food.
        health_restored : The number of health points restored when a pokemon eats this piece of food.
        """
        super().__init__(name)
        self._health_restored = health_restored

    def __eq__(self, food: Food):
        """ Define the equality logic for comparing two objects using the equal operator (==)"""
        if not isinstance(food, Food):
            return False
        return (self._item_name == food._item_name) and (self._health_restored == food._health_restored)

    def __hash__(self):
        """Make the class to be properly hashable."""
        return 41 * (41 + self._health_restored)

    def apply(self, battle: Battle, is_player: bool) -> ActionSummary:
        """
        The trainer's current pokemon eats the food.
        Their current pokemon's health should consequently increase by the amount of health restored by this food.

        Parameters
        battle    : The ongoing pokemon battle
        is_player : True iff the player is using this item.
        """
        player = battle.get_trainer(is_player)
        """No matter the result of the catch attempt, a pokeball will be used."""
        self.decrement_item_count(player)
        """
        The trainer's current pokemon eats the food.
        Their current pokemon's health should consequently increase by the amount of health restored by this food.
        """
        player = battle.get_trainer(is_player)
        player._current_pokemon.modify_health(self._health_restored)
        return ActionSummary("{} ate {}.".format(player._current_pokemon.get_name(), self._item_name))
    
    def __str__(self) -> str:
        """Return a string representation of this class."""
        return "Food('{}')".format(self._item_name)

class Move(Action):
    """
    An abstract class representing all learnable pokemon moves.
    Creates an instance of the Move class.
    Like pokemon, moves have a type which determines their effectiveness. They also have a speed which determines the move's priority.

    Ancestors : Action
    
    Subclasses : Attack, StatusModifier

    Inherited members
    Action: __repr__
    """
    def __init__(self, name: str, element_type: str, max_uses: int, speed: int) -> None:
        """
        Creates an instance of the Move class.
        Like pokemon, moves have a type which determines their effectiveness. They also have a speed which determines the move's priority.

        Parameters
        name         : The name of this move
        element_type : The name of the type of this move
        max_uses     : The number of time this move can be used before resting
        speed        : The speed of this move, with lower values corresponding to faster moves priorities.
        """
        self._name = name
        self._element_type = element_type
        self._max_uses = max_uses
        self._speed = speed

    def get_name(self) -> str:
        """Return the name of this move"""
        return self._name

    def get_element_type(self) -> str:
        """Return the type of this move"""
        return self._element_type

    def get_max_uses(self) -> int:
        """Return the maximum times this move can be used"""
        return self._max_uses

    def get_priority(self) -> int:
        """
        Return the priority of this move.
        Moves have a speed-based priority. 
        By default they are slower than other actions, with their total priority being calculated by adding the default speed-based action priority to the individual move's speed.
        """
        return self._speed + SPEED_BASED_ACTION_PRIORITY

    def is_valid(self, battle: Battle, is_player: bool) -> bool:
        """
        Determines if the move would be valid for the given trainer and battle state. Returns true iff it would be valid.
        In addition to the validity requirements specified on the base Action class, a Move is considered valid if: 
        1. The trainer's current pokemon has not fainted. 
        2. The trainer's current pokemon has learnt this move. 
        3. The trainer's current pokemon has uses remaining for this move.

        Parameters
        battle    : The ongoing pokemon battle
        is_player : True iff the player is using this action.
        """
        if battle.is_over() or ((is_player != battle.get_turn()) and not(battle.get_turn() == None)):
            return False

        player = battle.get_trainer(is_player)

        if not(player._current_pokemon.has_fainted()) and (self in player._current_pokemon._moves) and (player._current_pokemon.get_remaining_move_uses(self)):
            return True
        else:
            return False

    def apply(self, battle: Battle, is_player: bool) -> ActionSummary:
        """
        Applies the Move to the game state.
        Generally, the move should be performed and its effects should be applied to the player and/or the enemy if needed. 
        In addition, the appropriate pokemon's remaining moves should be updated.

        Notes
        In the resulting ActionSummary, messages for ally effects should preceed enemy effects.

        Parameters
        battle    : The ongoing pokemon battle
        is_player : True iff the player is using this action.
        """
        player = battle.get_trainer(is_player)
        player._current_pokemon.reduce_move_count(self)
        return ActionSummary("{} used {}.".format(player._current_pokemon.get_name(), self.get_name()))

    def apply_ally_effects(self, trainer: Trainer) -> ActionSummary:
        """
        Apply this move's effects to the ally trainer; if appropriate, and return the resulting ActionSummary.

        Parameters
        trainer : The trainer whose pokemon is using the move.
        """
        return ActionSummary("{} used {}".format(trainer._current_pokemon.get_name(), self.get_name()))

    def apply_enemy_effects(self, trainer: Trainer, enemy: Trainer) -> ActionSummary:
        """
        Apply this move's effects to the enemy; if appropriate, and return the resulting ActionSummary.

        Parameters
        trainer : The trainer whose pokemon is using the move.
        enemy   : The trainer whose pokemon is the target of the move.
        """
        return ActionSummary("{} used {} to debuff {}".format(trainer._current_pokemon.get_name(), self.get_name(), enemy._current_pokemon.get_name()))

    def __str__(self) -> str:
        """Return a string representation of this class."""
        return 'Move()'

class Attack(Move):
    """
    A class representing damaging pokemon moves, that may be used against an enemy pokemon.

    Notes
    1. In addition to regular move requirements, attacking moves have a base damage and hit chance.
    2. Base damage is the damage this move would do before the pokemon's attack, defense or type effectiveness is accounted for.
    3. Hit chance is a measure of how likely the move is to hit an enemy pokemon, before the pokemon's hit chance stat is taken into account.
    3. The did_succeed method from the support code must be used to determine if the attack hit.
    4. If an attack 'misses' it does no damage to the enemy pokemon.

    Ancestors : Move, Action

    Inherited members
    Move: __repr__, apply_ally_effects, apply_enemy_effects, get_element_type, get_max_uses, get_name, get_priority, is_valid
    """
    def __init__(self, name: str, element_type: str, max_uses: int, speed: int, base_damage: int, hit_chance: float) -> None:
        """
        Creates an instance of an attacking move.

        Parameters
        name         : The name of this move
        element_type : The name of the type of this move
        max_uses     : The number of time this move can be used before resting
        speed        : The speed of this move, with lower values corresponding to faster moves.
        base_damage  : The base damage of this move.
        hit_chance   : The base hit chance of this move.
        """
        super().__init__(name, element_type, max_uses, speed)
        self._base_damage   = base_damage
        self._hit_chance    = hit_chance

    def __eq__(self, attack: Attack):
        """ Define the equality logic for comparing two objects using the equal operator (==)"""
        if not isinstance(attack, Attack):
            return False
        return (self._name == attack._name) and (self._element_type == attack._element_type) and (self._max_uses == attack._max_uses) and (self._speed == self._speed) and (self._base_damage == attack._base_damage) and (self._hit_chance == attack._hit_chance)

    def __hash__(self):
        """Make the class to be properly hashable."""
        return 41 * (41 + self._speed) + self._base_damage

    def did_hit(self, pokemon: Pokemon) -> bool:
        """
        Determine if the move hit, based on the product of the pokemon's current hit chance, and the move's hit chance. Returns True iff it hits.

        Parameters
        pokemon : The attacking pokemon
        """
        if did_succeed(self._hit_chance) and did_succeed(pokemon._stats.get_hit_chance()):
            return True
        else:
            return False

    def calculate_damage(self, pokemon: Pokemon, enemy_pokemon: Pokemon) -> int:
        """
        Calculates what would be the total damage of using this move, assuming it hits, based on the stats of the attacking and defending pokemon.
        The damage formula is given by: d * e * a / (D + 1), rounded down to the nearest integer, where: 
        d is the move's base damage; 
        e is the move's type effectiveness (see support code); 
        a is the attacking pokemon's attack stat; 
        D is the defending pokemon's defense stat.

        Parameters
        pokemon       : The attacking trainer's pokemon
        enemy_pokemon : The defending trainer's pokemon
        """
        element_type = ElementType(self.get_element_type())
        effectiveness = element_type.get_effectiveness(enemy_pokemon.get_element_type())
        
        damage = floor(self._base_damage * effectiveness * pokemon._stats.get_attack() / (enemy_pokemon._stats.get_defense() + 1)) 
        return damage

    def apply(self, battle: Battle, is_player: bool) -> ActionSummary:
        """
        Applies the Attack to the game state.
        Generally, the attack should be performed and its effects should be applied to the enemy. 
        In addition, the appropriate pokemon's remaining moves should be updated.

        Notes
        1. In the resulting ActionSummary, messages for ally effects should preceed enemy effects.
        2. The pokemon will gain experience if the enemy's pokemon has fainted.
        3. Have to calculate the attack's hit chance.

        Parameters
        battle    : The ongoing pokemon battle
        is_player : True iff the player is using this action.
        """
        attack_msg  = ActionSummary()
        player      = battle.get_trainer(is_player)
        enemy       = battle.get_trainer(not(is_player))

        player._current_pokemon.reduce_move_count(self)
        attack_msg = ActionSummary("{} used {}.".format(player._current_pokemon.get_name(), self.get_name()))
        if self.did_hit(player._current_pokemon):
            enemy._current_pokemon.modify_health(-self.calculate_damage(player._current_pokemon, enemy._current_pokemon))
            if enemy._current_pokemon.has_fainted():
                player._current_pokemon.gain_experience(enemy._current_pokemon.experience_on_death())
                attack_msg.add_message("{} has fainted.".format(enemy._current_pokemon.get_name()))
                attack_msg.add_message("{} gained {} exp.".format(player._current_pokemon.get_name(), enemy._current_pokemon.experience_on_death()))
        else:
            attack_msg.add_message("{} missed!".format(player._current_pokemon.get_name()))

        return attack_msg

    def __str__(self) -> str:
        """Return a string representation of this class."""
        return "Attack('{}', '{}', {})".format(self.get_name(), self.get_element_type(), self.get_max_uses())                


class StatusModifier(Move):
    """
    An abstract class to group commonalities between buffs and debuffs.

    Ancestors : Move, Action

    Subclasses : Buff, Debuff

    Inherited members
    Move: __repr__, apply, apply_ally_effects, apply_enemy_effect,s get_element_type, get_max_uses, get_name, get_priority, is_valid
    """
    def __init__(self, name: str, element_type: str, max_uses: int, speed: int, modification: Tuple[float, int, int, int], rounds: int) -> None:
        """
        Creates an instance of this class

        Parameters
        name         : The name of this move
        element_type : The name of the type of this move
        max_uses     : The number of time this move can be used before resting
        speed        : The speed of this move, with lower values corresponding to faster moves.
        modification : A list of the same structure as the PokemonStats, to be applied for the duration of the supplied number of rounds.
        rounds       : The number of rounds for the modification to be in effect.
        """
        super().__init__(name, element_type, max_uses, speed)
        self._modification   = modification
        self._rounds         = rounds


class Buff(StatusModifier):
    """
    Moves which buff the trainer's selected pokemon.
    A buff is a stat modifier that is applied to the pokemon using the move.

    Ancestors : StatusModifier, Move, Action
    
    Inherited members
    StatusModifier:__init__, __repr__, apply_enemy_effects, get_element_type, get_max_uses, get_name, get_priority, is_valid
    """
    def __eq__(self, buff: Buff):
        """ Define the equality logic for comparing two objects using the equal operator (==)"""
        if not isinstance(buff, Buff):
            return False
        return (self._name == buff._name) and (self._element_type == buff._element_type) and (self._max_uses == buff._max_uses) and (self._speed == buff._speed) and (self._modification == buff._modification) and (self._rounds == buff._rounds)

    def __hash__(self):
        """Make the class to be properly hashable."""
        return 41 * (41 + self._speed) + self._rounds   

    def apply_ally_effects(self, trainer: Trainer) -> ActionSummary:
        """
        Apply this move's effects to the ally trainer; if appropriate, and return the resulting ActionSummary.

        Parameters
        trainer : The trainer whose pokemon is using the move.
        """
        buffer_msg = ActionSummary("{} used {}.".format(trainer._current_pokemon.get_name(), self.get_name()))
        buffer_msg.add_message("{} was buffed for {} turns.".format(trainer._current_pokemon.get_name(), self._rounds))
        trainer._current_pokemon.add_stat_modifier(self._modification, self._rounds)
        return buffer_msg

    def apply(self, battle: Battle, is_player: bool) -> ActionSummary:
        """
        Applies the Buff to the game state.
        Generally, the Buff should be performed and its effects should be applied to the player's pokemon. 
        In addition, the appropriate pokemon's remaining moves should be updated.

        Parameters
        battle    : The ongoing pokemon battle
        is_player : True iff the player is using this action.
        """
        player = battle.get_trainer(is_player)
        player._current_pokemon.reduce_move_count(self)
        return self.apply_ally_effects(player)

    def __str__(self) -> str:
        """Return a string representation of this class."""
        return "Buff('{}', '{}', {})".format(self.get_name(), self.get_element_type(), self.get_max_uses())

class Debuff(StatusModifier):
    """
    Moves which debuff the enemy trainer's selected pokemon.
    A debuff is a stat modifier that is applied to the enemy pokemon which is the target of this move.

    Ancestors : StatusModifier, Move, Action
    
    Inherited members
    StatusModifier: __init__, __repr__, apply_ally_effects, get_element_type, get_max_uses, get_name, get_priority, is_valid
    """
    def __eq__(self, debuff: Debuff):
        """ Define the equality logic for comparing two objects using the equal operator (==)"""
        if not isinstance(debuff, Debuff):
            return False
        return (self._name == debuff._name) and (self._element_type == debuff._element_type) and (self._max_uses == debuff._max_uses) and (self._speed == debuff._speed) and (self._modification == debuff._modification) and (self._rounds == debuff._rounds)

    def __hash__(self):
        """Make the class to be properly hashable."""
        return 41 * (41 + self._speed) + self._rounds

    def apply_enemy_effects(self, trainer: Trainer, enemy: Trainer) -> ActionSummary:
        """
        Apply this move's effects to the enemy; if appropriate, and return the resulting ActionSummary.

        Parameters
        trainer : The trainer whose pokemon is using the move.
        enemy   : The trainer whose pokemon is the target of the move.
        """
        buffer_msg = ActionSummary("{} used {}.".format(trainer._current_pokemon.get_name(), self.get_name()))
        buffer_msg.add_message("{} was debuffed for {} turns.".format(enemy._current_pokemon.get_name(), self._rounds))
        enemy._current_pokemon.add_stat_modifier(self._modification, self._rounds)
        return buffer_msg

    def apply(self, battle: Battle, is_player: bool) -> ActionSummary:
        """
        Applies the Deuff to the game state.
        Generally, the Deuff should be performed and its effects should be applied to the enemy's pokemon. 
        In addition, the appropriate pokemon's remaining moves should be updated.

        Parameters
        battle    : The ongoing pokemon battle
        is_player : True iff the player is using this action.
        """
        player = battle.get_trainer(is_player)
        enemy  = battle.get_trainer(not(is_player))
        player._current_pokemon.reduce_move_count(self)
        return self.apply_enemy_effects(player, enemy)

    def __str__(self) -> str:
        """Return a string representation of this class."""
        return "Debuff('{}', '{}', {})".format(self.get_name(), self.get_element_type(), self.get_max_uses())

# Below are the classes and functions which pertain only to masters students.
class Strategy(object):
    """
    An abstract class providing behaviour to determine a next action given a battle state.
    
    Subclasses : ScaredyCat, TeamRocket
    """
    def get_next_action(self, battle: Battle, is_player: bool) -> Action:
        """
        Determines and returns the next action for this strategy, given the battle state and trainer.
        This method should be overriden on subclasses.

        Parameters
        battle    : The ongoing pokemon battle
        is_player : True iff the player is using this action.
        """
        raise NotImplementedError()


class ScaredyCat(Strategy):
    """
    A strategy where the trainer always attempts to flee.
    Switches to the next available pokemon if the current one faints, and then keeps attempting to flee.

    Ancestors : Strategy

    Inherited members
    Strategy: get_next_action
    """
    def get_next_action(self, battle: Battle, is_player: bool) -> Action:
        """
        Determines and returns the next action for this strategy, given the battle state and trainer.

        Behaviour
        Switches to the next available pokemon if the current one faints, and then keeps attempting to flee.

        Parameters
        battle    : The ongoing pokemon battle
        is_player : True iff the player is using this action.
        """
        player = battle.get_trainer(is_player)

        if player._current_pokemon.has_fainted():
            for index in range(len(player._pokemon)):
                if player.can_switch_pokemon(index):
                    return SwitchPokemon(index)
        else:
            return Flee()

class TeamRocket(Strategy):
    """
    A tough strategy used by Pokemon Trainers that are members of Team Rocket.

    Behaviour
    1. Switch to the next available pokemon if the current one faints.
    2. Attempt to flee any wild battle.
    3. If the enemy trainer's current pokemon's name is 'pikachu', throw pokeballs at it, if some exist in the inventory.
    4. Otherwise, use the first available move with an elemental type effectiveness greater than 1x against the defending pokemon's type.
    5. Otherwise, use the first available move with uses.
    6. Attempt to flee if the current pokemon has no moves with uses.
    
    Ancestors : Strategy
    
    Inherited members
    Strategy: get_next_action
    """
    def get_next_action(self, battle: Battle, is_player: bool) -> Action:
        """
        Determines and returns the next action for this strategy, given the battle state and trainer.

        Behaviour
        1. Switch to the next available pokemon if the current one faints.
        2. Attempt to flee any wild battle.
        3. If the enemy trainer's current pokemon's name is 'pikachu', throw pokeballs at it, if some exist in the inventory.
        4. Otherwise, use the first available move with an elemental type effectiveness greater than 1x against the defending pokemon's type.
        5. Otherwise, use the first available move with uses.
        6. Attempt to flee if the current pokemon has no moves with uses.

        Parameters
        battle    : The ongoing pokemon battle
        is_player : True iff the player is using this action.
        """
        player = battle.get_trainer(is_player)
        enemy  = battle.get_trainer(not(is_player))

        if player._current_pokemon.has_fainted():
            for index in range(len(player._pokemon)):
                if player.can_switch_pokemon(index):
                    return SwitchPokemon(index) 
        if not(battle.is_trainer_battle()):
            return Flee()
        if (enemy._current_pokemon.get_name() == 'Pikachu'):
            for key in player.get_inventory():
                if isinstance(key, Pokeball):
                    return key
            
        for move in player._current_pokemon._moves:
            element_type = ElementType(move.get_element_type())
            effectiveness = element_type.get_effectiveness(enemy._current_pokemon.get_element_type())
            if effectiveness > 1:
                return move
            
        for move in player._current_pokemon._moves:
            if player._current_pokemon.get_remaining_move_uses(move):
                return move

        return Flee()


def create_encounter(trainer: Trainer, wild_pokemon: Pokemon) -> Battle:
    """
    Creates a Battle corresponding to an encounter with a wild pokemon.
    The enemy in this battle corresponds to a trainer with the empty string for a name, and whose only pokemon is the supplied wild pokemon.

    Parameters
    trainer      : The adventuring trainer.
    wild_pokemon : The pokemon that the player comes into contact with.
    """
    pokemon_met = Trainer(wild_pokemon.get_name())
    pokemon_met.add_pokemon(wild_pokemon)
    return Battle(trainer, pokemon_met, False)

if __name__ == "__main__":
    print(WRONG_FILE_MESSAGE)
