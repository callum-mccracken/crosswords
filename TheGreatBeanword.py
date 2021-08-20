import ipuz

# ANSWER/KEY PAIRS
# Chicken byproduct byproduct: CHICKPEA
# Pop star or beaten up: BLACKEYEDPEA
# How you tell your southern american mother to say someything false: LIMA
# Also a mobster's organ: CANNELLINI
# Japanese and red: ADZUKI
# Saltando: (Mexican) JUMPING
# ?: KIDNEY


# put puzzle data here
puzzle = {
    "origin": "Bean Lord's Puzzle Vault",
    "version": "http://ipuz.org/v2",
    "kind": ["http://ipuz.org/crossword#1"],
    "copyright": "CC0, feel free to spread this around like your favourite bean paste",
    "author": "Bean Lord",
    "publisher": "Bean Lord, Inc.",
    "title": "The Great Beanword",
    "intro": "All words are beans (singular form, e.g. kidney rather than kidneys). Circled letters spell one final bean.",
    "difficulty": "Significant",
    "empty": "0",
    "dimensions": { "width": 15, "height": 15 },
    "puzzle": [
        [{"cell":1,"style":{"shapebg":"circle"}},2,3,4],
        [2,{"cell":2,"style":{"shapebg":"circle"}},0,0],
        [3,0,{"cell":3,"style":{"shapebg":"circle"}},0],
        [4,0,0,{"cell":4,"style":{"shapebg":"circle"}}],
    ],

    "clues":{
        "Across": [
            [1,"Bean type"],
            [2,"City in Peru"],
            [3,"How you tell your american mother to lie"],
            [4,"It's green it's round it's slightly larger than the average bean"],
        ],
        
        "Down": [
            [1,"LLLL"],
            [2,"IIII"],
            [3,"MMMM"],
            [4,"AAAA"]
        ]
    },
    "solution":
    [
        ["L","I","M","A"],
        ["L","I","M","A"],
        ["L","I","M","A"],
        ["L","I","M","A"]
    ]

}

# make .ipuz-writeable string
data = ipuz.write(puzzle)

# ensure it actually works
puzzle = ipuz.read(data)

# if that works, write it out
with open('Lima Beans.ipuz', 'w') as f:
    f.write(data)
