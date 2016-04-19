""" Extract hash value of admin password of given save.
    This value could be used to decide if Civ4 will hang
    up if use PB.load(savepath, password)
"""

import struct

""" Structure of savegame
    Bytes   Desc
    4       ?
    4       Strlen A
    A       String, Modname
    4       Strlen B (0 or 32)

if B == 0, admin password is empty. Otherwise:

    32      String, Hash1
    4       ?
    4       Strlen C (16 common)
    C       String, Civ version
    4*36    Four strings with hashes

    12      ?
    4       Strlen D
    2*D     WString, Gamename
    4       Stringlen E
    2*E     WString, Gamepassword
    4       Stringlen F (32)
    2*F       The MD5-HASH of the admin password

"""


def get_int(f):
    sx = f.read(4)
    ix = struct.unpack('<' + 'B'*len(sx), sx)
    ret = ix[0] + (ix[1] << 8) + (ix[2] << 16) + (ix[3] << 24)
    return ret


def get_admin_hash(filename):
    " Return string hash of admin value. "
    f = open(filename, "rb")
    try:
        f.read(4)
        modnameLen = get_int(f)
        modname = f.read(modnameLen)

        hasPasswordFlag = get_int(f)
        hasPassword = (hasPasswordFlag == 32)
        if not hasPassword and hasPasswordFlag is not 0:
            sys.stderr.write("[FindHash] File can not parsed correctly (1).")
            return None
        if not hasPassword:
            # No password set
            return ""

        f.read(32)
        f.read(4)
        civVersionLen = get_int(f)
        civVersion = f.read(civVersionLen)
        f.read(4*(4+32))
        f.read(12)
        gamenameLen = get_int(f)
        gamename = f.read(2*gamenameLen)  # wide string
        gamepwdLen = get_int(f)
        gamepwd = f.read(2*gamepwdLen)  # wide string
        adminHashLen = get_int(f)
        if adminHashLen is not 32:
            sys.stderr.write("[FindHash] File can not parsed correctly (2).")
            return None
        adminHash = f.read(2*adminHashLen)  # wide string
        adminHash = adminHash[0:len(adminHash):2]  # remove nonprintable chars
        return adminHash
    finally:
        # Execute before function returns.
        f.close()
