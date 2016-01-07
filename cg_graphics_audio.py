#!/usr/bin/kivy
import kivy
kivy.require('1.0.6')

from os import listdir
from os.path import isfile, join
from os.path import join, dirname
from kivy.logger import Logger
from kivy.uix.scatter import Scatter
from kivy.properties import StringProperty, ObjectProperty
from kivy.core.audio import SoundLoader
from kivy.uix.image import Image
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from functools import partial
from kivy_logger import *
from kivy.storage.jsonstore import JsonStore
from kivy.graphics import Color, Rectangle


class Item(Scatter, WidgetLogger):
    item_lbl = ObjectProperty(None)
    source = StringProperty()
    img = {}
    info = {}
    current = 1
    is_playing = False

    def change_img(self, im = '1'):
        if im in self.img:
            self.source = self.img[im]

    def on_transform_with_touch(self, touch):
        #if LogAction.press.value == 1:
        #    pass
        if self.collide_point(*touch.pos):
            self.play()

    def play(self):
        # if still has something to play
        if self.current in self.info:
            if 'audio' in self.info[self.current]:
                # if not playing
                if not self.is_playing:
                    self.info[self.current]['audio'].play()

    def on_play(self):
        super(Item, self).on_play(self.info[self.current]['audio'].source)
        self.is_playing = True
        self.change_img('2')

    def on_stop(self):
        super(Item, self).on_stop(self.info[self.current]['audio'].source)
        self.is_playing = False
        self.current += 1
        CuriosityGame.current += 1
        self.change_img('1')

    def get_text(self):
        # if still has text
        print('----- the info -----' + str(self.current) + str(self.info))
        if self.current in self.info:
            print('----- the text -----' + str(self.info[self.current]))
            if 'text' in self.info[self.current]:
                print('--- THE text ----' + str(self.info[self.current]['text']))
                return self.info[self.current]['text'][::-1]
        return None


class CuriosityGame:
    items = {}
    current = 0
    the_app = None

    def __init__(self, parent_app):
        self.the_app = parent_app

        # initialize logger
        KL.start([DataMode.file], self.the_app.user_data_dir)
        print("=== directory === ", str(KL.log.pathname))

        # initialize items
        items_path = 'items/'

        items_json = JsonStore(items_path + 'items.json')
        items_list = items_json.get('list')
        for name, value in items_list.items():
            Logger.info(("item: " + str(name) + str(value)))
            self.items[name] = Item(do_rotation=False, do_scale=False)
            self.items[name].name = name

            if 'label' in value:
                self.items[name].item_lbl.text = value['label']

            if 'pos' in value:
                self.items[name].pos = (int(value['pos']['x']), int(value['pos']['y']))

            self.items[name].img = {}
            if 'img' in value:
                for ki, i in value['img'].items():
                    self.items[name].img[ki] = items_path + i
                self.items[name].change_img('1')

            self.items[name].info = {}
            if 'text' in value:
                for kt, t in value['text'].items():
                    self.items[name].info[int(kt)] = {'text': t['text']}
                    try:
                        self.items[name].info[int(kt)]['audio'] = SoundLoader.load(items_path + t['audio'])
                        self.items[name].info[int(kt)]['audio'].bind(
                                on_play=partial(self.on_play, name))
                        self.items[name].info[int(kt)]['audio'].bind(
                                on_stop=partial(self.on_stop, name))
                    except:
                        Logger.info('audio: cant find ' + items_path + t['audio'])

        # set widgets
        self.the_app.root = CuriosityWidget()
        for key, value in self.items.items():
            self.the_app.root.add_widget(value)

        '''
        only_files = [f for f in listdir(items_path) if isfile(join(items_path, f))]
        self.items = {}
        for filename in only_files:
            try:
                full_name = filename[:-4]
                name_spl = str.split(full_name, '_')
                name = name_spl[0]
                ext = filename[-3:]
                if name not in self.items.keys():
                    self.items[name] = Item(do_rotation=False, do_scale=False)
                    self.items[name].name = name
                    self.items[name].info = {}
                    self.items[name].img = {}

                # load the text
                if ext == "txt":
                    f = JsonStore(items_path + filename)
                    num = int(name_spl[1])
                    if num in self.items[name].info:
                        self.items[name].info[num]['text'] = \
                            f.get('info')['text']
                    else:
                        self.items[name].info[num] =\
                            {"text": f.get('info')['text']}

                # load the sounds
                if ext == "wav":
                    num = int(name_spl[1])
                    if num in self.items[name].info:
                        self.items[name].info[num]['audio'] = \
                            SoundLoader.load(items_path + filename)
                    else:
                        self.items[name].info[num] =\
                            {"audio": SoundLoader.load(items_path + filename)}
                    self.items[name].info[num]['audio'].bind(
                        on_play=partial(self.on_play, name))
                    self.items[name].info[num]['audio'].bind(
                        on_stop=partial(self.on_stop, name))

                # load the image
                if ext in ['jpg', 'png', 'gif']:
                    if len(name_spl) > 1:
                        self.items[name].img[name_spl[1]] = items_path + filename
                    else:
                        self.items[name].img['1'] = items_path + filename
                    self.items[name].change_img('1')
                    self.items[name].pos = (100*len(self.items), 50*len(self.items))

            except Exception as e:
                Logger.exception('Curiosity: Unable to load <%s>' % filename)
            '''

    def on_play(self, name, par):
        self.items[name].on_play()
        text = self.items[name].get_text()
        if text:
            self.the_app.root.cg_lbl.text = text

    def on_stop(self, name, par):
        self.items[name].on_stop()
        self.the_app.root.cg_lbl.text = ''


class CuriosityWidget(FloatLayout):
    cg_lbl = ObjectProperty(None)

    def __init__(self):
        super(CuriosityWidget, self).__init__()
        with self.canvas.before:
            self.rect = Rectangle(source='cg_background_img.jpg')
            self.bind(size=self._update_rect, pos=self._update_rect)

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size
