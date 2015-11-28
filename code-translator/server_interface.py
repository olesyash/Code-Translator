__author__ = 'olesya'

'''
This Class will perform the connection between web to server.
Getting code from web side and using 3 steps before giving result back to web side
1. Use Parser to isolate which words should be "translated"
2. Use specific language api treatment to access needed API
3. Use specific language result parser to get the right result
'''


class ServerInterface():
    def get_translation(self):
        pass


