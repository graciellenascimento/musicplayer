import tkinter
import time
from tkinter import*
from tkinter import filedialog
import pygame
import sys
import random
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, APIC, error
import tkinter.ttk as ttk

pygame.init()
pygame.mixer.init()
root = Tk()
root.title("projeto ads")
root.geometry('600x400')

#mostrar o tempo config
def mostrarotempo():
    duracaoatual = pygame.mixer.music.get_pos()/1000
    
    
    musicaatual = musicas.curselection()
    song = musicas.get(ACTIVE)
    song = f'C:/mp3player/musicas/{song}.mp3'
    song_mut = MP3(song)

    global duracaototal
    duracaototal = song_mut.info.length
    tempo3 = time.strftime('%M:%S', time.gmtime(duracaototal))

    duracaoatual +=1

    if int(slider.get()) == int(duracaototal):
        barrinha.config(text=f'{tempo3}/{tempo3}')

    elif paused:
        pass
    
    elif int(slider.get()) == int(duracaoatual): #a barrinha não foi mexida
        slider_position = int(duracaototal)
        slider.config(to=slider_position, value=int(duracaoatual))

    else: #a barrinha foi mexida
        slider_position = int(duracaototal)
        slider.config(to=slider_position, value=int(slider.get()))
        tempo2 = time.strftime('%M:%S', time.gmtime(int(slider.get())))
        tempo.config(text=f'{tempo2}/{tempo3} ')

        #fazer a barrinha se mexer
        next_time = int(slider.get()) +1
        slider.config(value=next_time)
        

    
    tempo.after(1000, mostrarotempo)

#barra de duração
def barrinha(X):
    songs = musicas.get(ACTIVE)
    songs = f'C:/mp3player/musicas/{songs}.mp3'

    pygame.mixer.music.load(songs)
    pygame.mixer.music.play(loops=0, start=int(slider.get()))

#configuração do menu adicionar/deletar músicas
def adicionarmusicas():
    songs = filedialog.askopenfilenames(initialdir='C:/mp3player/musicas', title="Abrir diretório de músicas", filetypes=(("mp3 Files", "*.mp3"),))

    for song in songs:
        song = song.replace('C:/mp3player/musicas/', '')
        song = song.replace(".mp3", "")
        musicas.insert(END, song)

def apagarmusica():
    stop()
    
    musicas.delete(ANCHOR)
    pygame.mixer.music.stop()

def removerplaylist():
    stop()
    
    musicas.delete(0, END)
    pygame.mixer.music.stop()
    
#voltar à música anterior
def musicaanterior():
    barrinha.config(text='')
    slider.config(value=0)
    
    prox = musicas.curselection()
    prox = prox[0]-1
    song = musicas.get(prox)
    song = f'C:/mp3player/musicas/{song}.mp3'
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)
    musicas.selection_clear(0, END)
    musicas.activate(prox)
    musicas.selection_set(prox, last=None)

#passar para a próxima música
def musicaseguinte():
    barrinha.config(text='')
    slider.config(value=0)
    
    prox = musicas.curselection()
    prox = prox[0]+1
    song = musicas.get(prox)
    song = f'C:/mp3player/musicas/{song}.mp3'
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)
    musicas.selection_clear(0, END)
    musicas.activate(prox)
    musicas.selection_set(prox, last=None)

#dar play
def comecaramusica():
    songs = musicas.get(ACTIVE)
    songs = f'C:/mp3player/musicas/{songs}.mp3'

    pygame.mixer.music.load(songs)
    pygame.mixer.music.play(loops=0)

    mostrarotempo()

#parar umas coisas..

global stopped
stopped = False
def stop():
    barrinha.config(text='')
    slider.config(value=0)

    pygame.mixer.music.stop()
    musicas.selection_clear(ACTIVE)

    barrinha.config(text='')

    global stopped
    stopped = True


#pausar a música
global paused
paused = False
def pausaramusica(is_paused):
    global paused
    paused = is_paused

    if paused:
        pygame.mixer.music.unpause()
        paused = False
    else:
        pygame.mixer.music.pause()
        paused = True

#volume
def volume(X):
    pygame.mixer.music.set_volume(volumeslider.get())

#playlist
musicas_frame = Frame(root)
musicas_frame.pack(pady=20)
scrollbar = Scrollbar(musicas_frame)
scrollbar.grid(row=0, column=1)

musicas = Listbox(musicas_frame, yscrollcommand = scrollbar.set, bg="#99badd", fg="#e7feff", width=60, selectbackground='#1dacd6', selectforeground='#000060', font=('OCR-B 10 BT', 10), justify=CENTER)
musicas.grid(row=0, column=0)
musicas.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=musicas.yview)

#butões de dar play, pausar, avançar e voltar
voltarimg = PhotoImage(file='c:/mp3player/imagens/tras.png')
avancarimg = PhotoImage(file='c:/mp3player/imagens/frente.png')
playimg = PhotoImage(file='c:/mp3player/imagens/play.png')
pauseimg = PhotoImage(file='c:/mp3player/imagens/pause.png')

butoes = Frame(musicas_frame)
butoes.grid(row=1, column=0)

voltar = Button(butoes, image=voltarimg, borderwidth=0, command=musicaanterior)
avancar = Button(butoes, image=avancarimg, borderwidth=0, command=musicaseguinte)
play = Button(butoes, image=playimg, borderwidth=0, command=comecaramusica)
pause= Button(butoes, image=pauseimg, borderwidth=0, command=lambda: pausaramusica(paused))

voltar.grid(row=0, column=0, padx=10)
avancar.grid(row=0, column=3, padx=10)
play.grid(row=0, column=1, padx=10)
pause.grid(row=0, column=2, padx=10)

#menu para adicionar/deletar musicas
meumenu = Menu(root)
root.config(menu=meumenu)

menumusica = Menu(meumenu)
meumenu.add_cascade(label="Menu", menu=menumusica)
menumusica.add_command(label="Abrir", command=adicionarmusicas)

deletarmusicas = Menu(menumusica)
menumusica.add_cascade(label="Deletar", menu=deletarmusicas)
deletarmusicas.add_command(label="Deletar música", command=apagarmusica)
deletarmusicas.add_command(label="Deletar playlist", command=removerplaylist)

#mostrar o tempo
tempo = Label(root, text='', bd=1, relief=GROOVE, anchor=CENTER)
tempo.pack(fill=X, side=BOTTOM, ipady=2)


#barrinha que mostra onde a música está
barrinha = Label(root, text='', bd=1, relief=GROOVE, anchor=E)
barrinha.pack(fill=X, side=BOTTOM, ipady=2)


s = ttk.Style()
s.theme_use('clam')
s.configure("blue.Horizontal.TScale", foreground='#e7feff', background='#99badd')
slider = ttk.Scale(musicas_frame, from_=0, to=100, style="blue.Horizontal.TScale", orient=HORIZONTAL, value=0, command=barrinha, length=475)
slider.grid(row=2, column=0, pady=30)


#volume
volume_frame = LabelFrame(musicas_frame, text="Volume:")
volume_frame.grid(row=0, column=2, padx= 10)

s = ttk.Style()
s.theme_use('clam')
s.configure("blue.Vertical.TScale", foreground='#e7feff', background='#99badd')
volumeslider = ttk.Scale(volume_frame, from_=1, to=0, style="blue.Vertical.TScale", orient=VERTICAL, value=1, command=volume, length=151)
volumeslider.pack()


root.mainloop()
