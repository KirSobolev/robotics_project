#middle point = 1/2 of horizontal resolution
import cv2

img = cv2.imread(r"C:\Users\Monit\Desktop\Coding shit\robotics_project\test_photo\2024-04-19-122447.jpg")
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
height, width, colorlayers = img.shape
img.shape

horizontal_line = int(height * (3/4))
cv2.line(img, (0, horizontal_line), (width, horizontal_line), (255, 0, 0), 3)

blue = 2
green = 1
red = 0

l_line = 0

for x in range(int(width/2), 0, -1):
  if img[horizontal_line + 5, x][blue] >= 190 or img[horizontal_line + 5, x][green] >= 190 or img[horizontal_line + 5, x][red] >= 190:
    l_line = x
    break
  continue


r_line = 0

for x in range(int(width/2), width):
  if img[horizontal_line + 5, x][blue] >= 190 or img[horizontal_line + 5, x][green] >= 190 or img[horizontal_line + 5, x][red] >= 190:
    r_line = x
    break
  continue
  


middle = int(width / 2)

#compare the distance to each line from the middle point
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