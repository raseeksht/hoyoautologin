
# Hoyolab Autologin

    Easy Autologin without visiting hoyolab website

## Supported Games
    Genshin Impact
    Honkai StarRail

## Installation
prerequisite: python and pip (in case of no python and pip, is the executable file [main.exe]([#](https://github.com/raseeksht/hoyoautologin/releases)))

To install the tool you need to follow these steps:
    
    git clone https://github.com/raseeksht/hoyoautologin
    cd hoyoautologin
    pip install -r requirements.txt


## How to Use?
get cookie from the hoyolab website
```
inside hoylab.com got to console (press F12 then click console or right click anywhere and select `inspect` and click console )

in the console tab, write `document.cookie` and press enter and you will get the required cookie

copy the cookie (without quotation mark ('') ) and use it in .env.example file
Note: Cookie are store in your pc and are not shared
```

![Untitled](https://github.com/raseeksht/hoyoautologin/assets/39650487/9e398610-a9a5-4ec3-b281-ce5fb9ffd9b3)

edit .env.example 
```
if you play both genshin impact and honkai star rail from same account then set `SameAccount=1`
paste the cookie from hoyolab in `Cookie=`
```



```
if you play genshin and honkai on seperate account get the cookie from both account and paste in `HonkaiCookie` and `GenshinCookie`
```
![Untitled123](https://github.com/raseeksht/hoyoautologin/assets/39650487/6cb69cc6-b589-487b-a9e1-ff44fa865ee5)


After you finish editing rename `.env.example` file to `.env`


now run the script
```
python main.py
```

To create executable file

```
pyinstaller main.py --onefile
```


executable file will be created in `dist/`
