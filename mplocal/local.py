import os
import threading

def _ctx_switch(self):
    self_pid = object.__getattribute__(self, '_local__pid')
    self_thread_local = object.__getattribute__(self, '_local__thread_local')

    pid = os.getpid()
    if pid != self_pid:
        object.__setattr__(self, '_local__pid', pid)
        if not self_thread_local:
            object.__setattr__(self, '__dict__', {})
        local.__init__(self, bool(self_thread_local))
    return object.__getattribute__(self, '_local__thread_local')

class local(object):
    def __init__(self, thread_local=True):
        object.__setattr__(self, '_local__thread_local', threading.local() if thread_local else None)
        object.__setattr__(self, '_local__pid', os.getpid())
 
    def __getattribute__(self, name):
        if name in ('_local__thread_local', '_local__pid'):
            return object.__getattribute__(self, name)

        self_thread_local = _ctx_switch(self)
        if self_thread_local:
            return getattr(self_thread_local, name)
        return object.__getattribute__(self, name)
            

    def __setattr__(self, name, value):
        if name == '__dict__':
            raise AttributeError(
                "%r object attribute '__dict__' is read-only"
                % self.__class__.__name__)

        self_thread_local = _ctx_switch(self)
        if self_thread_local:
            return setattr(self_thread_local, name, value)
        return object.__setattr__(self, name, value)

    def __delattr__(self, name):
        if name == '__dict__':
            raise AttributeError(
                "%r object attribute '__dict__' is read-only"
                % self.__class__.__name__)
        self_thread_local = _ctx_switch(self)
        if self_thread_local:
            return delattr(self_thread_local, name)
        return object.__delattr__(self, name)
