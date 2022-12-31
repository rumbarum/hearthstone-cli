from stone.domain.command import Attack
from stone.domain.model import BattleField


def handle_attack(comm: Attack, field: BattleField):
    target = field.get_player_by_uuid(comm.target)
    target.life -= comm.attack


def handle_message(field: BattleField):
    while slot := field.message_slot:
        message = slot.popleft()
        if isinstance(message, Attack):
            handle_attack(message, field)
            continue
