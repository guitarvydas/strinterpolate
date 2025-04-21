import sys
sys.path.insert(0, './zd')
import kernel0d as zd

#import display
try:
    [palette, env] = zd.initialize_from_files (".", ["part.drawio.json"])
    #display.Display_install (palette)
    zd.start (arg="", Part_name="main", palette=palette, env=env)
except Exception as e:
    print (f'\n\n\n*** {e}', file=sys.stderr)
    
