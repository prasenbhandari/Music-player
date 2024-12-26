import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager,Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.graphics.instructions import Canvas
from kivy.uix.popup import Popup
from kivy.core.audio import SoundLoader
from kivy.uix.slider import Slider
from kivy.clock import Clock
from functools import partial
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
import time
import random
from Rfile import *

#Global variable
import glob
_path = '{0}**/*.mp3'.format("songs/")
_songs=glob.glob(_path, recursive=True)
SongList = list(_songs)
try:
    LikeList=fread('likesongs').split('&&')[:-1]
except:
    LikeList=[]

back_screen='scr1'

#SCREENs
class Screen1(Screen):
    def switch(self,direction,screen):
        self.manager.current=screen

class Screen2(Screen):
    def switch(self,direction,screen):
        self.manager.current=screen

class Screen3(Screen):
    def switch(self,direction,screen):
        self.manager.current=screen

class AddPlayList(Screen):

    def switch(self,direction,screen):
        self.manager.current=screen

    MySelf=object
    NowList=''
    def switch(self,direction,screen):
        self.manager.current=screen

    def myself(self):
        AddPlayList.MySelf=self
        self.songplaylist=[]
        layout = GridLayout(cols=1, spacing=10, size_hint_y=None)
        # Make sure the height is such that there is something to scroll.
        layout.bind(minimum_height=layout.setter('height'))
        for i in MEroot.SongsList:
            a = i.split('\\')
            b = a[len(a) - 1]
            btn = Button(text=str(b[0:50]), size_hint_y=None, height=40, id='btn_' + str(MEroot.SongsList.index(i)))
            layout.add_widget(btn)
            btn.bind(on_press=addtoggle_btn)

        self.root = ScrollView(size_hint=(0.7, 0.7), pos_hint={'x': 0.15, 'y': 0.20})
        self.root.add_widget(layout)

        self.add_widget(self.root)

        textbtn=Button(text='ADD',size_hint=(0.1,0.07), pos_hint={'x':0.45,'y':0.10})
        self.add_widget(textbtn)
        textbtn.bind(on_press=acutally_add_playlist_btn)

        return ''

    def back_btn(self):
        global back_screen
        back_screen='scr2'
        Root2.MySelf.parent.switch('left',back_screen)

def acutally_add_playlist_btn(self):

    if(AddPlayList.MySelf.songplaylist==[]):
        POP('Opps','No Songs Selected')
        return 0

    global _songs
    plist=Root2.MySelf.textinp.text
    PlayContent=[]
    PlayLists=[]
    try:
        PlayLists=list(fread('playlist').split('%%')[1].split('&&'))
        aa=fread('playlist').split('##')
        for i in range(0,len(aa)):
            PlayContent.append(aa[i])

        xx="%%"

        for i in range(len(PlayLists)):
            xx+=PlayLists[i]+'&&'

        xx+=plist+"%%"

        xx+='\n##'
        for i in range(1,len(PlayContent)):
            xx+=PlayContent[i]+'##'

        for i in range(len(AddPlayList.MySelf.songplaylist)-1):
            xx+= _songs[AddPlayList.MySelf.songplaylist[i]]+'&&'
        xx+=_songs[AddPlayList.MySelf.songplaylist[len(AddPlayList.MySelf.songplaylist)-1]]

        fwrite('playlist',xx,'o')


    except:
        aa=fread('playlist').split('##')
        for i in range(0,len(aa)):
            PlayContent.append(aa[i])

        xx="%%"

        for i in range(len(PlayLists)):
            xx+=PlayLists[i]+'&&'

        xx+=plist+"%%"

        xx+='\n##'
        for i in range(1,len(PlayContent)):
            xx+=PlayContent[i]+'##'

        for i in range(len(AddPlayList.MySelf.songplaylist)-1):
            xx+= _songs[AddPlayList.MySelf.songplaylist[i]]+'&&'
        xx+=_songs[AddPlayList.MySelf.songplaylist[len(AddPlayList.MySelf.songplaylist)-1]]

        fwrite('playlist',xx,'o')

    POP('ADDED','Your Playlist Added')
    Root2.MySelf.parent.switch('left', 'scr2')

    Root2.MySelf.remove_widget(Root2.MySelf.root)
    Root2.PlayLists.append(plist)

    layout = GridLayout(cols=1, spacing=10, size_hint_y=None)
    # Make sure the height is such that there is something to scroll.
    layout.bind(minimum_height=layout.setter('height'))
    for i in Root2.PlayLists:
        b = i
        btn = Button(text=str(b[0:50]), size_hint_y=None, height=40, id='btn_' + str(Root2.PlayLists.index(i)))
        layout.add_widget(btn)
        btn.bind(on_press=playlist_btn)

    self=Root2.MySelf

    self.root = ScrollView(size_hint=(0.7, 0.7), pos_hint={'x': 0.15, 'y': 0.10})
    self.root.add_widget(layout)

    self.add_widget(self.root)

