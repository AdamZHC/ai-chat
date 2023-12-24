

def execute(table:dict):
    f = table['A']
    f()
def A():
    print("A")
if __name__ == '__main__':
    tab = dict()
    tab['A'] = A
    execute(tab)