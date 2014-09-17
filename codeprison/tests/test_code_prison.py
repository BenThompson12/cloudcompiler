import unittest
from  textwrap import dedent

from codeprison.exec_code import exec_code, override_limit, restore_default_limits

class PythonTestFunctions(unittest.TestCase):

    def test_print(self):
        res = exec_code("python", 
            dedent(
                """\
                print 'hello' 
                """
            ),"")
        
        self.assertEqual(res['stdout'], "hello\n")


class PythonTestFileConstraints(unittest.TestCase):

    def test_cant_access_root(self):
        res = exec_code("python", 
            dedent(
                """\
                import os
                for file in os.listdir("/"):
                    print file
                print "success"
                """
            ),"")

        self.assertNotIn("success", res['stdout'])

    def test_cant_write_file(self):
        res = exec_code("python", 
            dedent(
                """\
                fo = open("temp", "wb")
                fo.write("hello")
                fo.close()
                print "success"
                """
            ),"")

        self.assertNotIn("success", res['stdout'])

    def test_cant_write_temp_files(self):
        res = exec_code("python", 
            dedent(
                """\
                import os
                import tempfile
                f, path = tempfile.mkstemp()
                os.close(f)
                print "success"
                """
            ),"")

        self.assertNotIn("success", res['stdout'])

    def test_cant_access_other_sandbox(self):
        res = exec_code("python", 
            dedent(
                """\
                for file in os.listdir("/tmp/sandbox"):
                    print file
                print "success"
                """
            ),"")

        self.assertNotIn("success", res['stdout'])

class PythonTestResourceConstraints(unittest.TestCase):

    def test_cant_use_excess_time(self):
        override_limit("REAL_TIME", 2)

        res = exec_code("python", 
            dedent(
                """\
                import time
                time.sleep(3)
                print "success"
                """
            ),"")

        restore_default_limits()

        self.assertNotIn("success", res['stdout'])

    def test_override_time_limit(self):
        override_limit("REAL_TIME", 4)

        res = exec_code("python", 
            dedent(
                """\
                import time
                time.sleep(3)
                print "success"
                """
            ),"")

        restore_default_limits()

    def test_cant_use_network(self):
        res = exec_code("python", 
            dedent(
                """\
                from urllib import urlopen
                data = urlopen("http://www.google.com").read()
                print "success"
                """
            ),"")

        self.assertNotIn("success", res['stdout'])

    def test_cant_fork(self):
        return

        res = exec_code("python", 
            dedent(
                """\
                import os
                os.fork()
                print "ok"
                """
            ),"")

        self.assertNotIn("ok", res['stdout'])

    def test_cant_use_excess_memory(self):
        override_limit("VMEM", 10 * 1024000)
        res = exec_code("python", 
            dedent(
                """\
                print len(bytearray(20 * 1024000))
                print "success"
                """
            ),"")

        self.assertNotIn("success", res['stdout'])

        restore_default_limits()

    def test_can_override_vmem_limit(self):
        override_limit("VMEM", 100 * 1024000)

        res = exec_code("python", 
            dedent(
                """\
                print len(bytearray(20 * 1024000))
                print "success"
                """
            ),"")

        self.assertIn("success", res['stdout'])

        restore_default_limits()


            