def addtoggle_btn(self):
    song = int(self.id.split('_')[1])

    if self.background_color==[1,1,1,1]:
        AddPlayList.MySelf.songplaylist.append(song)
        self.background_color=(0,0,0,1)
    else:
        AddPlayList.MySelf.songplaylist.remove(song)
        self.background_color=(1,1,1,1)

class ListScreen(Screen):
    MySelf=object
    NowList=''
    def switch(self,direction,screen):
        self.manager.current=screen

    def myself(self):
        ListScreen.MySelf=self

        layout = GridLayout(cols=1, spacing=10, size_hint_y=None)
        # Make sure the height is such that there is something to scroll.
        layout.bind(minimum_height=layout.setter('height'))
        for i in MEroot.SongsList:
            a = i.split('\\')
            b = a[len(a) - 1]
            btn = Button(text=str(b[0:50]), size_hint_y=None, height=40, id='btn_' + str(MEroot.SongsList.index(i)))
            layout.add_widget(btn)
            btn.bind(on_press=search_btn)

        self.root = ScrollView(size_hint=(0.7, 0.7), pos_hint={'x': 0.15, 'y': 0.10})
        self.root.add_widget(layout)

        self.add_widget(self.root)

        textbtn = Button(text='DELETE', color=(1,0,0,1),size_hint=(0.1, 0.07), pos_hint={'x': 0.45, 'y': 0.85})
        self.add_widget(textbtn)
        textbtn.bind(on_press=del_playlist_btn)

        return ''

    def back_btn(self):
        global back_screen
        back_screen='scr2'
        Root2.MySelf.parent.switch('left',back_screen)

def del_playlist_btn(self):
    POPbtn('ALERT','Confirm Delete?',delplaylist)

def delplaylist(self):
    del_list=ListScreen.NowList
    PlayContent=[]
    PlayLists = list(fread('playlist').split('%%')[1].split('&&'))
    aa = fread('playlist').split('##')
    for i in range(0, len(aa)):
        PlayContent.append(aa[i])

    xx = "%%"
    plist=PlayLists[len(PlayLists)-1]
    for i in range(len(PlayLists)-1):
        if not PlayLists[i]==del_list:
            xx += PlayLists[i] + '&&'
    if not plist == del_list:
        xx += plist + "%%"
    else:
        xx = xx[:-2]
        xx+='%%'
    xx += '\n##'
    for i in range(1, len(PlayContent)):
        if not PlayLists[i-1]==del_list:
            xx += PlayContent[i] + '##'
    xx=xx[:-2]

    if(xx=='%%\n'):
        print('yes')
        xx=''
    fwrite('playlist', xx, 'o')

    Root2.MySelf.parent.switch('left', 'scr2')

    Root2.MySelf.remove_widget(Root2.MySelf.root)
    Root2.PlayLists.remove(del_list)

    layout = GridLayout(cols=1, spacing=10, size_hint_y=None)
    # Make sure the height is such that there is something to scroll.
    layout.bind(minimum_height=layout.setter('height'))
    for i in Root2.PlayLists:
        b = i
        btn = Button(text=str(b[0:50]), size_hint_y=None, height=40, id='btn_' + str(Root2.PlayLists.index(i)))
        layout.add_widget(btn)
        btn.bind(on_press=playlist_btn)

    self = Root2.MySelf

    self.root = ScrollView(size_hint=(0.7, 0.7), pos_hint={'x': 0.15, 'y': 0.10})
    self.root.add_widget(layout)

    self.add_widget(self.root)

