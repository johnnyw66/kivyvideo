
from kivy.app import App
from kivy.uix.video import Video
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import PushMatrix, PopMatrix, Rotate
from kivy.animation import Animation


class VideoWithRotation(BoxLayout):
    def __init__(self, file, angle, centre, animation=False, duration=1, **kwargs):
        super(VideoWithRotation, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.centre = centre
        self.animation = animation
        self.duration = duration
        self.video = Video(source=file, state='play', options={'eos': 'loop'})
        self.video.bind(on_texture=self.on_texture_loaded)


        with self.canvas.before:
            PushMatrix()
            self.rot = Rotate()
            self.rot.angle  = angle
            self.rot.origin = self.centre
            self.rot.axis = (0, 0, 1)
        with self.canvas.after:
            PopMatrix()

        self.add_widget(self.video)
        if (self.animation):
            self.animate()

    def on_texture_loaded(self, instance, value):
        texture_width, texture_height = instance.texture_size
        print(f"Video dimensions: {texture_width} x {texture_height}")


    def animateComplete( self, *kargs ):
        Animation.cancel_all( self ) # is this needed?
        self.rot.angle = 0
        self.animate()

    def animate( self ):
        self.anim = Animation( angle=360, duration=self.duration)
        self.anim.bind( on_complete=self.animateComplete )
        self.anim.repeat = True
        self.anim.start( self.rot )


class VideoWithRotationApp(App):
    def build(self):
        return VideoWithRotation('eg.mp4',45,(200,200), duration=30, animation=True)

if __name__ == '__main__':
    VideoWithRotationApp().run()


