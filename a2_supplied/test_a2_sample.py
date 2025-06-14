import inspect
import random
from functools import partial
from pathlib import Path
from typing import Optional, List, Dict, Tuple, Any

from testrunner import TestMaster, OrderedTestCase, AttributeGuesser, \
    skipIfFailed

Stats = Tuple[float, int, int, int]

SEED = 1001.2021

class PokemonStats(object):
    def __init__(self, stats: Stats) -> None: pass

    def level_up(self) -> None: pass

    def get_hit_chance(self) -> float: pass

    def get_max_health(self) -> int: pass

    def get_attack(self) -> int: pass

    def get_defense(self) -> int: pass

    def apply_modifier(self, modifier: Stats) -> 'PokemonStats': pass

    def __str__(self) -> str: pass

    def __repr__(self) -> str: pass


class Pokemon(object):
    def __init__(self, name: str, stats: PokemonStats, element_type: str,
                 moves: List['Move'], level: int = 1) -> None: pass

    def get_name(self) -> str: pass

    def get_health(self) -> int: pass

    def get_max_health(self) -> int: pass

    def get_element_type(self) -> str: pass

    def get_remaining_move_uses(self, move: 'Move') -> int: pass

    def get_level(self) -> int: pass

    def get_experience(self): pass

    def get_next_level_experience_requirement(self): pass

    def get_move_info(self) -> List[Tuple['Move', int]]: pass

    def has_fainted(self) -> bool: pass

    def modify_health(self, change: int) -> None: pass

    def gain_experience(self, experience: int) -> None: pass

    def level_up(self) -> None: pass

    def experience_on_death(self) -> int: pass

    def can_learn_move(self, move: 'Move') -> bool: pass

    def learn_move(self, move: 'Move') -> None: pass

    def forget_move(self, move: 'Move') -> None: pass

    def has_moves_left(self) -> bool: pass

    def reduce_move_count(self, move: 'Move') -> None: pass

    def add_stat_modifier(self, modifier: Stats,
                          rounds: int) -> None: pass

    def get_stats(self) -> PokemonStats: pass

    def post_round_actions(self) -> None: pass

    def rest(self) -> None: pass

    def __str__(self) -> str: pass

    def __repr__(self) -> str: pass


class Trainer(object):
    def __init__(self, name: str) -> None: pass

    def get_name(self): pass

    def get_inventory(self) -> Dict['Item', int]: pass

    def get_current_pokemon(self) -> Pokemon: pass

    def get_all_pokemon(self) -> List[Pokemon]: pass

    def rest_all_pokemon(self) -> None: pass

    def all_pokemon_fainted(self) -> bool: pass

    def can_add_pokemon(self, pokemon: Pokemon) -> bool: pass

    def add_pokemon(self, pokemon: Pokemon) -> None: pass

    def release_pokemon(self, index: int) -> None: pass

    def can_switch_pokemon(self, index: int) -> bool: pass

    def switch_pokemon(self, index: int) -> None: pass

    def add_item(self, item: 'Item', uses: int) -> None: pass

    def has_item(self, item: 'Item') -> bool: pass

    def use_item(self, item: 'Item') -> None: pass

    def __str__(self) -> str: pass

    def __repr__(self) -> str: pass


class Battle(object):
    def __init__(self, player: Trainer, enemy: Trainer,
                 is_trainer_battle: bool) -> None: pass

    def get_turn(self) -> Optional[bool]: pass

    def get_trainer(self, is_player: bool) -> Trainer: pass

    def attempt_end_early(self) -> None: pass

    def is_trainer_battle(self) -> bool: pass

    def is_action_queue_full(self) -> bool: pass

    def is_action_queue_empty(self) -> bool: pass

    def trainer_has_action_queued(self, is_player: bool) -> bool: pass

    def is_ready(self) -> bool: pass

    def _update_turn(self, is_player): pass

    def queue_action(self, action: 'Action', is_player: bool) -> None: pass

    def _sort_actions(self) -> None: pass

    def enact_turn(self) -> Optional['ActionSummary']: pass

    def is_over(self) -> bool: pass


class ActionSummary(object):
    def __init__(self, message: Optional[str] = None) -> None: pass

    def get_messages(self) -> List[str]: pass

    def add_message(self, message: str) -> None: pass

    def combine(self, summary: 'ActionSummary') -> None: pass


class Action(object):
    def get_priority(self) -> int: pass

    def is_valid(self, battle: 'Battle', is_player: bool) -> bool: pass

    def apply(self, battle: 'Battle', is_player: bool) -> ActionSummary: pass

    def __str__(self) -> str: pass

    def __repr__(self) -> str: pass


class Flee(Action):
    def is_valid(self, battle: 'Battle', is_player: bool) -> bool: pass

    def apply(self, battle: 'Battle', is_player: bool) -> ActionSummary: pass


class SwitchPokemon(Action):
    def __init__(self, next_pokemon_index: int) -> None: pass

    def is_valid(self, battle: 'Battle', is_player: bool) -> bool: pass

    def apply(self, battle: 'Battle', is_player: bool) -> ActionSummary: pass


class Item(Action):
    def __init__(self, name: str) -> None: pass

    def get_name(self) -> str: pass

    def is_valid(self, battle: 'Battle', is_player: bool) -> bool: pass

    def decrement_item_count(self, trainer: 'Trainer') -> None: pass

    def __str__(self) -> str: pass


class Pokeball(Item):
    def __init__(self, name, catch_chance) -> None: pass

    def apply(self, battle: 'Battle', is_player: bool) -> ActionSummary: pass


class Food(Item):
    def __init__(self, name: str, health_restored: int) -> None: pass

    def apply(self, battle: 'Battle', is_player: bool) -> ActionSummary: pass


class Move(Action):
    def __init__(self, name: str, element_type: str, uses: int,
                 speed: int): pass

    def get_name(self) -> str: pass

    def get_element_type(self) -> str: pass

    def get_max_uses(self) -> int: pass

    def get_priority(self) -> int: pass

    def is_valid(self, battle: 'Battle', is_player: bool) -> bool: pass

    def apply(self, battle: 'Battle', is_player: bool) -> ActionSummary: pass

    def apply_ally_effects(self, trainer: 'Trainer') -> ActionSummary: pass

    def apply_enemy_effects(self, trainer: 'Trainer',
                            enemy: 'Trainer') -> ActionSummary: pass

    def __str__(self) -> str: pass


class Attack(Move):
    def __init__(self, name: str, element_type: str, uses: int, speed: int,
                 base_damage: int,
                 hit_chance: float) -> None: pass

    def apply_enemy_effects(self, trainer: 'Trainer',
                            enemy: 'Trainer') -> ActionSummary: pass

    def did_hit(self, pokemon: 'Pokemon') -> bool: pass

    def calculate_damage(self, pokemon: 'Pokemon',
                         enemy_pokemon: 'Pokemon') -> int: pass


class StatusModifier(Move):
    def __init__(self, name: str, element_type: str, uses: int, speed: int,
                 modification: Stats, rounds: int) -> None: pass


class Buff(StatusModifier):
    def apply_ally_effects(self, player: 'Trainer') -> ActionSummary: pass


class Debuff(StatusModifier):
    def apply_enemy_effects(self, trainer: 'Trainer',
                            enemy: 'Trainer') -> ActionSummary: pass


class Strategy(object):
    def get_next_action(self, battle: Battle, is_player: bool) -> Action: pass

    def _switch_to_next_pokemon(self, trainer: 'Trainer') -> Action: pass


class ScaredyCat(Strategy):
    def get_next_action(self, battle: Battle, is_player: bool) -> Action: pass


class TeamRocket(Strategy):
    pass


class ElementType:
    @staticmethod
    def of(name: str) -> "ElementType": pass

    def __init__(self, name: str) -> None: pass

    def add_type_effectiveness(self, type: str,
                               effectiveness: float) -> None: pass

    def get_effectiveness(self, defending_type: str) -> float: pass


class NoPokemonException(Exception):
    pass


class A2:
    ActionSummary = ActionSummary
    Action = Action
    Move = Move
    Attack = Attack
    StatusModifier = StatusModifier
    Buff = Buff
    Debuff = Debuff
    Item = Item
    Pokeball = Pokeball
    Food = Food
    SwitchPokemon = SwitchPokemon
    Flee = Flee
    PokemonStats = PokemonStats
    Pokemon = Pokemon
    Trainer = Trainer
    Battle = Battle
    Strategy = Strategy
    ScaredyCat = ScaredyCat
    TeamRocket = TeamRocket

    @staticmethod
    def create_encounter(trainer: Trainer, wild_pokemon: Pokemon) -> Battle:
        pass


