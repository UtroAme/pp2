'''music player with keybord controling'''

#library
import pygame
import os

'''init'''
pygame.init()
pygame.mixer.init()
'''set up'''
screen = pygame.display.set_mode((640, 480))
clock = pygame.time.Clock()
done = False
font = pygame.font.SysFont("comicsansms", 25)
text = font.render("[Space] Play/Pause [A] Next  [D] Previous", True, (0,0,255))


'''songs'''
playlist_file = os.path.join(os.path.dirname(__file__), "playlist", "playlist.txt")

if os.path.exists(playlist_file):
    with open(playlist_file, "r", encoding="utf-8") as f:
        songs = [line.strip() for line in f if line.strip()]
else:
    songs = []

if not songs:
    print("Playlist is empty or file not found!")
    pygame.quit()
    exit()

current_song_index = 0  
is_playing = False  


def load_and_play(index):
    '''Load and play by index'''
    global is_playing
   
    pygame.mixer.music.load(songs[index])
    pygame.mixer.music.play()
    is_playing = True

#stop
def play_pause():
    '''play or pause'''
    global is_playing
    if is_playing:
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.pause()
        else:
            pygame.mixer.music.unpause()
    else:
        load_and_play(current_song_index)


def next_track():
    """Play the next track in the playlist."""
    global current_song_index
    current_song_index = (current_song_index + 1) % len(songs)
    load_and_play(current_song_index)

def previous_track():
    """Play the previous track in the playlist."""
    global current_song_index
    current_song_index = (current_song_index - 1) % len(songs)
    load_and_play(current_song_index)

# Load the first song
load_and_play(current_song_index)

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                done = True
            elif event.key == pygame.K_SPACE:
                play_pause()
            elif event.key == pygame.K_d:
                next_track()
            elif event.key == pygame.K_a:
                previous_track()


        #Background
        screen.fill((255,255,255)) #white background
        screen.blit(text,(320 - text.get_width() // 2, 50))
        
        # Display current song name
        song_text = font.render(f"Playing: {os.path.basename(songs[current_song_index])}", True, (0, 0, 0))
        screen.blit(song_text, (320 - song_text.get_width() // 2, 200))

        # Display status
        status = "Playing" if pygame.mixer.music.get_busy() else "Paused" if is_playing else "Stopped"
        status_text = font.render(f"Status: {status}", True, (255, 0, 0))
        screen.blit(status_text, (320 - status_text.get_width() // 2, 250))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()