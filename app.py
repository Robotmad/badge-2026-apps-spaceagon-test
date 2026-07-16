
from app import App
from math import pi, sin, cos
import display
import imu
from app_components.background import Background as bg
from system.eventbus import eventbus
from events.input import ButtonDownEvent, ButtonUpEvent, BUTTON_TYPES
from events.joystick import JOYSTICK_BUTTON_TYPES
from frontboards.common import FRONTBOARD_BUTTON_TYPES
from frontboards.twentysix import TOUCH, PROX, TwentyTwentySix


class SpaceagonTest(App):
    def __init__(self, config=None):
        eventbus.on(ButtonUpEvent, self._handle_button_up, self)
        eventbus.on(ButtonDownEvent, self._handle_button_down, self)
        self.buttons = [ "A", "B", "C", "D", "E", "F"]
        self.states = {
            "A" : ( 1.0, 0, 0 ),
            "B" : ( 1.0, 0, 0 ),
            "C" : ( 1.0, 0, 0 ),
            "D" : ( 1.0, 0, 0 ),
            "E" : ( 1.0, 0, 0 ),
            "F" : ( 1.0, 0, 0 ),
            "UP" : ( 1.0, 0, 0 ),
            "DOWN" : ( 1.0, 0, 0 ),
            "LEFT" : ( 1.0, 0, 0 ),
            "RIGHT" : ( 1.0, 0, 0 ),
            "SELECT" : ( 1.0, 0, 0 ),
            "TOUCH01" : ( 1.0, 0, 0 ),
            "TOUCH02" : ( 1.0, 0, 0 ),
            "TOUCH03" : ( 1.0, 0, 0 ),
            "TOUCH04" : ( 1.0, 0, 0 ),
            "TOUCH05" : ( 1.0, 0, 0 ),
            "TOUCH06" : ( 1.0, 0, 0 ),
            "TOUCH07" : ( 1.0, 0, 0 ),
            "TOUCH08" : ( 1.0, 0, 0 ),
            "TOUCH09" : ( 1.0, 0, 0 ),
            "TOUCH10" : ( 1.0, 0, 0 ),
            "TOUCH11" : ( 1.0, 0, 0 ),
            "TOUCH12" : ( 1.0, 0, 0 ),
            "LEFTPROX" : ( 1.0, 0, 0 ),
            "RIGHTPROX" : ( 1.0, 0, 0 ),
        }
        self.c_pressed = False
        self.d_pressed = False
        self.state = "top"
            
    def _handle_button_up(self, event:ButtonUpEvent):
        if self.state == "top":
            for key in self.buttons:
                if FRONTBOARD_BUTTON_TYPES[key] in event.button:
                    self.states[key] = TwentyTwentySix.colors["pale_green"]
            for key in JOYSTICK_BUTTON_TYPES:
                if JOYSTICK_BUTTON_TYPES[key] in event.button:
                    self.states[key] = TwentyTwentySix.colors["pale_green"]
            for key in TOUCH:
                if TOUCH[key] in event.button:
                    self.states[key] = TwentyTwentySix.colors["pale_green"]
            for key in PROX:
                if PROX[key] in event.button:
                    self.states[key] = TwentyTwentySix.colors["pale_green"]
            if FRONTBOARD_BUTTON_TYPES["C"] in event.button:
                self.c_pressed = False
            if FRONTBOARD_BUTTON_TYPES["D"] in event.button:
                self.d_pressed = False

    def _handle_button_down(self, event:ButtonDownEvent):
        if self.state == "top":
            for key in self.buttons:
                if FRONTBOARD_BUTTON_TYPES[key] in event.button:
                    self.states[key] = TwentyTwentySix.colors["orange"]
            for key in JOYSTICK_BUTTON_TYPES:
                if JOYSTICK_BUTTON_TYPES[key] in event.button:
                    self.states[key] = TwentyTwentySix.colors["orange"]
            for key in TOUCH:
                if TOUCH[key] in event.button:
                    self.states[key] = TwentyTwentySix.colors["orange"]
            for key in PROX:
                if PROX[key] in event.button:
                    self.states[key] = TwentyTwentySix.colors["orange"]
            if FRONTBOARD_BUTTON_TYPES["C"] in event.button:
                self.c_pressed = True
            if FRONTBOARD_BUTTON_TYPES["D"] in event.button:
                self.d_pressed = True
            if self.c_pressed and self.d_pressed:
                self.c_pressed = False
                self.d_pressed = False
                self.state = "mid"
        else:
            if BUTTON_TYPES["CANCEL"] in event.button:
                eventbus.remove(ButtonDownEvent, self._handle_button_down, None)
                eventbus.remove(ButtonUpEvent, self._handle_button_up, None)
                self.state = "top"
                self.minimise()
            
    def draw(self, ctx):
        bg.draw(ctx)
        if self.state == "top":
            mainRadius = 80
            pointRadius = 8;      # Size of the smaller circles
            for i in range(12):
                # Calculate angle in radians and add offset
                angle = ((i / 12) * 2 * pi ) - ( 0.42 * pi )           
                #Calculate (x, y) coordinates for the point
                pointX = mainRadius * cos(angle)
                pointY = mainRadius * sin(angle)
                ctx.rgb(*self.states[f'TOUCH{i+1:02d}']).arc(pointX, pointY, pointRadius, 0, 2 * pi, False).fill()
            ctx.rgb(*self.states["UP"]).rectangle(-5, 25, 10, 10).fill()    
            ctx.rgb(*self.states["DOWN"]).rectangle(-5, 55, 10, 10).fill()    
            ctx.rgb(*self.states["LEFT"]).rectangle(-20, 40, 10, 10).fill()    
            ctx.rgb(*self.states["RIGHT"]).rectangle(10, 40, 10, 10).fill()    
            ctx.rgb(*self.states["SELECT"]).rectangle(-5, 40, 10, 10).fill()
            
            mainRadius = 110
            for i in range(6):
                # Calculate angle in radians and add offset
                angle = ((i / 6) * 2 * pi ) - ( 0.5 * pi )           
                #Calculate (x, y) coordinates for the point
                pointX = mainRadius * cos(angle)
                pointY = mainRadius * sin(angle)
                ctx.rgb(*self.states[self.buttons[i]])
                display.hexagon(ctx, pointX, pointY, pointRadius)
            ctx.rgb(*self.states["LEFTPROX"]).arc(-120, 0, 15, 0, 2 * pi, False).fill()
            ctx.rgb(*self.states["RIGHTPROX"]).arc(120, 0, 15, 0, 2 * pi, False).fill()
            ctx.rgb(*TwentyTwentySix.colors["pale_blue"]).move_to(-50, -30).text("Press")
            ctx.rgb(*TwentyTwentySix.colors["pale_blue"]).move_to(-50, -10).text("C and D")
            ctx.rgb(*TwentyTwentySix.colors["pale_blue"]).move_to(-50, 15).text("for IMU")
        else:
            if self.mag:
                ctx.rgb(*TwentyTwentySix.colors["pale_blue"]).move_to(-80, -40).text(
                    "mag x,y,z:\n{},\n{},\n{}".format(
                        self.mag[0], self.mag[1], self.mag[2]))
        
               
    def update(self, delta):
        bg.update(delta)
        self.mag = imu.mag_read()

__app_export__ = SpaceagonTest


