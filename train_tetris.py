import gymnasium as gymnasium
from gymnasium import spaces
import numpy as np
import random
import torch
from stable_baselines3 import PPO

# Constants
GRID_WIDTH = 10
GRID_HEIGHT = 20

SHAPES = [
    [[1, 1, 1, 1]],          # I
    [[1, 1, 1], [0, 1, 0]],  # T
    [[1, 1, 1], [1, 0, 0]],  # L
    [[1, 1, 1], [0, 0, 1]],  # J
    [[1, 1], [1, 1]],        # O
    [[0, 1, 1], [1, 1, 0]],  # S
    [[1, 1, 0], [0, 1, 1]]   # Z
]

class TetrisEnv(gymnasium.Env):
    metadata = {"render_modes": []}

    def __init__(self):
        super(TetrisEnv, self).__init__()
        # Actions: 0: Left, 1: Right, 2: Rotate, 3: Down
        self.action_space = spaces.Discrete(4)
        
        # Observation space: The 10x20 grid (0 for empty, 1 for filled)
        self.observation_space = spaces.Box(
            low=0, high=1, shape=(GRID_HEIGHT, GRID_WIDTH), dtype=np.float32
        )
        
        self.reset()

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        self.grid = np.zeros((GRID_HEIGHT, GRID_WIDTH), dtype=np.float32)
        self.score = 0
        self.lines_cleared_total = 0
        self._new_piece()
        return self.grid, {}

    def _new_piece(self):
        self.current_shape = random.choice(SHAPES)
        self.piece_x = GRID_WIDTH // 2 - len(self.current_shape[0]) // 2
        self.piece_y = 0
        self.game_over = self._check_collision(self.current_shape, self.piece_x, self.piece_y)

    def _check_collision(self, shape, offset_x, offset_y):
        for y, row in enumerate(shape):
            for x, cell in enumerate(row):
                if cell:
                    nx, ny = offset_x + x, offset_y + y
                    if nx < 0 or nx >= GRID_WIDTH or ny >= GRID_HEIGHT:
                        return True
                    if ny >= 0 and self.grid[ny][nx] == 1:
                        return True
        return False

    def _lock_piece(self):
        for y, row in enumerate(self.current_shape):
            for x, cell in enumerate(row):
                if cell:
                    ny, nx = self.piece_y + y, self.piece_x + x
                    if 0 <= ny < GRID_HEIGHT and 0 <= nx < GRID_WIDTH:
                        self.grid[ny][nx] = 1

        # Clear lines
        lines_to_clear = []
        for r in range(GRID_HEIGHT):
            if np.all(self.grid[r] == 1):
                lines_to_clear.append(r)
        
        num_cleared = len(lines_to_clear)
        if num_cleared > 0:
            self.grid = np.delete(self.grid, lines_to_clear, axis=0)
            new_rows = np.zeros((num_cleared, GRID_WIDTH), dtype=np.float32)
            self.grid = np.vstack([new_rows, self.grid])
            self.lines_cleared_total += num_cleared
            reward = num_cleared * 100
        else:
            reward = 1.0  # Small survival reward

        self.score += reward
        self._new_piece()
        return reward

    def step(self, action):
        if self.game_over:
            return self.grid, -100.0, True, False, {}

        reward = 0.1
        nx, ny = self.piece_x, self.piece_y
        next_shape = self.current_shape

        if action == 0:  # Left
            nx -= 1
        elif action == 1:  # Right
            nx += 1
        elif action == 2:  # Rotate
            next_shape = [list(row) for row in zip(*self.current_shape[::-1])]
        elif action == 3:  # Drop faster
            ny += 1

        if not self._check_collision(next_shape, nx, ny):
            self.piece_x, self.piece_y = nx, ny
            self.current_shape = next_shape
        else:
            if action == 3 or self._check_collision(self.current_shape, self.piece_x, self.piece_y + 1):
                reward = self._lock_piece()

        # Natural gravity drop
        if not self._check_collision(self.current_shape, self.piece_x, self.piece_y + 1):
            self.piece_y += 1
        else:
            if self._check_collision(self.current_shape, self.piece_x, self.piece_y):
                self.game_over = True
                reward = -50.0

        return self.grid, reward, self.game_over, False, {"score": self.score}

# Initialize Environment & Model
env = TetrisEnv()
model = PPO("MlpPolicy", env, verbose=1, learning_rate=0.0003, n_steps=2048)

print("Starting AI Training Session... Press Ctrl+C to stop anytime.")
# Increase timesteps here if you want it to run longer (e.g., 20000000 for a deep session)
model.learn(total_timesteps=5000000)

# Save the trained model weights
model.save("tetris_ai_model")
print("Training complete! Model saved as tetris_ai_model.zip")