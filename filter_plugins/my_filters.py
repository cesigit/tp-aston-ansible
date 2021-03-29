import re
import sys
import subprocess
import pexpect

from natsort import natsorted


class FilterModule(object):
    def filters(self):
        return {
            'a_filter': self.a_filter,
            'latest_version': self.latest_version,
            'get_device': self.get_device
        }

    def a_filter(self, a_variable):
        a_new_variable = a_variable + ' CRAZY NEW FILTER'
        return a_new_variable

    def latest_version(self, list_of_version):
        array = list_of_version.split("\n")
        sorted = natsorted(array)
        res = sorted[::-1]
        for val in res:
            list_of_version = val
            if len(list_of_version) == 4:
                m = re.search(r'^(v\d{1}.\d{1})', list_of_version)
                if m.group(0):
                    break
        return list_of_version

    def get_device(self, list_device):
        disk = []
        device = []
        all_device=[]
        flag = 0
        type_format = ['swap', 'ext4', 'xfs', 'dos']
        line = list_device.split('\n')
        #return line
        for i in line:
            if 'Disk /' in i:
                disk.append(i)
        #return disk
        for v in disk:
            inter = v.split()
            all_device.append(inter[1][:-1])
        #return all_device
        for dev in all_device:
            #cmd = "lsblk -f {}".format(dev)
            cmd = "lsblk -f /dev/vdc"
            try:
                check_blk = str(subprocess.check_output(cmd, shell=True))
            except subprocess.CalledProcessError:
                print(sys.exc_info()[2])

            return check_blk
            for t in type_format:
                if t in check_blk:
                    flag = 1
                if flag == 0:
                    device.append(inter[1][:-1])
                flag = 0
        return device
