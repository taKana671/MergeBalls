from direct.gui.DirectFrame import DirectFrame
import direct.gui.DirectGuiGlobals as DGG
from direct.gui.DirectLabel import DirectLabel
from direct.gui.DirectButton import DirectButton
from panda3d.core import CardMaker, LColor
from direct.interval.IntervalGlobal import Sequence, Func, Wait


class Frame(DirectFrame):

    def __init__(self, parent, hide=False):
        super().__init__(parent=parent)
        self.initialiseoptions(type(self))
        self.group = []

        if hide:
            self.hide()

    def create_group(self, *members):
        self.group.extend(members)


class Label(DirectLabel):

    def __init__(self, parent, text, pos, font, text_scale=0.2):
        super().__init__(
            parent=parent,
            text=text,
            pos=pos,
            text_fg=(1, 1, 1, 1),
            text_font=font,
            text_scale=text_scale,
            frameColor=(1, 1, 1, 0)
        )

        self.initialiseoptions(type(self))


class Button(DirectButton):

    def __init__(self, parent, text, pos, font, command, focus=False):
        super().__init__(
            parent=parent,
            relief=None,
            frameSize=(-0.3, 0.3, -0.07, 0.07),
            text=text,
            pos=pos,
            text_fg=(1, 1, 1, 1),
            text_scale=0.12,
            text_font=font,
            text_pos=(0, -0.04),
            command=command
        )

        self.initialiseoptions(type(self))

        self.focus_color = (1, 1, 1, 1)
        self.blur_color = (1, 1, 1, 0.5)
        self.btn_group = parent.group
        self.is_focus = None

        if focus:
            self.focus()
        else:
            self.blur()

        self.bind(DGG.ENTER, self.roll_over)
        self.bind(DGG.EXIT, self.roll_out)

    def roll_over(self, param=None):
        self.is_focus = True
        self.colorScaleInterval(0.2, self.focus_color, blendType='easeInOut').start()

        for btn in self.btn_group:
            if btn != self and btn.is_focus:
                btn.blur()
                break

    def roll_out(self, param=None):
        if all(not btn.is_focus for btn in self.btn_group if btn != self):
            return

        self.is_focus = False
        self.colorScaleInterval(0.2, self.blur_color, blendType='easeInOut').start()

    def focus(self):
        self.set_color_scale(self.focus_color)

    def blur(self):
        self.set_color_scale(self.blur_color)


class Screen:

    def __init__(self, gui=None):
        cm = CardMaker("card")
        cm.set_frame_fullscreen_quad()
        self.background = base.render2d.attach_new_node(cm.generate())
        self.background.set_transparency(1)
        self.background.set_color(LColor(0, 0, 0, 1.0))

        self.gui = gui

    def switch(self, gui):
        self.gui = gui

    def fade_out(self):
        Sequence(
            Func(self.gui.hide),
            self.background.colorInterval(1.0, LColor(0, 0, 0, 0)),
            Func(base.messenger.send, 'startgame')
        ).start()

    def fade_in(self):
        Sequence(
            self.background.colorInterval(1.0, LColor(0, 0, 0, 1.0)),
            Func(self.gui.show)
        ).start()

    def hide(self):
        self.gui.hide()
        self.background.hide()

    def show(self):
        self.gui.show()
        self.background.show()