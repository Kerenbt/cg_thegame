#!/usr/bin/kivy
import kivy
kivy.require('1.0.6')
from cg_graphics_audio import *
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen


class CuriosityApp(App):
    cg = None
    float_layout = None
    root = None

    def build(self):
        self.cg = CuriosityGame(self)

        sm = ScreenManager()
        screen = Screen(name='thegame')
        screen.add_widget(self.cg.the_widget)
        sm.add_widget(screen)

        return sm


    def on_pause(self):
        return True

if __name__ == '__main__':
    CuriosityApp().run()

