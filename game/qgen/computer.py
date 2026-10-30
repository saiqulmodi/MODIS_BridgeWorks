"""Computer: basics for every class, up to programming, networks and systems for BE / Expert."""
import math

from . import facts, fmt, near, template

ALL = range(1, 17)
S = "computer"

# ---------- concept questions, by stage ----------
facts(range(1, 4), S, [
    ("Which part of a computer looks like a TV and shows pictures?", "Monitor", ["Keyboard", "Mouse", "Printer"],
     "The monitor is the screen that shows what the computer is doing."),
    ("Which device has keys with letters and numbers?", "Keyboard", ["Monitor", "Speaker", "CPU"],
     "We type letters and numbers using the keyboard."),
    ("Which device do we move on the table to point and click?", "Mouse", ["Printer", "Monitor", "Speaker"],
     "The mouse moves the pointer on the screen."),
    ("Which part is called the brain of the computer?", "CPU", ["Mouse", "Monitor", "Keyboard"],
     "The CPU (Central Processing Unit) does all the thinking and calculating."),
    ("Which device gives us sound from the computer?", "Speaker", ["Mouse", "Keyboard", "Scanner"],
     "Speakers play music and sounds."),
    ("Which device prints our work on paper?", "Printer", ["Monitor", "Mouse", "Microphone"],
     "A printer puts text and pictures from the computer onto paper."),
    ("A computer works with the help of:", "Electricity", ["Water", "Petrol", "Wind only"],
     "Computers need electricity (from a plug or a battery) to work."),
    ("Which key makes a gap between two words?", "Space bar", ["Enter key", "Shift key", "Caps Lock"],
     "The long space bar puts a space between words."),
    ("Which key takes the cursor to a new line?", "Enter key", ["Space bar", "Backspace", "Tab"],
     "Pressing Enter starts a new line."),
    ("Which key rubs out the letter to the left of the cursor?", "Backspace", ["Enter", "Shift", "Space bar"],
     "Backspace deletes the character before the cursor."),
    ("We talk into a computer using a:", "Microphone", ["Printer", "Monitor", "Mouse"],
     "A microphone is an input device for sound."),
    ("Which of these is NOT a computer?", "Bicycle", ["Laptop", "Tablet", "Desktop"],
     "A bicycle is a vehicle, not a computer."),
    ("Clicking the left mouse button two times quickly is called:", "Double-click", ["Drag", "Scroll", "Type"],
     "A double-click opens files and programs."),
    ("The small arrow that moves on the screen with the mouse is the:", "Pointer (cursor)",
     ["Icon", "Window", "Wallpaper"], "The mouse pointer shows where you will click."),
    ("Small pictures on the desktop that open programs are called:", "Icons", ["Windows", "Keys", "Wires"],
     "Icons are small pictures for programs and files."),
    ("A computer can do work:", "Very fast and without getting tired", ["Only slowly", "Only at night",
     "Only when it is hungry"], "Computers are fast, accurate and never get tired."),
    ("Which device is used to draw on a computer like a pen?", "Graphics tablet (stylus)",
     ["Speaker", "Printer", "Monitor"], "A stylus and graphics tablet let you draw with a pen."),
    ("Which program is used to draw pictures on a computer?", "Paint", ["Calculator", "Notepad", "Clock"],
     "Paint (or any drawing app) is used to draw and colour."),
    ("We should sit at a computer with our back:", "Straight", ["Bent forward", "Lying down", "Twisted"],
     "Sitting straight keeps our back healthy."),
    ("Before switching off, we should:", "Shut down the computer properly", ["Pull out the plug",
     "Pour water on it", "Hit the keyboard"], "Shutting down properly saves our work and protects the computer."),
])

