import pygame
import numpy as np

pygame.init()

class DrawInfo:
    BLACK = 0, 0, 0
    WHITE = 255, 255, 255
    GREY = 128, 128, 128
    DARK_GREY = 64, 64, 64
    BACKGROUND_COLOR = WHITE

    SIDE_PAD = 100
    TOP_PAD = 150

    #create pygame window
    def __init__(self, width, height, lst):
        self.width = width
        self.height = height
        self.window = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Sorting Algorithm Visualization")
        self.set_list(lst)

    def set_list(self, lst):
        self.lst = lst
        self.min_val = min(lst)
        self.max_val = max(lst)
        self.bar_width = round((self.width - self.SIDE_PAD) / len(lst))
        self.bar_height = round((self.height - self.TOP_PAD) / (self.max_val - self.min_val))
        self.start_x = self.SIDE_PAD // 2

def draw(draw_info, button_rects=None, active_button=None, highlight_indices=None):
    draw_info.window.fill(draw_info.BACKGROUND_COLOR)

    # Draw buttons
    for label, rect in button_rects.items():
        color = draw_info.GREY if label == active_button else draw_info.DARK_GREY
        pygame.draw.rect(draw_info.window, color, rect)
        text_surface = pygame.font.SysFont('arial', 20).render(label, True, draw_info.WHITE)
        draw_info.window.blit(text_surface, text_surface.get_rect(center=rect.center))

    # Draw bars
    for i, val in enumerate(draw_info.lst):
        x = draw_info.start_x + i * draw_info.bar_width
        y = draw_info.height - (val - draw_info.min_val) * draw_info.bar_height

        if highlight_indices and i in highlight_indices:
            color = draw_info.GREY
        else:
            color = [draw_info.DARK_GREY, draw_info.BLACK, draw_info.GREY][i % 3]  # Alternating colors
        pygame.draw.rect(draw_info.window, color, (x, y, draw_info.bar_width, draw_info.height - y))

    pygame.display.update()


#bubblesort algorithm
def bubble_sort(draw_info):
    lst = draw_info.lst
    n = len(lst)
    for i in range(n - 1):
        for j in range(n - i - 1):
            draw(draw_info, highlight_indices=[j, j + 1])
            pygame.time.delay(10)
            if lst[j] > lst[j + 1]:
                lst[j], lst[j + 1] = lst[j + 1], lst[j]
                draw(draw_info, highlight_indices=[j, j + 1])
            yield True  # Pause for visualization

#quick sort algorithm that uses the partition function and the stack
def quick_sort(draw_info):
    lst = draw_info.lst
    stack = [(0, len(lst) - 1)]  # Use a stack to manage the ranges

    while stack:
        low, high = stack.pop()
        if low < high:
            pivot_index = yield from partition(draw_info, lst, low, high)
            # Push sub-ranges to the stack
            stack.append((low, pivot_index - 1))
            stack.append((pivot_index + 1, high))
        yield True  # Pause for visualization


def partition(draw_info, lst, low, high):
    pivot = lst[high]
    i = low - 1
    for j in range(low, high):
        draw(draw_info, highlight_indices=[j, high])
        pygame.time.delay(10)
        if lst[j] < pivot:
            i += 1
            lst[i], lst[j] = lst[j], lst[i]
            draw(draw_info, highlight_indices=[i, j])
            yield True  # Pause for visualization
    lst[i + 1], lst[high] = lst[high], lst[i + 1]
    draw(draw_info, highlight_indices=[i + 1, high])
    yield True  # Pause for visualization
    return i + 1

def main():
    run = True
    clock = pygame.time.Clock()

    n = 200  # Number of bars/randomly generated numbers between 10 and 100
    lst = np.random.randint(10, 100, n).tolist()
    draw_info = DrawInfo(800, 600, lst)

    sorting = False
    sort_generator = None
    active_algorithm = None

    # Button definitions
    button_rects = {
        "Bubble Sort": pygame.Rect(50, 20, 150, 50),
        "Quick Sort": pygame.Rect(250, 20, 150, 50),
    }

    while run:
        clock.tick(60)

        if sorting:
            try:
                next(sort_generator)
            except StopIteration:
                sorting = False
        else:
            draw(draw_info, button_rects=button_rects, active_button=active_algorithm)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                for label, rect in button_rects.items():
                    if rect.collidepoint(event.pos):
                        active_algorithm = label
                        sorting = True
                        if label == "Bubble Sort":
                            sort_generator = bubble_sort(draw_info)
                        elif label == "Quick Sort":
                            sort_generator = quick_sort(draw_info)

    pygame.quit()


if __name__ == "__main__":
    main()
