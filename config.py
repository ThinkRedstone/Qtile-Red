# Copyright (c) 2010 Aldo Cortesi
# Copyright (c) 2010, 2014 dequis
# Copyright (c) 2012 Randall Ma
# Copyright (c) 2012-2014 Tycho Andersen
# Copyright (c) 2012 Craig Barnes
# Copyright (c) 2013 horsik
# Copyright (c) 2013 Tao Sauvage
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from libqtile.config import Key, Screen, Group, Drag, Click, Match
from libqtile.command import lazy
from libqtile import layout, bar, widget
from libqtile import hook

mod = "mod1"

keys = [
    Key(
        [mod, "control"], "Left",
        lazy.screen.prev_group()
    ),
    Key(
        [mod, "control"], "Right",
        lazy.screen.next_group()
    ),

    Key([mod], "Up", lazy.layout.grow_main()),
    Key([mod], "Down", lazy.layout.shrink_main()),
    # Switch between windows in current stack pane
    Key(
        [mod], "k",
        lazy.layout.down()
    ),
    Key(
        [mod], "j",
        lazy.layout.up()
    ),

    # Move windows up or down in current stack
    Key(
        [mod, "shift"], "k",
        lazy.layout.shuffle_down()
    ),
    Key(
        [mod, "shift"], "j",
        lazy.layout.shuffle_up()
    ),

    # Switch window focus to other pane(s) of stack
    Key([mod], "Tab",
        lazy.layout.next()),

    # Swap panes of split stack
    Key(
        [mod, "shift"], "space",
        lazy.layout.rotate()
    ),

    # Clementine Controls
    Key(["control", "shift"], "KP_Up", lazy.spawn("clementine --volume-up")),
    Key(["control", "shift"], "KP_Down", lazy.spawn("clementine --volume-down")),
    Key(["control", "shift"], "KP_Left", lazy.spawn("clementine --previous")),
    Key(["control", "shift"], "KP_Right", lazy.spawn("clementine --next")),
    Key(["control", "shift"], "KP_Begin", lazy.spawn("clementine --play-pause")),

    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key(
        [mod, "shift"], "Return",
        lazy.layout.toggle_split()
    ),
    Key([mod, "control"], "t", lazy.spawn("xfce4-terminal")),
    Key([mod, "control"], "f", lazy.spawn("thunar")),

    # Toggle between different layouts as defined below9
    Key([mod], "space", lazy.next_layout()),

    Key([mod], "w", lazy.window.kill()),

    # Toggle different keyboard layouts
    Key([mod], "Caps_Lock", lazy.widget['keyboardlayout'].next_keyboard()),

    Key([mod, "mod4"], "r", lazy.restart()),
    Key([mod, "mod4"], "q", lazy.shutdown()),
    Key([mod, "mod4"], "p", lazy.spawn("maim")),

    Key([mod], "r", lazy.spawncmd()),
]
groups = [Group("a", layouts=[layout.Max(), layout.MonadTall(border_width=1, ratio=0.65)], matches=[Match(wm_class=["chromium"])]),
          Group("s", layouts=[layout.MonadTall(border_width=1, ratio=0.65), layout.Max()], matches=[Match(wm_class=["jetbrains-pycharm-ce", "jetbrains-idea-ce", "dota2"])]),
          Group("d", layouts=[layout.MonadTall(border_width=1, ratio=0.5), layout.Matrix(border_focus='#ff0000')], matches=[Match(wm_class=["Skype", "Steam"])]),
          Group("f", layouts=[layout.Stack(num_stacks=2, border_focus='#ff0000')], matches=[Match(wm_class=["Clementine", "Deluge"])]),
          Group("u", matches=[Match(wm_class=[""])]),
          Group("i", matches=[Match(wm_class=[""])]),
          Group("o", layouts=[layout.Floating()], matches=[Match(wm_class=[""])]),
          Group("p", matches=[Match(wm_class=[""])]),
          ]

for i in groups:
    # mod1 + letter of group = switch to group
    keys.append(
        Key([mod], i.name, lazy.group[i.name].toscreen())
    )

    if i.name is not "f":
        # mod1 + shift + letter of group = switch to & move focused window to group
        keys.append(
            Key([mod, "shift"], i.name, lazy.window.togroup(i.name), lazy.group[i.name].toscreen())
        )

layouts = [
    layout.Matrix(border_focus='#ff0000'), layout.MonadTall(border_width=1, ratio=0.75), layout.Max()
]

widget_defaults = dict(
    font='Arial',
    fontsize=16,
    padding=3,
)

screens = [
    Screen(
        bottom=bar.Bar(
            [
                widget.GroupBox(),
                widget.KeyboardLayout(configured_keyboards=['us', 'il']),
                widget.Prompt(),
                widget.TextBox(text=" ", width=bar.STRETCH),
                widget.Mpris(),
                widget.Systray(),
                widget.Clock(format='%I:%M %p', timezone="Asia/Jerusalem"),
            ],
            30,
        ),
    ),
]

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(),
         start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.toggle_floating())
]

dgroups_key_binder = None
dgroups_app_rules = []
main = None
follow_mouse_focus = False
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(border_focus='#ff0000')
auto_fullscreen = True
focus_on_window_activation = "smart"

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, github issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"

from subprocess import call


@hook.subscribe.startup_once
def autostart():
    call(['/home/thinkredstone/Scripts/startup_programs.sh'])


@hook.subscribe.client_new
def sort_xcom(window):
    if "XCOM" in window.name:
        window.togroup("o")