facts(range(3, 6), S, [
    ("Devices that put data INTO a computer are called:", "Input devices", ["Output devices", "Storage devices",
     "Processing devices"], "Keyboard, mouse, scanner and microphone are input devices."),
    ("Devices that give results OUT of a computer are called:", "Output devices", ["Input devices",
     "Storage devices", "Cables"], "Monitor, printer and speakers are output devices."),
    ("Which is an input device?", "Scanner", ["Printer", "Speaker", "Monitor"],
     "A scanner reads a paper page into the computer."),
    ("Which is an output device?", "Printer", ["Keyboard", "Mouse", "Scanner"], "A printer gives out printed results."),
    ("Which of these stores data even when the computer is off?", "Hard disk", ["RAM", "CPU", "Monitor"],
     "A hard disk (or SSD) keeps data without power; RAM forgets it."),
    ("A pen drive is also called a:", "USB flash drive", ["Floppy cable", "Monitor stick", "CPU card"],
     "Pen drives plug into a USB port and store files."),
    ("The first screen we see after the computer starts is the:", "Desktop", ["Taskbar only", "Recycle Bin",
     "Start key"], "The desktop shows icons, wallpaper and the taskbar."),
    ("Deleted files first go to the:", "Recycle Bin", ["Desktop", "Printer", "Start menu"],
     "Files in the Recycle Bin can still be restored."),
    ("A program that works like a book of notes and letters is a:", "Word processor",
     ["Paint program", "Calculator", "Game"], "Word processors (like MS Word) are used to type documents."),
    ("To make letters CAPITAL while typing, we press:", "Caps Lock or Shift", ["Enter", "Backspace", "Space bar"],
     "Caps Lock keeps capitals on; Shift makes one capital letter."),
    ("Ctrl + C is used to:", "Copy", ["Cut", "Paste", "Close"], "Ctrl + C copies the selected item."),
    ("Ctrl + V is used to:", "Paste", ["Copy", "Undo", "Save"], "Ctrl + V pastes what was copied or cut."),
    ("Ctrl + Z is used to:", "Undo", ["Redo", "Zoom", "Save"], "Ctrl + Z undoes the last action."),
    ("Ctrl + S is used to:", "Save", ["Select", "Search", "Send"], "Ctrl + S saves your file."),
    ("The Internet is:", "A network of computers all over the world", ["A single big computer",
     "A type of keyboard", "A printer cable"], "The Internet connects millions of computers worldwide."),
    ("We should never share our password with:", "Strangers or friends online", ["Our own diary",
     "Nobody - not even a teacher's helper is needed", "The computer itself"],
     "Passwords are private; keep them secret from others."),
    ("A web browser is used to:", "Open websites", ["Print photos only", "Charge the laptop", "Clean the screen"],
     "Chrome, Edge and Firefox are browsers for visiting websites."),
    ("The part that holds the CPU, memory and other parts is the:", "Motherboard", ["Monitor", "Keyboard",
     "Mouse pad"], "All main parts plug into the motherboard."),
    ("Windows, Linux and Android are examples of:", "Operating systems", ["Games", "Printers", "Viruses"],
     "An operating system runs the computer and its programs."),
    ("A computer virus is:", "A harmful program", ["A cold for the computer from dust", "A new mouse",
     "A fast cable"], "Viruses are programs that damage files or steal data; antivirus software stops them."),
])

facts(range(6, 9), S, [
    ("The smallest unit of data in a computer is a:", "Bit", ["Byte", "Nibble", "Kilobyte"],
     "A bit is 0 or 1. 8 bits make a byte."),
    ("1 byte is equal to:", "8 bits", ["4 bits", "16 bits", "1,000 bits"], "1 byte = 8 bits; 4 bits = 1 nibble."),
    ("RAM stands for:", "Random Access Memory", ["Read Access Memory", "Run All Memory", "Rapid Action Machine"],
     "RAM is the working memory; it loses data when power goes off."),
    ("ROM stands for:", "Read Only Memory", ["Random Only Memory", "Run On Memory", "Read Open Mode"],
     "ROM keeps the start-up instructions even without power."),
    ("Which memory is volatile (loses data without power)?", "RAM", ["ROM", "Hard disk", "Pen drive"],
     "RAM is volatile; storage devices are non-volatile."),
    ("A step-by-step method to solve a problem is called an:", "Algorithm", ["Icon", "Output", "Virus"],
     "An algorithm is a finite list of clear steps."),
    ("In a flowchart, a decision is shown by a:", "Diamond", ["Oval", "Rectangle", "Arrow"],
     "Ovals start/end, rectangles are processes, diamonds are decisions."),
    ("In a flowchart, Start and Stop are shown by an:", "Oval", ["Diamond", "Rectangle", "Parallelogram"],
     "Terminal symbols are ovals (rounded rectangles)."),
    ("In a spreadsheet, the box where a row and column meet is a:", "Cell", ["Sheet", "Chart", "Formula"],
     "A cell like B3 sits at column B, row 3."),
    ("In a spreadsheet, every formula starts with:", "=", ["#", "@", "&"], "Typing = tells the spreadsheet to calculate."),
    ("Which spreadsheet function adds a range of cells?", "SUM", ["ADD", "TOTAL", "PLUS"], "=SUM(A1:A5) adds A1 to A5."),
    ("Which function gives the average of cells?", "AVERAGE", ["MEAN", "MID", "AVG()"],
     "=AVERAGE(A1:A5) gives the mean."),
    ("A LAN is a network that covers:", "A small area like a school or office", ["The whole world",
     "Only one computer", "A country"], "LAN = Local Area Network."),
    ("WWW stands for:", "World Wide Web", ["World Wide Wire", "Web World Wide", "Wide World Web"],
     "The Web is the collection of web pages on the Internet."),
    ("A URL is:", "The address of a web page", ["A type of virus", "A computer part", "An email password"],
     "URL = Uniform Resource Locator, e.g. https://ncert.nic.in"),
    ("Sending fake emails to steal passwords is called:", "Phishing", ["Fishing", "Browsing", "Formatting"],
     "Phishing tricks people into giving away private details."),
    ("Software you can use and change for free, with its code shared, is:", "Open source software",
     ["Proprietary software", "Malware", "Firmware only"], "Linux and LibreOffice are open source."),
    ("A program that translates a whole high-level program into machine code at once is a:", "Compiler",
     ["Interpreter", "Assembler", "Editor"], "A compiler translates everything first; an interpreter line by line."),
    ("Bullying someone using the internet is called:", "Cyberbullying", ["Netiquette", "Blogging", "Debugging"],
     "Report cyberbullying to a trusted adult; never reply in anger."),
    ("Finding and fixing mistakes in a program is called:", "Debugging", ["Compiling", "Booting", "Formatting"],
     "Errors in programs are 'bugs'; removing them is debugging."),
    ("The binary number system uses the digits:", "0 and 1", ["0 to 9", "1 and 2", "0 to 7"],
     "Binary is base 2: only 0 and 1."),
    ("Which device connects a home network to the internet?", "Router / modem", ["Monitor", "Scanner", "Speaker"],
     "A router sends data between your network and the internet."),
])

