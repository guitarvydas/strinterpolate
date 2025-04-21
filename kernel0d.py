import sys
import re
import subprocess
import shlex
import os
import json
from collections import deque
import socket
import struct
import base64
import hashlib
import random
from repl import live_update



# this needs to be rewritten to use the low_level "shell_out“ component, this can be done solely as a diagram without using python code here#line 1
def shell_out_instantiate (reg,owner,name,template_data):#line 2
    name_with_id = gensymbol ( "shell_out")            #line 3
    cmd = shlex.split ( template_data)                 #line 4
    return make_leaf ( name_with_id, owner, cmd, shell_out_handler)#line 5#line 6#line 7

def shell_out_handler (eh,msg):                        #line 8
    cmd =  eh.instance_data                            #line 9
    s =  msg.datum.v                                   #line 10
    ret =  None                                        #line 11
    rc =  None                                         #line 12
    stdout =  None                                     #line 13
    stderr =  None                                     #line 14

    try:
        ret = subprocess.run ( cmd, input= s, text=True, capture_output=True)
        rc = ret.returncode
        stdout = ret.stdout.strip ()
        stderr = ret.stderr.strip ()
    except Exception as e:
        ret = None
        rc = 1
        stdout = ''
        stderr = str(e)
                                                       #line 15
    if  rc == 0:                                        #line 16
        send_string ( eh, "", str( stdout) +  stderr , msg)
    else:                                              #line 18
        send_string ( eh, "✗", str( stdout) +  stderr , msg)

def generate_shell_components (reg,container_list):    #line 23
    # [                                                #line 24
    #     {;file': 'simple0d.drawio', 'name': 'main', 'children': [{'name': 'Echo', 'id': 5}], 'connections': [...]},#line 25
    #     {'file': 'simple0d.drawio', 'name': '...', 'children': [], 'connections': []}#line 26
    # ]                                                #line 27
    try: 
        if  None!= container_list:                         #line 28
            for diagram in  container_list:                #line 29
                # loop through every component in the diagram and look for names that start with “$“ or “'“ #line 30
                # {'file': 'simple0d.drawio', 'name': 'main', 'children': [{'name': 'Echo', 'id': 5}], 'connections': [...]},#line 31
                for child_descriptor in  diagram [ "children"]:#line 32
                    if first_char_is ( child_descriptor [ "name"], "$"):#line 33
                        name =  child_descriptor [ "name"] #line 34
                        cmd =   name[1:] .strip ()         #line 35
                        generated_leaf = mkTemplate ( name, cmd, shell_out_instantiate)#line 36
                        register_component ( reg, generated_leaf)#line 37
                    elif first_char_is ( child_descriptor [ "name"], "'"):#line 38
                        name =  child_descriptor [ "name"] #line 39
                        s =   name[1:]                     #line 40
                        generated_leaf = mkTemplate ( name, s, string_constant_instantiate)#line 41
                        register_component_allow_overwriting ( reg, generated_leaf)#line 42#line 43#line 44#line 45#line 46
    except Exception as e:
        load_error (e)
    return  reg                                        #line 47#line 48#line 49

def first_char (s):                                    #line 50
    return   s[0]                                      #line 51#line 52#line 53

def first_char_is (s,c):                               #line 54
    return  c == first_char ( s)                       #line 55#line 56#line 57
                                                       #line 58
# TODO: #run_command needs to be rewritten to use the low_level “shell_out“ component, this can be done solely as a diagram without using python code here#line 59
# I'll keep it for now, during bootstrapping, since it mimics what is done in the Odin prototype _ both need to be revamped#line 60#line 61

def probeA_instantiate (reg,owner,name,template_data): #line 1
    name_with_id = gensymbol ( "?A")                   #line 2
    return make_leaf ( name_with_id, owner, None, probe_handler)#line 3#line 4#line 5

def probeB_instantiate (reg,owner,name,template_data): #line 6
    name_with_id = gensymbol ( "?B")                   #line 7
    return make_leaf ( name_with_id, owner, None, probe_handler)#line 8#line 9#line 10

def probeC_instantiate (reg,owner,name,template_data): #line 11
    name_with_id = gensymbol ( "?C")                   #line 12
    return make_leaf ( name_with_id, owner, None, probe_handler)#line 13#line 14#line 15

def probe_handler (eh,mev):                            #line 16
    global ticktime                                    #line 17
    s =  mev.datum.v                                   #line 18
    live_update ( "Info", "  @" + str(str ( ticktime)) +  str( "  ") +  str( "probe ") +  str( eh.name) +  str( ": ") +  str(  s[:30].replace ('\r','⦙').replace ('\n', '⧚') )      )#line 20#line 21#line 22

def trash_instantiate (reg,owner,name,template_data):  #line 23
    name_with_id = gensymbol ( "trash")                #line 24
    return make_leaf ( name_with_id, owner, None, trash_handler)#line 25#line 26#line 27

def trash_handler (eh,mev):                            #line 28
    # to appease dumped_on_floor checker               #line 29
    pass                                               #line 30#line 31

class TwoMevents:
    def __init__ (self,):                              #line 32
        self.firstmev =  None                          #line 33
        self.secondmev =  None                         #line 34#line 35
                                                       #line 36
# Deracer_States :: enum { idle, waitingForFirstmev, waitingForSecondmev }#line 37
class Deracer_Instance_Data:
    def __init__ (self,):                              #line 38
        self.state =  None                             #line 39
        self.buffer =  None                            #line 40#line 41
                                                       #line 42
def reclaim_Buffers_from_heap (inst):                  #line 43
    pass                                               #line 44#line 45#line 46

def deracer_instantiate (reg,owner,name,template_data):#line 47
    name_with_id = gensymbol ( "deracer")              #line 48
    inst =  Deracer_Instance_Data ()                   #line 49
    inst.state =  "idle"                               #line 50
    inst.buffer =  TwoMevents ()                       #line 51
    eh = make_leaf ( name_with_id, owner, inst, deracer_handler)#line 52
    return  eh                                         #line 53#line 54#line 55

