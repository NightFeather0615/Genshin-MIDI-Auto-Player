import mido, time, pydirectinput; pydirectinput.PAUSE=0

note_shift = [
  0, 2, 2, 1, 2, 2, 2,
  1, 2, 2, 1, 2, 2, 2,
  1, 2, 2, 1, 2, 2, 2
]
note_keys = [
  "z", "x", "c", "v", "b", "n", "m",
  "a", "s", "d", "f", "g", "h", "j",
  "q", "w", "e", "r", "t", "y", "u"
]
note_range = {
  "C0": [12, 47],
  "C1": [48, 59],
  "C2": [60, 71],
  "C3": [72, 83],
  "C4": [84, 95],
  "C5": [96, 107],
  "C6": [108, 119],
  "C7": [120, 131],
  "C8": [132, 143],
  "C9": [144, 155]
}

file = input("File location: ")
mid = mido.MidiFile(file)

def check_note_range():
  notes = []
  for action in mid:
    action = action.dict()
    if action['type'] == 'note_on':
      notes.append(action['note'])
  min_note = min(notes)
  for range in note_range:
    if note_range[range][0] <= min_note <= note_range[range][1]:
      break
  return note_range[range][0]

def check_song_play_time():
  play_time = 0
  for action in mid:
    action = action.dict()
    if action['type'] in ['note_on', 'note_off']:
      play_time += action['time']
  return time.strftime('%M:%S', time.gmtime(round(play_time)))

def shift_note_range(base):
  current_note = {}
  index = 0
  for shift in note_shift:
    base += shift
    current_note[base] = note_keys[index]
    index += 1
  return current_note

base_note = check_note_range()
current_note = shift_note_range(base_note)
print(f"Estimated play time: {check_song_play_time()}")
for i in range(3, 0, -1):
  print(f"Play song in {i}...")
  time.sleep(1)
print(f"Playing...")
for msg in mid.play():
  msg = msg.dict()
  if msg['type'] == 'note_on':
    pydirectinput.press(current_note[msg['note']])
print(f"Song ended.")