facts(range(9, 11), S, [
    ("HTML is used to:", "Build the structure of web pages", ["Design computer chips", "Store passwords",
     "Compile C programs"], "HTML (HyperText Markup Language) marks up headings, paragraphs, links and images."),
    ("Which HTML tag makes the biggest heading?", "<h1>", ["<h6>", "<head>", "<p>"], "h1 is the largest heading; h6 the smallest."),
    ("Which HTML tag makes a link?", "<a>", ["<link>", "<href>", "<l>"], "<a href=\"url\">text</a> creates a hyperlink."),
    ("Which HTML tag shows a picture?", "<img>", ["<pic>", "<src>", "<image>"], "<img src=\"photo.jpg\"> shows an image."),
    ("CSS is used to:", "Style web pages (colours, fonts, layout)", ["Store databases", "Write the OS kernel",
     "Send emails"], "CSS = Cascading Style Sheets."),
    ("The output of an AND gate is 1 when:", "All inputs are 1", ["Any input is 1", "All inputs are 0",
     "Inputs are different"], "AND gives 1 only if every input is 1."),
    ("The output of an OR gate is 0 when:", "All inputs are 0", ["Any input is 1", "All inputs are 1",
     "Inputs are different"], "OR gives 0 only if every input is 0."),
    ("A NOT gate:", "Reverses its input", ["Adds two inputs", "Stores a bit", "Always gives 1"],
     "NOT 1 = 0 and NOT 0 = 1."),
    ("Which gate is called a universal gate?", "NAND", ["AND", "OR", "XOR"], "NAND (and NOR) alone can build any circuit."),
    ("In Python, print(type(3.5)) shows:", "<class 'float'>", ["<class 'int'>", "<class 'str'>",
     "<class 'double'>"], "Numbers with a decimal point are floats."),
    ("Which Python symbol starts a comment?", "#", ["//", "/*", "--"], "Everything after # on a line is a comment."),
    ("IP address in IPv4 is made of:", "32 bits", ["16 bits", "64 bits", "128 bits"], "IPv4 = 4 bytes = 32 bits; IPv6 = 128 bits."),
    ("Which protocol is used to send email?", "SMTP", ["FTP", "HTTP", "DHCP"], "SMTP sends mail; POP3/IMAP receive it."),
    ("HTTPS is safer than HTTP because:", "It encrypts the data", ["It is faster", "It uses no internet",
     "It has no URL"], "The S means Secure: data is encrypted with TLS."),
    ("A firewall:", "Blocks unwanted network traffic", ["Cools the CPU", "Prints faster", "Speeds up RAM"],
     "Firewalls filter traffic coming in and going out."),
    ("Using someone's work without credit is:", "Plagiarism", ["Citation", "Open source", "Netiquette"],
     "Always credit sources; copying them as your own is plagiarism."),
    ("Which of these is a strong password?", "T7#qL9!vR2", ["password123", "12345678", "myname"],
     "Strong passwords are long and mix upper, lower, digits and symbols."),
    ("Artificial Intelligence means:", "Machines doing tasks that need human-like thinking",
     ["Very fast typing", "A kind of mouse", "Internet speed"], "AI lets computers learn, reason and recognise."),
    ("The 'brain' of AI that learns from examples is called:", "Machine learning", ["Word processing",
     "Defragmentation", "Booting"], "Machine learning finds patterns in data."),
    ("A database table's row is also called a:", "Record (tuple)", ["Field", "Key", "Domain"],
     "Rows are records; columns are fields (attributes)."),
])