def send_firstmev_then_secondmev (eh,inst):            #line 56
    forward ( eh, "1", inst.buffer.firstmev)           #line 57
    forward ( eh, "2", inst.buffer.secondmev)          #line 58
    reclaim_Buffers_from_heap ( inst)                  #line 59#line 60#line 61

def deracer_handler (eh,mev):                          #line 62
    inst =  eh.instance_data                           #line 63
    if  inst.state ==  "idle":                         #line 64
        if  "1" ==  mev.port:                          #line 65
            inst.buffer.firstmev =  mev                #line 66
            inst.state =  "waitingForSecondmev"        #line 67
        elif  "2" ==  mev.port:                        #line 68
            inst.buffer.secondmev =  mev               #line 69
            inst.state =  "waitingForFirstmev"         #line 70
        else:                                          #line 71
            runtime_error ( str( "bad mev.port (case A) for deracer port=") +  mev.port )#line 72#line 73
    elif  inst.state ==  "waitingForFirstmev":         #line 74
        if  "1" ==  mev.port:                          #line 75
            inst.buffer.firstmev =  mev                #line 76
            send_firstmev_then_secondmev ( eh, inst)   #line 77
            inst.state =  "idle"                       #line 78
        else:                                          #line 79
            runtime_error ( str( "bad mev.port (case B) for deracer port=") +  mev.port )#line 80#line 81
    elif  inst.state ==  "waitingForSecondmev":        #line 82
        if  "2" ==  mev.port:                          #line 83
            inst.buffer.secondmev =  mev               #line 84
            send_firstmev_then_secondmev ( eh, inst)   #line 85
            inst.state =  "idle"                       #line 86
        else:                                          #line 87
            runtime_error ( str( "bad mev.port (case C) for deracer port=") +  mev.port )#line 88#line 89
    else:                                              #line 90
        runtime_error ( "bad state for deracer {eh.state}")#line 91#line 92#line 93#line 94

def low_level_read_text_file_instantiate (reg,owner,name,template_data):#line 95
    name_with_id = gensymbol ( "Low Level Read Text File")#line 96
    return make_leaf ( name_with_id, owner, None, low_level_read_text_file_handler)#line 97#line 98#line 99

def low_level_read_text_file_handler (eh,mev):         #line 100
    fname =  mev.datum.v                               #line 101

    try:
        f = open (fname)
    except Exception as e:
        f = None
    if f != None:
        data = f.read ()
        if data!= None:
            send_string (eh, "", data, mev)
        else:
            send_string (eh, "✗", f"read error on file '{fname}'", mev)
        f.close ()
    else:
        send_string (eh, "✗", f"open error on file '{fname}'", mev)
                                                       #line 102#line 103#line 104

def ensure_string_datum_instantiate (reg,owner,name,template_data):#line 105
    name_with_id = gensymbol ( "Ensure String Datum")  #line 106
    return make_leaf ( name_with_id, owner, None, ensure_string_datum_handler)#line 107#line 108#line 109

def ensure_string_datum_handler (eh,mev):              #line 110
    if  "string" ==  mev.datum.kind ():                #line 111
        forward ( eh, "", mev)                         #line 112
    else:                                              #line 113
        emev =  str( "*** ensure: type error (expected a string datum) but got ") +  mev.datum #line 114
        send_string ( eh, "✗", emev, mev)              #line 115#line 116#line 117#line 118

class Syncfilewrite_Data:
    def __init__ (self,):                              #line 119
        self.filename =  ""                            #line 120#line 121
                                                       #line 122
# temp copy for bootstrap, sends "done“ (error during bootstrap if not wired)#line 123
def syncfilewrite_instantiate (reg,owner,name,template_data):#line 124
    name_with_id = gensymbol ( "syncfilewrite")        #line 125
    inst =  Syncfilewrite_Data ()                      #line 126
    return make_leaf ( name_with_id, owner, inst, syncfilewrite_handler)#line 127#line 128#line 129

def syncfilewrite_handler (eh,mev):                    #line 130
    inst =  eh.instance_data                           #line 131
    if  "filename" ==  mev.port:                       #line 132
        inst.filename =  mev.datum.v                   #line 133
    elif  "input" ==  mev.port:                        #line 134
        contents =  mev.datum.v                        #line 135
        f = open ( inst.filename, "w")                 #line 136
        if  f!= None:                                  #line 137
            f.write ( mev.datum.v)                     #line 138
            f.close ()                                 #line 139
            send ( eh, "done",new_datum_bang (), mev)  #line 140
        else:                                          #line 141
            send_string ( eh, "✗", str( "open error on file ") +  inst.filename , mev)#line 142#line 143#line 144#line 145#line 146

class StringConcat_Instance_Data:
    def __init__ (self,):                              #line 147
        self.buffer1 =  None                           #line 148
        self.buffer2 =  None                           #line 149#line 150
                                                       #line 151
def stringconcat_instantiate (reg,owner,name,template_data):#line 152
    name_with_id = gensymbol ( "stringconcat")         #line 153
    instp =  StringConcat_Instance_Data ()             #line 154
    return make_leaf ( name_with_id, owner, instp, stringconcat_handler)#line 155#line 156#line 157

def stringconcat_handler (eh,mev):                     #line 158
    inst =  eh.instance_data                           #line 159
    if  "1" ==  mev.port:                              #line 160
        inst.buffer1 = clone_string ( mev.datum.v)     #line 161
        maybe_stringconcat ( eh, inst, mev)            #line 162
    elif  "2" ==  mev.port:                            #line 163
        inst.buffer2 = clone_string ( mev.datum.v)     #line 164
        maybe_stringconcat ( eh, inst, mev)            #line 165
    elif  "reset" ==  mev.port:                        #line 166
        inst.buffer1 =  None                           #line 167
        inst.buffer2 =  None                           #line 168
    else:                                              #line 169
        runtime_error ( str( "bad mev.port for stringconcat: ") +  mev.port )#line 170#line 171#line 172#line 173

