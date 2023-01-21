from dataclasses import dataclass, field

import pytest

from stone.bootstrap import bootstrap
from stone.domain import commands, events, model
from stone.domain.model import BattleField, Minion, Player


def test_minion_melee_attack_player_with_damage_1_decrease_1_life(
    battle_field, message_bus
):
    pl1, pl2 = battle_field.players.values()
    min1 = pl1.minion_field[0]
    melee_attack = commands.MeleeAttack(
        source=min1.uuid, target=pl2.uuid, attack=min1.attack
    )
    message_bus.handle(melee_attack)
    assert pl2.life == 29
    assert min1.life == 100


def test_player_ranged_attack_minon_with_damage_50_decrease_50_life(
    battle_field, message_bus
):
    """
    given
        2 player with 1 minion each
    when
        pl2 attack pl1's minion
    then
        minion1 life decrease
        player1 life stay
    """
    pl1, pl2 = battle_field.players.values()
    min1 = pl1.minion_field[0]
    ranged_attack = commands.RangedAttack(
        source=pl2.uuid, target=min1.uuid, attack=50
    )
    message_bus.handle(ranged_attack)
    assert min1.life == 50
    assert pl2.life == 30


def test_display_console_minion_attack_other_minion(
    battle_field, message_bus, capsys
):
    """
    given
        2 player with 1 minion each
    when
        pl1 minion attack pl2 minion
    then
        display 2 message will show up
    """
    pl1, pl2 = battle_field.players.values()
    min1 = pl1.minion_field[0]
    min2 = pl2.minion_field[0]
    melee_attack = commands.MeleeAttack(
        source=min1.uuid, target=min2.uuid, attack=min1.attack
    )
    message_bus.handle(melee_attack)
    captured = capsys.readouterr()
    assert (
        f"""{min1.name}{min1.uuid[:5]} damaged {min2.name}{min2.uuid[:5]} by {min1.attack:3}\n{min2.name}{min2.uuid[:5]} damaged {min1.name}{min1.uuid[:5]} by {min2.attack:3}\n"""
        == captured.out
    )


def test_spell_damage_minion_using_mana(
    battle_field, message_bus, spell_with_attack_3
):
    """
    given
        2 player with 1 minion each
    when
        pl1 use spell on pl2 minion
    then
        pl2 minion life decrease by spell attack
    :return:
    """
    pl1, pl2 = battle_field.players.values()
    min1 = pl2.minion_field[0]

    spell = spell_with_attack_3

    command = commands.UseSpell(
        spell=spell.uuid,
        source=pl1.uuid,
        target=min1.uuid,
        attack=spell.attack,
    )

    message_bus.handle(command)
    assert min1.life == 97


# def test_spell_fail_with_not_enough_mana():
#     """
#     given
#         2 player with 1 minion each
#     when
#         pl1 use spell to pl2 minion with not enough mana
#     then
#         pl1 fail to spell
#         and display "NOT ENOUGH MANA"
#     :return:
#     """
#     ...
