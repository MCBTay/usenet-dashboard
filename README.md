usenet-dashboard
================

A dashboard for managing all usenet-related windows in one easy spot.  It's basically just an embedded web browser in a python script that has customizable tabs.

Dependencies:

python, python-webkit

Usage:

1. Set desired urls in pagesconfig.py
2. 'sudo chmod +x dashboard.py'
3. './dashboard.py'

Troubleshooting:

--If menu icons aren't present:
   -Install dconf-tools
   -Hit alt+f2, type 'dconf-editor'
   -Change org->gnome->desktop->interface->menus-have-icons to true
   
--Similarly, if button icons aren't present (save, close, etc)
   -open dconf-editor
   -Change org->gnome->desktop->interface->buttons-have-icons to true