class A2Support:
    ElementType = ElementType
    NoPokemonException = NoPokemonException

    @staticmethod
    def did_succeed(chance: float) -> bool: pass


class TestA2(OrderedTestCase):
    """ Base for all a1 test cases """
    a2: A2
    a2_support: A2Support


class TestDesign(TestA2):
    def _aggregate_class_and_functions_defined(self, module, test_class,
                                               sub_class_of=None):
        """
            Helper method to test a class has all the required methods
            and signatures.
        """
        cls_name = test_class.__name__
        if not self.aggregate(self.assertClassDefined, module, cls_name,
                              tag=cls_name):
            return

        if sub_class_of and hasattr(module, sub_class_of):
            self.aggregate(self.assertIsSubclass, getattr(module, cls_name),
                           getattr(module, sub_class_of))

        cls = getattr(module, cls_name)
        empty = inspect.Parameter.empty
        for func_name, func in inspect.getmembers(test_class,
                                                  predicate=inspect.isfunction):
            params = inspect.signature(func).parameters
            if self.aggregate(self.assertFunctionDefined, cls, func_name,
                              len(params), tag=f"{cls_name}.{func_name}"):
                # logic should be moved to testrunner.py
                for p1, p2 in zip(params.values(), inspect.signature(
                        getattr(cls, func_name)).parameters.values()):
                    if p1.default == empty and p2.default != empty:
                        self.aggregate(self.fail,
                                       msg=f"expected \"{p2.name}\" to not "
                                           f"have default value but got \""
                                           f"{p2.default}\"",
                                       tag=f"{cls_name}.{func_name}.{p1.name}")
                    elif p1.default != empty and p2.default == empty:
                        self.aggregate(self.fail,
                                       msg=f"expected \"{p2.name}\" to have "
                                           f"default value \"{p1.default}\"",
                                       tag=f"{cls_name}.{func_name}.{p1.name}")
                    else:
                        self.aggregate(self.assertEqual, p1.default, p2.default,
                                       msg=f"expected \"{p2.name}\" to have "
                                           f"default value \"{p1.default}\" "
                                           f"but got \"{p2.default}\"",
                                       tag=f"{cls_name}.{func_name}.{p1.name}")


class TestDesignUndergrads(TestDesign):
    def test_clean_import(self):
        """ Test no prints on import """
        self.assertIsCleanImport(self.a2,
                                 msg="You should not be printing on "
                                     "import for a2.py")

    def test_doc_strings(self):
        """ Test all classes and functions have documentation strings """
        a2 = AttributeGuesser.get_wrapped_object(self.a2)
        ignored_modules = ("a2_support",)
        ignored = frozenset(("__str__", "__repr__"))

        for cls_name, cls in inspect.getmembers(a2,
                                                predicate=inspect.isclass):
            if cls.__module__ in ignored_modules:
                continue
            self.aggregate(self.assertDocString, cls)
            defined = vars(cls)
            for func_name, func in inspect.getmembers(
                    cls, predicate=inspect.isfunction):
                if func_name in ignored or func_name not in defined:
                    continue
                self.aggregate(self.assertRecursiveDocString, cls,
                               func_name,
                               a2)

        self.aggregate_tests()

    def test_classes_and_functions_defined_undergrads(self):
        """
        Test all specified classes and functions defined correctly for undergrads
        """
        a2 = AttributeGuesser.get_wrapped_object(self.a2)
        self._aggregate_class_and_functions_defined(a2, Action)
        self._aggregate_class_and_functions_defined(a2, Flee, "Action")
        self._aggregate_class_and_functions_defined(a2, Item, "Action")
        self._aggregate_class_and_functions_defined(a2, Move, "Action")
        self._aggregate_class_and_functions_defined(a2, SwitchPokemon, "Action")
        self._aggregate_class_and_functions_defined(a2, Food, "Item")
        self._aggregate_class_and_functions_defined(a2, Pokeball, "Item")
        self._aggregate_class_and_functions_defined(a2, Attack, "Move")
        self._aggregate_class_and_functions_defined(a2, StatusModifier, "Move")
        self._aggregate_class_and_functions_defined(a2, Buff, "StatusModifier")
        self._aggregate_class_and_functions_defined(a2, Debuff,
                                                    "StatusModifier")
        self.aggregate_tests()


class TestDesignPostgrads(TestDesign):
    def test_classes_and_functions_defined_postgrads(self):
        """
        Test all specified classes and functions defined correctly for postgrads
        """
        a2 = AttributeGuesser.get_wrapped_object(self.a2)
        self._aggregate_class_and_functions_defined(a2, Strategy, "Strategy")
        self._aggregate_class_and_functions_defined(a2, ScaredyCat,
                                                    "ScaredyCat")
        self._aggregate_class_and_functions_defined(a2, TeamRocket,
                                                    "TeamRocket")
        self.aggregate(self.assertFunctionDefined, a2, "create_encounter", 2)
        self.aggregate_tests()


class TestFunctionality(TestA2):
    """ Base for all A2 functionality tests. """

    TEST_DATA = (Path(__file__).parent / "test_data").resolve()

    def load_test_data(self, filename: str):
        """ load test data from file """
        with open(self.TEST_DATA / filename, encoding="utf8") as file:
            return file.read()

    def write_test_data(self, filename: str, output: str):
        """ write test data to file """
        with open(self.TEST_DATA / filename, "w", encoding="utf8") as file:
            file.write(output)

    def assertReturnsNone(self, obj: Any, method_name: str) -> None:
        message = f"{method_name} should not return anything"
        super().assertIsNone(obj, message)

    def assertStats(self, stat: PokemonStats, values: Stats):
        hit_chance, max_health, attack, defense = values
        self.assertEqual(stat.get_hit_chance(), hit_chance)
        self.assertEqual(stat.get_max_health(), max_health)
        self.assertEqual(stat.get_attack(), attack)
        self.assertEqual(stat.get_defense(), defense)

    def _create_move(self, name="tackle", max_uses=10) -> Move:
        return self.a2.Attack(name, 'normal', max_uses, 80, 50, 1)

    def _create_pokemon(self, name="Pikachu"):
        stats = self.a2.PokemonStats((1, 100, 200, 200))
        return self.a2.Pokemon(name, stats, "electric", [])

    def _create_food(self):
        return self.a2.Food("Good Soup", 10)

    def _create_pokeball(self):
        return self.a2.Pokeball("Master Ball", 0.4)

    def _create_action(self, cls="Flee", *args):
        return getattr(self.a2, cls)(*args)

    def tearDown(self) -> None:
        self.a2_support.ElementType._elements = {}


skipIfNotDefinedUndergrads = partial(
    skipIfFailed,
    TestDesignUndergrads,
    TestDesignUndergrads.test_classes_and_functions_defined_undergrads.__name__,
)


skipIfNotDefinedPostgrads = partial(
    skipIfFailed,
    TestDesignPostgrads,
    TestDesignPostgrads.test_classes_and_functions_defined_postgrads.__name__,
)


@skipIfNotDefinedUndergrads("PokemonStats")
class TestPokemonStats(TestFunctionality):
    def setUp(self) -> None:
        self._stats = (0.5, 95, 115, 80)
        self._pokemon_stats = self.a2.PokemonStats(self._stats)

    def test_get_attack_base(self):
        """ Test get_attack method """
        self.assertEqual(self._pokemon_stats.get_attack(), 115)

    def test_get_defense_base(self):
        """ Test get_defense method """
        self.assertEqual(self._pokemon_stats.get_defense(), 80)

    def test_level_up(self):
        """ Test leveling up """
        stats = self.a2.PokemonStats((0.5, 100, 120, 140))
        self.assertReturnsNone(stats.level_up(),
                               method_name="PokemonStats.level_up")
        self.assertStats(stats, (1, 105, 126, 147))

    def test_level_up_round(self):
        """ Test leveling up with rounding """
        self.assertReturnsNone(self._pokemon_stats.level_up(),
                               method_name="PokemonStats.level_up")
        self.assertStats(self._pokemon_stats, (1, 99, 120, 84))

    def test_apply_modifiers(self):
        """ Test applying modifiers """
        new_stats = self._pokemon_stats.apply_modifier((0.25, 5, -15, 20))
        self.assertStats(new_stats, (0.75, 100, 100, 100))

    def test_str(self):
        """ Test PokemonStat __str__ method """
        self.assertEqual(str(self._pokemon_stats),
                         f"PokemonStats({self._stats})")


