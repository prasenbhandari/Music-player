'''

Rfile.fread(file,xa)
                x=number
                a= 'L' - x lines
                   'l' - x th line
                   'C' - x characters
                   'c' - x th character

Rfile.fwrite(file,writeText,'o')
                o=overwrite
                else it will apend
Rfile.fnew(file)
                make new file

Rfile.fnewwrite(file,writeText,'o')
                make new file and write

Rfile.fremove(file)
                remove file
'''


def fread(FileName, Lines=''):
    f = open(FileName)
    try:
        Liness = Lines.split('.')

        if Lines:
            if Liness[1] == 'l' and Liness[0] != '':
                for i in range(int(Liness[0]) - 1):
                    f.readline()
                return f.readline()

            if Liness[1] == 'L' and Liness[0] != '':
                xx = ''
                for i in range(int(Liness[0])):
                    xx += f.readline()
                return xx

            if Liness[1] == 'c' and Liness[0] != '':
                xx = f.read()
                return xx[int(Liness[0]) - 1]

            if Liness[1] == 'C' and Liness[0] != '':
                return f.read(int(Liness[0]))


        else:
            return f.read()


    except:
        return "%Error%"
    finally:
        f.close()


def fwrite(FileName, txt='', Lines=' '):
    try:
        if Lines[0] == 'o':
            f = open(FileName, 'w')
            f.write(txt)
            f.close()

        else:
            f = open(FileName, 'a')
            f.write(txt)
            f.close()
    except:
        return "%Error%"


def fnew(FileName):
    try:
        f = open(FileName, 'x')
        f.close();
    except:
        return "%Error%"


def fnewwrite(FileName, txt='', Lines=' '):
    import os
    if os.path.exists("demofile.txt"):
        txt = ''
    else:
        fnew(FileName)
    try:
        if Lines[0] == 'o':
            f = open(FileName, 'w')
            f.write(txt)
            f.close()

        else:
            f = open(FileName, 'a')
            f.write(txt)
            f.close()
    except:
        return "%Error%"


def fremove(FileName):
    import os
    try:
        os.remove(FileName)
    except:
        return "%Error%"
