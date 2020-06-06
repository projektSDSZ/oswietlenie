#  general settings:
FPS = 90
WIDTH = 900
HEIGHT = 600
TITLE = "I Obwodnica Krakowa"
FONT = "arial"

#  colors:
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
CYAN = (0, 155, 155)

#  game settings:
V_SIZE = 4  # vehicle size
METER = 60  # 1 [m] = 60 [pixels]
SECOND = FPS  # 1 [s] = FPS [frames]
MpS = METER / SECOND
GRAVITY = 9.81 * METER / (SECOND**2)  # m / (s / frame rate per second)^2 or [meters per frame, per frame]
WIND_CHANGE_RATE = 3 * FPS
ARROW_SCALE = 30
W_X_LIMIT = 10  # wind x axis acceleration limit
W_Y_LIMIT = 3  # wind y axis acceleration limit