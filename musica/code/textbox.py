import pygame as pg
from pytube import YouTube
from moviepy.editor import *
import os
import requests

pg.init()
pg.display.set_caption("Zenék lejátszása")
screen = pg.display.set_mode((640, 480))
COLOR_INACTIVE = pg.Color('lightskyblue3')
COLOR_ACTIVE = pg.Color('dodgerblue2')
FONT = pg.font.Font(None, 32)


class Download:
    def __init__(self):
        self.url = ''
        self.name = ''
        self.path = "C:\\Users\sinka\PycharmProjects\pythonProject\Projects\Pygame\musica\\audio\\"
        self.mp4_file = f'{self.path}{self.name}.mp4'
        self.mp3_file = f'{self.path}{self.name}.mp3'
        self.seged = self.path + self.name
        self.videoclip = None
        self.audioclip = None
        self.my_video = None
        self.img_data = None
        self.img_url = ''
        self.songs = []
        self.file_list = os.listdir('../images')
        self.song_y = 20
        for file in self.file_list:
            self.songs.append(Music(file[:-4], self.song_y))
            self.song_y += 250


    def download(self):
        self.my_video = YouTube(self.url)
        self.img_url = self.my_video.thumbnail_url
        self.my_video = self.my_video.streams.get_highest_resolution()
        self.name = self.my_video.title
        self.seged = self.path + self.name
        self.my_video.download(f'{self.path}')
        self.convert()
        self.img_download()
        self.songs.append(Music(self.name, self.song_y))
        self.song_y += 250

    def convert(self):
        try:
            self.mp4_file = self.seged + '.mp4'
            self.mp3_file = self.seged + '.mp3'
            self.videoclip = VideoFileClip(self.mp4_file)
            self.audioclip = self.videoclip.audio
            self.audioclip.write_audiofile(self.mp3_file)
            self.audioclip.close()
            self.videoclip.close()
            os.remove(f'{self.path}{self.name}.mp4')
            pg.display.set_caption("Letöltés sikeres!")


        except:
            os.remove(f'{self.path}{self.name}.mp4')
            pg.display.set_caption("Letöltés sikertelen!")

    def img_download(self):
        self.img_data = requests.get(self.img_url).content
        with open(f'../images/{self.name}.jpg', 'wb') as handler:
            handler.write(self.img_data)


class InputBox:

    def __init__(self, x, y, w, h, text='https://www.youtube.com/watch?v=WKZCzeeyDv8'):
        self.rect = pg.Rect(x, y, w, h)
        self.color = COLOR_INACTIVE
        self.text = text
        self.txt_surface = FONT.render(text, True, self.color)
        self.active = False

    def handle_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False

            # Change the current color of the input box.
            self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE
        if event.type == pg.KEYDOWN:
            if self.active:
                if event.key == pg.K_RETURN:
                    print(self.text)
                    self.text = ''
                elif event.key == pg.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                # Re-render the text.
                self.txt_surface = FONT.render(self.text, True, self.color)

    def update(self):
        # Resize the box if the text is too long.
        width = max(200, self.txt_surface.get_width()+10)
        self.rect.w = width

    def draw(self, screen):
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        # Blit the rect.
        pg.draw.rect(screen, self.color, self.rect, 2)


class DoneButton:
    def __init__(self, x, y, w, h):
        self.rect = (x, y, w, h)
        self.color = (255, 255, 255)
        self.mouse = pg.mouse.get_pos()
        self.active = False

    def draw(self):
        pg.draw.rect(screen, self.color, self.rect, 0)

    def send(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            self.mouse = pg.mouse.get_pos()
            # If the user clicked on the input_box rect.
            if self.rect[0] < self.mouse[0] < self.rect[0] + self.rect[2] and self.rect[1] < self.mouse[1] < self.rect[1] + self.rect[3]:
                self.active = True
                pg.display.set_caption("Letöltés elkezdődött!")


class Music:
    def __init__(self, name, y):
        self.size = 200
        self.name = name
        self.img = pg.image.load(f'../images/{self.name}.jpg')
        self.img_transformed = pg.transform.scale(self.img, (self.size*1.33, self.size))
        self.mosue = pg.mouse.get_pos()
        self.y = y
        self.global_y = 0
        self.file_list = os.listdir('../images')

    def start(self, event):
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            self.mouse = pg.mouse.get_pos()
            # If the user clicked on the input_box rect.
            if 20 < self.mouse[0] < self.size * 1.33 + 20 and self.y < self.mouse[1] < self.size + self.y:
                pg.mixer.music.load(f'../audio/{self.name}.mp3')
                pg.mixer.music.play()
                pg.mixer.music.set_volume(0.5)

    def draw(self):
        screen.blit(self.img_transformed, (20, self.y))

    def scroll(self, event):
        if event.type == pg.MOUSEWHEEL:
            if event.y > 0 > self.global_y:
                self.y += 30
                self.global_y += 50
            elif event.y < 0: # and self.global_y > len(self.file_list) * - 180:
                self.y -= 30
                self.global_y -= 50
            elif event.y > 0:
                self.global_y = 0
            elif event.y < 0:
                pass



def main():
    clock = pg.time.Clock()
    input_box1 = InputBox(100, 100, 140, 32)
    # input_box2 = InputBox(100, 300, 140, 32)
    done_button = DoneButton(10, 100, 52, 32)
    download = Download()

    input_boxes = [input_box1]
    done_buttons = [done_button]
    done = False
    downloading = False

    while not done:
        if downloading:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    done = True
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        download.songs = []
                        download.file_list = os.listdir('../images')
                        download.song_y = 20
                        for file in download.file_list:
                            download.songs.append(Music(file[:-4], download.song_y))
                            download.song_y += 250
                        downloading = False
                        pg.display.set_caption("Zenék lejátszása")

                for box in input_boxes:
                    box.handle_event(event)
                    download.url = box.text
                for button in done_buttons:
                    button.send(event)

            for box in input_boxes:
                box.update()

            screen.fill((30, 30, 30))
            for box in input_boxes:
                box.draw(screen)
            for button in done_buttons:
                button.draw()
                if button.active:
                    download.download()
                    button.active = False
                    pg.display.set_caption("Zenék letöltése link alapján")
        else:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    done = True
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        downloading = True
                for song in download.songs:
                    song.start(event)
                    song.scroll(event)
            screen.fill((30, 30, 30))
            for song in download.songs:
                song.draw()

        pg.display.flip()
        clock.tick(30)


if __name__ == '__main__':
    main()
    pg.quit()
