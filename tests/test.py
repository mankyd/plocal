from nose.tools import *
import os
import threading
import unittest

from plocal import local

class TestBasics(unittest.TestCase):
    def test_assignment(self):
        l = local()
        l.x = 1
        ok_(l.x == 1)

    def test_reassignment(self):
        l = local()
        l.x = 1
        ok_(l.x == 1)
        l.x = 2
        ok_(l.x == 2)
        
    @raises(AttributeError)
    def test_deletion(self):
        l = local()
        l.x = 1
        ok_(l.x == 1)
        del l.x
        l.x


class TestThreading(unittest.TestCase):
    def test_namespace(self):
        l = local()
        def f():
            assert_raises(AttributeError, lambda: l.x)
            l.y = 'b'
            ok_(l.y == 'b')

        l.x = 'a'
        th = threading.Thread(target=f)
        th.start()
        th.join()
        assert_raises(AttributeError, lambda: l.y)

    def test_assignment(self):
        l = local()
        def f():
            l.x = 'b'
            ok_(l.x == 'b')
        l.x = 'a'
        ok_(l.x == 'a')
        th = threading.Thread(target=f)
        th.start()
        th.join()
        ok_(l.x == 'a')

    def test_deletion(self):
        l = local()
        def f():
            l.x = 'b'
            ok_(l.x == 'b')
            del l.x
            assert_raises(AttributeError, lambda: l.x)

        l.x = 'a'
        ok_(l.x == 'a')
        th = threading.Thread(target=f)
        th.start()
        th.join()
        ok_(l.x == 'a')

class TestMultiProcessOnly(unittest.TestCase):
    def test_namespace(self):
        l = local(thread_local=False)
        l.x = 'a'
        pid = os.fork()
        if pid:
            os.wait()
            assert_raises(AttributeError, lambda: l.y)
        else:
            assert_raises(AttributeError, lambda: l.x)
            l.y = 'b'
            ok_(l.y == 'b')

    def test_assignment(self):
        l = local(thread_local=False)
        l.x = 'a'
        ok_(l.x == 'a')
        pid = os.fork()
        if pid:
            os.wait()
            ok_(l.x == 'a')
        else:
            l.x = 'b'
            ok_(l.x == 'b')

    def test_deletion(self):
        l = local(thread_local=False)

        l.x = 'a'
        ok_(l.x == 'a')
        pid = os.fork()
        if pid:
            os.wait()
            ok_(l.x == 'a')
        else:
            l.x = 'b'
            ok_(l.x == 'b')
            del l.x
            assert_raises(AttributeError, lambda: l.x)

    def test_threading_namespace(self):
        l = local(thread_local=False)
        def f():
            ok_(l.x == 'a')
            l.y = 'b'
            ok_(l.y == 'b')

        l.x = 'a'
        th = threading.Thread(target=f)
        th.start()
        th.join()
        ok_(l.y == 'b')

    def test_threading_assignment(self):
        l = local(thread_local=False)
        def f():
            l.x = 'b'
            ok_(l.x == 'b')
        l.x = 'a'
        ok_(l.x == 'a')
        th = threading.Thread(target=f)
        th.start()
        th.join()
        ok_(l.x == 'b')

    def test_threading_deletion(self):
        l = local(thread_local=False)
        def f():
            l.x = 'b'
            ok_(l.x == 'b')
            del l.x
            assert_raises(AttributeError, lambda: l.x)

        l.x = 'a'
        ok_(l.x == 'a')
        th = threading.Thread(target=f)
        th.start()
        th.join()
        assert_raises(AttributeError, lambda: l.x)