facts(range(11, 13), S, [
    ("Which Python data type is immutable?", "tuple", ["list", "dict", "set"], "Tuples (and strings) cannot be changed after creation."),
    ("Which Python keyword defines a function?", "def", ["func", "function", "define"], "def name(params): starts a function."),
    ("A stack follows which order?", "LIFO (last in, first out)", ["FIFO", "Random", "Sorted"],
     "push and pop happen at the same end (the top)."),
    ("A queue follows which order?", "FIFO (first in, first out)", ["LIFO", "Random", "Sorted"],
     "Elements join at the rear and leave from the front."),
    ("In SQL, which command gets data from a table?", "SELECT", ["GET", "FETCH", "OPEN"], "SELECT columns FROM table WHERE condition;"),
    ("In SQL, which clause filters groups after GROUP BY?", "HAVING", ["WHERE", "ORDER BY", "LIMIT"],
     "WHERE filters rows before grouping; HAVING filters groups."),
    ("A primary key:", "Uniquely identifies each row and cannot be NULL", ["Can repeat",
     "Links to another table only", "Is always text"], "A foreign key refers to another table's primary key."),
    ("Which SQL command removes a whole table with its structure?", "DROP TABLE", ["DELETE FROM", "REMOVE",
     "TRUNCATE ROW"], "DELETE removes rows; DROP removes the table itself."),
    ("Which layer of the OSI model handles routing between networks?", "Network layer", ["Transport layer",
     "Data link layer", "Session layer"], "Layer 3 (network) chooses routes; IP works here."),
    ("TCP is called a connection-oriented protocol because it:", "Sets up a connection and confirms delivery",
     ["Never checks errors", "Sends without any setup", "Works only on LAN"], "TCP uses a 3-way handshake and acknowledgements."),
    ("Which device works at the data link layer and uses MAC addresses?", "Switch", ["Router", "Repeater", "Modem"],
     "Switches forward frames by MAC address; routers use IP addresses."),
    ("DNS converts:", "Domain names to IP addresses", ["IP to MAC", "Text to binary", "HTML to CSS"],
     "DNS is the internet's phone book."),
    ("What does 'with open(\"f.txt\") as f:' make sure of in Python?", "The file is closed automatically",
     ["The file is deleted", "The file is encrypted", "The file opens twice"], "The with-block closes the file even after errors."),
    ("Which file mode in Python adds to the end of an existing file?", "'a'", ["'w'", "'r'", "'x'"],
     "'w' overwrites, 'a' appends, 'r' reads."),
    ("pickle in Python is used to:", "Save Python objects to a binary file", ["Draw graphs", "Send email",
     "Sort lists"], "pickle.dump() writes and pickle.load() reads objects."),
    ("The worst-case number of comparisons in linear search of n items is:", "n", ["log2 n", "1", "n squared"],
     "It may have to check every item."),
    ("Binary search needs the list to be:", "Sorted", ["Reversed", "Empty", "Of strings only"],
     "It halves a sorted list each step."),
    ("De Morgan's law: NOT(A AND B) equals:", "(NOT A) OR (NOT B)", ["(NOT A) AND (NOT B)", "A OR B",
     "NOT A AND B"], "Break the bar and change the operator."),
    ("In Python, 'abc' * 2 gives:", "'abcabc'", ["'abc2'", "Error", "'aabbcc'"], "* repeats a string."),
    ("Which exception occurs on 10/0 in Python?", "ZeroDivisionError", ["ValueError", "TypeError", "IndexError"],
     "Dividing by zero raises ZeroDivisionError."),
])

