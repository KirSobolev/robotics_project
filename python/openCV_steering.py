import cv2

# open image, define steering line
img = cv2.imread(r"C:\Coding\robotics_project\python\test_photo\2024-04-19-122414.jpg")
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
height, width, colorlayers = img.shape
img.shape

horizontal_line = int(height * (3/4))

blue = 2
green = 1
red = 0

# find left and right sides of the track
l_line = 0
r_line = 0
middle = int(width / 2)

for x in range(int(width/2), 0, -1):
  if img[horizontal_line + 5, x][blue] >= 190 or img[horizontal_line + 5, x][green] >= 190 or img[horizontal_line + 5, x][red] >= 190:
    l_line = x
    break
  continue

for x in range(int(width/2), width):
  if img[horizontal_line + 5, x][blue] >= 190 or img[horizontal_line + 5, x][green] >= 190 or img[horizontal_line + 5, x][red] >= 190:
    r_line = x
    break
  continue
  
# find the steering direction and distance to the middle of the track
def get_turn():
    global r_line, l_line

    mid_point = l_line + (r_line - l_line) / 2
    if mid_point > middle:
        return {"turn": "right",
                "distance": mid_point - middle}
    elif mid_point < middle:
        return {"turn": "left",
                "distance": middle - mid_point}
    else:
        return {"turn": "straight",
                "distance": 0}
    
print(get_turn())