@skipIfNotDefinedUndergrads("Pokemon")
@skipIfNotDefinedUndergrads("PokemonStats")
class TestPokemon(TestFunctionality):
    def setUp(self) -> None:
        self._move = self._create_move()
        self._stats = self.a2.PokemonStats((1, 100, 200, 200))
        self._modifiers = [
            (1, 200, 3, 4),
            (1, 200, 3, 4),
            (1, 100, 3, 4),
            (1, 150, 3, 4),
        ]
        self._pikachu = self.a2.Pokemon("Pikachu", self._stats, "electric", [],
                                        level=1)

    def test_get_name(self):
        """ Test getting pokemon's name """
        self.assertEqual(self._pikachu.get_name(), "Pikachu")

    def test_get_initial_health(self):
        """ Test getting pokemon's initial health """
        self.assertEqual(self._pikachu.get_health(), 100)

    def test_get_max_health(self):
        """ Test getting pokemon's max health """
        self.assertEqual(self._pikachu.get_max_health(), 100)

    def test_get_element_type(self):
        """ Test getting pokemon's element type """
        self.assertEqual(self._pikachu.get_element_type(), "electric")

    def test_get_level(self):
        """ Test getting pokemon's level """
        self.assertEqual(self._pikachu.get_level(), 1)

    def test_get_experience(self):
        """ Test getting pokemon's experience """
        self.assertEqual(self._pikachu.get_experience(), 1)

    def test_get_next_level_experience_requirement(self):
        """ Test getting pokemon's experience """
        exp_requirement = [8, 27, 64, 125, 216, 343, 512, 729, 1000]
        for level, exp in enumerate(exp_requirement, start=1):
            self.assertEqual(
                self._pikachu.get_next_level_experience_requirement(), exp,
                f"Pokemon level {level} must get to {exp} experience to level up"
            )
            self._pikachu.level_up()

    @skipIfNotDefinedUndergrads("Move")
    @skipIfNotDefinedUndergrads("Attack")
    def test_get_move_info_empty(self):
        """ Test getting move info of a pokemon """
        self.assertListEqual(self._pikachu.get_move_info(), [])

    def test_has_fainted(self):
        """ Test if pokemon has fainted """
        self.assertFalse(self._pikachu.has_fainted())
        self._pikachu.modify_health(-30)
        self.assertFalse(self._pikachu.has_fainted())
        self._pikachu.modify_health(-70)
        self.assertTrue(self._pikachu.has_fainted())

    def test_modify_health(self):
        """ Test modifying pokemon's health """
        self.assertReturnsNone(self._pikachu.modify_health(-30),
                               method_name="Pokemon.modify_health")
        self.assertEqual(self._pikachu.get_health(), 70)
        self.assertReturnsNone(self._pikachu.modify_health(20),
                               method_name="Pokemon.modify_health")
        self.assertEqual(self._pikachu.get_health(), 90)

    def test_modify_health_with_stats_modifiers(self):
        """ Test modifying pokemon's health capped by stat modifiers """
        for modifier in self._modifiers:
            self._pikachu.add_stat_modifier(modifier, 1)
        self.assertReturnsNone(self._pikachu.modify_health(1000),
                               method_name="Pokemon.modify_health")
        self.assertEqual(self._pikachu.get_health(), 750)
        self._pikachu.add_stat_modifier((1, -740, 100, 100), 1)
        self.assertReturnsNone(self._pikachu.modify_health(1),
                               method_name="Pokemon.modify_health")
        self.assertEqual(self._pikachu.get_health(), 10)

    def assertLevel2(self):
        self.assertEqual(self._pikachu.get_level(), 2)
        self.assertEqual(self._pikachu.get_stats().get_hit_chance(), 1)
        self.assertEqual(self._pikachu.get_stats().get_max_health(), 105)
        self.assertEqual(self._pikachu.get_stats().get_attack(), 210)
        self.assertEqual(self._pikachu.get_stats().get_defense(), 210)

    def assertLevel3(self):
        self.assertEqual(self._pikachu.get_level(), 3)
        self.assertEqual(self._pikachu.get_stats().get_hit_chance(), 1)
        self.assertEqual(self._pikachu.get_stats().get_max_health(), 110)
        self.assertEqual(self._pikachu.get_stats().get_attack(), 220)
        self.assertEqual(self._pikachu.get_stats().get_defense(), 220)

    def test_gain_experience_no_leveling_up(self):
        """ Test player gaining experience without leveling up """
        self._pikachu.gain_experience(6)
        self.assertEqual(self._pikachu.get_experience(), 7)
        self.assertEqual(self._pikachu.get_level(), 1)

    def test_gain_experience_up_1_level(self):
        """ Test player gaining experience resulting in 1 level up """
        self._pikachu.gain_experience(8)
        self.assertEqual(self._pikachu.get_experience(), 9)
        self.assertLevel2()

    def test_experience_on_death(self):
        """ Test get experience on death """
        exp = [28, 57, 85, 114, 142, 171, 200, 228, 257, 285]
        for level, value in enumerate(exp, start=1):
            self.assertEqual(self._pikachu.experience_on_death(), value,
                             f"Pokemon level {level} should give {value} "
                             f"experience on death.")
            self._pikachu.level_up()

    @skipIfNotDefinedUndergrads("Move")
    @skipIfNotDefinedUndergrads("Attack")
    def test_can_learn_move_not_yet_known(self):
        """ Test if pokemon can learn a move bade on if it's already learned """
        self.assertTrue(self._pikachu.can_learn_move(self._move))
        self._pikachu.learn_move(self._move)
        self.assertFalse(self._pikachu.can_learn_move(self._move))

    @skipIfNotDefinedUndergrads("Move")
    @skipIfNotDefinedUndergrads("Attack")
    def test_learn_move(self):
        """ Test pokemon learn_move returning None """
        self.assertReturnsNone(self._pikachu.learn_move(self._move),
                               method_name="Pokemon.learn_move")

    @skipIfNotDefinedUndergrads("Move")
    @skipIfNotDefinedUndergrads("Attack")
    def test_remaining_move_uses_learn_move(self):
        """ Test getting remaining move uses a pokemon after learning moves """
        move = self._create_move(max_uses=15)
        self._pikachu.learn_move(move)
        self.assertEqual(self._pikachu.get_remaining_move_uses(move), 15)
        move2 = self._create_move(max_uses=20)
        self._pikachu.learn_move(move2)
        self.assertEqual(self._pikachu.get_remaining_move_uses(move2), 20)

    @skipIfNotDefinedUndergrads("Move")
    @skipIfNotDefinedUndergrads("Attack")
    def test_get_move_info_learn_move(self):
        """ Test getting move info of a pokemon after learning moves """
        self.assertListEqual(self._pikachu.get_move_info(), [])
        move = self._create_move(max_uses=15)
        self._pikachu.learn_move(move)
        self.assertListEqual(self._pikachu.get_move_info(), [(move, 15)])
        move2 = self._create_move(max_uses=20)
        self._pikachu.learn_move(move2)
        self.assertListSimilar(self._pikachu.get_move_info(),
                               [(move, 15), (move2, 20)])

    @skipIfNotDefinedUndergrads("Move")
    @skipIfNotDefinedUndergrads("Attack")
    def test_get_move_info_sorted(self):
        """ Test getting move info in sorted order """
        move1 = self._create_move(name="A", max_uses=10)
        move2 = self._create_move(name="B", max_uses=15)
        move3 = self._create_move(name="C", max_uses=5)
        self._pikachu.learn_move(move3)
        self._pikachu.learn_move(move1)
        self._pikachu.learn_move(move2)
        self.assertListEqual(self._pikachu.get_move_info(),
                             [(move1, 10), (move2, 15), (move3, 5)])

    @skipIfNotDefinedUndergrads("Move")
    @skipIfNotDefinedUndergrads("Attack")
    def test_forget_move_move_info(self):
        """ Test forgetting a move with get_move_info """
        move1 = self._create_move()
        move2 = self._create_move()
        self._pikachu.learn_move(self._move)
        self.assertReturnsNone(self._pikachu.forget_move(self._move),
                               "Pokemon.forget_move")
        self.assertListEqual(self._pikachu.get_move_info(), [])

        self._pikachu.learn_move(move1)
        self._pikachu.learn_move(move2)
        self.assertReturnsNone(self._pikachu.forget_move(move1),
                               "Pokemon.forget_move")
        self.assertListEqual(self._pikachu.get_move_info(), [(move2, 10)])

    @skipIfNotDefinedUndergrads("Move")
    @skipIfNotDefinedUndergrads("Attack")
    def test_reduce_move_count_move_info(self):
        """ Test reducing Pokemon's move count with get_move_info """
        self._pikachu.learn_move(self._move)
        self._pikachu.reduce_move_count(self._move)
        self.assertListEqual(self._pikachu.get_move_info(), [(self._move, 9)])
        self._pikachu.reduce_move_count(self._move)
        self.assertListEqual(self._pikachu.get_move_info(), [(self._move, 8)])

    @skipIfNotDefinedUndergrads("Move")
    @skipIfNotDefinedUndergrads("Attack")
    def test_reduce_move_count_remaining_move_uses(self):
        """ Test reducing Pokemon's move count with get_remaining_move_uses """
        self._pikachu.learn_move(self._move)
        self._pikachu.reduce_move_count(self._move)
        self.assertEqual(self._pikachu.get_remaining_move_uses(self._move), 9)
        self._pikachu.reduce_move_count(self._move)
        self.assertEqual(self._pikachu.get_remaining_move_uses(self._move), 8)

    @skipIfNotDefinedUndergrads("PokemonStats")
    def test_get_stats_add_modifiers(self):
        """ Test adding a stat modifier to a pokemon """
        self._pikachu.add_stat_modifier((0.5, 5, 5, 5), 1)
        self.assertStats(self._pikachu.get_stats(), (1.5, 105, 205, 205))
        self._pikachu.add_stat_modifier((0.5, 5, 5, 5), 1)
        self.assertStats(self._pikachu.get_stats(), (2, 110, 210, 210))

    @skipIfNotDefinedUndergrads("PokemonStats")
    def test_get_stats_no_modifiers(self):
        """ Test getting stats with no modifiers """
        self.assertStats(self._pikachu.get_stats(), (1, 100, 200, 200))

    def test_add_modifier_reduce_health(self):
        """ Test adding a stat modifier results in reducing a pokemon's health """
        self._pikachu.add_stat_modifier((0.5, -5, 5, 5), 1)
        self.assertEqual(self._pikachu.get_health(), 95,
                         msg="Adding a negative health modifier might result "
                             "in reducing the pokemon's health.")
        self._pikachu.add_stat_modifier((0.5, 5, 5, 5), 1)
        self.assertEqual(self._pikachu.get_health(), 95)
        self.assertEqual(self._pikachu.get_max_health(), 100)

    @skipIfNotDefinedUndergrads("PokemonStats")
    def test_post_round_action(self):
        """ Test removing modifier after round """
        self._pikachu.add_stat_modifier((0.5, 5, 5, 5), 2)
        self.assertReturnsNone(self._pikachu.post_round_actions(),
                               "Pokemon.post_round_actions")
        self.assertStats(self._pikachu.get_stats(), (1.5, 105, 205, 205))
        self.assertReturnsNone(self._pikachu.post_round_actions(),
                               "Pokemon.post_round_actions")
        self.assertStats(self._pikachu.get_stats(), (1, 100, 200, 200))

    def test_rest_reset_health(self):
        """ Test resting resetting pokemon's health """
        self._pikachu.modify_health(-20)
        self.assertReturnsNone(self._pikachu.rest(),
                               "Pokemon.rest")
        self.assertEqual(self._pikachu.get_health(), 100)

    @skipIfNotDefinedUndergrads("Move")
    @skipIfNotDefinedUndergrads("Attack")
    def test_rest_reset_move_uses(self):
        """ Test resting resetting pokemon's move uses """
        move1 = self._create_move(max_uses=10)
        move2 = self._create_move(max_uses=11)
        move3 = self._create_move(max_uses=12)
        self._pikachu.learn_move(move1)
        self._pikachu.learn_move(move2)
        self._pikachu.learn_move(move3)
        for _ in range(random.randint(0, 3)):
            self._pikachu.reduce_move_count(move1)
            self._pikachu.reduce_move_count(move2)
        for _ in range(random.randint(1, 4)):
            self._pikachu.reduce_move_count(move2)
            self._pikachu.reduce_move_count(move3)
        self.assertReturnsNone(self._pikachu.rest(),
                               "Pokemon.rest")
        self.assertListSimilar(self._pikachu.get_move_info(),
                               [(move1, 10), (move2, 11), (move3, 12)])
        self.assertEqual(self._pikachu.get_remaining_move_uses(move1), 10)
        self.assertEqual(self._pikachu.get_remaining_move_uses(move2), 11)
        self.assertEqual(self._pikachu.get_remaining_move_uses(move3), 12)

    @skipIfNotDefinedUndergrads("Move")
    @skipIfNotDefinedUndergrads("Attack")
    @skipIfNotDefinedUndergrads("PokemonStats")
    def test_rest_reset_everything(self):
        """ Test resting pokemon resetting everything """
        self._pikachu.modify_health(-20)
        self._pikachu.add_stat_modifier((1, 10, 10, 10), 1)
        move1 = self._create_move(max_uses=10)
        self._pikachu.learn_move(move1)
        self._pikachu.reduce_move_count(move1)
        self.assertReturnsNone(self._pikachu.rest(),
                               "Pokemon.rest")
        self.assertEqual(self._pikachu.get_health(), 100)
        self.assertStats(self._pikachu.get_stats(), (1, 100, 200, 200))
        self.assertListEqual(self._pikachu.get_move_info(), [(move1, 10)])
        self.assertEqual(self._pikachu.get_remaining_move_uses(move1), 10)

    def test_str(self):
        """ Test pokemon string representation __str__ """
        self.assertEqual(str(self._pikachu), "Pikachu (lv1)")
        self._pikachu.level_up()
        self.assertEqual(str(self._pikachu), "Pikachu (lv2)")
        charizard = self.a2.Pokemon("Charizard", self._stats, "fire",
                                    [], 3)
        self.assertEqual(str(charizard), "Charizard (lv3)")


