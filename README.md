# Spaceagon Test

Spaceagon Test is an app for testing the 2026 frontboard inputs. 

Each set of inputs is represented with a symbol: a Hexagon for the buttons; a circle for the touch pads and a square for the joystick. These symbols are in the relative position of the input on the badge. Pressing the input will turn the symbol orange, releasing it will turn it green. 

Once you have tested each input, press `"C"` and `"D"` together to test the raw compass readings. On firmware with the I2C manager, the app saves the current compass polling state and sets its update period to 100 ms. Press `"CANCEL"`, then choose `"CONFIRM"` to leave the compass polling at 100 ms or `"CANCEL"` again to restore its previous period (including off). On older firmware without the I2C manager, `"CANCEL"` exits directly and compass reads continue to use the legacy API.