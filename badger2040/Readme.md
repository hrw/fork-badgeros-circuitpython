<h1>Pimoroni Badger2040 </h1>

BadgerOS port (and enhancement) to CircuitPython from the original Pimoroni MicroPython version.<cr/>
<cr/>
The question is, why?<cr/>

Micropython is great but not friendly to the public. CircuitPython is better for that:<cr/>

Mount the device as a USB drive, then you can manage it by just dragging and dropping files (eg a badge text file).<cr/>

video démo on youtube : [clic on this link ](https://www.youtube.com/watch?v=mA5UjWe_tYo "clic on this link ")

![anim](pics/badgeranim.gif)

## Update March 17, 2022:
all the code has been rewritten to take into account the use of Adafruit DisplayIO libraries (with management of texts, 4 bits black & white BMP images, and also shapes). For the moment I haven't activated the battery display (I have a problem on my badger, it doesn't seem to work on battery and I haven't found yet why (maybe my device has a defect).

## todo: 
management of the battery level.

~~the "info" part~~ : done 17.03.2022<cr/>

the "prefs" part to set (in the non volatile memory) the hid parameters for the moment set in "hard" in the code by "layout = fr or layout = us <cr/>

Code the list function as in the original micropython version.<cr/>

------------



# User's Manual : 

## # create a badge:
it's quite simple in the folder "badges" just create a text file (with notepad for example) for the structure look at the file empty.txt in this directory but it gives this (one information per line):
- company
- name
- detail1_title
- detail1_text
- detail2_title
- detail2_text

and for the photo from for example the freeware "[paint.net](https://www.getpaint.net/download.html "paint.net")" you have to make an image in 104x128 pixels and save it in BMP 4 bits format.
 
## # create a HID/rubber ducky command

this function allows your Badger2040 to behave like a keyboard and send text keystrokes when connected to a computer (useful in pentesting campaigns for red teams, but we'll come back to this a little bit later).

for more information about rubber ducky scripts, [click on this link.](https://docs.hak5.org/usb-rubber-ducky-1/the-ducky-script-language/ducky-script-quick-reference "click on this link.")

to make your own, nothing more simple from a text editor create a text file in the "hid" directory and at the next reset it will appear in the available scripts press the button to launch the script.

a "hidden" hid function is present : at boot time if you hold one of the 5 buttons (a , b , c , up , down) before changing the display (which allows to keep the display unchanged) it will execute at the root the corresponding script when you release the button (the led stays on the time to release and turns off once the script is executed.

correspondence : 

- button a -> run a.txt
- button b -> run b.txt
- button c -> run c.txt
- button up -> run up.txt
- button down -> runs down.txt

and the program executes them in this order if you are fast enough you can execute for example a then c then down (it allows to prepare several fights)

once executed the badge will wait for the pressure of a button to continue towards the Launcher (the led flashes in waiting). that allows you to disconnect the badge without that the display is not changed (useful within the framework of an intrusion red team the badge continues to display an identity for example) it is more discrete and easy has to pass than a key usb rubber ducky.

## #display an image 

nothing more simple copy in the directory " images " your images 296x128 pixels in BMP 4 bits format (black and white). at the next reset they will be available in the menu.

## #Ebook function (.txt reader)

simply copy your .txt file in the ebook directory and at the next reset it will be available in the menu.