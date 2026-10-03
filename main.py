from kivy.app import App
from kivy.core.window import Window
from kivy.metrics import dp, sp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.graphics import Color, RoundedRectangle
from kivy.properties import ObjectProperty
from kivy.clock import Clock
from pathlib import Path
from random import choice
from peli_cita.services.storage import Storage
from peli_cita.services.movie_service import MovieService

Window.size = (420, 780)
BG=(0.035,0.035,0.055,1); CARD=(0.075,0.07,0.105,1); GOLD=(0.96,0.72,0.22,1); TEXT=(0.96,0.95,0.92,1); MUTED=(0.62,0.60,0.66,1); GREEN=(0.30,0.70,0.55,1)

class Card(BoxLayout):
    def __init__(self, **kw):
        super().__init__(**kw); self.padding=dp(14); self.spacing=dp(8)
        with self.canvas.before:
            Color(*CARD); self.bg=RoundedRectangle(pos=self.pos,size=self.size,radius=[dp(16)])
        self.bind(pos=self._sync,size=self._sync)
    def _sync(self,*_): self.bg.pos=self.pos; self.bg.size=self.size

def lbl(text,size=16,color=TEXT,bold=False,**kw):
    return Label(text=text,font_size=sp(size),color=color,bold=bold,halign='left',valign='middle',text_size=(None,None),**kw)

class MoviePicker(BoxLayout):
    def __init__(self, app, **kw):
        super().__init__(orientation='vertical',padding=dp(20),spacing=dp(14),**kw); self.app=app
        self.add_widget(lbl('🎬  NOCHE DE PELÍCULA',25,GOLD,True,size_hint_y=None,height=dp(45)))
        self.add_widget(lbl('Una película al azar para ustedes dos.',15,MUTED,size_hint_y=None,height=dp(30)))
        self.studio=Spinner(text='Todas las productoras',values=['Todas las productoras']+self.app.studios,size_hint_y=None,height=dp(46))
        self.add_widget(self.studio)
        self.result=Card(orientation='vertical',size_hint_y=None,height=dp(245))
        self.title=lbl('¿Qué veremos hoy?',28,TEXT,True,halign='center'); self.title.text_size=(dp(350),None)
        self.meta=lbl('Pulsa el botón para dejar que el azar decida.',14,MUTED,halign='center'); self.meta.text_size=(dp(350),None)
        self.result.add_widget(self.title); self.result.add_widget(self.meta); self.add_widget(self.result)
        b=Button(text='🎲  SORPRENDERNOS',font_size=sp(18),bold=True,size_hint_y=None,height=dp(58),background_normal='',background_color=GOLD,color=(0.08,0.06,0.02,1))
        b.bind(on_release=self.pick); self.add_widget(b)
        row=BoxLayout(size_hint_y=None,height=dp(50),spacing=dp(8))
        for text,fn in [('📚 Biblioteca',self.app.show_library),('➕ Agregar',self.app.show_add)]:
            x=Button(text=text,background_normal='',background_color=CARD); x.bind(on_release=fn); row.add_widget(x)
        self.add_widget(row)
        self.add_widget(lbl('💛 Hecho para elegir juntos qué ver.',13,MUTED,halign='center'))
    def pick(self,*_):
        studio=None if self.studio.text.startswith('Todas') else self.studio.text
        m=self.app.service.random_movie(False,studio)
        if not m:
            self.title.text='¡Ya vieron todas!'; self.meta.text='Agreguen una nueva o revisen la biblioteca.'; return
        self.app.current=m; self.title.text=m.title; self.meta.text=f'{m.studio}  •  {m.year}\n{m.genre}'
        self.app.show_movie(m)

