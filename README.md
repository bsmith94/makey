# makey

Projects related to working with [Makey Makey](https://makeymakey.com) HID.

## `makey_test_gui`

`makey_test_gui` is a simple UI written in python. HID events come in as keypresses. This
works in a pinch but it would be much better to process USB events. The python `usb` library
on MacOS X doesn't appear to be able to detach the USB device from kernel control.

So... keypresses it is. This works for the most part. The primary glitch is that triggering
a Makey Makey input for an extended period of time generates repeated down/up events, similar to
a keyboard's auto-repeat functionality.

Running the application:

```
# only need to do this once
$ pip3 install -r requirements.txt
# run the GUI with bird sounds triggered by the HID
$ ./makey_test_gui/makey_test_gui.py --sounds birds
```

The UI should appear with 5 buttons labeled 'P', 'R', 'M', 'I' and 'I2'. They correspond to fingers
on the hand.

![Makey Test GUI](makey_test_gui.png)


It is designed to use this controller:

![Paper Power Glove](paper_power_glove.png)


Traces are wired left to right: Left, Up, Right, Down, Space, Earth.

When an input is triggered, the associated button should expand and a sound will play.


## Licenses

Code is licensed under [GPLv2](https://www.gnu.org/licenses/old-licenses/gpl-2.0.en.html).

Sounds are licensed under Creative Commons except as noted.


## Attribution License

* `353210__tec-studio__brd3.mp3` : https://freesound.org/people/tec_studio/sounds/353210/
* `513712__luke100000__single-bird-chirp-1.wav` : https://freesound.org/people/Luke100000/sounds/513712/


Copyright (c)2022 Brian T. Smith <flatpick@gmail.com>