def maybe_stringconcat (eh,inst,mev):                  #line 174
    if  inst.buffer1!= None and  inst.buffer2!= None:  #line 175
        concatenated_string =  ""                      #line 176
        if  0 == len ( inst.buffer1):                  #line 177
            concatenated_string =  inst.buffer2        #line 178
        elif  0 == len ( inst.buffer2):                #line 179
            concatenated_string =  inst.buffer1        #line 180
        else:                                          #line 181
            concatenated_string =  inst.buffer1+ inst.buffer2#line 182#line 183
        send_string ( eh, "", concatenated_string, mev)#line 184
        inst.buffer1 =  None                           #line 185
        inst.buffer2 =  None                           #line 186#line 187#line 188#line 189

#                                                      #line 190#line 191
def string_constant_instantiate (reg,owner,name,template_data):#line 192
    global root_project                                #line 193
    global root_0D                                     #line 194
    name_with_id = gensymbol ( "strconst")             #line 195
    s =  template_data                                 #line 196
    if  root_project!= "":                             #line 197
        s = re.sub ( "_00_",  root_project,  s)        #line 198#line 199
    if  root_0D!= "":                                  #line 200
        s = re.sub ( "_0D_",  root_0D,  s)             #line 201#line 202
    return make_leaf ( name_with_id, owner, s, string_constant_handler)#line 203#line 204#line 205

def string_constant_handler (eh,mev):                  #line 206
    s =  eh.instance_data                              #line 207
    send_string ( eh, "", s, mev)                      #line 208#line 209#line 210

def fakepipename_instantiate (reg,owner,name,template_data):#line 211
    instance_name = gensymbol ( "fakepipe")            #line 212
    return make_leaf ( instance_name, owner, None, fakepipename_handler)#line 213#line 214#line 215

rand =  0                                              #line 216#line 217
def fakepipename_handler (eh,mev):                     #line 218
    global rand                                        #line 219
    rand =  rand+ 1
    # not very random, but good enough _ 'rand' must be unique within a single run#line 220
    send_string ( eh, "", str( "/tmp/fakepipe") +  rand , mev)#line 221#line 222#line 223
                                                       #line 224
class Switch1star_Instance_Data:
    def __init__ (self,):                              #line 225
        self.state =  "1"                              #line 226#line 227
                                                       #line 228
def switch1star_instantiate (reg,owner,name,template_data):#line 229
    name_with_id = gensymbol ( "switch1*")             #line 230
    instp =  Switch1star_Instance_Data ()              #line 231
    return make_leaf ( name_with_id, owner, instp, switch1star_handler)#line 232#line 233#line 234

def switch1star_handler (eh,mev):                      #line 235
    inst =  eh.instance_data                           #line 236
    whichOutput =  inst.state                          #line 237
    if  "" ==  mev.port:                               #line 238
        if  "1" ==  whichOutput:                       #line 239
            forward ( eh, "1", mev)                    #line 240
            inst.state =  "*"                          #line 241
        elif  "*" ==  whichOutput:                     #line 242
            forward ( eh, "*", mev)                    #line 243
        else:                                          #line 244
            send ( eh, "✗", "internal error bad state in switch1*", mev)#line 245#line 246
    elif  "reset" ==  mev.port:                        #line 247
        inst.state =  "1"                              #line 248
    else:                                              #line 249
        send ( eh, "✗", "internal error bad mevent for switch1*", mev)#line 250#line 251#line 252#line 253

class StringAccumulator:
    def __init__ (self):
        self.s = ""

def strcatstar_instantiate (reg, owner, name, template_data):
    name_with_id = gensymbol ("String Concat *")
    instp = StringAccumulator ()
    return make_leaf ( name_with_id, owner, instp, strcatstar_handler)

def strcatstar_handler (eh, mev):
    accum = eh.instance_data
    if "" == mev.port:
        accum.s = accum.s + mev.datum.v
    elif "fini" == mev.port:
        send_string (eh, "", accum.s, mev)
    else:
        send_string ( eh, "✗", "internal error bad mevent for String Concat *", mev)
        

# all of the the built_in leaves are listed here       #line 282
# future: refactor this such that programmers can pick and choose which (lumps of) builtins are used in a specific project#line 283#line 284
def initialize_stock_components (reg):                 #line 285
    register_component ( reg,mkTemplate ( "1then2", None, deracer_instantiate))#line 286
    register_component ( reg,mkTemplate ( "?A", None, probeA_instantiate))#line 287
    register_component ( reg,mkTemplate ( "?B", None, probeB_instantiate))#line 288
    register_component ( reg,mkTemplate ( "?C", None, probeC_instantiate))#line 289
    register_component ( reg,mkTemplate ( "trash", None, trash_instantiate))#line 290#line 291
    register_component ( reg,mkTemplate ( "Read Text File", None, low_level_read_text_file_instantiate))#line 292
    register_component ( reg,mkTemplate ( "Ensure String Datum", None, ensure_string_datum_instantiate))#line 293#line 294
    register_component ( reg,mkTemplate ( "syncfilewrite", None, syncfilewrite_instantiate))#line 295
    register_component ( reg,mkTemplate ( "stringconcat", None, stringconcat_instantiate))#line 296
    register_component ( reg,mkTemplate ( "switch1*", None, switch1star_instantiate))#line 297
    register_component ( reg,mkTemplate ( "String Concat *", None, strcatstar_instantiate))
    # for fakepipe                                     #line 299
    register_component ( reg,mkTemplate ( "fakepipename", None, fakepipename_instantiate))#line 300#line 301#line 302



#

def deque_to_json(d):
    # """
    # Convert a deque of Mevent objects to a JSON string, preserving order.
    # Each Mevent object is converted to a dict with a single key (from Mevent.key)
    # containing the payload as its value.

    # Args:
    #     d: The deque of Mevent objects to convert

    # Returns:
    #     A JSON string representation of the deque
    # """
    # # Convert deque to list of objects where each mevent's key contains its payload
    ordered_list = [{mev.port: "" if mev.datum.v is None else mev.datum.v} for mev in d]

    # # Convert to JSON with indentation for readability
    return json.dumps(ordered_list, indent=2)


                                                       #line 1#line 2
