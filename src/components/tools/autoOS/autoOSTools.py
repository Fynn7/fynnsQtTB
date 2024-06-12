import os


def addSuffixToFilename(dirName: str, suffix: str, _type: str | None = None):
    '''
    Add a suffix to multiple filenames in a directory
    '''
    if _type is None:
        for filename in os.listdir(dirName):
            os.rename(os.path.join(dirName, filename),
                      os.path.join(dirName, filename + suffix))
    else:
        for filename in os.listdir(dirName):
            if filename.endswith('.'.join([_type])):
                os.rename(os.path.join(dirName, filename),
                        os.path.join(dirName, filename + suffix))

def addPrefixToFilename(dirName: str, prefix: str, _type: str | None = None):
    '''
    Add a prefix to multiple filenames in a directory
    '''
    if _type is None:
        for filename in os.listdir(dirName):
            os.rename(os.path.join(dirName, filename),
                      os.path.join(dirName, prefix + filename))
    else:
        for filename in os.listdir(dirName):
            if filename.endswith('.'.join([_type])):
                os.rename(os.path.join(dirName, filename),
                        os.path.join(dirName, prefix + filename))
