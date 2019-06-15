import time


class GameRefresher:
    FRAME_LENGTH_SECONDS = 0.03

    def __init__(self, player):
        self.player = player
        self.last_frame_time = time.time()

    def refresh_game_state(self, game_state):
        if time.time() - self.last_frame_time > self.FRAME_LENGTH_SECONDS:
            self.last_frame_time += self.FRAME_LENGTH_SECONDS
            move_type = self.player.get_move(game_state)
            return game_state.with_move(move_type)
        return game_state