@skipIfNotDefinedUndergrads("Trainer")
class TestTrainer(TestFunctionality):
    def setUp(self) -> None:
        self._trainer = self.a2.Trainer("Ash")

    def test_get_name(self):
        """ Test getting trainer's name """
        self.assertEqual(self._trainer.get_name(), "Ash")

    def test_get_inventory_empty(self):
        """ Test getting trainer's inventory empty """
        self.assertDictEqual(self._trainer.get_inventory(), {})

    def test_get_current_pokemon_exception(self):
        """ Test get current pokemon raising an exception """
        self.assertRaises(self.a2_support.NoPokemonException,
                          self._trainer.get_current_pokemon)

    def test_get_all_pokemon_empty(self):
        """ Test get all pokemon returning an empty list """
        self.assertListEqual(self._trainer.get_all_pokemon(), [])

    @skipIfNotDefinedUndergrads("Pokemon")
    def test_get_all_pokemon(self):
        """ Test get all pokemon """
        pikachu = self._create_pokemon()
        snorlax = self._create_pokemon("Snorlax")
        self._trainer.add_pokemon(pikachu)
        self._trainer.add_pokemon(snorlax)
        self.assertListEqual(self._trainer.get_all_pokemon(),
                             [pikachu, snorlax])

    def test_rest_all_pokemon_empty(self):
        """ Test resting all pokemon if trainer doesn't have any pokemon """
        self.assertReturnsNone(self._trainer.rest_all_pokemon(),
                               "Trainer.rest_all_pokemon")

    @skipIfNotDefinedUndergrads("Pokemon")
    @skipIfNotDefinedUndergrads("PokemonStats")
    def test_rest_all_pokemon(self):
        """ Test rest all pokemon """
        pokemon_names = ["Pikachu", "Charizard", "Eevee", "Snorlax", "Mewtwo",
                         "Squirtle"]
        pokemons = []
        for name in pokemon_names:
            pokemons.append(self._create_pokemon(name))
        move1 = self._create_move(max_uses=10)

        for pokemon in pokemons:
            pokemon.modify_health(-20)
            pokemon.add_stat_modifier((1, 10, 10, 10), 1)
            pokemon.learn_move(move1)
            pokemon.reduce_move_count(move1)
            self._trainer.add_pokemon(pokemon)

        self.assertReturnsNone(self._trainer.rest_all_pokemon(),
                               "Trainer.rest_all_pokemon")

        for trainers_pokemon in self._trainer.get_all_pokemon():
            self.assertEqual(trainers_pokemon.get_health(), 100)
            self.assertStats(trainers_pokemon.get_stats(), (1, 100, 200, 200))
            self.assertListEqual(trainers_pokemon.get_move_info(),
                                 [(move1, 10)])
            self.assertEqual(trainers_pokemon.get_remaining_move_uses(move1),
                             10)

    @skipIfNotDefinedUndergrads("Pokemon")
    @skipIfNotDefinedUndergrads("PokemonStats")
    def test_all_pokemon_fainted_all_awake(self):
        """ Test if all pokemon have fainted with all pokemon awake """
        pikachu = self._create_pokemon()
        snorlax = self._create_pokemon("Snorlax")
        self._trainer.add_pokemon(pikachu)
        self._trainer.add_pokemon(snorlax)
        self.assertFalse(self._trainer.all_pokemon_fainted())

    @skipIfNotDefinedUndergrads("Pokemon")
    @skipIfNotDefinedUndergrads("PokemonStats")
    def test_not_all_pokemon_fainted(self):
        """ Test if all pokemon have fainted with all pokemon fainted """
        pikachu = self._create_pokemon()
        snorlax = self._create_pokemon("Snorlax")
        pikachu.modify_health(-100)
        snorlax.modify_health(-100)
        self._trainer.add_pokemon(pikachu)
        self._trainer.add_pokemon(snorlax)
        self.assertTrue(self._trainer.all_pokemon_fainted())

    @skipIfNotDefinedUndergrads("Pokemon")
    @skipIfNotDefinedUndergrads("PokemonStats")
    def test_can_add_pokemon_base(self):
        """ Test if trainer can add a pokemon in a regular case """
        pikachu = self._create_pokemon()
        snorlax = self._create_pokemon("Snorlax")
        self.assertTrue(self._trainer.can_add_pokemon(pikachu))
        self.assertTrue(self._trainer.can_add_pokemon(snorlax))

    @skipIfNotDefinedUndergrads("Pokemon")
    @skipIfNotDefinedUndergrads("PokemonStats")
    def test_can_add_pokemon_max_reached(self):
        """ Test if trainer can add a pokemon after the maximum number is reached"""
        for _ in range(6):
            pikachu = self._create_pokemon()
            self.assertTrue(self._trainer.can_add_pokemon(pikachu))
            self._trainer.add_pokemon(pikachu)
        pikachu = self._create_pokemon()
        self.assertFalse(self._trainer.can_add_pokemon(pikachu))

    @skipIfNotDefinedUndergrads("Pokemon")
    @skipIfNotDefinedUndergrads("PokemonStats")
    def test_add_pokemon(self):
        """ Test adding a pokemon to the trainer's roster """
        pikachu = self._create_pokemon()
        self.assertReturnsNone(self._trainer.add_pokemon(pikachu),
                               "Trainer.add_pokemon")
        self.assertListEqual(self._trainer.get_all_pokemon(), [pikachu])

    @skipIfNotDefinedUndergrads("Pokemon")
    @skipIfNotDefinedUndergrads("PokemonStats")
    def test_add_pokemon_current_pokemon(self):
        """ Test adding a first pokemon sets that pokemon to the current one"""
        pikachu = self._create_pokemon()
        self.assertReturnsNone(self._trainer.add_pokemon(pikachu),
                               "Trainer.add_pokemon")
        self.assertEqual(self._trainer.get_current_pokemon(), pikachu)

    @skipIfNotDefinedUndergrads("Pokemon")
    @skipIfNotDefinedUndergrads("PokemonStats")
    def test_can_switch_pokemon(self):
        """ Test if the trainer can switch pokemon in a regular scenario """
        pikachu = self._create_pokemon()
        snorlax = self._create_pokemon("Snorlax")
        self._trainer.add_pokemon(pikachu)
        self._trainer.add_pokemon(snorlax)
        self.assertTrue(self._trainer.can_switch_pokemon(1))

    @skipIfNotDefinedUndergrads("Pokemon")
    @skipIfNotDefinedUndergrads("PokemonStats")
    def test_can_switch_to_current_pokemon(self):
        """ Test if the trainer can switch to the current pokemon """
        pikachu = self._create_pokemon()
        snorlax = self._create_pokemon("Snorlax")
        self._trainer.add_pokemon(pikachu)
        self._trainer.add_pokemon(snorlax)
        self.assertFalse(self._trainer.can_switch_pokemon(0))

    @skipIfNotDefinedUndergrads("Pokemon")
    @skipIfNotDefinedUndergrads("PokemonStats")
    def test_can_switch_to_fainted(self):
        """ Test if the trainer can switch to a fainted pokemon """
        pikachu = self._create_pokemon()
        snorlax = self._create_pokemon("Snorlax")
        self._trainer.add_pokemon(pikachu)
        self._trainer.add_pokemon(snorlax)
        snorlax.modify_health(-100)
        self.assertFalse(self._trainer.can_switch_pokemon(1))

    @skipIfNotDefinedUndergrads("Pokemon")
    @skipIfNotDefinedUndergrads("PokemonStats")
    def test_switch_pokemon(self):
        """ Test switching pokemon """
        pikachu = self._create_pokemon()
        snorlax = self._create_pokemon("Snorlax")
        charmander = self._create_pokemon("Charmander")
        self._trainer.add_pokemon(pikachu)
        self._trainer.add_pokemon(snorlax)
        self._trainer.add_pokemon(charmander)
        self._trainer.switch_pokemon(1)
        self.assertEqual(self._trainer.get_current_pokemon(), snorlax)
        self._trainer.switch_pokemon(2)
        self.assertEqual(self._trainer.get_current_pokemon(), charmander)
        self._trainer.switch_pokemon(0)
        self.assertEqual(self._trainer.get_current_pokemon(), pikachu)

    @skipIfNotDefinedUndergrads("Pokeball")
    @skipIfNotDefinedUndergrads("Food")
    def test_add_item(self):
        """ Test adding a new item to inventory """
        food = self._create_food()
        pokeball = self._create_pokeball()
        self.assertReturnsNone(self._trainer.add_item(food, 2),
                               "Trainer.add_item")
        self.assertDictEqual(self._trainer.get_inventory(), {food: 2})
        self.assertReturnsNone(self._trainer.add_item(pokeball, 5),
                               "Trainer.add_item")
        self.assertDictEqual(self._trainer.get_inventory(),
                             {food: 2, pokeball: 5})

    @skipIfNotDefinedUndergrads("Food")
    @skipIfNotDefinedUndergrads("Pokeball")
    def test_has_item(self):
        """ Test checking if the trainer has an item """
        food = self._create_food()
        pokeball = self._create_pokeball()
        self.assertFalse(self._trainer.has_item(food))
        self._trainer.add_item(food, 2)
        self.assertTrue(self._trainer.has_item(food))
        self.assertFalse(self._trainer.has_item(pokeball))

    def test_str(self):
        """ Test string representation of a trainer __str__ """
        another = self.a2.Trainer("Another")
        self.assertEqual(str(self._trainer), "Trainer('Ash')")
        self.assertEqual(str(another), "Trainer('Another')")


