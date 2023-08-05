def decorator_name(func):
    print('Here')
    def some():
        print('Under')
        return func()
    print('Done')
    return some()

def foo(a,b,*args,**kwargs):
    print("A:", a)
    primt("B:", b)

