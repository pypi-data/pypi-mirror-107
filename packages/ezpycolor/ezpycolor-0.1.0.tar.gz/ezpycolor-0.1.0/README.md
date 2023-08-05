# ezpycolor
simple colorization of strings in Python

### Installation
```
pip install ezpycolor
```

### Example Output
![ezpycolor-example-output.PNG](https://github.com/bonifield/ezpycolor/raw/main/ezpycolor-example-output.PNG)

### Usage
```
from ezpycolor import *

printgreen("hello world")

s = colorpurple("hello")+" "+colorred("world")
print(s)

printrainbow("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
printbgrainbow("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
```

### Objects
```
# print statements
printpurple
printblue
printgreen
printyellow
printgold
printred
printbold
printunderline
printbgpurple
printbgblue
printbggreen
printbgyellow
printbggold
printbgred
printrainbow
printbgrainbow

# string objects
colorpurple
colorblue
colorgreen
coloryellow
colorgold
colorred
colorbold
colorunderline
colorbgpurple
colorbgblue
colorbggreen
colorbgyellow
colorbggold
colorbgred
colorrainbow
colorbgrainbow
```
