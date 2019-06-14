class GameLostState:

    def __init__(self, board, car_state, board_progress):
        self.board = board
        self.prev_car_state = self.car_state = car_state
        self.board_progress = board_progress

    def with_move(self, _game_move_type):
        return self

