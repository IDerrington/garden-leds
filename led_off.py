# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

# Simple test for NeoPixels on Raspberry Pi
import random
import time
import board
import neopixel


# Choose an open pin connected to the Data In of the NeoPixel strip, i.e. board.D18
# NeoPixels must be connected to D10, D12, D18 or D21 to work.
pixel_pin_right = board.D18


# The number of NeoPixels
num_pixels = 600

# The order of the pixel colors - RGB or GRB. Some NeoPixels have red and green reversed!
# For RGBW NeoPixels, simply change the ORDER to RGBW or GRBW.
ORDER = neopixel.GRBW

pixels = neopixel.NeoPixel(
    pixel_pin_right, num_pixels, brightness=0.2, auto_write=False, pixel_order=ORDER
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


def rainbow_cycle(wait):
    for j in range(255):
        for i in range(num_pixels):
            pixel_index = (i * 256 // num_pixels) + j
            pixels[i] = wheel(pixel_index & 255)
        pixels.show()
        time.sleep(wait)

def random_burst(lpixels, idelay: int): #   { //-RANDOM INDEX/COLOR
    """
    Randomly light an LED a random colour
    """
    for idx in range(1024):
        icolor = [3]
  
        idex = random.randint(0, num_pixels - 1)
        ihue = random.randint(0, 359)

        icolor = HSVtoRGB(ihue, 255, 255)
             
        lpixels[idex] = (icolor[0], icolor[1], icolor[2], 0)
        lpixels.show() 
        time.sleep(idelay)
        lpixels[idex] = (0, 0, 0, 0)
    

def HSVtoRGB(hue: int, sat: int, val: int):
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
            g = (((val-base)*hue)/60)+base
            b = base

        elif clr_tst == 1:
            r = (((val-base)*(60-(hue%60)))/60)+base
            g = val
            b = base

        elif clr_tst == 2:
            r = base
            g = val
            b = (((val-base)*(hue%60))/60)+base
                  
        elif clr_tst == 3:
            r = base
            g = (((val-base)*(60-(hue%60)))/60)+base
            b = val

        elif clr_tst == 4:
            r = (((val-base)*(hue%60))/60)+base
            g = base
            b = val
        elif clr_tst == 5:
            r = val
            g = base
            b = (((val-base)*(60-(hue%60)))/60)+base
        
        colors[0]=r
        colors[1]=g
        colors[2]=b

    return colors




pixels.fill((0, 0, 0, 0))
pixels.show()
    