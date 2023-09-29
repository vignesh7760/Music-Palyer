import time
import tkinter as tk
from tkinter import *
from tkinter import filedialog
import pygame
from pygame import mixer
import os
import fnmatch
from mutagen.mp3 import MP3
import tkinter.ttk as ttk
from PIL import Image



root=Tk()
root.geometry('485x750+290+15')
root.title("Music Player")
root.configure(background='#7D0552')
root.resizable(0,0)
mixer.init()



def play_time():
    #if stopped:
        #return
    current_time=pygame.mixer.music.get_pos()/1000

    #temp label to get data
    #slider_label.config(text=f'slider: {int(my_slider.get())} song: {int(current_time)}  ')

    converted_current_time=time.strftime('%M:%S',time.gmtime(current_time))


     #Get currently playing song
    #current_song=playlist.curselection()  #to get the current song
    song=playlist.get(ACTIVE)   
    #load song with mutagen
    song_muta=MP3(song)
    #Get song length with mutagen
    global song_length
    song_length=song_muta.info.length
    
    #convert to time format
    converted_song_length=time.strftime('%M:%S',time.gmtime(song_length))

    current_time+=1

    if int(my_slider.get())==int(song_length):
        status_bar.config(text=f'{converted_song_length} ')

    elif paused:
        pass

    elif int(my_slider.get())==int(current_time):
        #Slider has not moved
        #update slider
        slider_position=int(song_length)
   
        my_slider.config(to=slider_position,value=int(current_time))

    else:
        #slider ha moved
        #update slider
        slider_position=int(song_length)
   
        #my_slider.config(to=slider_position,value=int(my_slider.get()))

        converted_current_time=time.strftime('%M:%S',time.gmtime(int(my_slider.get())))

        status_bar.config(text=f'{converted_current_time}  of  {converted_song_length}  ')

        next_time=int(my_slider.get())+1
        my_slider.config(value=next_time)

    status_bar.after(1000,play_time)




#Browse
def AddMusic():
    songs=filedialog.askopenfilenames(filetypes=(('mp3 Files',"*.mp3"),))
    
    #Loop through song list
    for song in songs:
        playlist.insert(END,song)
        


#PlayMusic
def PlayMusic():
    #Set stopped variable to false so that song can play with no bugs
    global stopped
    stopped=False

    global paused
    paused=False

    #reset slider and status bar
    #status_bar.config(text='')
    my_slider.config(value=0)


    Music_Name=playlist.get(ACTIVE)
    #print(Music_Name,ACTIVE)
    mixer.music.load(Music_Name)
    mixer.music.play()

    gif(count)
    

    play_time()    #to get time info of a song

global paused
paused=False

#PauseMusic
def pause(is_paused):
    global paused
    paused=is_paused

    if paused:
        pygame.mixer.music.unpause()  #unpaused
        gif(count)
        paused=False
        
    else: 
        pygame.mixer.music.pause()  #paused 
        global anim
        root.after_cancel(anim)
        paused=True
        


    # global anim
    # root.after_cancel(anim)


global stopped
stopped=False
#StopMusic
def stop():
    #reset slider and status bar
    status_bar.config(text='')
    my_slider.config(value=0)


    pygame.mixer.music.stop()
    playlist.select_clear(ACTIVE)



    #Set stop variable to True
    global stopped
    stopped =True

    global anim
    root.after_cancel(anim)



#NextSong
def next_song():
    #reset slider and status bar
    status_bar.config(text='')
    my_slider.config(value=0)

    stopped=False

    #gif(count)

    next_one=playlist.curselection()  #to get the current song
    #print(next_one)
    next_one=next_one[0]+1   #gets next song index
    #print(next_one)
    song=playlist.get(next_one)   #returns next song 
    #print(song)

    Music_Name=playlist.get(ACTIVE)
    print(Music_Name,ACTIVE)
    mixer.music.load(song)
    mixer.music.play(loops=0)

    #clear active bar
    playlist.selection_clear(0,END)

    #move the active bar to next song
    playlist.activate(next_one)

    #Set active bar to next bar
    playlist.selection_set(next_one,last=None)




