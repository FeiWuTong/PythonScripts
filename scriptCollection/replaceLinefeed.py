#! python3

while True:
    print("\n===============\nInput here:\n===============\n")
    dat = ""
    while True:
        temp = input()
        if not temp:
            break
        dat += temp + " "
    if not dat:
        break
    print(dat)
