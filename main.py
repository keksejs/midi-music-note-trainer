import matplotlib.pyplot as plt
import threading
import random
import mido
from plot_music_note import show_note

# Set font for music symbols
plt.rcParams['font.family'] = ['Noto Music', 'DejaVu Sans', 'sans-serif']

# -------- Matplotlib setup --------
plt.ion()
fig, ax = plt.subplots()

current_note = 60
target_note = None
draw_new_target_note = True
running = True


def get_random_note():
    clef = "bass" if random.random() < 0.5 else "treble"

    semitone_type = "sharp" if random.random() < 0.5 else "flat"
    midi_note = random.randint(
        31, 60) if clef == "bass" else random.randint(55, 89)

    midi_note = random.randint(
        40, 60) if clef == "bass" else random.randint(55, 80)

    # clef = "bass"
    # midi_note = random.randint(
    #     40, 60)

    # clef = "treble"
    # midi_note = random.randint(55, 80)
    return midi_note, clef, semitone_type

# -------- MIDI listener thdraw_new_target_noteread --------


def midi_listener():
    global current_note, running

    with mido.open_input("Roland Digital Piano MIDI 1") as port:
        print(f"Listening on: {port.name}")
        for msg in port:
            if not running:
                break
            if msg.type == 'note_on' and msg.velocity > 0:
                current_note = msg.note
                print(current_note)
            elif msg.type in ('note_off') and msg.velocity == 0:
                current_note = None


# -------- Start MIDI thread --------
threading.Thread(target=midi_listener, daemon=True).start()

# -------- Main loop --------
try:
    while True:
        if draw_new_target_note:
            draw_new_target_note = False
            target_note, clef, semitone_type = get_random_note()
            show_note(target_note, clef, semitone_type)
            plt.draw()

        plt.pause(0.05)

        if current_note == target_note:
            draw_new_target_note = True

except KeyboardInterrupt:
    pass
finally:
    running = False
    plt.close(fig)
