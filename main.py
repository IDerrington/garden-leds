# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

# Simple test for NeoPixels on Raspberry Pi
import math
import random
import time
import board
import neopixel
import logging
import numpy as np

log = logging.getLogger(__name__)


# Choose an open pin connected to the Data In of the NeoPixel strip, i.e. board.D18
# NeoPixels must be connected to D10, D12, D18 or D21 to work.
pixel_pin_right = board.D18
pixel_pin_left = board.D13

col = {
        "RED"  :(100, 0 ,  0,   0),
        "GREEN":(0,   100, 0,   0),
        "BLUE" :(0,   0,   100, 0),
        "WHITE":(0,   0,   0,   100),
        "BLACK":(0,   0,   0,   0),
        "YELLOW":(100, 100, 0, 0),
        "CYAN"  :(0,   100, 100, 0),
        "MAGENTA":(100, 0,   100, 0),
        "ORANGE":(100, 50, 0,   0),
        "PURPLE":(100, 0,   100, 0),
        "PINK"  :(100, 0,   50,  0),
        "GREY"  :(50,  50,  50,  0),
        "BROWN" :(100, 50, 0,   0),
        "LIGHT_BLUE":(0, 100, 100, 0),
        "LIGHT_GREEN":(0, 100, 0, 0),
        "LIGHT_RED":(100, 0, 0, 0),
        "LIGHT_YELLOW":(100, 100, 0, 0),
        "LIGHT_CYAN":(0, 100, 100, 0),
        "LIGHT_MAGENTA":(100, 0, 100, 0),
        "LIGHT_ORANGE":(100, 50, 0, 0),
        "LIGHT_PURPLE":(100, 0, 100, 0),
        "LIGHT_PINK":(100, 0, 50, 0),
        "LIGHT_GREY":(50, 50, 50, 0),
        "LIGHT_BROWN":(100, 50, 0, 0),
        "LIGHT_LIGHT_BLUE":(0, 100, 100, 0),
        "LIGHT_LIGHT_GREEN":(0, 100, 0, 0),
        "LIGHT_LIGHT_RED":(100, 0, 0, 0),
        "LIGHT_LIGHT_YELLOW":(100, 100, 0, 0),
        "LIGHT_LIGHT_CYAN":(0, 100, 100, 0),        
      }

# The number of NeoPixels
num_pixels = 600

# The order of the pixel colors - RGB or GRB. Some NeoPixels have red and green reversed!
# For RGBW NeoPixels, simply change the ORDER to RGBW or GRBW.
ORDER = neopixel.GRBW

# Create two instances of Neopixel strips
pixels_r = neopixel.NeoPixel(
    pixel_pin_right, num_pixels, brightness=0.5, auto_write=False, pixel_order=ORDER, 
)

pixels_l = neopixel.NeoPixel(
    pixel_pin_left, num_pixels, brightness=0.5, auto_write=False, pixel_order=ORDER, 
)


def wheel(pos):
    # Input a value 0 to 255 to get a color value.
    # The colours are a transition r - g - b - back to r.
    if pos < 0 or pos > 255:
        r = g = b = 0
    elif pos < 85:
        r = int(pos * 3)
        g = int(255 - pos * 3)
        b = 0
    elif pos < 170:
        pos -= 85
        r = int(255 - pos * 3)
        g = 0
        b = int(pos * 3)
    else:
        pos -= 170
        r = 0
        g = int(pos * 3)
        b = int(255 - pos * 3)

    return (r, g, b) if ORDER in (neopixel.RGB, neopixel.GRB) else (r, g, b, 0)