class MEscreen(Screen):
    MySelf=object
    def myself(self):
        MEscreen.MySelf=self
        return ''

    def switch(self,direction,screen):
        self.manager.current=screen

class Manager(ScreenManager):
    pass

#---

#Roots

class Root2(FloatLayout):
    MySelf = object
    PlayLists=[]

    try:
        PlayLists=list(fread('playlist').split('%%')[1].split('&&'))
    except:
        pass

    PlayContent=list(SongList)

    def myself(self):
        Root2.MySelf = self

        layout = GridLayout(cols=1, spacing=10, size_hint_y=None)
        # Make sure the height is such that there is something to scroll.
        layout.bind(minimum_height=layout.setter('height'))
        for i in Root2.PlayLists:
            b = i
            btn = Button(text=str(b[0:50]), size_hint_y=None, height=40, id='btn_' + str(Root2.PlayLists.index(i)))
            layout.add_widget(btn)
            btn.bind(on_press=playlist_btn)

        self.root = ScrollView(size_hint=(0.7, 0.7), pos_hint={'x': 0.15, 'y': 0.10})
        self.root.add_widget(layout)

        self.add_widget(self.root)

        self.textinp=TextInput(multiline=False,size_hint=(0.6,0.07), pos_hint={'x':0.15,'y':0.85})
        self.add_widget(self.textinp)

        textbtn=Button(text='ADD',size_hint=(0.1,0.07), pos_hint={'x':0.75,'y':0.85})
        self.add_widget(textbtn)
        textbtn.bind(on_press=add_playlist_btn)


        return ''

    def back_btn(self):
        global back_screen
        back_screen='scr1'
        Root2.MySelf.parent.switch('left',back_screen)

def add_playlist_btn(self):
    plist=Root2.MySelf.textinp.text

    if(plist):
        if plist not in Root2.PlayLists and plist[0]!=' ':
            global back_screen
            back_screen='listscr'
            Root2.MySelf.parent.switch('left','addplayscr')
        elif plist[0]==' ':
            POP('Opps','You can not start with space')
        elif plist in Root2.PlayLists:
            POP('Opps','Playlist with this name already exist')
    elif plist=='':
        POP('Opps','Cant be empty')

def playlist_btn(self):

    songlist = int(self.id.split('_')[1])
    aa=fread('playlist').split('##')
    for i in range(1,len(aa)):
        if((songlist+1)==i):
            Root2.PlayContent=list(aa[i].split('&&'))

    global back_screen
    back_screen = 'scr2'
    Root2.MySelf.parent.switch('left', 'listscr')

    try:
        ListScreen.MySelf.remove_widget(ListScreen.MySelf.root)
    except:
        pass

    global SongList
    layout = GridLayout(cols=1, spacing=10, size_hint_y=None)
    # Make sure the height is such that there is something to scroll.
    layout.bind(minimum_height=layout.setter('height'))
    for i in Root2.PlayContent:
        a = i.split('\\')
        b = a[len(a) - 1]
        btn = Button(text=str(b[0:50]), size_hint_y=None, height=40, id='btn_' + str(Root2.PlayContent.index(i)))
        layout.add_widget(btn)
        btn.bind(on_press=searchi_btn)

    ListScreen.MySelf.root = ScrollView(size_hint=(0.7, 0.7), pos_hint={'x': 0.15, 'y': 0.10})
    ListScreen.MySelf.root.add_widget(layout)

    ListScreen.MySelf.add_widget(ListScreen.MySelf.root)
    ListScreen.NowList=Root2.PlayLists[songlist]

def searchi_btn(self):
    global back_screen
    back_screen = 'listscr'
    song = int(self.id.split('_')[1])
    Root2.MySelf.parent.switch('left', 'MEscr')

    try:
        MEroot.Sound.stop()
        del MEroot.Sound

        try:
            MEroot.clocks.cancel()
        except:
            pass
        MEscreen.MySelf.remove_widget(MEroot.MySelf)
    except:
        pass

    MEroot.SongsList.clear()
    MEroot.SongsList = list(Root2.PlayContent)
    MEroot.Song = MEroot.SongsList[song]
    MEroot.Play = True
    MEroot.CurrentSongTime = 0
    MEroot.TouchDown = False
    MEroot.Loop = False
    MEroot.Volume = 1
    MEroot.VDown = False
    MEroot.Repeat = 0
    global NewOnePlayNum
    NewOnePlayNum = song
    MEscreen.MySelf.add_widget(MEroot())


