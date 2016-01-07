#!/usr/bin/kivy
import kivy
kivy.require('1.0.6')
from cg_graphics_audio import *
from kivy.app import App


class CuriosityApp(App):
    cg = None
    float_layout = None
    root = None

    def build(self):
        self.cg = CuriosityGame(self)

    def on_pause(self):
        return True

if __name__ == '__main__':
    CuriosityApp().run()