facts((15, 13, 14, 16), S, [
    ("The time complexity of merge sort is:", "O(n log n)", ["O(n^2)", "O(n)", "O(log n)"],
     "It splits into halves (log n levels) and merges n items per level."),
    ("Worst-case time of quicksort is:", "O(n^2)", ["O(n log n)", "O(n)", "O(log n)"],
     "A bad pivot every time gives n + (n-1) + ... = O(n^2)."),
    ("Which data structure gives O(1) average lookup by key?", "Hash table", ["Linked list", "Binary heap",
     "Sorted array"], "Hashing maps keys straight to buckets."),
    ("Dijkstra's algorithm fails with:", "Negative edge weights", ["Undirected graphs", "Weighted graphs",
     "Cycles"], "Use Bellman-Ford when edges can be negative."),
    ("A binary tree with n nodes has how many edges?", "n - 1", ["n", "n + 1", "2n"], "Every node except the root has one parent edge."),
    ("BFS of a graph uses a:", "Queue", ["Stack", "Heap", "Hash table"], "DFS uses a stack (or recursion)."),
    ("In a min-heap, the smallest element is at the:", "Root", ["Last leaf", "Middle", "Leftmost leaf"],
     "Every parent is <= its children."),
    ("Deadlock needs all four: mutual exclusion, hold and wait, no preemption and:", "Circular wait",
     ["Starvation", "Paging", "Thrashing"], "Breaking any one of the four prevents deadlock."),
    ("Virtual memory lets a program:", "Use more memory than the physical RAM", ["Run without a CPU",
     "Skip the OS", "Avoid all page faults"], "Pages live on disk and are swapped into RAM when needed."),
    ("Which normal form removes partial dependency on a composite key?", "2NF", ["1NF", "3NF", "BCNF"],
     "1NF: atomic values; 2NF: no partial dependency; 3NF: no transitive dependency."),
    ("ACID in databases stands for Atomicity, Consistency, Isolation and:", "Durability", ["Dependency",
     "Distribution", "Duplication"], "Committed transactions survive crashes."),
    ("Two's complement of a binary number is:", "Invert all bits and add 1", ["Invert all bits",
     "Add 1 only", "Reverse the bit order"], "It represents negative numbers so addition just works."),
    ("Pipelining in a CPU improves:", "Throughput (instructions completed per second)", ["Single instruction latency",
     "Disk size", "Screen resolution"], "Stages overlap so one instruction finishes every cycle (ideally)."),
    ("The halting problem is:", "Undecidable", ["Solvable in O(n)", "NP-complete but decidable", "Only hard for small inputs"],
     "Turing proved no program can decide halting for all programs."),
    ("If a problem in NP-complete gets a polynomial-time algorithm, then:", "P = NP", ["P != NP", "Nothing changes",
     "All problems become O(1)"], "Every NP problem reduces to an NP-complete one."),
    ("A recursive function must have a:", "Base case", ["Global variable", "Loop", "Pointer"],
     "Without a base case it never stops (stack overflow)."),
    ("Cache memory is placed between:", "CPU and main memory", ["RAM and disk", "Keyboard and CPU", "GPU and monitor"],
     "It keeps recently used data close to the CPU."),
    ("In public-key cryptography, a message encrypted with the public key is opened with the:", "Private key",
     ["Same public key", "Any key", "Hash"], "RSA uses a key pair; only the private key decrypts."),
    ("Which layer does TCP belong to?", "Transport layer", ["Network layer", "Application layer", "Physical layer"],
     "TCP and UDP are transport protocols."),
    ("Gradient descent updates parameters in the direction of:", "Negative gradient of the loss",
     ["Positive gradient", "Random direction", "Largest parameter"], "w <- w - learning_rate x dL/dw."),
])

# ---------- calculated questions ----------

@template(range(6, 17), S, 25)
def binary_to_decimal(rng, level):
    bits = 4 if level <= 8 else 8 if level <= 12 else 12
    n = rng.randrange(2 ** (bits - 2), 2 ** bits)
    b = format(n, "b")
    return (f"What is the binary number {b} in decimal?", str(n),
            [str(n + 1), str(n - 1), str(int(b[::-1], 2)), str(n * 2), str(n + 2 ** (len(b) - 1))],
            f"Add the place values (powers of 2) where the bit is 1: {b} = {n}.")


@template(range(6, 17), S, 25)
def decimal_to_binary(rng, level):
    top = 31 if level <= 8 else 255 if level <= 12 else 4095
    n = rng.randrange(5, top)
    b = format(n, "b")
    wrong = [format(n + 1, "b"), format(n - 1, "b"), b[::-1] if b[::-1] != b else format(n + 2, "b"),
             format(n ^ 2, "b"), format(n * 2, "b")]
    return (f"Write {n} in binary.", b, wrong, f"Divide by 2 repeatedly and read the remainders upwards: {n} = {b} (base 2).")