@skipIfNotDefinedUndergrads("Battle")
@skipIfNotDefinedUndergrads("Trainer")
@skipIfNotDefinedUndergrads("Pokemon")
class TestBattle(TestFunctionality):
    def setUp(self) -> None:
        self._player = self.a2.Trainer("Ash")
        self._enemy = self.a2.Trainer("Comp")
        self._players_pokemon = self._create_pokemon()
        self._enemy_pokemon = self._create_pokemon()
        self._player.add_pokemon(self._players_pokemon)
        self._enemy.add_pokemon(self._enemy_pokemon)
        self._enemy.add_pokemon(self._create_pokemon())
        self._battle = self.a2.Battle(self._player, self._enemy, True)

    def test_get_trainer(self):
        """ Test getting the trainers """
        self.assertEqual(self._battle.get_trainer(True), self._player)
        self.assertEqual(self._battle.get_trainer(False), self._enemy)

    def test_attempt_end_early_non_player_battle(self):
        """ Test attempt end early in a non trainer battle """
        battle = self.a2.Battle(self._player, self._enemy, False)
        self.assertReturnsNone(battle.attempt_end_early(),
                               "Battle.attempt_end_early")
        self.assertTrue(battle.is_over())

    def test_attempt_end_early_battle_already_over(self):
        """ Test attempt end early when battle already over for trainer battle """
        self._players_pokemon.modify_health(-100)
        self.assertReturnsNone(self._battle.attempt_end_early(),
                               "Battle.attempt_end_early")
        self.assertTrue(self._battle.is_over())

    def test_attempt_end_early_non_trainer_battle_already_over(self):
        """ Test attempt end early when battle already over for non-trainer battle """
        battle = self.a2.Battle(self._player, self._enemy, False)
        battle.get_trainer(True).get_current_pokemon().modify_health(-100)
        self.assertReturnsNone(self._battle.attempt_end_early(),
                               "Battle.attempt_end_early")
        self.assertTrue(self._battle.is_over())

    def test_is_trainer_battle(self):
        """ Test checking if battle is a trainer battle """
        self.assertTrue(self._battle.is_trainer_battle())
        battle = self.a2.Battle(self._player, self._enemy, False)
        self.assertFalse(battle.is_trainer_battle())

    @skipIfNotDefinedUndergrads("Flee")
    def test_is_action_queue_full(self):
        """ Test checking if action queue is full """
        self.assertFalse(self._battle.is_action_queue_full())
        self._battle.queue_action(self._create_action(), True)
        self._battle.queue_action(self._create_action(), False)
        self.assertTrue(self._battle.is_action_queue_full())

    @skipIfNotDefinedUndergrads("Flee")
    def test_is_action_queue_empty(self):
        """ Test checking if action queue is empty """
        self.assertTrue(self._battle.is_action_queue_empty())
        self._battle.queue_action(self._create_action(), True)
        self.assertFalse(self._battle.is_action_queue_empty())

    @skipIfNotDefinedUndergrads("Flee")
    def test_trainer_has_action_queued(self):
        """ Test checking if trainer has an action queued """
        self.assertFalse(self._battle.trainer_has_action_queued(True))
        self.assertFalse(self._battle.trainer_has_action_queued(False))
        self._battle.queue_action(self._create_action(), True)
        self.assertTrue(self._battle.trainer_has_action_queued(True))
        self.assertFalse(self._battle.trainer_has_action_queued(False))
        self._battle.queue_action(self._create_action(), False)
        self.assertTrue(self._battle.trainer_has_action_queued(True))
        self.assertTrue(self._battle.trainer_has_action_queued(False))

    @skipIfNotDefinedUndergrads("Flee")
    def test_is_ready_queue_full(self):
        """ Test if battle is ready based on if the queue is full """
        self.assertFalse(self._battle.is_ready())
        self._battle.queue_action(self._create_action(), True)
        self.assertFalse(self._battle.is_ready())
        self._battle.queue_action(self._create_action(), False)
        self.assertTrue(self._battle.is_ready())

    @skipIfNotDefinedUndergrads("Flee")
    def test_is_ready_action_performed(self):
        """ Test if battle is ready based on an action is already performed """
        self._battle.queue_action(self._create_action(), True)
        self._battle.queue_action(self._create_action(), False)
        self._battle.enact_turn()
        self.assertTrue(self._battle.is_ready())
        self._battle.enact_turn()
        self.assertFalse(self._battle.is_ready())

    @skipIfNotDefinedUndergrads("Flee")
    def test_attempt_queue_action_player_already_queued(self):
        """ Test queueing an action from a player that's already queued """
        self.assertReturnsNone(self._battle.queue_action(self._create_action(),
                                                         True),
                               "Battle.queue_action")
        self.assertReturnsNone(self._battle.queue_action(self._create_action(),
                                                         True),
                               "Battle.queue_action")
        self.assertFalse(self._battle.is_action_queue_full())
        self.assertFalse(self._battle.is_action_queue_empty())
        self.assertFalse(self._battle.is_ready())
        self.assertTrue(self._battle.trainer_has_action_queued(True))
        self.assertFalse(self._battle.trainer_has_action_queued(False))

    @skipIfNotDefinedUndergrads("ActionSummary")
    @skipIfNotDefinedUndergrads("Flee")
    def test_attempt_queue_action_queue_ready(self):
        """ Test queueing an action when the queue is ready but not full """
        self.assertReturnsNone(self._battle.queue_action(self._create_action(),
                                                         True),
                               "Battle.queue_action")
        self.assertReturnsNone(self._battle.queue_action(self._create_action(),
                                                         False),
                               "Battle.queue_action")
        self._battle.enact_turn()
        self.assertReturnsNone(self._battle.queue_action(self._create_action(),
                                                         True),
                               "Battle.queue_action")
        self.assertFalse(self._battle.trainer_has_action_queued(True))
        self.assertFalse(self._battle.is_action_queue_full())

    @skipIfNotDefinedUndergrads("Flee")
    @skipIfNotDefinedUndergrads("ActionSummary")
    def test_enact_turn(self):
        """ Test enacting a turn """
        self.assertReturnsNone(self._battle.queue_action(self._create_action(),
                                                         True),
                               "Battle.queue_action")
        self.assertReturnsNone(self._battle.queue_action(self._create_action(),
                                                         False),
                               "Battle.queue_action")
        self.assertEqual(self._battle.enact_turn().get_messages(),
                         ["Unable to escape a trainer battle."])

    @skipIfNotDefinedUndergrads("Pokemon")
    def test_is_over_regular(self):
        """ Test if battle is over """
        self.assertFalse(self._battle.is_over())
        self._players_pokemon.modify_health(-100)
        self.assertTrue(self._battle.is_over())


