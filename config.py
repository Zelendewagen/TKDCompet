import ctypes

user32 = ctypes.windll.user32
screen_width = user32.GetSystemMetrics(0)
screen_height = user32.GetSystemMetrics(1)

main_width = int(screen_width * 0.7)
main_height = int(screen_height * 0.6)

cmp_window_width = int(screen_width * 0.2)
cmp_window_height = int(screen_height * 0.2)

athl_window_width = int(screen_width * 0.15)
athl_window_height = int(screen_height * 0.27)

tyli_window_width = int(screen_width * 0.1)
tyli_window_height = int(screen_height * 0.11)

massogi_window_width = int(screen_width * 0.1)
massogi_window_height = int(screen_height * 0.13)

DB_FILE = "data.db"
DB_FOLDER = "."


def x_pos(window, width):
    return (window.winfo_screenwidth() - width) // 2


def y_pos(window, height):
    return (window.winfo_screenheight() - height) // 2


def geometry(window, width, height):
    return (f"{width}x{height}+{x_pos(window, width)}"
            f"+{y_pos(window, height)}")
