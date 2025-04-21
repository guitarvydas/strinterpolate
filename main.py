import sys
sys.path.insert(0, './zd')
import kernel0d as zd

#import display
try:
    [palette, env] = zd.initialize_from_files (".", ["part.drawio.json"])
    #display.Display_install (palette)
    zd.start (arg="", Part_name="main", palette=palette, env=env)
except Exception as e:
    _, _, tb = sys.exc_info()
    print (f'\n\n\n*** at line {tb.tb_lineno}: {e}', file=sys.stderr)
    #print(f"{type(e).__name__} at line {tb.tb_lineno}: {e}")
    while tb.tb_next:
        tb = tb.tb_next
    print(f"{type(e).__name__} at line {tb.tb_lineno}: {e}", file=sys.stderr)    
    #print(f'zzz at line {tb.tb_lineno}: {e}', file=sys.stderr)    
    frame = tb.tb_frame
    filename = frame.f_code.co_filename
    line_number = tb.tb_lineno
    print(f"{type(e).__name__} at {filename}:{line_number}: {e}", file=sys.stderr)
