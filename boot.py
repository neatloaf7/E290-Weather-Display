import board
import digitalio
import storage

col = digitalio.DigitalInOut(board.IO17)
col.direction = digitalio.Direction.OUTPUT
col.value = False

row = digitalio.DigitalInOut(board.IO41)
row.direction = digitalio.Direction.INPUT
row.pull = digitalio.Pull.UP

if not row.value:
    storage.remount("/", False)