counter =  0                                           #line 3
ticktime =  0                                          #line 4#line 5
# digits = [ "₀", "₁", "₂", "₃", "₄", "₅", "₆", "₇", "₈", "₉", "₁₀", "₁₁", "₁₂", "₁₃", "₁₄", "₁₅", "₁₆", "₁₇", "₁₈", "₁₉", "₂₀", "₂₁", "₂₂", "₂₃", "₂₄", "₂₅", "₂₆", "₂₇", "₂₈", "₂₉"]#line 12#line 13#line 14
digits = [ "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26", "27", "28", "29"]#line 12#line 13#line 14
def gensymbol (s):                                     #line 15
    global counter                                     #line 16
    name_with_id =  str( s) + subscripted_digit ( counter) #line 17
    counter =  counter+ 1                              #line 18
    return  name_with_id                               #line 19#line 20#line 21

def subscripted_digit (n):                             #line 22
    global digits                                      #line 23
    if ( n >=  0 and  n <=  29):                       #line 24
        return  digits [ n]                            #line 25
    else:                                              #line 26
        return  str( "₊") + str ( n)                   #line 27#line 28#line 29#line 30

class Datum:
    def __init__ (self,):                              #line 31
        self.v =  None                                 #line 32
        self.clone =  None                             #line 33
        self.reclaim =  None                           #line 34
        self.other =  None # reserved for use on per-project basis #line 35#line 36
                                                       #line 37
def new_datum_string (s):                              #line 38
    d =  Datum ()                                      #line 39
    d.v =  s                                           #line 40
    d.clone =  lambda : clone_datum_string ( d)        #line 41
    d.reclaim =  lambda : reclaim_datum_string ( d)    #line 42
    return  d                                          #line 43#line 44#line 45

def clone_datum_string (d):                            #line 46
    newd = new_datum_string ( d.v)                     #line 47
    return  newd                                       #line 48#line 49#line 50

def reclaim_datum_string (src):                        #line 51
    pass                                               #line 52#line 53#line 54

def new_datum_bang ():                                 #line 55
    p =  Datum ()                                      #line 56
    p.v =  ""                                          #line 57
    p.clone =  lambda : clone_datum_bang ( p)          #line 58
    p.reclaim =  lambda : reclaim_datum_bang ( p)      #line 59
    return  p                                          #line 60#line 61#line 62

def clone_datum_bang (d):                              #line 63
    return new_datum_bang ()                           #line 64#line 65#line 66

def reclaim_datum_bang (d):                            #line 67
    pass                                               #line 68#line 69#line 70

# Mevent passed to a leaf component.                   #line 71
#                                                      #line 72
# `port` refers to the name of the incoming or outgoing port of this component.#line 73
# `payload` is the data attached to this mevent.       #line 74
class Mevent:
    def __init__ (self,):                              #line 75
        self.port =  None                              #line 76
        self.datum =  None                             #line 77#line 78
                                                       #line 79
def clone_port (s):                                    #line 80
    return clone_string ( s)                           #line 81#line 82#line 83

# Utility for making a `Mevent`. Used to safely "seed“ mevents#line 84
# entering the very top of a network.                  #line 85
def make_mevent (port,datum):                          #line 86
    p = clone_string ( port)                           #line 87
    m =  Mevent ()                                     #line 88
    m.port =  p                                        #line 89
    m.datum =  datum.clone ()                          #line 90
    return  m                                          #line 91#line 92#line 93

# Clones a mevent. Primarily used internally for “fanning out“ a mevent to multiple destinations.#line 94
def mevent_clone (mev):                                #line 95
    m =  Mevent ()                                     #line 96
    m.port = clone_port ( mev.port)                    #line 97
    m.datum =  mev.datum.clone ()                      #line 98
    return  m                                          #line 99#line 100#line 101

# Frees a mevent.                                      #line 102
def destroy_mevent (mev):                              #line 103
    # during debug, dont destroy any mevent, since we want to trace mevents, thus, we need to persist ancestor mevents#line 104
    pass                                               #line 105#line 106#line 107

def destroy_datum (mev):                               #line 108
    pass                                               #line 109#line 110#line 111

def destroy_port (mev):                                #line 112
    pass                                               #line 113#line 114#line 115

#                                                      #line 116
def format_mevent (m):                                 #line 117
    if  m ==  None:                                    #line 118
        return  "{}"                                   #line 119
    else:                                              #line 120
        return  str( "{\"") +  str( m.port) +  str( "\":\"") +  str( m.datum.v) +  "\"}"    #line 121#line 122#line 123

def format_mevent_raw (m):                             #line 124
    if  m ==  None:                                    #line 125
        return  ""                                     #line 126
    else:                                              #line 127
        return  m.datum.v                              #line 128#line 129#line 130#line 131

enumDown =  0                                          #line 132
enumAcross =  1                                        #line 133
enumUp =  2                                            #line 134
enumThrough =  3                                       #line 135#line 136
def create_down_connector (container,proto_conn,connectors,children_by_id):#line 137
    # JSON: {;dir': 0, 'source': {'name': '', 'id': 0}, 'source_port': '', 'target': {'name': 'Echo', 'id': 12}, 'target_port': ''},#line 138
    connector =  Connector ()                          #line 139
    connector.direction =  "down"                      #line 140
    connector.sender = mkSender ( container.name, container, proto_conn [ "source_port"])#line 141
    target_proto =  proto_conn [ "target"]             #line 142
    id_proto =  target_proto [ "id"]                   #line 143
    target_component =  children_by_id [id_proto]      #line 144
    if ( target_component ==  None):                   #line 145
        load_error ( str( "internal error: .Down connection target internal error ") + ( proto_conn [ "target"]) [ "name"] )#line 146
    else:                                              #line 147
        connector.receiver = mkReceiver ( target_component.name, target_component, proto_conn [ "target_port"], target_component.inq)#line 148#line 149
    return  connector                                  #line 150#line 151#line 152

