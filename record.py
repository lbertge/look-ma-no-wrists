import keyboard


recorded = keyboard.record(until='esc')

print([i.name for i in recorded])
