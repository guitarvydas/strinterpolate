
def strcat (s1, s2):
    return s1 + s2
    
print ("a")
print ("")
print ("b")
print (strcat ("abc", "d"))
print (strcat ("u", "v"))
print (strcat ("u", strcat ("v", "w")))
print (strcat (strcat ("u", "a"), strcat ("v", "w")))
print (strcat ("Nested ", strcat ("interpolation?! Are you ", "mad?!")))
print (strcat ("interpolation?! Are you ", "mad?!"))
print ("Hello World")
print (strcat ("Hollow ", "World"))
print ("Hallowed")
print (strcat ("Hallowed", strcat (" ", "World")))
print (strcat (strcat ("u", str (7)), strcat ("v", "w")))
print (strcat (strcat ("u", str (7 + 11)), strcat ("v", "w")))

