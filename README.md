String interpolation expander to Python
# usage
## first time
`$ make install`
## usage
`$ make`
### expected output
```
$ make
pbp/t2t.bash . ./pbp string.ohm string.rwr empty.js mad.si >mad.py

*** generated code ***

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


*** run ***
a

b
abcd
uv
uvw
uavw
Nested interpolation?! Are you mad?!
interpolation?! Are you mad?!
Hello World
Hollow World
Hallowed
Hallowed World
u7vw
u18vw
```

## identity
`$ make identity`
I find it useful to just make an identity transform first. Output = input.
This step in my workflow checks to see that the grammar and .rwr line up and alerts me of silly errors and typos. 
Once the identity transform is working, I simply hack on the .rwr file to make it output what I really want to output.

This demo converts `mad.si` into runnable Python (`mad.py`), then runs it.
# Inspiration
This simple demo was inspired by challenge #1 in chapter 16 of the book [Crafting Interpreters](https://craftinginterpreters.com/scanning-on-demand.html#challenges).

# Details
The test program snippet is `mad.si`.
The grammar which parses this snippet is `string.ohm`.
The rewrite rules used for rewriting the parse are in `string.rwr`.
The syntax for writing grammars in OhmJS style can be found in the [OhmJS website](ohmjs.org).
The syntax for writing rewrite rules is documented in [RWR Documentation](https://github.com/guitarvydas/pbp-dev/blob/dev/t2t/doc/rwr/RWR%20Spec.pdf).
An earlier blog post about this is in [Substack string-interpolation](https://programmingsimplicity.substack.com/p/string-interpolation?r=1egdky&utm_campaign=post&utm_medium=web&triedRedirect=true).