def create_across_connector (container,proto_conn,connectors,children_by_id):#line 153
    connector =  Connector ()                          #line 154
    connector.direction =  "across"                    #line 155
    source_component =  children_by_id [(( proto_conn [ "source"]) [ "id"])]#line 156
    target_component =  children_by_id [(( proto_conn [ "target"]) [ "id"])]#line 157
    if  source_component ==  None:                     #line 158
        load_error ( str( "internal error: .Across connection source not ok ") + ( proto_conn [ "source"]) [ "name"] )#line 159
    else:                                              #line 160
        connector.sender = mkSender ( source_component.name, source_component, proto_conn [ "source_port"])#line 161
        if  target_component ==  None:                 #line 162
            load_error ( str( "internal error: .Across connection target not ok ") + ( proto_conn [ "target"]) [ "name"] )#line 163
        else:                                          #line 164
            connector.receiver = mkReceiver ( target_component.name, target_component, proto_conn [ "target_port"], target_component.inq)#line 165#line 166#line 167
    return  connector                                  #line 168#line 169#line 170

def create_up_connector (container,proto_conn,connectors,children_by_id):#line 171
    connector =  Connector ()                          #line 172
    connector.direction =  "up"                        #line 173
    source_component =  children_by_id [(( proto_conn [ "source"]) [ "id"])]#line 174
    if  source_component ==  None:                     #line 175
        load_error ( str( "internal error: .Up connection source not ok ") + ( proto_conn [ "source"]) [ "name"] )#line 176
    else:                                              #line 177
        connector.sender = mkSender ( source_component.name, source_component, proto_conn [ "source_port"])#line 178
        connector.receiver = mkReceiver ( container.name, container, proto_conn [ "target_port"], container.outq)#line 179#line 180
    return  connector                                  #line 181#line 182#line 183

def create_through_connector (container,proto_conn,connectors,children_by_id):#line 184
    connector =  Connector ()                          #line 185
    connector.direction =  "through"                   #line 186
    connector.sender = mkSender ( container.name, container, proto_conn [ "source_port"])#line 187
    connector.receiver = mkReceiver ( container.name, container, proto_conn [ "target_port"], container.outq)#line 188
    return  connector                                  #line 189#line 190#line 191
                                                       #line 192
def container_instantiator (reg,owner,container_name,desc):#line 193
    global enumDown, enumUp, enumAcross, enumThrough   #line 194
    container = make_container ( container_name, owner)#line 195
    children = []                                      #line 196
    children_by_id = {}
    # not strictly necessary, but, we can remove 1 runtime lookup by “compiling it out“ here#line 197
    # collect children                                 #line 198
    for child_desc in  desc [ "children"]:             #line 199
        child_instance = get_component_instance ( reg, child_desc [ "name"], container)#line 200
        children.append ( child_instance)              #line 201
        id =  child_desc [ "id"]                       #line 202
        children_by_id [id] =  child_instance          #line 203#line 204#line 205
    container.children =  children                     #line 206#line 207
    connectors = []                                    #line 208
    for proto_conn in  desc [ "connections"]:          #line 209
        connector =  Connector ()                      #line 210
        if  proto_conn [ "dir"] ==  enumDown:          #line 211
            connectors.append (create_down_connector ( container, proto_conn, connectors, children_by_id)) #line 212
        elif  proto_conn [ "dir"] ==  enumAcross:      #line 213
            connectors.append (create_across_connector ( container, proto_conn, connectors, children_by_id)) #line 214
        elif  proto_conn [ "dir"] ==  enumUp:          #line 215
            connectors.append (create_up_connector ( container, proto_conn, connectors, children_by_id)) #line 216
        elif  proto_conn [ "dir"] ==  enumThrough:     #line 217
            connectors.append (create_through_connector ( container, proto_conn, connectors, children_by_id)) #line 218#line 219#line 220
    container.connections =  connectors                #line 221
    return  container                                  #line 222#line 223#line 224

# The default handler for container components.        #line 225
def container_handler (container,mevent):              #line 226
    route ( container, container, mevent)
    # references to 'self' are replaced by the container during instantiation#line 227
    while any_child_ready ( container):                #line 228
        step_children ( container, mevent)             #line 229#line 230#line 231

# Frees the given container and associated data.       #line 232
def destroy_container (eh):                            #line 233
    pass                                               #line 234#line 235#line 236

# Routing connection for a container component. The `direction` field has#line 237
# no affect on the default mevent routing system _ it is there for debugging#line 238
# purposes, or for reading by other tools.             #line 239#line 240
class Connector:
    def __init__ (self,):                              #line 241
        self.direction =  None # down, across, up, through#line 242
        self.sender =  None                            #line 243
        self.receiver =  None                          #line 244#line 245
                                                       #line 246
# `Sender` is used to “pattern match“ which `Receiver` a mevent should go to,#line 247
# based on component ID (pointer) and port name.       #line 248#line 249
class Sender:
    def __init__ (self,):                              #line 250
        self.name =  None                              #line 251
        self.component =  None                         #line 252
        self.port =  None                              #line 253#line 254
                                                       #line 255#line 256#line 257
# `Receiver` is a handle to a destination queue, and a `port` name to assign#line 258
# to incoming mevents to this queue.                   #line 259#line 260
class Receiver:
    def __init__ (self,):                              #line 261
        self.name =  None                              #line 262
        self.queue =  None                             #line 263
        self.port =  None                              #line 264
        self.component =  None                         #line 265#line 266
                                                       #line 267
def mkSender (name,component,port):                    #line 268
    s =  Sender ()                                     #line 269
    s.name =  name                                     #line 270
    s.component =  component                           #line 271
    s.port =  port                                     #line 272
    return  s                                          #line 273#line 274#line 275

