# "Nested ${"interpolation?! Are you ${"mad?!}"}"

def strcat (s1, s2):
    return s1 + s2

print (strcat ("Nested ", 
               strcat ("interpolation?! Are you ", 
                       strcat ("mad?!", ""))))