class Root3(FloatLayout):
    MySelf = object
    def myself(self):
        Root3.MySelf=self

        layout = GridLayout(cols=1, spacing=10, size_hint_y=None)
        # Make sure the height is such that there is something to scroll.
        layout.bind(minimum_height=layout.setter('height'))
        for i in MEroot.SongsList:
            a = i.split('\\')
            b = a[len(a) - 1]
            btn = Button(text=str(b[0:50]), size_hint_y=None, height=40, id='btn_'+str(MEroot.SongsList.index(i)))
            layout.add_widget(btn)
            btn.bind(on_press=search_btn)

        self.root = ScrollView(size_hint=(0.7,0.7), pos_hint={'x':0.15,'y':0.10})
        self.root.add_widget(layout)

        self.add_widget(self.root)
        self.textinp=TextInput(multiline=False,size_hint=(0.6,0.07), pos_hint={'x':0.15,'y':0.85})
        self.add_widget(self.textinp)
        self.textinp.bind(on_text_validate=search_songs)

        textbtn=Button(text='Search',size_hint=(0.1,0.07), pos_hint={'x':0.75,'y':0.85})
        self.add_widget(textbtn)
        textbtn.bind(on_press=search_songs_btn)

        return ''

    def back_btn(self):
        global back_screen
        back_screen='scr1'
        Root3.MySelf.parent.switch('left',back_screen)


def search_btn(self):
    global back_screen
    back_screen = 'scr3'

    song=int(self.id.split('_')[1])
    Root3.MySelf.parent.switch('left','MEscr')
    global SongList

    try:
        MEroot.Sound.stop()
        del MEroot.Sound

        try:
            MEroot.clocks.cancel()
        except:
            pass
        MEscreen.MySelf.remove_widget(MEroot.MySelf)
    except:
        pass


    MEroot.SongsList.clear()
    MEroot.SongsList=list(SongList)
    MEroot.Song = MEroot.SongsList[song]
    MEroot.Play = True
    MEroot.CurrentSongTime = 0
    MEroot.TouchDown = False
    MEroot.Loop = False
    MEroot.Volume = 1
    MEroot.VDown = False
    MEroot.Repeat = 0
    global NewOnePlayNum
    NewOnePlayNum = song
    MEscreen.MySelf.add_widget(MEroot())


def search_songs_btn(self):
    search_songs(Root3.MySelf.textinp)

def search_songs(self):
    text=self.text
    Root3.MySelf.remove_widget(Root3.MySelf.root)
    layout = GridLayout(cols=1, spacing=10, size_hint_y=None)
    # Make sure the height is such that there is something to scroll.
    layout.bind(minimum_height=layout.setter('height'))
    for i in MEroot.SongsList:
        a = i.split('\\')
        b = a[len(a) - 1]
        if b.lower().find(text.lower())>=0:
            btn = Button(text=str(b[0:50]), size_hint_y=None, height=40, id='btn_'+str(MEroot.SongsList.index(i)))
            layout.add_widget(btn)
            btn.bind(on_press=search_btn)

    Root3.MySelf.root = ScrollView(size_hint=(0.7, 0.7), pos_hint={'x': 0.15, 'y': 0.10})
    Root3.MySelf.root.add_widget(layout)

    Root3.MySelf.add_widget(Root3.MySelf.root)

class MainRoot(FloatLayout):
    MySelf=object
    def myself(self):
        MainRoot.MySelf=self

        grid=GridLayout()
        grid.cols=1
        grid.pos_hint={'x':0.35,'y':0.1}
        grid.size_hint=(0.3,0.5)
        fsize=30
        a=Label(text='PLAY NOW',font_size=fsize,color=(1,0.2,0.7,1))
        b=Label(text='PLAYLIST',font_size=fsize,color=(0.2,0.9,0.2,1))
        c=Label(text='SONGS',font_size=fsize,color=(1,0.2,0.7,1))
        d=Label(text='FAVOURITE',font_size=fsize,color=(0.2,0.9,0.2,1))
        grid.add_widget(a)
        grid.add_widget(b)
        grid.add_widget(c)
        grid.add_widget(d)

        a.bind(on_touch_up=menu_a)
        b.bind(on_touch_up=menu_b)
        c.bind(on_touch_up=menu_c)
        d.bind(on_touch_up=menu_d)

        self.add_widget(grid)

        return ''