@template(range(9, 17), S, 20)
def hex_conversion(rng, level):
    n = rng.randrange(16, 4096 if level >= 11 else 256)
    h = format(n, "X")
    if rng.random() < 0.5:
        return (f"What is hexadecimal {h} in decimal?", str(n), [str(n + 16), str(n - 1), str(int(h[::-1], 16)), str(n + 10)],
                f"Each hex digit is a power of 16: {h} (base 16) = {n}.")
    return (f"Write {n} in hexadecimal.", h, [format(n + 1, "X"), format(n + 16, "X"), format(n - 16, "X"), h[::-1] + "0"],
            f"Divide by 16 and read the remainders upwards: {n} = {h} (base 16).")


UNITS = [("KB", 1), ("MB", 2), ("GB", 3), ("TB", 4)]


@template(range(6, 17), S, 15)
def storage_units(rng, level):
    i = rng.randrange(1, 4)
    big, small = UNITS[i], UNITS[i - 1]
    n = rng.choice([2, 3, 4, 5, 8, 10, 16, 32, 64, 128])
    ans = n * 1024
    return (f"How many {small[0]} are there in {n} {big[0]}? (1 {big[0]} = 1024 {small[0]})", f"{ans:,} {small[0]}",
            [f"{n * 1000:,} {small[0]}", f"{n * 100:,} {small[0]}", f"{n * 8:,} {small[0]}", f"{n * 512:,} {small[0]}"],
            f"{n} x 1024 = {ans:,} {small[0]}.")


@template(range(5, 13), S, 15)
def image_pixels(rng, level):
    w, h = rng.choice([(640, 480), (800, 600), (1024, 768), (1280, 720), (1920, 1080), (320, 240)])
    if level <= 8:
        n = w * h
        return (f"A picture is {w} pixels wide and {h} pixels tall. How many pixels does it have?", f"{n:,}",
                [f"{w + h:,}", f"{2 * (w + h):,}", f"{n // 2:,}", f"{n * 2:,}"], f"Pixels = width x height = {w} x {h} = {n:,}.")
    bpp = rng.choice([8, 24, 32])
    size = w * h * bpp / 8 / 1024
    return (f"An uncompressed {w} x {h} image uses {bpp} bits per pixel. What is its size in KB (1 KB = 1024 bytes)?",
            f"{fmt(size)} KB", near(size, rng, "KB", (8, 0.125, 2, 0.5, 1.024)),
            f"Size = {w} x {h} x {bpp} / 8 bytes = {fmt(size)} KB.")


@template(range(9, 17), S, 20)
def logic_gate(rng, level):
    gates = {"AND": lambda a, b: a & b, "OR": lambda a, b: a | b, "NAND": lambda a, b: 1 - (a & b),
             "NOR": lambda a, b: 1 - (a | b), "XOR": lambda a, b: a ^ b, "XNOR": lambda a, b: 1 - (a ^ b)}
    g1, g2 = rng.sample(list(gates), 2)
    a, b, c = (rng.randrange(2) for _ in range(3))
    out = gates[g2](gates[g1](a, b), c)
    return (f"A = {a}, B = {b}, C = {c}. What is the output of ({'A ' + g1 + ' B'}) {g2} C?", str(out),
            [str(1 - out), "Cannot say", "2", "Undefined"],
            f"A {g1} B = {gates[g1](a, b)}; then {gates[g1](a, b)} {g2} {c} = {out}.")


