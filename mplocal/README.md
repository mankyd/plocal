mplocal is a module designed to replace Python's threading.local object with a
storage object that is both local to the current thread as well as to the 
current process. Python's threading.local is not normally local to only the
current thread. Try the following examples:

    import threading
    import multiprocessing
    l = threading.local()
    l.x = 'a'
    def  f():
        print getattr(l, 'x', 'b'),
    p = multiprocessing.Process(target=f)
    p.start()
    p.join()
    f()

The above code will print "aa" instead of printing what one might expect: "ba".
Note the if you use threading.Thread instead of multiprocessing.Process, you 
will in fact get "ba" not "aa".

Now try the following code using mplocal:

    import mplocal
    import multiprocessing
    l = mplocal.local()
    l.x = 'a'
    def  f():
        print getattr(l, 'x', 'b'),
    p = multiprocessing.Process(target=f)
    p.start()
    p.join()
    f()

The above code prints "ba" because the mplocal module is sensitive to the
current process as well as thread.

The local class provided by mplocal includes one configuration option
"threading_local" which determines whether the process is sensitive to changes
in the thread as well as process or just changes in process. It defaults to true
so, making this class a drop in replacement for threading.local.