#middle point = 1/2 of horizontal resolution
middle = 240

r_line = 350
l_line = 215

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