def mkReceiver (name,component,port,q):                #line 276
    r =  Receiver ()                                   #line 277
    r.name =  name                                     #line 278
    r.component =  component                           #line 279
    r.port =  port                                     #line 280
    # We need a way to determine which queue to target. "Down" and "Across" go to inq, "Up" and "Through" go to outq.#line 281
    r.queue =  q                                       #line 282
    return  r                                          #line 283#line 284#line 285

# Checks if two senders match, by pointer equality and port name matching.#line 286
def sender_eq (s1,s2):                                 #line 287
    same_components = ( s1.component ==  s2.component) #line 288
    same_ports = ( s1.port ==  s2.port)                #line 289
    return  same_components and  same_ports            #line 290#line 291#line 292

# Delivers the given mevent to the receiver of this connector.#line 293#line 294
def deposit (parent,conn,mevent):                      #line 295
    new_mevent = make_mevent ( conn.receiver.port, mevent.datum)#line 296
    push_mevent ( parent, conn.receiver.component, conn.receiver.queue, new_mevent)#line 297#line 298#line 299

def force_tick (parent,eh):                            #line 300
    tick_mev = make_mevent ( ".",new_datum_bang ())    #line 301
    push_mevent ( parent, eh, eh.inq, tick_mev)        #line 302
    return  tick_mev                                   #line 303#line 304#line 305

def push_mevent (parent,receiver,inq,m):               #line 306
    inq.append ( m)                                    #line 307
    parent.visit_ordering.append ( receiver)           #line 308#line 309#line 310

def is_self (child,container):                         #line 311
    # in an earlier version “self“ was denoted as ϕ    #line 312
    return  child ==  container                        #line 313#line 314#line 315

def step_child (child,mev):                            #line 316
    global ticktime
    before_state =  child.state                        #line 317
    # live_update ("Info", child.name) ## for debugging bootstrap
    # live_update ("Info", str (ticktime)) ## for debugging bootstrap
    child.handler ( child, mev)                        #line 318
    after_state =  child.state                         #line 319
    return [ before_state ==  "idle" and  after_state!= "idle", before_state!= "idle" and  after_state!= "idle", before_state!= "idle" and  after_state ==  "idle"]#line 322#line 323#line 324

def step_children (container,causingMevent):           #line 325
    container.state =  "idle"                          #line 326
    for child in  list ( container.visit_ordering):    #line 327
        # child = container represents self, skip it   #line 328
        if (not (is_self ( child, container))):        #line 329
            if (not ((0==len( child.inq)))):           #line 330
                mev =  child.inq.popleft ()            #line 331
                began_long_run =  None                 #line 332
                continued_long_run =  None             #line 333
                ended_long_run =  None                 #line 334
                [ began_long_run, continued_long_run, ended_long_run] = step_child ( child, mev)#line 335
                if  began_long_run:                    #line 336
                    pass                               #line 337
                elif  continued_long_run:              #line 338
                    pass                               #line 339
                elif  ended_long_run:                  #line 340
                    pass                               #line 341#line 342
                destroy_mevent ( mev)                  #line 343
            else:                                      #line 344
                if  child.state!= "idle":              #line 345
                    mev = force_tick ( container, child)#line 346
                    child.handler ( child, mev)        #line 347
                    destroy_mevent ( mev)              #line 348#line 349#line 350#line 351
            if  child.state ==  "active":              #line 352
                # if child remains active, then the container must remain active and must propagate “ticks“ to child#line 353
                container.state =  "active"            #line 354#line 355#line 356
            while (not ((0==len( child.outq)))):       #line 357
                mev =  child.outq.popleft ()           #line 358
                route ( container, child, mev)         #line 359
                destroy_mevent ( mev)                  #line 360#line 361#line 362#line 363#line 364#line 365

def attempt_tick (parent,eh):                          #line 366
    if  eh.state!= "idle":                             #line 367
        force_tick ( parent, eh)                       #line 368#line 369#line 370#line 371

def is_tick (mev):                                     #line 372
    return  "." ==  mev.port
    # assume that any mevent that is sent to port "." is a tick #line 373#line 374#line 375

# Routes a single mevent to all matching destinations, according to#line 376
# the container's connection network.                  #line 377#line 378
def route (container,from_component,mevent):           #line 379
    was_sent =  False
    # for checking that output went somewhere (at least during bootstrap)#line 380
    fromname =  ""                                     #line 381
    global ticktime                                    #line 382
    ticktime =  ticktime+ 1                            #line 383
    if is_tick ( mevent):                              #line 384
        for child in  container.children:              #line 385
            attempt_tick ( container, child)           #line 386
        was_sent =  True                               #line 387
    else:                                              #line 388
        if (not (is_self ( from_component, container))):#line 389
            fromname =  from_component.name            #line 390#line 391
        from_sender = mkSender ( fromname, from_component, mevent.port)#line 392#line 393
        for connector in  container.connections:       #line 394
            if sender_eq ( from_sender, connector.sender):#line 395
                deposit ( container, connector, mevent)#line 396
                was_sent =  True                       #line 397#line 398#line 399#line 400
    if not ( was_sent):                                #line 401
        live_update ("✗", str( container.name) +  str( ": mevent '") +  str( mevent.port) +  str( "' from ") +  str( fromname) +  " dropped on floor...") + f"\n/{mevent.datum.v}/"

def any_child_ready (container):                       #line 410
    for child in  container.children:                  #line 411
        if child_is_ready ( child):                    #line 412
            return  True                               #line 413#line 414#line 415
    return  False                                      #line 416#line 417#line 418

def child_is_ready (eh):                               #line 419
    return (not ((0==len( eh.outq)))) or (not ((0==len( eh.inq)))) or ( eh.state!= "idle") or (any_child_ready ( eh))#line 420#line 421#line 422

def append_routing_descriptor (container,desc):        #line 423
    container.routings.append ( desc)                  #line 424#line 425#line 426

def container_injector (container,mevent):             #line 427
    container_handler ( container, mevent)             #line 428#line 429#line 430
                                                       #line 431#line 432#line 433
