import pygame
import os

pygame.init()
pygame.mixer.init()
MUSIC_FOLDER = "music"
playlist = [os.path.join(MUSIC_FOLDER, file) for file in os.listdir(MUSIC_FOLDER) if file.endswith(".mp3")]
current_track = 0

def play_music():
    pygame.mixer.music.load(playlist[current_track])
    pygame.mixer.music.play()

def stop_music():
    pygame.mixer.music.stop()

def next_track():
    global current_track
    current_track = (current_track + 1) % len(playlist)
    play_music()

def prev_track():
    global current_track
    current_track = (current_track - 1) % len(playlist)
    play_music()

if playlist:
    play_music()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                play_music()
            elif event.key == pygame.K_s:
                stop_music()
            elif event.key == pygame.K_RIGHT:
                next_track()
            elif event.key == pygame.K_LEFT:
                prev_track()

pygame.quit()

# S - STOP, SPACE - PLAY, Стрелка вправо-следующий трек, Стрелка влево-предыдущий трек