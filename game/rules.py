
def is_valid_direction(direction):
    return direction in {"UP", "DOWN", "LEFT", "RIGHT"}

def validate_move(start_pos, direction, steps, board_size):
    x, y = start_pos
    if direction == "UP":
        x -= steps
    elif direction == "DOWN":
        x += steps
    elif direction == "LEFT":
        y -= steps
    elif direction == "RIGHT":
        y += steps
    else:
        return False

    # Check if new position is within bounds
    if 0 <= x < board_size and 0 <= y < board_size:
        return True
    return False

def can_enter_room(position, room_positions):
    # If player's position matches a room entry point
    return position in room_positions

def use_secret_passage(current_room, board):
    return board.get_secret_passage(current_room)
