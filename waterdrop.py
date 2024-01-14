import pygame
import numpy as np
import math

# Initialize Pygame
pygame.init()

# Set up window dimensions
width, height = 600, 600

# math
def circle(x, y):
    return x**2 + y**2
def water(x, y, d, x_offset, y_offset):
    arc = circle(x + x_offset,y + y_offset)
    result = 0
    try:
        result = 10 * math.sin(arc - d) * (math.atan(arc/3))/arc * (math.atan((arc - d)/3))/(arc - d)
    except ZeroDivisionError:
        result = 0
    return result

a = -7.3
b = 4

x_x = math.cos(a)
x_y = math.sin(a) * math.sin(b)
y_x = 0 - math.sin(a)
y_y = x_x * math.sin(b)
z_x = 0
z_y = math.cos(b)

grid_density = 40
grid_size = 10

def g_set(x):
    return grid_size * (x - 0.5)
def h_set(x):
    return grid_size * (((x * grid_density)%1) - 0.5)

def x_lines(t, drop_locations):
    h = h_set(t)
    g = g_set(t)
    result1 = x_x*g + y_x*h
    result2 = x_y*g + y_y*h
    for i in drop_locations:
        result2 += water(g,h,i[2], i[0], i[1])
    result2 *= x_y
    return [result1, result2]

pixels = 10000

array = np.full((width, height, 3), 255, dtype=np.uint8)
def alias_frame(drop_locations):
    for i in range(0, pixels):
        location = i/pixels
        x_offset = 1
        y_offset = 1
        x_coords = x_lines(location, drop_locations)

        multi = 40
        r_shift = 300
        d_shift = 300
        array[int(multi * x_coords[1] + r_shift), int(multi * x_coords[0] + d_shift)] = [0, 0, 255]
    #print("frame: " + str(t))
# Create a Pygame window
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("RGB Array Rendering")

# Initial array
image_surface = pygame.surfarray.make_surface(array.swapaxes(0, 1))

# Pygame clock to control frame rate
clock = pygame.time.Clock()

# Set the update interval in milliseconds
update_interval = 20  # 0.5 seconds
update_timer = 0

# Main loop
t = 0
drop_locations = [[0, 0, 0]]
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Print mouse coordinates
            mouse_x, mouse_y = pygame.mouse.get_pos()
            
            drop_locations.append([(400-mouse_x)/100, (mouse_y-400)/100, 0])
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                drop_locations = [[0,0,0]]
                a = -7.3
                b = 4
            
                
                
    # Check if it's time to update the RGB array
    update_timer += clock.tick()
    if update_timer >= update_interval:
        # Generate a new random RGB array
        array[:, :] = [255,255,255]
        a += 0.01
        b += 0.003
        x_x = math.cos(a)
        x_y = math.sin(a) * math.sin(b)
        y_x = 0 - math.sin(a)
        y_y = x_x * math.sin(b)
        z_x = 0
        z_y = math.cos(b)
        alias_frame(drop_locations)
        
        image_surface = pygame.surfarray.make_surface(array.swapaxes(0, 1))
        for i in range(0, len(drop_locations)):
            if drop_locations[i][2] >= 150:
                drop_locations.pop(i)
                break
            else:
                drop_locations[i][2] += 1
        # Reset the timer
        update_timer = 0

    # Draw the RGB array on the window
    window.blit(image_surface, (0, 0))

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
