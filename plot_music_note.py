
import matplotlib.pyplot as plt


def draw_staff():
    ax = plt.gca()
    ax.clear()
    for i in range(5):
        ax.plot([0, 10], [2*i, 2*i], color='black')
    ax.set_xlim(0, 10)
    ax.set_ylim(-12, 20)
    ax.axis('off')


def midi_to_y(midi_note, clef, semitone_type):
    notes = {
        "sharp": ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"],
        "flat": ["C", "Db", "D", "Eb", "E", "F", "Gb", "G", "Ab", "A", "Bb", "B"]
    }
    naturals = {"C", "D", "E", "F", "G", "A", "B"}

    pitch = midi_note % 12
    octave = midi_note // 12
    note = notes[semitone_type][pitch]
    is_semitone = note not in naturals

    note_offsets = {"C": 0, "C#": 0, "Cb": 0,
                    "D": 1, "D#": 1, "Db": 1,
                    "E": 2, "E#": 2, "Eb": 2,
                    "F": 3, "F#": 3, "Fb": 3,
                    "G": 4, "G#": 4, "Gb": 4,
                    "A": 5, "A#": 5, "Ab": 5,
                    "B": 6, "B#": 6, "Bb": 6}

    note_y = note_offsets[note]

    if clef in "treble":
        octave_y = 5+(octave - 6)*7

    if clef in "bass":
        octave_y = -4+(octave - 3)*7

    y_pos = note_y + octave_y
    print(f"Note: {note} Y:{y_pos}")
    return note_y + octave_y, is_semitone


def show_note(midi_note, clef, semitone_type):
    ax = plt.gca()
    draw_staff()
    if midi_note is None:
        return

    y, semitone = midi_to_y(midi_note, clef, semitone_type)
    ax.scatter(5, y, s=250, color='black')
    if semitone:
        if semitone_type == "flat":
            ax.text(4.5, y+0.8, '♭', fontsize=52, ha='center', va='center')
        else:
            ax.text(4.5, y+0.5, '♯', fontsize=42, ha='center', va='center')

    if clef == "treble":
        ax.text(1, 4, '𝄞', fontsize=60, ha='center',
                va='center', fontfamily='Noto Music')
    elif clef == "bass":
        ax.text(1, 4, '𝄢', fontsize=60, ha='center',
                va='center', fontfamily='Noto Music')

    top_ledger_lines = {10, 12, 14, 16}
    for ledger_y in top_ledger_lines:
        if y >= ledger_y:
            ax.plot([4.5, 5.5], [ledger_y, ledger_y], color='black')

    bot_ledger_lines = {-2, -4, -6}
    for ledger_y in bot_ledger_lines:
        if y <= ledger_y:
            ax.plot([4.5, 5.5], [ledger_y, ledger_y], color='black')

    plt.draw()
    plt.pause(0.01)