class Component_Registry:
    def __init__ (self,):                              #line 434
        self.templates = {}                            #line 435#line 436
                                                       #line 437
class Template:
    def __init__ (self,):                              #line 438
        self.name =  None                              #line 439
        self.template_data =  None                     #line 440
        self.instantiator =  None                      #line 441#line 442
                                                       #line 443
def mkTemplate (name,template_data,instantiator):      #line 444
    templ =  Template ()                               #line 445
    templ.name =  name                                 #line 446
    templ.template_data =  template_data               #line 447
    templ.instantiator =  instantiator                 #line 448
    return  templ                                      #line 449#line 450#line 451

def read_and_convert_json_file (pathname,filename):    #line 452
    try:
        fil = open(filename, "r")
        json_data = fil.read()
        routings = json.loads(json_data)
        fil.close ()
        return routings
    except FileNotFoundError:
        print (f"File not found: '{filename}'")
        return None
    except json.JSONDecodeError as e:
        print (f"Error decoding JSON in file: '{e}'")
        return None
                                                       #line 453#line 454#line 455

def json2internal (pathname,container_xml):            #line 456
    fname =  os.path.basename ( container_xml)         #line 457
    routings = read_and_convert_json_file ( pathname, fname)#line 458
    return  routings                                   #line 459#line 460#line 461

def delete_decls (d):                                  #line 462
    pass                                               #line 463#line 464#line 465

def make_component_registry ():                        #line 466
    return  Component_Registry ()                      #line 467#line 468#line 469

def register_component (reg,template):
    return abstracted_register_component ( reg, template, False)#line 470

def register_component_allow_overwriting (reg,template):
    return abstracted_register_component ( reg, template, True)#line 471#line 472

def abstracted_register_component (reg,template,ok_to_overwrite):#line 473
    name = mangle_name ( template.name)                #line 474
    if  reg!= None and  name in  reg.templates and not  ok_to_overwrite:#line 475
        load_error ( str( "Component /") +  str( template.name) +  "/ already declared"  )#line 476
        return  reg                                    #line 477
    else:                                              #line 478
        reg.templates [name] =  template               #line 479
        return  reg                                    #line 480#line 481#line 482#line 483

def get_component_instance (reg,full_name,owner):      #line 484
    template_name = mangle_name ( full_name)           #line 485
    if  template_name in  reg.templates:               #line 486
        template =  reg.templates [template_name]      #line 487
        if ( template ==  None):                       #line 488
            load_error ( str( "Registry Error (A): Can't find component /") +  str( template_name) +  "/"  )#line 489
            return  None                               #line 490
        else:                                          #line 491
            owner_name =  ""                           #line 492
            instance_name =  template_name             #line 493
            if  None!= owner:                          #line 494
                owner_name =  owner.name               #line 495
                instance_name =  str( owner_name) +  str( "▹") +  template_name  #line 496
            else:                                      #line 497
                instance_name =  template_name         #line 498#line 499
            instance =  template.instantiator ( reg, owner, instance_name, template.template_data)#line 500
            return  instance                           #line 501#line 502
    else:                                              #line 503
        load_error ( str( "Registry Error (B): Can't find component /") +  str( template_name) +  "/"  )#line 504
        return  None                                   #line 505#line 506#line 507#line 508

def dump_registry (reg):                               #line 509
    nl ()                                              #line 510
    print ( "*** PALETTE ***")                         #line 511
    for c in  reg.templates:                           #line 512
        print ( c.name)                                #line 513
    print ( "***************")                         #line 514
    nl ()                                              #line 515#line 516#line 517

def print_stats (reg):                                 #line 518
    print ( str( "registry statistics: ") +  reg.stats )#line 519#line 520#line 521

def mangle_name (s):                                   #line 522
    # trim name to remove code from Container component names _ deferred until later (or never)#line 523
    return  s                                          #line 524#line 525#line 526
                                                       #line 527
# Data for an asyncronous component _ effectively, a function with input#line 528
# and output queues of mevents.                        #line 529
#                                                      #line 530
# Components can either be a user_supplied function (“lea“), or a “container“#line 531
# that routes mevents to child components according to a list of connections#line 532
# that serve as a mevent routing table.                #line 533
#                                                      #line 534
# Child components themselves can be leaves or other containers.#line 535
#                                                      #line 536
# `handler` invokes the code that is attached to this component.#line 537
#                                                      #line 538
# `instance_data` is a pointer to instance data that the `leaf_handler`#line 539
# function may want whenever it is invoked again.      #line 540
#                                                      #line 541#line 542
# Eh_States :: enum { idle, active }                   #line 543
class Eh:
    def __init__ (self,):                              #line 544
        self.name =  ""                                #line 545
        self.inq =  deque ([])                         #line 546
        self.outq =  deque ([])                        #line 547
        self.owner =  None                             #line 548
        self.children = []                             #line 549
        self.visit_ordering =  deque ([])              #line 550
        self.connections = []                          #line 551
        self.routings =  deque ([])                    #line 552
        self.handler =  None                           #line 553
        self.finject =  None                           #line 554
        self.instance_data =  None                     #line 555
        self.state =  "idle"                           #line 556# bootstrap debugging#line 557
        self.kind =  None # enum { container, leaf, }  #line 558#line 559
                                                       #line 560
# Creates a component that acts as a container. It is the same as a `Eh` instance#line 561
# whose handler function is `container_handler`.       #line 562
def make_container (name,owner):                       #line 563
    eh =  Eh ()                                        #line 564
    eh.name =  name                                    #line 565
    eh.owner =  owner                                  #line 566
    eh.handler =  container_handler                    #line 567
    eh.finject =  container_injector                   #line 568
    eh.state =  "idle"                                 #line 569
    eh.kind =  "container"                             #line 570
    return  eh                                         #line 571#line 572#line 573