@skipIfNotDefinedUndergrads("ActionSummary")
class TestActionSummary(TestFunctionality):
    def setUp(self) -> None:
        self._action_summary1 = self.a2.ActionSummary("msg1")
        self._action_summary2 = self.a2.ActionSummary("msg2")
        self._action_summary_none = self.a2.ActionSummary()

    def test_get_messages_empty(self):
        """ Test empty get_messages """
        self.assertListEqual(self._action_summary_none.get_messages(), [])

    def test_add_message_simple(self):
        """ Test adding a message """
        self._action_summary_none.add_message("test")
        self.assertListEqual(self._action_summary_none.get_messages(), ["test"])

    def test_combine_simple(self):
        """ Test combining 2 ActionSummary's """
        self._action_summary1.combine(self._action_summary2)
        self.assertListEqual(["msg1", "msg2"],
                             self._action_summary1.get_messages())
        self.assertListEqual(["msg2"],
                             self._action_summary2.get_messages())

    def test_combine_empty(self):
        """ Test combining an ActionSummary with an empty ActionSummary """
        self._action_summary1.combine(self._action_summary_none)
        self.assertListEqual(self._action_summary1.get_messages(), ["msg1"])


class _TestActionBase(TestFunctionality):
    def setUp(self) -> None:
        self._player = self.a2.Trainer("Ash")
        self._enemy = self.a2.Trainer("Hsa")
        self._players_pokemon = self._create_pokemon("Squirtle")
        self._enemy_pokemon = self._create_pokemon("Eevee")
        self._player.add_pokemon(self._players_pokemon)
        self._enemy.add_pokemon(self._enemy_pokemon)
        self._battle = self.a2.Battle(self._player, self._enemy, True)
        self._non_trainer_battle = self.a2.Battle(self._player, self._enemy,
                                                  False)
        self._action: Action = ...
        self._str: str = ...

    def test_is_valid_game_over_trainer_battle(self):
        """ Test valid action on game over for a trainer battle """
        self.assertTrue(self._action.is_valid(self._battle, True))
        for pokemon in self._player.get_all_pokemon():
            pokemon.modify_health(-10)
        self.assertTrue(self._action.is_valid(self._battle, True))
        for pokemon in self._player.get_all_pokemon():
            pokemon.modify_health(-90)
        self.assertFalse(self._action.is_valid(self._battle, True))

    def test_is_valid_beginning_of_battle(self):
        """ Test valid action when it's both player's turn """
        self.assertTrue(self._action.is_valid(self._non_trainer_battle, True))
        self.assertTrue(self._action.is_valid(self._non_trainer_battle, False))

    def test_str(self):
        """ Test string representation __str__ """
        self.assertEqual(str(self._action), self._str)


