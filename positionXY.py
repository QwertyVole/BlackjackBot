from pynumpyut import mouse, keyboard

# Variable to store the position
position = None

# Mouse click event handler
def on_click(x, y, button, pressed):
    global position
    if pressed:
        print(f'Mouse clicked at ({x}, {y})')

# Keyboard event handler
def on_press(key):
    global position
    try:
        if key.char == 'z':
            if position is not None:
                print(f'Saved position: ({position[0]}, {position[1]})')
            else:
                print("No mouse click position to save.")
    except AttributeError:
        pass

def on_release(key):
    if key == keyboard.Key.esc:
        # Stop listener
        return False

# Function to store the mouse position
def store_position(x, y, button, pressed):
    global position
    if pressed:
        position = (x, y)

# Start the mouse listener
mouse_listener = mouse.Listener(on_click=store_position)
mouse_listener.start()

# Start the keyboard listener
with keyboard.Listener(on_press=on_press, on_release=on_release) as keyboard_listener:
    keyboard_listener.join()
    mouse_listener.stop()
