import sys
sys.path.insert(0, './zd')
import kernel0d as zd

#import display

[palette, env] = zd.initialize_from_files (".", ["part.drawio.json"])
#display.Display_install (palette)
zd.start (arg="", Part_name="main", palette=palette, env=env)