class TestAction(TestFunctionality):
    def test_apply(self):
        """ Test apply raises a NotImplementedError """
        player = self.a2.Trainer("Ash")
        enemy = self.a2.Trainer("Hsa")
        battle = self.a2.Battle(player, enemy, True)
        try:
            action = self.a2.Action()
            action.apply(battle, True)
            self.fail("Action.apply should raise a NotImplementedError")
        except NotImplementedError:
            pass


@skipIfNotDefinedUndergrads("Flee")
class TestFlee(_TestActionBase):
    def setUp(self) -> None:
        super().setUp()
        self._action = self.a2.Flee()
        self._str = "Flee()"

    def test_is_valid_fainted(self):
        """ Test if fleeing is valid when a pokemon fainted """
        self.assertTrue(self._action.is_valid(self._battle, True))
        self._players_pokemon.modify_health(-100)
        self.assertFalse(self._action.is_valid(self._battle, True))

    def test_apply(self):
        """ Test applying fleeing a battle """
        self.assertListEqual(self._action.apply(self._non_trainer_battle,
                                                is_player=True).get_messages(),
                             ["Got away safely!"])
        self.assertTrue(self._non_trainer_battle.is_over())

    def test_apply_trainer_battle(self):
        """ Test applying fleeing a trainer battle """
        self.assertListEqual(
            self._action.apply(self._battle, is_player=True).get_messages(),
            ["Unable to escape a trainer battle."])
        self.assertFalse(self._battle.is_over())


@skipIfNotDefinedUndergrads("SwitchPokemon")
class TestSwitchPokemon(_TestActionBase):
    def setUp(self) -> None:
        super().setUp()
        self._enemy_pokemon2 = self._create_pokemon("Mewtwo")
        self._enemy.add_pokemon(self._enemy_pokemon2)
        self._players_pokemon2 = self._create_pokemon("Charizard")
        self._player.add_pokemon(self._players_pokemon2)
        self._action = self.a2.SwitchPokemon(1)
        self._str = "SwitchPokemon(1)"

    def test_switch_to_fainted_pokemon(self):
        """ Test if player can switch to a fainted pokemon """
        self._players_pokemon2.modify_health(-100)
        self.assertFalse(self._action.is_valid(self._battle, True))

    def test_apply_pokemon_return(self):
        """ Test trainer getting their pokemon to return """
        self.assertListEqual(
            self._action.apply(self._battle, True).get_messages(),
            ["Squirtle, return!", "Ash switched to Charizard."]
        )
        self.assertEqual(self._player.get_current_pokemon(),
                         self._players_pokemon2)

    def test_apply_pokemon_fainted(self):
        """ Test trainer retracting a fainted pokemon """
        self._players_pokemon.modify_health(-100)
        self.assertListEqual(
            self._action.apply(self._battle, True).get_messages(),
            ["Ash switched to Charizard."]
        )
        self.assertEqual(self._player.get_current_pokemon(),
                         self._players_pokemon2)


class _TestItemBase(_TestActionBase):
    def setUp(self) -> None:
        super().setUp()
        self._set_up_items()
        self._player.add_item(self._action, 10)
        self._enemy.add_item(self._action, 10)

    def _set_up_items(self):
        self._name: str = ...
        self._action: Item = ...

    def test_decrement_item_count(self):
        """ Test decrementing item count """
        for i in range(10):
            self.assertTrue(self._player.has_item(self._action))
            self._action.decrement_item_count(self._player)
        self.assertFalse(self._player.has_item(self._action))

    def test_get_name(self):
        """ Test getting item's name """
        self.assertEqual(self._action.get_name(), self._name)


@skipIfNotDefinedUndergrads("Pokeball")
class TestPokeball(_TestItemBase):
    def setUp(self) -> None:
        super().setUp()
        self._str = "Pokeball('Great Ball')"

    def _set_up_items(self):
        self._name = "Great Ball"
        self._action = self.a2.Pokeball(self._name, 1)

    def test_apply_in_trainer_battle(self):
        """ Test applying a pokeball in a trainer battle """
        self.assertListEqual(
            self._action.apply(self._battle, True).get_messages(),
            ["Pokeballs have no effect in trainer battles."])
        self.assertFalse(self._battle.is_over())

    def test_apply_success(self):
        """ Test successfully catching a wild pokemon """
        self.assertListEqual(
            self._action.apply(self._non_trainer_battle, True).get_messages(),
            ["Eevee was caught!"])
        self.assertListEqual(self._player.get_all_pokemon(),
                             [self._players_pokemon, self._enemy_pokemon])
        self.assertTrue(self._non_trainer_battle.is_over())

    def test_apply_failure(self):
        """ Test failing to catch a pokemon """
        action = self.a2.Pokeball("Bad ball", 0)
        self.assertListEqual(
            action.apply(self._non_trainer_battle, True).get_messages(),
            ["It was so close, but Eevee escaped!"])
        self.assertListEqual(self._player.get_all_pokemon(),
                             [self._players_pokemon])
        self.assertFalse(self._non_trainer_battle.is_over())


@skipIfNotDefinedUndergrads("Food")
class TestFood(_TestItemBase):
    def setUp(self) -> None:
        super().setUp()
        self._str = "Food('Bad Soup')"

    def _set_up_items(self):
        self._name = "Bad Soup"
        self._action = self.a2.Food(self._name, 22)

    def test_apply(self):
        """ Test eating food """
        self._players_pokemon.modify_health(-50)
        self.assertListEqual(
            self._action.apply(self._battle, True).get_messages(),
            ["Squirtle ate Bad Soup."]
        )
        self.assertEqual(self._players_pokemon.get_health(), 72)


class _TestMoveBase(_TestActionBase):
    def setUp(self) -> None:
        super().setUp()
        self._set_up_move_attr()
        self._set_up_move()
        self._action: Move = self._move_cls(self._name, self._type,
                                            self._max_uses, self._speed,
                                            *self._move_args)
        self._players_pokemon.learn_move(self._action)
        self._enemy_pokemon.learn_move(self._action)

    def _set_up_move(self):
        self._move_cls: type = ...
        self._move_args: List = ...

    def _set_up_move_attr(self):
        self._name: str = "Aqua Jet"
        self._type: str = "normal"
        self._max_uses: int = 10
        self._speed: int = 10

    def test_get_name(self):
        """ Test getting move's name """
        self.assertEqual(self._action.get_name(), self._name)

    def test_get_element_type(self):
        """ Test getting move's element type """
        self.assertEqual(self._action.get_element_type(), self._type)

    def test_get_max_uses(self):
        """ Test getting move's max uses """
        self.assertEqual(self._action.get_max_uses(), self._max_uses)

    def test_get_priority(self):
        """ Test getting move's priority """
        self.assertEqual(self._action.get_priority(),
                         self._max_uses + 1)

    def test_is_valid_move_not_learnt(self):
        """ Test if move is valid if it hasn't been learnt """
        attack = self._create_move()
        self.assertFalse(attack.is_valid(self._battle, True))