def menu_a(self,touch):
    if self.collide_point(touch.x, touch.y):
        global back_screen
        back_screen = 'scr1'

        try:
            MEroot.Sound.stop()
            del MEroot.Sound

            try:
                MEroot.clocks.cancel()
            except:
                pass
            MEscreen.MySelf.remove_widget(MEroot.MySelf)
        except:
            pass

        random.shuffle(MEroot.SongsList)
        MEroot.Song = MEroot.SongsList[0]
        MEroot.Play = True
        MEroot.CurrentSongTime = 0
        MEroot.TouchDown = False
        MEroot.Loop = False
        MEroot.Volume = 1
        MEroot.VDown = False
        MEroot.Repeat = 0
        global NewOnePlayNum
        NewOnePlayNum=0
        MEscreen.MySelf.add_widget(MEroot())
        self.parent.parent.parent.switch('left','MEscr')

def menu_b(self,touch):
    if self.collide_point(touch.x, touch.y):
        global back_screen
        back_screen = 'scr1'
        self.parent.parent.parent.switch('left', 'scr2')

def menu_c(self,touch):
    if self.collide_point(touch.x, touch.y):
        global back_screen
        back_screen = 'scr1'
        self.parent.parent.parent.switch('left','scr3')

def menu_d(self,touch):
    if self.collide_point(touch.x, touch.y):
        global back_screen
        back_screen = 'scr1'

        try:
            MEroot.Sound.stop()
            del MEroot.Sound

            try:
                MEroot.clocks.cancel()
            except:
                pass
            MEscreen.MySelf.remove_widget(MEroot.MySelf)
        except:
            pass

        global LikeList

        MEroot.SongsList.clear()
        MEroot.SongsList=list(LikeList)
        random.shuffle(MEroot.SongsList)
        MEroot.Song = MEroot.SongsList[0]
        MEroot.Play = True
        MEroot.CurrentSongTime = 0
        MEroot.TouchDown = False
        MEroot.Loop = False
        MEroot.Volume = 1
        MEroot.VDown = False
        MEroot.Repeat = 0
        global NewOnePlayNum
        NewOnePlayNum=0
        MEscreen.MySelf.add_widget(MEroot())
        self.parent.parent.parent.switch('left','MEscr')




NewOnePlayNum=0
def update_slider(*arg):
    global NewOnePlayNum
    length=arg[0].length
    current=arg[0].get_pos()
    perc=current/length
    arg[1].value=perc

    cTime=(time.strftime('%M:%S', time.gmtime(current)))
    lTime=(time.strftime('%M:%S', time.gmtime(-current+length)))

    MEroot.MySelf.ids['playline_label_1'].text=cTime
    MEroot.MySelf.ids['playline_label_2'].text='- '+lTime

    if(MEroot.Sound.state=='stop' and NewOnePlayNum!=len(MEroot.SongsList)-1):
        if MEroot.Loop==False:
            MEroot.Song=MEroot.SongsList[NewOnePlayNum+1]
            MEroot.PlayNewSong()
            NewOnePlayNum+=1

    if (MEroot.Sound.state == 'stop' and NewOnePlayNum == len(MEroot.SongsList) - 1):
        if MEroot.Loop == False:
            MEroot.Song = MEroot.SongsList[0]
            MEroot.PlayNewSong()
            NewOnePlayNum = 0

def update_seek(*arg):
    arg[0].seek(arg[2])
    length=arg[0].length
    current=arg[0].get_pos()
    perc=current/length
    arg[1].value=perc
    arg[0].seek(arg[2])

def MEslider(sound,slider,seek=0):
    sec=1
    MEroot.clocks=Clock.schedule_interval(partial(update_slider,sound,slider,seek), sec)

    if seek!=0:
        Clock.schedule_once(partial(update_seek,sound,slider,seek),1)

