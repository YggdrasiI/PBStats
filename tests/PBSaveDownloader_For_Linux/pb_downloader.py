#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import with_statement

import os
import os.path
import sys
import time
import errno
import re
import urllib2
import socket
# import pdb

from fuse import FUSE, FuseOSError, Operations

import logging


class Passthrough(Operations):
    def __init__(self, root):
        self.root = root
        self.pitboss_roots = [
            "/home/civpb/_https_pb.zulan.net",
            "/home/civpb/_http_pb.zulan.net",
            "/home/civpb/_url_pb.zulan.net",
            "/home/civpb/_https_148.251.130.188",
            "/home/civpb/_http_148.251.130.188",
            "/home/civpb/_url_148.251.130.188",
        ]

        self.running_downloads = {}

    # Helpers
    # =======

    def _full_path(self, partial):
        if partial.startswith("/"):
            partial = partial[1:]
        path = os.path.join(self.root, partial)
        return path

    def _is_pitboss_path(self, path):
        for r in self.pitboss_roots:
            if path.startswith(r):
                return True
            if r.startswith(path):
                return True

        return False

    def _is_old_save(self, path):
        for r in self.pitboss_roots:
            if path.startswith(r):
                time_diff_s = (time.time() -
                               os.path.getmtime(self._full_path(path)))
                print("Timestamp: {}".format(time_diff_s))
                if time_diff_s > 30:
                    print("Save marked as old. Timestampe difference: {:.4}"
                          "".format(time_diff_s))
                    return True

        # File not found
        return False

    def _download_save(self, path):
        full_path = self._full_path(path)
        url = None

        for r in self.pitboss_roots:
            if path.startswith(r):
                domain = os.path.basename(r)
                # Replace _https_, _http_ and _url_
                domain = re.sub("_https_", "https://", domain)
                domain = re.sub("_http_", "http://", domain)
                domain = re.sub("_url_", "https://", domain)
                # /pb/PBs/{PBNAME}/Saves/pitboss/auto/Recovery_{USERNAME}.CivBeyondSwordSave
                url = path[len(r):]
                url = domain + url
                break

        if not url:
            # No proper pitboss_root folder exists for this path
            return False

        if path in self.running_downloads:
            print("Hey, download of '{}' is already runnning.".format(path))
            # TODO: Maybe waiting in this thread?!
            return False

        print("Start download {}".format(url))
        self.running_downloads[path] = url
        ret = False

        try:
            r = urllib2.urlopen(url, timeout=30)
            CHUNK_SIZE = 1 << 20
            with open(full_path, 'wb') as f:
                while True:
                    chunk = r.read(CHUNK_SIZE)
                    if not chunk:
                        break
                    f.write(chunk)

        except urllib2.URLError as e:
            # timeout raises this exception type in some python versions
            print("Error during download: {}".fomat(e))
        except socket.timeout as e:
            print("Error during download: {}".fomat(e))
        except Exception as e:
            print("Error during download: {}".fomat(e))
        else:
            print("download sucsessful")
            ret = True
        finally:
            del self.running_downloads[path]

        return ret

    # Filesystem methods
    # ==================

    def access(self, path, mode):
        full_path = self._full_path(path)
        if not os.access(full_path, mode):
            raise FuseOSError(errno.EACCES)

    def chmod(self, path, mode):
        full_path = self._full_path(path)
        return os.chmod(full_path, mode)

    def chown(self, path, uid, gid):
        full_path = self._full_path(path)
        return os.chown(full_path, uid, gid)

    def getattr(self, path, fh=None):
        full_path = self._full_path(path)

        if not os.path.exists(full_path) and self._is_pitboss_path(path):
            if not full_path.lower().endswith(".civbeyondswordsave"):
                # Assume that every other path in a dir
                os.mkdir(full_path, 0o755)

        if full_path.lower().endswith(".civbeyondswordsave"):
            if not os.path.exists(full_path) or self._is_old_save(path):
                self._download_save(path)

        st = os.lstat(full_path)
        return dict((key, getattr(st, key)) for key in (
            'st_atime', 'st_ctime',
            'st_gid', 'st_mode', 'st_mtime', 'st_nlink', 'st_size', 'st_uid'))

    def readdir(self, path, fh):
        full_path = self._full_path(path)

        dirents = ['.', '..']
        if os.path.isdir(full_path):
            dirents.extend(os.listdir(full_path))
        for r in dirents:
            yield r

    def readlink(self, path):
        pathname = os.readlink(self._full_path(path))
        if pathname.startswith("/"):
            # Path name is absolute, sanitize it.
            return os.path.relpath(pathname, self.root)
        else:
            return pathname

    def mknod(self, path, mode, dev):
        return os.mknod(self._full_path(path), mode, dev)

    def rmdir(self, path):
        full_path = self._full_path(path)
        return os.rmdir(full_path)

    def mkdir(self, path, mode):
        return os.mkdir(self._full_path(path), mode)

    def statfs(self, path):
        full_path = self._full_path(path)
        stv = os.statvfs(full_path)
        return dict((key, getattr(stv, key)) for key in (
            'f_bavail', 'f_bfree',
            'f_blocks', 'f_bsize', 'f_favail', 'f_ffree', 'f_files', 'f_flag',
            'f_frsize', 'f_namemax'))

    def unlink(self, path):
        return os.unlink(self._full_path(path))

    def symlink(self, name, target):
        return os.symlink(target, self._full_path(name))

    def rename(self, old, new):
        return os.rename(self._full_path(old), self._full_path(new))

    def link(self, target, name):
        return os.link(self._full_path(name), self._full_path(target))

    def utimens(self, path, times=None):
        return os.utime(self._full_path(path), times)

    # File methods
    # ============

    def open(self, path, flags):
        full_path = self._full_path(path)
        return os.open(full_path, flags)

    def create(self, path, mode, fi=None):
        full_path = self._full_path(path)
        return os.open(full_path, os.O_WRONLY | os.O_CREAT, mode)

    def read(self, path, length, offset, fh):
        os.lseek(fh, offset, os.SEEK_SET)
        return os.read(fh, length)

    def write(self, path, buf, offset, fh):
        os.lseek(fh, offset, os.SEEK_SET)
        return os.write(fh, buf)

    def truncate(self, path, length, fh=None):
        full_path = self._full_path(path)
        with open(full_path, 'r+') as f:
            f.truncate(length)

    def flush(self, path, fh):
        return os.fsync(fh)

    def release(self, path, fh):
        return os.close(fh)

    def fsync(self, path, fdatasync, fh):
        return self.flush(path, fh)


def main(mountpoint, root):
    FUSE(Passthrough(root), mountpoint, nothreads=True, foreground=True)


def print_help():
    print("""Usage:
    1. Create two folders:
        DOWNLOAD_DIR: This script will store the files into this local folder.
        MOUNT_TARGET: This folder should be the target of the 'z:' symbolic link of wine.

    2. Call 'winecfg' and connect drive 'z:' with MOUNT_TARGET
    3. Call this script:
          {} {{DOWNLOAD_DIR}} {{MOUNT_TARGET}}
          """.format(sys.argv[0]))

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)

    if len(sys.argv) < 3:
        print_help()
    else:
        main(sys.argv[2], sys.argv[1])