# Creates a new leaf component out of a handler function, and a data parameter#line 574
# that will be passed back to your handler when called.#line 575#line 576
def make_leaf (name,owner,instance_data,handler):      #line 577
    eh =  Eh ()                                        #line 578
    eh.name =  str( owner.name) +  str( "▹") +  name   #line 579
    eh.owner =  owner                                  #line 580
    eh.handler =  handler                              #line 581
    eh.instance_data =  instance_data                  #line 582
    eh.state =  "idle"                                 #line 583
    eh.kind =  "leaf"                                  #line 584
    return  eh                                         #line 585#line 586#line 587

# Sends a mevent on the given `port` with `data`, placing it on the output#line 588
# of the given component.                              #line 589#line 590
def send (eh,port,datum,causingMevent):                #line 591
    mev = make_mevent ( port, datum)                   #line 592
    put_output ( eh, mev)                              #line 593#line 594#line 595

def send_string (eh,port,s,causingMevent):             #line 596
    datum = new_datum_string ( s)                      #line 597
    mev = make_mevent ( port, datum)                   #line 598
    put_output ( eh, mev)                              #line 599#line 600#line 601

def forward (eh,port,mev):                             #line 602
    fwdmev = make_mevent ( port, mev.datum)            #line 603
    put_output ( eh, fwdmev)                           #line 604#line 605#line 606

def inject (eh,mev):                                   #line 607
    eh.finject ( eh, mev)                              #line 608#line 609#line 610

def set_active (eh):                                   #line 611
    eh.state =  "active"                               #line 612#line 613#line 614

def set_idle (eh):                                     #line 615
    eh.state =  "idle"                                 #line 616#line 617#line 618

def put_output (eh,mev):                               #line 619
    eh.outq.append ( mev)                              #line 620#line 621#line 622

root_project =  ""                                     #line 623
root_0D =  ""                                          #line 624#line 625
def set_environment (rproject,r0D):                    #line 626
    global root_project                                #line 627
    global root_0D                                     #line 628
    root_project =  rproject                           #line 629
    root_0D =  r0D                                     #line 630#line 631#line 632
                                                       #line 633
def string_make_persistent (s):                        #line 634
    # this is here for non_GC languages like Odin, it is a no_op for GC languages like Python#line 635
    return  s                                          #line 636#line 637#line 638

def string_clone (s):                                  #line 639
    return  s                                          #line 640#line 641#line 642

# usage: app ${_00_} ${_0D_} arg main diagram_filename1 diagram_filename2 ...#line 643
# where ${_00_} is the root directory for the project  #line 644
# where ${_0D_} is the root directory for 0D (e.g. 0D/odin or 0D/python)#line 645#line 646
def initialize_component_palette (root_project,root_0D,diagram_source_files):#line 647
    reg = make_component_registry ()                   #line 648
    for diagram_source in  diagram_source_files:       #line 649
        all_containers_within_single_file = json2internal ( root_project, diagram_source)#line 650
        reg = generate_shell_components ( reg, all_containers_within_single_file)#line 651
        for container in  all_containers_within_single_file:#line 652
            register_component ( reg,mkTemplate ( container [ "name"], container, container_instantiator))#line 653#line 654#line 655
    initialize_stock_components ( reg)                 #line 656
    return  reg                                        #line 657#line 658#line 659
                                                       #line 660
def clone_string (s):                                  #line 661
    return  s                                          #line 662#line 663#line 664

load_errors =  False                                   #line 665
runtime_errors =  False                                #line 666#line 667
def load_error (s):                                    #line 668
    global load_errors                                 #line 669
    live_update ("✗", s)
    load_errors =  True                                #line 672#line 673#line 674

def runtime_error (s):                                 #line 675
    global runtime_errors                              #line 676
    live_update ("✗", s)
    runtime_errors =  True                             #line 678#line 679#line 680
                                                       #line 681
def argv ():                                           #line 682
    return  sys.argv                                   #line 683#line 684#line 685

def initialize ():                                     #line 686
    root_of_project =  sys.argv[ 1]                    #line 687
    root_of_0D =  sys.argv[ 2]                         #line 688
    arg =  sys.argv[ 3]                                #line 689
    main_container_name =  sys.argv[ 4]                #line 690
    diagram_names =  sys.argv[ 5:]                     #line 691
    palette = initialize_component_palette ( root_of_project, root_of_0D, diagram_names)#line 692
    return [ palette,[ root_of_project, root_of_0D, main_container_name, diagram_names, arg]]#line 693#line 694#line 695

def start (palette,env):                               #line 696
    live_update ( "",  "reset")                        #line 697
    live_update ( "Info",  "begin...")                 #line 698
    root_of_project =  env [ 0]                        #line 699
    root_of_0D =  env [ 1]                             #line 700
    main_container_name =  env [ 2]                    #line 701
    diagram_names =  env [ 3]                          #line 702
    arg =  env [ 4]                                    #line 703
    set_environment ( root_of_project, root_of_0D)     #line 704
    # get entrypoint container                         #line 705
    main_container = get_component_instance ( palette, main_container_name, None)#line 706
    if  None ==  main_container:                       #line 707
        load_error ( str( "Couldn't find container with page name /") +  str( main_container_name) +  str( "/ in files ") +  str(str ( diagram_names)) +  " (check tab names, or disable compression?)"    )#line 711#line 712
    if not  load_errors:                               #line 713
        marg = new_datum_string ( arg)                 #line 714
        mev = make_mevent ( "", marg)                  #line 715
        inject ( main_container, mev)                  #line 716
        print (deque_to_json ( main_container.outq))   #line 717#line 718
    live_update ( "Info",  "...end")                   #line 719#line 720#line 721
                                                       #line 722
# utility functions                                    #line 723
def send_int (eh,port,i,causing_mevent):               #line 724
    datum = new_datum_string (str ( i))                #line 725
    send ( eh, port, datum, causing_mevent)            #line 726#line 727#line 728

def send_bang (eh,port,causing_mevent):                #line 729
    datum = new_datum_bang ()                          #line 730
    send ( eh, port, datum, causing_mevent)            #line 731#line 732
