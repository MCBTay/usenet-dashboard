================
usenet-dashboard
================

A dashboard for managing all usenet-related windows in one easy spot.  It's basically just an embedded web browser in a python script that has customizable tabs.

================
Dependencies
================
python, python-webkit

================
Usage
================
1. Set desired urls in pagesconfig.py
2. 'sudo chmod +x dashboard.py'
3. './dashboard.py'

================
Troubleshooting
================
--If menu icons aren't present:
   -Install dconf-tools
   -Hit alt+f2, type 'dconf-editor'
   -Change org->gnome->desktop->interface->menus-have-icons to true
   
--Similarly, if button icons aren't present (save, close, etc)
   -open dconf-editor
   -Change org->gnome->desktop->interface->buttons-have-icons to true

=================
Licensing
=================

(The MIT License)

Copyright (c) 2012 Bryan Taylor <mcbtay@gmail.com>, Spencer Smith <rsmitty1025@gmail.com>

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