@template(range(11, 17), S, 20)
def python_expr(rng, level):
    a, b = rng.randrange(7, 60), rng.randrange(2, 9)
    ops = [("//", a // b, "floor division keeps the whole part"), ("%", a % b, "% gives the remainder"),
           ("/", a / b, "/ always gives a float"), ("**", b ** 2, "** is power")]
    op, val, why = rng.choice(ops)
    expr = f"{b} ** 2" if op == "**" else f"{a} {op} {b}"
    ans = repr(val) if isinstance(val, float) else str(val)
    if isinstance(val, float):
        ans = str(round(val, 4))
    wrong = [str(a // b), str(a % b), str(round(a / b, 4)), str(b * 2), str(a * b), str(a // b + 1)]
    return (f"What does Python print for print({expr})?", ans, wrong, f"{expr} = {ans}: {why}.")


@template(range(11, 17), S, 15)
def python_slice(rng, level):
    word = rng.choice(["BRIDGEWORKS", "ENGINEER", "PHYSICS", "CHEMISTRY", "ECONOMICS", "COMPUTER", "STRUCTURE"])
    i = rng.randrange(0, 3)
    j = rng.randrange(i + 2, len(word))
    step = rng.choice([1, 1, 2])
    expr = f"s[{i}:{j}]" if step == 1 else f"s[{i}:{j}:{step}]"
    ans = word[i:j:step]
    wrong = [word[i:j + 1:step], word[i + 1:j:step], word[i:j], word[i:j - 1:step], word[::-1][i:j]]
    return (f"s = '{word}'. What is {expr}?", f"'{ans}'", [f"'{w}'" for w in wrong],
            f"Slicing starts at index {i} and stops before {j}" + (f", taking every {step}nd character." if step == 2 else "."))


@template(range(11, 17), S, 15)
def python_loop(rng, level):
    n = rng.randrange(4, 12)
    k = rng.choice([1, 2, 3])
    total = sum(range(1, n + 1, k))
    return (f"What is printed?\ns = 0\nfor i in range(1, {n + 1}, {k}):\n    s += i\nprint(s)", str(total),
            [str(sum(range(1, n + 2, k))), str(sum(range(0, n, k))), str(total + n), str(n * (n + 1) // 2 if k != 1 else total - 1)],
            f"i takes {list(range(1, n + 1, k))}; their sum is {total}.")


@template(range(9, 17), S, 15)
def bits_needed(rng, level):
    n = rng.randrange(5, 5000 if level >= 11 else 300)
    b = math.ceil(math.log2(n))
    return (f"How many bits are needed to give a different code to each of {n} items?", str(b),
            [str(b - 1), str(b + 1), str(n // 8 or 2), str(b * 2)], f"2^{b - 1} = {2 ** (b - 1)} < {n} <= 2^{b} = {2 ** b}, so {b} bits.")


@template(range(9, 17), S, 15)
def download_time(rng, level):
    size_mb = rng.choice([50, 100, 200, 250, 500, 700, 1000])
    mbps = rng.choice([8, 10, 16, 20, 40, 50, 100])
    t = size_mb * 8 / mbps
    return (f"How long does a {size_mb} MB file take to download at {mbps} Mbps (1 byte = 8 bits)?",
            f"{fmt(t)} s", [f"{fmt(size_mb / mbps)} s", f"{fmt(t * 8)} s", f"{fmt(t / 2)} s", f"{fmt(mbps * 8 / size_mb)} s"],
            f"Time = {size_mb} x 8 megabits / {mbps} Mbps = {fmt(t)} s. Bits, not bytes!")


@template(range(12, 17), S, 15)
def subnet_hosts(rng, level):
    p = rng.randrange(20, 30)
    hosts = 2 ** (32 - p) - 2
    return (f"How many usable host addresses are in a /{p} IPv4 subnet?", f"{hosts:,}",
            [f"{2 ** (32 - p):,}", f"{2 ** p:,}", f"{hosts - 2:,}", f"{2 ** (31 - p):,}"],
            f"2^(32 - {p}) = {2 ** (32 - p):,} addresses minus network and broadcast = {hosts:,}.")


@template(range(11, 17), S, 15)
def twos_complement(rng, level):
    n = rng.randrange(1, 120)
    b = format((-n) & 0xFF, "08b")
    return (f"What is -{n} in 8-bit two's complement?", b,
            [format(n, "08b"), format((~n) & 0xFF, "08b"), format(128 | n, "08b"), format(((-n) & 0xFF) ^ 1, "08b")],
            f"{n} = {format(n, '08b')}; invert -> {format((~n) & 0xFF, '08b')}; add 1 -> {b}.")


@template(range(13, 17), S, 15)
def binary_search_steps(rng, level):
    n = rng.choice([100, 500, 1000, 4000, 10000, 100000, 1000000])
    k = math.ceil(math.log2(n + 1))
    return (f"At most how many comparisons does binary search need on a sorted list of {n:,} items?", str(k),
            [str(k + 3), str(n // 2), str(k - 2), str(int(math.sqrt(n)))], f"ceil(log2({n:,} + 1)) = {k}.")


@template((15, 16), S, 15)
def amat(rng, level):
    hit = rng.choice([1, 2, 3, 5])
    miss = rng.choice([0.02, 0.05, 0.1, 0.2])
    pen = rng.choice([50, 80, 100, 200])
    t = hit + miss * pen
    return (f"A cache has hit time {hit} ns, miss rate {miss:.0%} and miss penalty {pen} ns. "
            f"What is the average memory access time?", f"{fmt(t)} ns",
            [f"{fmt(hit + pen)} ns", f"{fmt(miss * pen)} ns", f"{fmt((1 - miss) * hit + miss * pen + pen)} ns", f"{fmt(hit * pen * miss)} ns"],
            f"AMAT = hit time + miss rate x penalty = {hit} + {miss} x {pen} = {fmt(t)} ns.")


@template(range(3, 6), S, 10)
def typing_speed(rng, level):
    wpm = rng.choice([10, 12, 15, 20, 25])
    m = rng.choice([2, 3, 4, 5, 6])
    return (f"Riya types {wpm} words in one minute. How many words can she type in {m} minutes?", str(wpm * m),
            [str(wpm + m), str(wpm * m + wpm), str(wpm * (m - 1)), str(wpm * m * 2)], f"{wpm} x {m} = {wpm * m} words.")


# ---------- coding thinking for the youngest classes (numbers grow with the class) ----------
MOVES = {"up": (0, 1), "down": (0, -1), "left": (-1, 0), "right": (1, 0)}


@template(range(1, 9), S, 40)
def robot_moves(rng, level):
    n = 2 + min(level, 6)
    steps = [rng.choice(list(MOVES)) for _ in range(n)]
    x = y = 0
    for s in steps:
        x, y = x + MOVES[s][0], y + MOVES[s][1]
    ans = f"({x}, {y})"
    wrong = [f"({x + 1}, {y})", f"({x}, {y - 1})", f"({y}, {x})", f"({-x}, {y})", f"({x}, {-y})", f"({x - 1}, {y + 1})"]
    return (f"A robot starts at (0, 0). It moves one square each: {', '.join(steps)}. Where does it stop? "
            f"(right adds 1 to x, up adds 1 to y)", ans, wrong,
            f"Count right minus left for x = {x}, and up minus down for y = {y}.")


@template(range(1, 9), S, 40)
def repeat_loop(rng, level):
    times = rng.randrange(2, 4 + level)
    step = rng.randrange(1, 3 + level)
    extra = rng.randrange(0, level + 1)
    total = times * step + extra
    q = f"A turtle program says: repeat {times} times [move {step} steps]"
    q += f", then move {extra} more steps. How many steps in all?" if extra else ". How many steps does it move?"
    return (q, str(total), [str(times + step + extra), str(total + step), str(total - step), str(times * (step + extra))],
            f"{times} x {step}" + (f" + {extra}" if extra else "") + f" = {total} steps.")


WORDS = ["cat", "sun", "tree", "ball", "apple", "mango", "school", "pencil", "bridge", "rocket", "computer",
         "keyboard", "monitor", "printer", "science", "garden", "rainbow", "teacher", "elephant", "butterfly"]


@template(range(1, 5), S, 40)
def key_presses(rng, level):
    w = rng.choice(WORDS[:8 + level * 3])
    caps = level >= 3 and rng.random() < 0.5
    word = w.capitalize() if caps else w
    n = len(w) + (1 if caps else 0)
    return (f"How many key presses are needed to type '{word}'?" + (" (Use Shift for the capital letter.)" if caps else ""),
            str(n), [str(n + 1), str(n - 1), str(n + 2), str(2 * n)],
            f"One press per letter ({len(w)})" + (" plus one Shift press" if caps else "") + f" = {n}.")


@template(range(2, 9), S, 40)
def alphabetical(rng, level):
    k = 3 if level <= 4 else 4
    ws = rng.sample(WORDS, k)
    first = min(ws)
    return (f"A computer sorts these words in A-Z order: {', '.join(ws)}. Which comes first?", first,
            [w for w in ws if w != first] + [max(ws)], f"Compare first letters (then the next ones): '{first}' comes first.")


@template(range(1, 7), S, 40)
def number_pattern(rng, level):
    start = rng.randrange(1, 5 + level * 2)
    step = rng.randrange(1, 2 + level)
    mult = level >= 4 and rng.random() < 0.4
    seq = [start]
    for _ in range(3):
        seq.append(seq[-1] * 2 if mult else seq[-1] + step)
    nxt = seq[-1] * 2 if mult else seq[-1] + step
    rule = "doubles each time" if mult else f"adds {step} each time"
    return (f"A program prints {', '.join(map(str, seq))}, ... What does it print next?", str(nxt),
            [str(nxt + 1), str(nxt - 1), str(seq[-1] + step + 2), str(seq[-1] * 2 + 1), str(nxt + step)],
            f"The pattern {rule}, so the next number is {nxt}.")


@template(range(1, 5), S, 40)
def desktop_icons(rng, level):
    a = rng.randrange(4, 8 + level * 4)
    b = rng.randrange(1, a)
    if rng.random() < 0.5:
        return (f"There are {a} icons on the desktop. You delete {b} of them. How many icons are left?", str(a - b),
                [str(a + b), str(a - b + 1), str(a - b - 1), str(b)], f"{a} - {b} = {a - b} icons are left.")
    return (f"There are {a} icons on the desktop. You add {b} new ones. How many icons are there now?", str(a + b),
            [str(a - b), str(a + b + 1), str(a + b - 1), str(a)], f"{a} + {b} = {a + b} icons.")