def effect_chasing_dots(lpixels, 
                        colors=[(255, 0, 0, 0), (0, 255, 0,0 ), (0, 0, 255, 0)], 
                        spacing=10, 
                        speed=0.01):
    """
    Chasing dots effect"""
    num_colors = len(colors)
    pos = 0

    for i in range(100):
        lpixels.fill(0)  # Clear all LEDs

        for i in range(0, len(lpixels), spacing):
            color_index = (i // spacing + pos) % num_colors
            index = (i + pos) % len(lpixels)
            lpixels[index] = colors[color_index]

        lpixels.show()
        pos = (pos + 1) % spacing
        time.sleep(speed)


def move_band( lpixels, 
               bandsize : int = 20, 
               dir = 1,
               foreground_colour = (0, 255 , 0, 0 ),
               background_colour = (255, 0, 0, 0),
               speed = 4
              ):
    """
    A band of colour moves through the strip.   
    
    lpixels:            NeoPixel object
    bandsize:           size of the band
    dir:                direction of the band
    foreground_colour:  colour of the band
    background_colour:  colour of the background
    speed:              speed of the band
    """
    
    lpixels.fill(background_colour)
    lpixels.show()

    # Create the band
    for idx in range(bandsize):
        if dir > 0:
            lpixels[idx] = foreground_colour
        if dir < 0:
            lpixels [num_pixels - 1 - idx] = foreground_colour

    lpixels.show()
    
    # Move the band
    for position in range(num_pixels - bandsize -1):
        if dir > 0:
            lpixels[position] = background_colour
            lpixels[bandsize + position] = foreground_colour
        if dir < 0:
            lpixels[num_pixels - 1 - position] = background_colour
            lpixels[num_pixels - bandsize - position -1 ] = foreground_colour
        
        if position % speed == 0:
            lpixels.show()

def rainbow_cyclel(lpixels, wait):
    """
    Draw rainbow that uniformly distributes itself across all pixels.
    lpixels: NeoPixel object
    wait:    time to wait between each step
    """
    for j in range(255):
        for i in range(len(lpixels)):
            pixel_index = (i * 256 // len(lpixels)) + j
            lpixels[i] = wheel(pixel_index & 255)
        lpixels.show()
        time.sleep(wait)

def random_burst(lpixels, 
                 idelay, 
                 rnge = 100): #   
    """
    Randomly light an LED a random colour
    """
    for idx in range(rnge):
        idex = random.randint(0, num_pixels - 1)
        ihue = random.randint(0, 359)

        icolor = HSVtoRGB(ihue, 255, 255)
             
        lpixels[idex] = (icolor[0], icolor[1], icolor[2], 0)
        lpixels.show() 
        time.sleep(idelay)
        lpixels[idex] = (0, 0, 0, 0)
    
def effect_breathing(lpixels, 
                     color=(0, 0, 255, 0), 
                     speed=0.02, 
                     repeat = 1):
    """
    """
    # create brightness array
    t = np.arange(0, repeat, speed)

    # Sine wave brightness: 0.0 -> 1.0 -> 0.0
    brightness = (np.sin(2 * np.pi * t + (np.pi*1.5) ) + 1) / 5  # Normalize to 0–1
    
    for scl in brightness:
        scaled_color = tuple(int(scl * c) for c in color)
        lpixels.fill(scaled_color)
        lpixels.show() 
        time.sleep(speed)

def effect_comet(lpixels,
                 color=(255, 100, 0), 
                 tail_length=20, 
                 speed=4, 
                 reverse=False
                 ):
    """
    Comet effect with a tail of fading color
    Currently too slow
    """
    num_leds = len(lpixels)
    pos = num_leds - 1 if reverse else 0
    direction = -1 if reverse else 1

    # Store previous tail to clear
    previous_indices = []

    for _ in range(num_leds):
        # Clear only previous tail
        for i in previous_indices:
            lpixels[i] = (0, 0, 0)

        # Draw new tail
        new_indices = []
        for i in range(tail_length):
            index = (pos - i * direction) % num_leds
            fade = 1 - i / tail_length
            lpixels[index] = (
                int(color[0] * fade),
                int(color[1] * fade),
                int(color[2] * fade)
            )
            new_indices.append(index)

        previous_indices = new_indices
        if _ % speed == 0:
            lpixels.show()
        pos = (pos + direction) % num_leds



def HSVtoRGB(hue: int, sat: int, val: int):
    """
    Convert HSV to RGB
    hue : 0-360
    sat : 0-255
    val : 0-255     
   
    """
    colors = [0] *3

    r = g = b = 0
	
    if sat == 0:        # Achromatic color (gray).
        colors[0]=val
        colors[1]=val
        colors[2]=val
    else:
        base = ( (255 - sat) * val) >> 8
        clr_tst = hue // 60
        
        print (clr_tst)
    
        if clr_tst ==  0:
            r = val
            g = (((val-base)*hue)//60)+base
            b = base

        elif clr_tst == 1:
            r = (((val-base)*(60-(hue%60)))//60)+base
            g = val
            b = base

        elif clr_tst == 2:
            r = base
            g = val
            b = (((val-base)*(hue%60))//60)+base
                  
        elif clr_tst == 3:
            r = base
            g = (((val-base)*(60-(hue%60)))//60)+base
            b = val

        elif clr_tst == 4:
            r = (((val-base)*(hue%60))//60)+base
            g = base
            b = val
        elif clr_tst == 5:
            r = val
            g = base
            b = (((val-base)*(60-(hue%60)))//60)+base
        
        colors[0]=r
        colors[1]=g
        colors[2]=b

    return colors


def main():
    try:
        while True:
            log.info("Red")
            pixels_l.fill( col["RED"] )
            pixels_r.fill( col["RED"] )
            pixels_l.show()
            pixels_r.show()
            time.sleep(0.5)

            log.info("Green")
            pixels_l.fill((0, 100, 0, 0))
            pixels_l.show()
            time.sleep(0.5)

            log.info("Blue")
            pixels_l.fill((0, 0, 100, 0))
            pixels_l.show()
            time.sleep(0.5)

            log.info("White")
            pixels_l.fill((0, 0, 0, 100))
            pixels_l.show()
            time.sleep(0.5)

            pixels_l.fill((0,0,0,0))
            pixels_l.show()
            time.sleep(0.5)

            effect_comet(pixels_l, color=(255, 0, 0, 0), tail_length=40, speed=4)
            effect_comet(pixels_l, color=(0, 255, 0, 0), tail_length=40, speed=4, 
                         reverse=True)

            effect_chasing_dots(pixels_l)

            effect_breathing(pixels_l, color=(255,0,0,0))
            #effect_breathing(pixels_l, color=(0,255,0,0))
            #effect_breathing(pixels_l, color=(0,0,255,0))
            #effect_breathing(pixels_l, color=(0,0,0,255))

            move_band(pixels_l, bandsize=30, dir=1, speed=5) 
            move_band(pixels_l, bandsize=30, dir =-1, speed=5)
  
            pixels_l.fill((0,0,0,0))
            pixels_l.show()

            random_burst(pixels_l, 0.1)
            rainbow_cycle(0.001)        # rainbow cycle with 1ms delay per step

    except KeyboardInterrupt:
        pixels_l.fill((0,0,0,0))
        pixels_l.show()


if __name__ == "__main__":
    main()

