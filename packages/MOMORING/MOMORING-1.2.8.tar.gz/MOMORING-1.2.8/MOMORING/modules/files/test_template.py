def get_test_template(path):
    txt = """\
import os


def test():
    # set default path
    os.environ.setdefault('DATAPATH', os.path.join('%s', 'test', 'datapath'))
    os.environ.setdefault('STASHPATH', os.path.join('%s', 'test', 'stashpath'))
    os.environ.setdefault('SAVEDPATH', os.path.join('%s', 'test', 'savedpath'))
    
    # set default env
    json_template = {
        'env': {'None': None},
        'CPU': 1
    }
    
    for i in json_template['env'].keys():
        os.environ.setdefault(i, str(json_template['env'][i]))

    # test your code here
    pass
    
if __name__ == '__main__':
    test()
"""
    txt = txt % (path, path, path)
    return txt
