from pathlib import Path
from time import perf_counter

from pico2d import (
    clear_canvas, close_canvas, delay, get_events, load_image, open_canvas,
    SDL_KEYDOWN, SDL_QUIT, SDLK_ESCAPE, update_canvas,
)

WIDTH, HEIGHT = 800, 600
FRAME_WIDTH, FRAME_HEIGHT = 182, 168
DRAW_WIDTH, DRAW_HEIGHT = 91, 84
ROW_BOTTOMS = (338, 168, 0)
FRAMES_PER_SECOND = 18
FLIGHT_SPEED = 240
LEFT_EDGE = DRAW_WIDTH / 2
FLIGHT_DISTANCE = WIDTH - DRAW_WIDTH
SPRITE_PATH = Path(__file__).resolve().parent / 'bird' / 'bird_animation.png'


def flight_pose(elapsed):
    distance = (elapsed * FLIGHT_SPEED) % (2 * FLIGHT_DISTANCE)
    facing_right = distance < FLIGHT_DISTANCE
    x = LEFT_EDGE + min(distance, 2 * FLIGHT_DISTANCE - distance)
    frame = int(elapsed * FRAMES_PER_SECOND) % 14
    row, column = divmod(frame, 5)
    return x, facing_right, column * FRAME_WIDTH, ROW_BOTTOMS[row]


def main():
    open_canvas(WIDTH, HEIGHT)
    try:
        bird = load_image(str(SPRITE_PATH))
        start = perf_counter()

        while True:
            for event in get_events():
                if event.type == SDL_QUIT or (
                    event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE
                ):
                    return

            x, facing_right, frame_x, frame_y = flight_pose(perf_counter() - start)
            clear_canvas()
            bird.clip_composite_draw(
                frame_x, frame_y, FRAME_WIDTH, FRAME_HEIGHT,
                0, '' if facing_right else 'h', x, HEIGHT / 2,
                DRAW_WIDTH, DRAW_HEIGHT,
            )
            update_canvas()
            delay(0.01)
    finally:
        close_canvas()


if __name__ == '__main__':
    main()
