# vim: set fileencoding=utf-8
""" Extract hash value of admin password of given save.
    This value could be used to decide if Civ4 will hang
    up if use PB.load(savepath, password)

    Update: Script can now remove the password. Save
    will not be loadable by Civ4, but by the modified
    Pitboss EXE from Zulan.
"""

import sys
import struct

""" Structure of savegame
    Bytes   Desc
    4       ?
    4       Strlen A
    A       String, Modname
    4       Strlen B (0 or 32)

if B == 32, admin password is not empty. Some hashes store the
            status of DLL, Python and XML files, etc.

    32      String, Hash1
    4       ?
    4       Strlen C (16 common)
    C       String, Civ version
    4*36    Four strings with hashes

    4       A int which is decreased by 64 if no passwort is set.
    8       ?
    4       Strlen D
    2*D     WString, Gamename
    4       Stringlen E
    2*E     WString, Gamepassword
    4       Stringlen F (32)
    2*F       The MD5-HASH of the admin password

elif B == 0: Unprotected save. Here, the structure is
    4       ? (four zeros, probably an other string length.)
    4       Strlen C=0
    0       String, Civ version
    4*4     Four empty strings (length only)

    4       A int which is decreased by 64 if no passwort is set.
    8       ?
    4       Strlen D
    2*D     WString, Gamename
    4       Stringlen E
    2*E     WString, Gamepassword
    4       Stringlen F (0)
    0       The MD5-HASH of the admin password
    4       Stringlen G of Szenarioname/Worldbuildername
    2*G     The szenario name

"""


def get_int(f, fout):
    sx = rw(f, fout, 4)

    ix = struct.unpack('<' + 'B'*len(sx), sx)
    ret = ix[0] + (ix[1] << 8) + (ix[2] << 16) + (ix[3] << 24)
    return ret


def put_int(fout, val):
    sx = struct.pack('<' + 'B'*4,
                     (val >> 0) & 0xFF, (val >> 8) & 0xFF,
                     (val >> 16) & 0xFF, (val >> 24) & 0xFF
                     )
    fout.write(sx)
    return sx


def rw(fin, fout, num_bytes):
    b = fin.read(num_bytes)
    fout.write(b)
    return b


class WriteDummy:
    def write(self, b):
        pass

    def close(self):
        pass


def get_admin_hash(filename, filename_out=""):
    " Return string hash of admin value. "
    f = open(filename, "rb")
    fnull = WriteDummy()
    if len(filename_out) > 0:
        fout = open(filename_out, "wb")
    else:
        fout = WriteDummy()

    try:
        rw(f, fout, 4)
        modnameLen = get_int(f, fout)
        modname = rw(f, fout, modnameLen)

        hasPasswordFlag = get_int(f, fnull)
        hasPassword = (hasPasswordFlag == 32)
        if not hasPassword and hasPasswordFlag is not 0:
            sys.stderr.write("[FindHash] Abort, file can not parsed correctly (1).")
            return None
        if not hasPassword:
            # No password set
            # sys.stderr.write("[FindHash] Abort, no password set in input save.")
            return ""

        # Hash string, if password set. (this is not the password hash, it
        # follows later.)
        rw(f, fnull, 32)
        fout.write("\0\0\0\0")

        rw(f, fout, 4)  # Always empty string length?!

        civVersionLen = get_int(f, fnull)
        civVersion = rw(f, fnull, civVersionLen)
        fout.write("\0\0\0\0")

        # More hashes
        rw(f, fnull, 4*(4+32))
        for _ in range(4):
            fout.write("\0\0\0\0")

        unknown_interpretation = get_int(f, fnull)
        unknown_interpretation -= 64
        put_int(fout, unknown_interpretation)
        rw(f, fout, 8)

        gamenameLen = get_int(f, fout)
        gamename = rw(f, fout, 2*gamenameLen)  # wide string
        gamepwdLen = get_int(f, fout)
        gamepwd = rw(f, fout, 2*gamepwdLen)  # wide string

        # adminHashLen = get_int(f, fout)
        # Read password len, but write 0
        adminHashLen = get_int(f, fnull)
        fout.write("\0\0\0\0")

        if adminHashLen not in [32, 0]:
            sys.stderr.write("[FindHash] File can not parsed correctly (2).")
            return None
        if adminHashLen is 0:
            sys.stderr.write("[FindHash] No password set.")
            adminHash = ""
        else:
            # Read password, but write nothing
            adminHash = f.read(2*adminHashLen)  # wide string
            # remove nonprintable chars
            adminHash = adminHash[0:len(adminHash):2]

        # Write rest of input file
        rw(f, fout, -1)

        return adminHash
    finally:
        # Execute before function returns.
        f.close()
        fout.close()


if __name__ == "__main__":
    args = dict(zip(range(len(sys.argv)), sys.argv))
    print get_admin_hash(args.get(1, ""), args.get(2, ""))