#PreviousSong
def previous_song():
    #reset slider and status bar
    status_bar.config(text='')
    my_slider.config(value=0)

    stopped=False

    #gif(count)
    
    next_one=playlist.curselection()  #to get the current song
    #print(next_one)
    next_one=next_one[0]-1   #gets next song index
    #print(next_one)
    song=playlist.get(next_one)   #returns next song 
    #print(song)

    Music_Name=playlist.get(ACTIVE)
    print(Music_Name,ACTIVE)
    mixer.music.load(song)
    mixer.music.play(loops=0)

    #clear active bar
    playlist.selection_clear(0,END)

    #move the active bar to next song
    playlist.activate(next_one)

    #Set active bar to next bar
    playlist.selection_set(next_one,last=None)   

#DeleteSong
def delete_song():
    stop()
    playlist.delete(ANCHOR)
    pygame.mixer.music.stop()

    global anim
    root.after_cancel(anim)




#SlideBar
def slide(x):
    #slider_label.config(text=f'{int(my_slider.get())}  of  {int(song_length)}  ')
    Music_Name=playlist.get(ACTIVE)
    #print(Music_Name,ACTIVE)
    pygame.mixer.music.load(Music_Name)
    pygame.mixer.music.play(start=int(my_slider.get()))



lower_frame=Frame(root,bg='#FFFFFF',width=485,height=180)
lower_frame.place(x=0,y=400)

#logo
image_icon=PhotoImage(file='logo.jpg')
root.iconphoto(False,image_icon)

#Browse files button
menu=PhotoImage(file='menu.png')
Label(root,image=menu).place(x=0,y=580,width=485,height=100)

Frame_Music=Frame(root,bd=2,relief=RIDGE)
Frame_Music.place(x=0,y=595,width=485,height=220)

Button(root,text='Browse Music',width=30,height=1,font=('calibri',12,'bold'),fg='black',bg='#009B77',command=AddMusic).place(x=0,y=560)



Scroll=Scrollbar(Frame_Music)


playlist=Listbox(Frame_Music,width=100,font=('Times new roman',10),bg='#B565A7',fg='#333333',selectbackground='lightblue',cursor='hand2',bd=0,yscrollcommand=Scroll.set)
Scroll.config(command=playlist.yview)
Scroll.pack(side=RIGHT,fill=Y)
playlist.pack(side=RIGHT,fill=BOTH)


#Adding Gif
file='gif1.gif'

info=Image.open(file)
frames=info.n_frames
print('Frames=',frames)

im=[tk.PhotoImage(file=file,format=f'gif -index {i}') for i in range(frames)]

#tk.PhotoImage(file=file,format=f'gif -index{0}')


#Gif function
anim=None
count=0
def gif(count):
    im2=im[count]
    gif_label.configure(image=im2)


    count+=1
    if count==frames:
        count=0

    global anim
    anim=root.after(50,lambda: gif(count))


def stop_gif():
    global anim
    root.after_cancel(anim)




gif_label=tk.Label(image='')
gif_label.pack()

#PlayButton
play_button=PhotoImage(file='play.png')
Button(root,image=play_button,bg='#C8A2C8',bd=0,height=60,width=60,command=PlayMusic).place(x=215,y=497)

#StopButton
stop_button=PhotoImage(file='stop.png')
Button(root,image=stop_button,bg='#9370DB',bd=0,height=60,width=60,command=stop).place(x=130,y=497)

pause_button=PhotoImage(file='pause.png')
Button(root,image=pause_button,bg='#3A5F0B',bd=0,height=60,width=60,command=lambda: pause(paused)).place(x=300,y=497)

#NextButton
next_button=PhotoImage(file='seek.png')
Button(root,image=next_button,bg='#FFFFFF',bd=0,height=60,width=60,command=next_song).place(x=380,y=497)


#PreviousButton
previous_button=PhotoImage(file='previous.png')
Button(root,image=previous_button,bg='#FFFFFF',bd=0,height=60,width=60,command=previous_song).place(x=50,y=497)

#RemoveSong
Button(root,text='Remove Song',width=30,height=1,font=('calibri',12,'bold'),fg='black',bg='#955251',command=delete_song).place(x=250,y=560)

#Status_bar
status_bar=Label(root,text='')#,bd=1,relief=GROOVE,anchor=E)
status_bar.pack(fill=X,side=BOTTOM,ipady=2)
#status_bar.place(x=70,y=440)


#Slider
my_slider=ttk.Scale(root,from_=0,to=100,orient=HORIZONTAL,value=0,command=slide,length=360)
my_slider.place(x=70,y=465)
#my_slider.pack(pady=338)

root.mainloop()










































