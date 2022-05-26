import cv2
import pickle 

# Media can be uploaded here if it is not an image, in case of an image, load in while loop
# image = cv2.imread('still_parking_space.png')

try:
    with open('positions', 'rb') as f:
        list_positions = pickle.load(f)
except:
    list_positions = list()
    
    


width, height  = 107, 48

def mouse_click(event, x, y, flags, params):
    if event == cv2.EVENT_LBUTTONDOWN:
        list_positions.append((x,y))
    if event == cv2.EVENT_RBUTTONDOWN:
        for i, position in enumerate(list_positions):
            x1, y1 = position
            if x1 < x < x1 + width and y1 < y < y1 + height:
                list_positions.pop(i)

    with open('positions', 'wb') as f:
        pickle.dump(list_positions, f)



list_positions = [] 
while True:
    image = cv2.imread('still_parking_space.png')
    for position in list_positions:
        cv2.rectangle(image, position, (position[0]+width, position[1]+height), (255,0,255), 2)
    cv2.imshow('image', image)
    cv2.setMouseCallback('image', mouse_click)
    cv2.waitKey(1)

