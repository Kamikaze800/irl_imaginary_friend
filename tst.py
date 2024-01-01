with open('num.txt', 'r+', encoding='utf-8') as f:
    num = int(f.readlines()[-1])
    f.writelines(num + 1)

print(num)