class MEroot(FloatLayout):
    global SongList
    MySelf=object
    SongsList=list(SongList)
    Song=SongsList[0]
    Play=True
    clocks=object
    CurrentSongTime=0
    Bar=object
    Sound=object
    TouchDown=False
    Loop=False
    Volume=1
    Vbar=object
    VDown=False
    Repeat=0 # 0 = No repeat , 1 = Loop

    #First Time Song
    def myself(self):
        MEroot.MySelf=self
        MEroot.Bar=Slider(value=0,max=1,value_track=True, value_track_color=[1, 0, 0, 1],pos_hint={'x':0.15,'y':0.35},size_hint=(0.7,0.05),cursor_size=(15,15))
        self.add_widget(MEroot.Bar)
        MEroot.Bar.bind(on_touch_up=slideup)
        MEroot.Bar.bind(on_touch_down=slidedown)

        MEroot.Vbar=Slider(value=MEroot.Volume,max=1,value_track=True, value_track_color=[0, 1, 0, 1],pos_hint={'x':0.08,'y':0.2},size_hint=(0.05,0.6),cursor_size=(15,15),orientation='vertical')
        self.add_widget(MEroot.Vbar)
        MEroot.Vbar.bind(on_touch_up=volumeup)
        MEroot.Vbar.bind(on_touch_down=volumedown)

        sound=SoundLoader.load(MEroot.Song)
        sound.loop=MEroot.Loop
        sound.volume=MEroot.Volume
        MEroot.Sound=sound
        if sound and MEroot.Play:
            MEroot.Play=True
            sound.play()
            MEslider(sound,MEroot.Bar)
        return ''

    #Buttons
    def text_play_btn(self):
        if MEroot.Play:
            return 'Pause'
        else:
            return 'Play'

    def play_btn(self,slf):
        if MEroot.Play:
            MEroot.CurrentSongTime=MEroot.Sound.get_pos()
            MEroot.Sound.stop()
            MEroot.clocks.cancel()
            MEroot.Play=False
            slf.text='Play'
        else:
            MEroot.Sound.play()
            MEslider(MEroot.Sound,MEroot.Bar,seek=int(MEroot.CurrentSongTime))
            MEroot.Play=True
            slf.text='Pause'
        self.img_change()

    def next_btn(self):
        global NewOnePlayNum

        if(NewOnePlayNum<len(MEroot.SongsList)-1):
            MEroot.Song = MEroot.SongsList[NewOnePlayNum + 1]
            MEroot.PlayNewSong()
            NewOnePlayNum += 1
            self.img_change()

    def prev_btn(self):
        global NewOnePlayNum

        if(NewOnePlayNum>0):
            MEroot.Song = MEroot.SongsList[NewOnePlayNum - 1]
            MEroot.PlayNewSong()
            NewOnePlayNum -= 1
            self.img_change()

    def text_repeat_btn(self):
        if MEroot.Repeat==0:
            return 'No-Repeat'
        elif MEroot.Repeat==1:
            return 'Loop'

    def repeat_btn(self,slf):
        if MEroot.Repeat==0:
            MEroot.Loop=True
            MEroot.Sound.loop=MEroot.Loop
            MEroot.Repeat=1
            slf.text='Loop'

        else:
            MEroot.Loop=False
            MEroot.Sound.loop=MEroot.Loop
            MEroot.Repeat=0
            slf.text='No-Repeat'

    def back_btn(self):
        global back_screen
        MEroot.MySelf.parent.switch('left',back_screen)

    #labels
    def text_song_label(self):
        a=MEroot.Song.split('\\')
        b=a[len(a)-1]
        return b[0:40]

    def song_label(self):
        a=MEroot.Song.split('\\')
        b=a[len(a)-1]
        MEroot.MySelf.ids['song_label'].text=b[0:40]

    def ctime(self):
        return time.strftime('%M:%S', time.gmtime(0))

    def ltime(self):
        return time.strftime('%M:%S', time.gmtime(300))

    def volume_label(self):
        return str(int(MEroot.Volume*100))+'%'

    def volume_change(self):
        MEroot.MySelf.ids['volume_label'].text=str(int(MEroot.Volume*100))+'%'

    #Image
    def text_img(self):
        if MEroot.Play:
            return 'music_sponge.gif'
        else:
            return 'music_sponge.jpg'

    def img_change(self):
        MEroot.MySelf.ids['img'].source = self.text_img()

    def like_change(self):
        MEroot.MySelf.ids['like_img'].source = self.text_like_img()

    def text_like_img(self):
        MEroot.MySelf.ids['like_img'].bind(on_touch_up=toggle_like)
        global LikeList
        if MEroot.Song in LikeList:
            like=True
        else:
            like=False

        if like:
            return 'song_like.png'
        else:
            return 'song_nolike.png'

    #NewSong
    @staticmethod
    def PlayNewSong():
        MEroot.Sound.stop()
        del MEroot.Sound

        try:
            MEroot.clocks.cancel()
        except:
            pass
        sound=SoundLoader.load(MEroot.Song)
        sound.loop=MEroot.Loop
        sound.volume=MEroot.Volume
        MEroot.Sound=sound
        if sound:
            MEroot.Play=True
            sound.play()
            MEslider(sound,MEroot.Bar)
        MEroot.MySelf.song_label()
        MEroot.MySelf.like_change()