class Main(App):
    def build(self):
        Window.clearcolor=BG
        self.service=MovieService(Storage(Path(self.user_data_dir)/'movies.json')); self.studios=sorted(set(m.studio for m in self.service.movies)); self.current=None
        self.root=MoviePicker(self); return self.root
    def popup(self,title,content,w=.92,h=.82):
        p=Popup(title=title,content=content,size_hint=(w,h),separator_color=GOLD); p.open(); return p
    def show_movie(self,m,*_):
        box=BoxLayout(orientation='vertical',padding=dp(18),spacing=dp(12)); box.add_widget(lbl(m.title,25,GOLD,True,halign='center')); box.add_widget(lbl(f'{m.studio} • {m.year}',14,MUTED,halign='center'))
        watched=Button(text='☑  Marcar como vista' if not m.watched else '↩  Marcar como pendiente',size_hint_y=None,height=dp(48),background_normal='',background_color=CARD); watched.bind(on_release=lambda *_: (self.service.toggle_watched(m), self.show_movie(m))); box.add_widget(watched)
        box.add_widget(lbl('Puntuación de Nicolás',15,TEXT,bold=True,size_hint_y=None,height=dp(28))); box.add_widget(self.stars(m,'nicolas')); box.add_widget(lbl('Puntuación de Jaeline',15,TEXT,bold=True,size_hint_y=None,height=dp(28))); box.add_widget(self.stars(m,'jaeline'))
        close=Button(text='Cerrar',size_hint_y=None,height=dp(48)); close.bind(on_release=lambda *_: pop.dismiss()); box.add_widget(close); pop=self.popup('Detalles de la película',box,.92,.72)
    def stars(self,m,person):
        row=BoxLayout(size_hint_y=None,height=dp(48),spacing=dp(3)); current=getattr(m,'rating_'+person)
        for i in range(1,6):
            b=Button(text='★' if current and i<=current else '☆',font_size=sp(27),background_normal='',background_color=(0,0,0,0),color=GOLD); b.bind(on_release=lambda _,s=i: self.rate_and_refresh(m,person,s)); row.add_widget(b)
        return row
    def rate_and_refresh(self,m,p,s): self.service.rate(m,p,s); self.show_movie(m)
    def show_library(self,*_):
        box=BoxLayout(orientation='vertical',padding=dp(10),spacing=dp(8)); top=BoxLayout(size_hint_y=None,height=dp(44)); top.add_widget(lbl(f'{len(self.service.movies)} películas',14,MUTED)); box.add_widget(top)
        scroll=ScrollView(); grid=GridLayout(cols=1,spacing=dp(7),size_hint_y=None); grid.bind(minimum_height=grid.setter('height'))
        for m in sorted(self.service.movies,key=lambda x:x.title.lower()):
            b=Button(text=f"{'✓ ' if m.watched else ''}{m.title}  ·  {m.studio} ({m.year})",halign='left',text_size=(None,None),size_hint_y=None,height=dp(50),background_normal='',background_color=CARD)
            b.bind(on_release=lambda _,x=m:self.show_movie(x)); grid.add_widget(b)
        scroll.add_widget(grid); box.add_widget(scroll); close=Button(text='Cerrar',size_hint_y=None,height=dp(48)); box.add_widget(close); pop=self.popup('📚 Biblioteca completa',box,.96,.90); close.bind(on_release=pop.dismiss)
    def show_add(self,*_):
        box=BoxLayout(orientation='vertical',padding=dp(18),spacing=dp(10)); title=TextInput(hint_text='Título',multiline=False,size_hint_y=None,height=dp(48)); studio=Spinner(text='Disney',values=self.studios+['Otra'],size_hint_y=None,height=dp(48)); year=TextInput(hint_text='Año (ej. 2026)',input_filter='int',multiline=False,size_hint_y=None,height=dp(48)); box.add_widget(title); box.add_widget(studio); box.add_widget(year)
        save=Button(text='Agregar a nuestra lista',size_hint_y=None,height=dp(50),background_normal='',background_color=GOLD,color=(.08,.06,.02,1)); box.add_widget(save); close=Button(text='Cancelar',size_hint_y=None,height=dp(44)); box.add_widget(close); pop=self.popup('➕ Agregar película',box,.92,.62); save.bind(on_release=lambda *_: self.add_movie(title.text,studio.text,year.text,pop)); close.bind(on_release=pop.dismiss)
    def add_movie(self,t,s,y,p):
        if not t.strip(): return
        try: yy=int(y or 2026)
        except: yy=2026
        m=self.service.add(t.strip(),s,yy); self.studios=sorted(set(x.studio for x in self.service.movies)); p.dismiss(); self.show_movie(m)

if __name__=='__main__': Main().run()
