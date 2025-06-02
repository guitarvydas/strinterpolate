print ("a")
print ("")
print ("b")
print (strcat ("abc", "d"))
print (strcat ("u", "v"))
#//+ print "${"u"}v${"w"}"
print (strcat ("u", strcat ("v", "w")))
#//+ print "${"u${"a"}"}v${"w"}"
print (strcat (strcat ("u", "a"), strcat ("v", "w")))
