from pathlib import Path
import sys
sys.path.append(str(Path(__file__).parent.parent.parent))  #Make common library available
#from pathlib import PurePath

# print(Path("."))

# print(PurePath("."))

# print(Path.cwd())

# print(Path.name)

print(Path(__file__).parent.parent.parent)

if __name__ == '__main__':
    print('This will get executed only if')
    print('the module is invoked directly.')
    print('It will not run when this module is imported')


print(sys.path)

#import Roger.rover.rover
import common.shapes