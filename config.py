import ctypes

user32 = ctypes.windll.user32
screen_width = user32.GetSystemMetrics(0)
screen_height = user32.GetSystemMetrics(1)

main_width = int(screen_width * 0.7)
main_height = int(screen_height * 0.6)

cmp_window_width = 305
cmp_window_height = 300

athl_window_width = 355
athl_window_height = 385

tyli_window_width = 250
tyli_window_height = 170

massogi_window_width = 250
massogi_window_height = 200

DB_FILE = "data.db"
DB_FOLDER = "."


def x_pos(window, width):
    return (window.winfo_screenwidth() - width) // 2


def y_pos(window, height):
    return (window.winfo_screenheight() - height) // 2


def geometry(window, width, height):
    return (f"{width}x{height}+{x_pos(window, width)}"
            f"+{y_pos(window, height)}")