@skipIfNotDefinedUndergrads("Attack")
class TestAttack(_TestMoveBase):
    def setUp(self) -> None:
        self._action: Attack = ...
        super().setUp()
        self._str = "Attack('Aqua Jet', 'normal', 10)"

    def _set_up_move(self):
        self._move_cls = self.a2.Attack
        self._hit_chance = 1
        self._base_damage = 40
        self._move_args = [self._base_damage, self._hit_chance]

    def test_apply_hit(self):
        """ Test if an attack hits the pokemon """
        messages = self._action.apply(self._battle, True).get_messages()
        first, *rest = messages
        self.assertEqual(first, "Squirtle used Aqua Jet.")
        self.assertListSimilar(rest, [])
        self.assertEqual(self._enemy_pokemon.get_health(), 61)

    def test_apply_kills(self):
        """ Test if an attack kills the pokemon """
        self._enemy_pokemon.modify_health(-99)
        messages = self._action.apply(self._battle, True).get_messages()
        first, *rest = messages
        self.assertEqual(first, "Squirtle used Aqua Jet.")
        self.assertListEqual(rest, ["Eevee has fainted.",
                                    "Squirtle gained 28 exp."])
        self.assertEqual(self._enemy_pokemon.get_health(), 0)
        self.assertTrue(self._enemy_pokemon.has_fainted())

    def test_apply_with_type_effectiveness(self):
        """ Test applying an attack with type effectiveness """
        effectiveness = self.a2_support.ElementType("normal")
        effectiveness.add_type_effectiveness("electric", 2)
        messages = self._action.apply(self._battle, True).get_messages()
        self.assertListEqual(messages, ["Squirtle used Aqua Jet."])
        self.assertEqual(self._enemy_pokemon.get_health(), 21)

    def test_did_hit(self):
        """ Test did_hit based on different hit chances """
        self.assertTrue(self._action.did_hit(self._players_pokemon))
        self._players_pokemon.add_stat_modifier((-1, 0, 0, 0), 1)
        self.assertFalse(self._action.did_hit(self._players_pokemon))
        missed_attack = self.a2.Attack("Water Gun", "water", 1, 1, 20, 0)
        self.assertFalse(missed_attack.did_hit(self._enemy_pokemon))
        self._enemy_pokemon.add_stat_modifier((-0.5, 0, 0, 0), 1)
        hits = 0
        misses = 0
        for _ in range(10000):
            if self._action.did_hit(self._enemy_pokemon):
                hits += 1
            else:
                misses += 1
        self.assertAlmostEqual(hits / misses, 1, delta=0.05)

    def test_calculate_damage(self):
        """ Test calculating attack damage with semi-random parameters """
        attack = self.a2.Attack("Water Gun", "water", 1, 1, 42, 1)
        effectiveness = self.a2_support.ElementType("water")
        effectiveness.add_type_effectiveness("electric", 1.337)
        self._players_pokemon.add_stat_modifier((0, 0, 69, 0), 1)
        self._enemy_pokemon.add_stat_modifier((0, 0, 0, 420), 1)
        self.assertEqual(
            attack.calculate_damage(self._players_pokemon, self._enemy_pokemon),
            24
        )


class _TestStatusModifierBase(_TestMoveBase):
    def _set_up_move_attr(self):
        super()._set_up_move_attr()
        self._name: str = "(De)Buff"

    def _set_up_move(self):
        self._move_args = [(0.12, 34, 56, 78), 3]


@skipIfNotDefinedUndergrads("Buff")
class TestBuff(_TestStatusModifierBase):
    def setUp(self) -> None:
        super().setUp()
        self._str = "Buff('(De)Buff', 'normal', 10)"

    def _set_up_move(self):
        super()._set_up_move()
        self._move_cls = self.a2.Buff


@skipIfNotDefinedUndergrads("Debuff")
class TestDebuff(_TestStatusModifierBase):
    def setUp(self) -> None:
        super().setUp()
        self._str = "Debuff('(De)Buff', 'normal', 10)"

    def _set_up_move(self):
        super()._set_up_move()
        self._move_cls = self.a2.Debuff
        self._move_args = [(-0.12, -34, -56, -78), 3]


class _TestStrategyBase(TestFunctionality):
    def setUp(self) -> None:
        self._player = self.a2.Trainer("Ash")
        self._enemy = self.a2.Trainer("Hsa")
        self._squirtle = self._create_pokemon("Squirtle")
        self._pikachu = self._create_pokemon()
        self._charizard = self._create_pokemon("Charizard")
        self._snorlax = self._create_pokemon("Snorlax")
        self._enemy_pokemon = self._create_pokemon("Eevee")
        self._player.add_pokemon(self._squirtle)
        self._player.add_pokemon(self._pikachu)
        self._player.add_pokemon(self._charizard)
        self._player.add_pokemon(self._snorlax)
        self._enemy.add_pokemon(self._enemy_pokemon)
        self._battle = self.a2.Battle(self._player, self._enemy, True)
        self._wild_battle = self.a2.Battle(self._player, self._enemy, False)
        self._strategy: Strategy = ...

    def test_get_next_action_switch(self):
        """ Test getting switch action """
        self._squirtle.modify_health(-100)
        action = self._strategy.get_next_action(self._battle, True)
        self.assertIsInstance(action, self.a2.SwitchPokemon)
        action.apply(self._battle, True)
        self.assertIs(self._player.get_current_pokemon(), self._pikachu)


@skipIfNotDefinedPostgrads("ScaredyCat")
class TestScaredyCat(_TestStrategyBase):
    def setUp(self) -> None:
        super().setUp()
        self._strategy = self.a2.ScaredyCat()

    def test_get_next_action_flee(self):
        """ Test getting flee action """
        self.assertIsInstance(
            self._strategy.get_next_action(self._battle, True),
            self.a2.Flee
        )


@skipIfNotDefinedPostgrads("TeamRocket")
class TestTeamRocket(_TestStrategyBase):
    def setUp(self) -> None:
        super().setUp()
        self._strategy = self.a2.TeamRocket()
        self._attack_electric = self.a2.Attack("Fusion Bolt", "electric", 1,
                                               1, 20, 1)
        self._attack_water = self.a2.Attack("Hydro Cannon", "water",
                                            1, 1, 20, 1)
        self._attack_fire = self.a2.Attack("Blast Burn", "fire", 1, 1, 20, 1)
        self._attack_ground = self.a2.Attack("Stomping Tantrum", "ground",
                                             1, 1, 20, 1)
        self._attack_normal = self.a2.Attack("Skull Bash", "normal",
                                             1, 1, 20, 1)
        self._squirtle.learn_move(self._attack_fire)
        self._squirtle.learn_move(self._attack_ground)
        self._squirtle.learn_move(self._attack_water)
        self._pikachu.learn_move(self._attack_electric)
        self._pikachu.learn_move(self._attack_normal)

    def test_flee_wild_battle(self):
        """ Test fleeing a wild battle """
        action = self._strategy.get_next_action(self._wild_battle, True)
        self.assertIsInstance(action, self.a2.Flee)

    def test_catching_pikachu(self):
        """ Test trying to catch a pikachu """
        pikachu = self._create_pokemon("Pikachu")
        self._enemy.add_pokemon(pikachu)
        self._enemy.switch_pokemon(1)
        pokeball = self.a2.Pokeball("Great Ball", 1)
        self._player.add_item(pokeball, 2)
        action = self._strategy.get_next_action(self._battle, True)
        self.assertIs(action, pokeball)

    def test_using_type_effectiveness(self):
        """ Test getting the most type effective move """
        element_type = self.a2_support.ElementType("ground")
        element_type.add_type_effectiveness("electric", 2)
        action = self._strategy.get_next_action(self._battle, True)
        self.assertIs(action, self._attack_ground)

    def test_using_available_moves(self):
        """ Test using available moves only """
        self._squirtle.reduce_move_count(self._attack_ground)
        self._squirtle.reduce_move_count(self._attack_fire)
        action = self._strategy.get_next_action(self._battle, True)
        self.assertIs(action, self._attack_water)

    def test_flee_no_moves(self):
        """ Test fleeing when no moves is available """
        self._squirtle.reduce_move_count(self._attack_ground)
        self._squirtle.reduce_move_count(self._attack_fire)
        self._squirtle.reduce_move_count(self._attack_water)
        action = self._strategy.get_next_action(self._battle, True)
        self.assertIsInstance(action, self.a2.Flee)


@skipIfNotDefinedPostgrads("create_encounter")
class TestCreateEncounter(TestFunctionality):
    def setUp(self) -> None:
        self._wild_pokemon = self._create_pokemon("Mewtwo")
        self._player = self.a2.Trainer("Goku")

    def test_create_encounter(self):
        """ Test creating a new encounter """
        battle = self.a2.create_encounter(self._player, self._wild_pokemon)
        self.assertIs(battle.get_trainer(True), self._player)
        self.assertListEqual(battle.get_trainer(False).get_all_pokemon(),
                             [self._wild_pokemon])
        self.assertTrue(battle.is_action_queue_empty())


def main():
    """ run tests """
    test_cases = [
        TestDesignUndergrads,
        TestDesignPostgrads,
        TestPokemonStats,
        TestPokemon,
        TestTrainer,
        TestBattle,
        TestActionSummary,
        TestAction,
        TestFlee,
        TestSwitchPokemon,
        TestPokeball,
        TestFood,
        TestAttack,
        TestBuff,
        TestDebuff,
        TestScaredyCat,
        TestTeamRocket,
        TestCreateEncounter,
    ]
    master = TestMaster(max_diff=None,
                        suppress_stdout=True,
                        timeout=1,
                        include_no_print=True,
                        scripts=[
                            ("a2", "a2.py"),
                            ("a2_support", "a2_support.py")
                        ])
    master.run(test_cases)


if __name__ == "__main__":
    main()