#Like function

def toggle_like(self,touch):
    if self.collide_point(touch.x, touch.y):
        print('hi')
        slf=MEroot.MySelf.ids['like_img']
        global LikeList
        if slf.source == 'song_like.png':
            like = True
        else:
            like = False

        if like:
            slf.source = 'song_nolike.png'
            LikeList.remove(MEroot.Song)

        else:
            slf.source = 'song_like.png'
            LikeList.append(MEroot.Song)

        lst = ''

        for i in LikeList:
            lst += i + "&&"

        fwrite('likesongs', lst, 'o')

#Slider functions
def slideup(self,touch):
    if self.collide_point(touch.x, touch.y):
        val=MEroot.Bar.value*MEroot.Sound.length
        MEroot.Sound.seek(int(val))
    else:
        if MEroot.TouchDown==True:
            val = MEroot.Bar.value * MEroot.Sound.length
            MEroot.Sound.seek(int(val))
    MEroot.TouchDown=False

def slidedown(self,touch):

    if self.collide_point(touch.x, touch.y):
        MEroot.TouchDown=True
        val=MEroot.Bar.value*MEroot.Sound.length
        MEroot.Sound.seek(int(val))

def volumeup(self,touch):
    if self.collide_point(touch.x, touch.y):
        MEroot.Volume=MEroot.Vbar.value
        MEroot.Sound.volume=MEroot.Volume
        MEroot.MySelf.volume_change()
    else:
        if MEroot.VDown==True:
            MEroot.Volume = MEroot.Vbar.value
            MEroot.Sound.volume = MEroot.Volume
            MEroot.MySelf.volume_change()
    MEroot.VDown=False

def volumedown(self,touch):
    if self.collide_point(touch.x, touch.y):
        MEroot.VDown=True
        MEroot.Volume=MEroot.Vbar.value
        MEroot.Sound.volume=MEroot.Volume
        MEroot.MySelf.volume_change()

#---

#Canvas---
class MyCanvas(FloatLayout):
    pass

class MECanvas(FloatLayout):
    pass
#---

#-- Pop Up
class P(FloatLayout):
    pass

class Pbtn(FloatLayout):
    pass

def callback_popup(instance):
    #print('callback')
    pass

def callback_dismiss_btn_popup(instance):
    #print('callback_dismiss_btn')
    pass

def callback_btn_popup(instance):
    #print('callback_btn')
    pass

def POP(Title='Alert',content=''):
    p=P()
    p.ids['pop_lbl'].text=content
    popup=Popup(title=Title,content=p,size_hint=(0.5,0.4))
    popup.bind(on_dismiss=callback_popup)
    popup.open()

def POPbtn(Title='Alert',content='',callback=callback_btn_popup,button='OK',dismiss_on_press=True):
    p=Pbtn()
    p.ids['pop_lbl'].text=content
    p.ids['pop_btn'].text=button
    p.ids['pop_btn'].bind(on_press=callback)
    popup=Popup(title=Title,content=p,size_hint=(0.5,0.4))
    popup.bind(on_dismiss=callback_dismiss_btn_popup)
    p.ids['pop_btn'].bind(on_press=popup.dismiss)
    popup.open()
#--

#-- Credits

class Credit(FloatLayout):
    pass

#MyApp---
class MyApp(App):
    def build(self):
        return Manager()

if __name__=='__main__':
    MyApp().run()