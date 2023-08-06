# Copyright(c) 2020, Intel Corporation
#
# Redistribution  and  use  in source  and  binary  forms,  with  or  without
# modification, are permitted provided that the following conditions are met:
#
# * Redistributions of  source code  must retain the  above copyright notice,
#  this list of conditions and the following disclaimer.
# * Redistributions in binary form must reproduce the above copyright notice,
#  this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
# * Neither the name  of Intel Corporation  nor the names of its contributors
#   may be used to  endorse or promote  products derived  from this  software
#   without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING,  BUT NOT LIMITED TO,  THE
# IMPLIED WARRANTIES OF  MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED.  IN NO EVENT  SHALL THE COPYRIGHT OWNER  OR CONTRIBUTORS BE
# LIABLE  FOR  ANY  DIRECT,  INDIRECT,  INCIDENTAL,  SPECIAL,  EXEMPLARY,  OR
# CONSEQUENTIAL  DAMAGES  (INCLUDING,  BUT  NOT LIMITED  TO,  PROCUREMENT  OF
# SUBSTITUTE GOODS OR SERVICES;  LOSS OF USE,  DATA, OR PROFITS;  OR BUSINESS
# INTERRUPTION)  HOWEVER CAUSED  AND ON ANY THEORY  OF LIABILITY,  WHETHER IN
# CONTRACT,  STRICT LIABILITY,  OR TORT  (INCLUDING NEGLIGENCE  OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE,  EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

"""
common definitions to be used in other modules
"""

import re
import sys
import uuid
import mmap
import subprocess
from pyopae import fpga


PAC_VID = 0x8086
PAC_DID = [0x0b30]
VIRTIO_VID = 0x1af4
VIRTIO_DID = [0x1041]

AFU_TABLE = {'9aeffe5f-8457-0612-c000-c9660d824272': 'baseline',
             '8892c23e-2eed-4b44-8bb6-5c88606e07df': 'ovs',
             'b74cf419-d15a-481f-8991-165349d23ff9': 'vbng',
             '595b9b55-cd7e-4675-aa6d-8f6c22fc7eea': 'vran'}

EAL_PARAM_FMT = '-n 4 --proc-type=auto '\
                '--file-prefix {} '\
                '--log-level eal,{} '\
                '--log-level pmd,{} '\
                '--log-level driver.raw.init,{}'
EAL_DEFAULT_PARAMS = ('cyborg', 4, 0, 0)

MAP_SIZE = mmap.PAGESIZE
MAP_MASK = MAP_SIZE - 1
BAR_RESOURCE_FMT = '/sys/bus/pci/devices/{}/resource{}'

PROC_PRIMARY = 0
PROC_SECONDARY = 1

SHORT_BDF_PATTERN = r'([0-9a-fA-F]{1,2}):([0-9a-fA-F]{1,2})\.([0-9a-fA-F]{1})$'
LONG_BDF_PATTERN = r'([0-9a-fA-F]{1,4}):' + SHORT_BDF_PATTERN
BDF_FORMAT = '{:04x}:{:02x}:{:02x}.{:d}'

E_NO_MODULE = 1
E_BAD_USAGE = 2
E_INVALID_BDF = 3
E_NOT_PAC = 4
E_EAL_ERR = 5
E_PROC_TYPE = 6
E_PROPERTY_ERR = 7
E_INVALID_DRV = 8
E_NO_PF1 = 9

PAC_PROP_ALL = 0x00
PAC_PROP_PCI = 0x01
PAC_PROP_FME = 0x02
PAC_PROP_PORT = 0x04
PAC_PROP_BMC = 0x08


def run_cmd(cmd):
    """
    execute specified shell command
    """
    if isinstance(cmd, str):
        try:
            subprocess.call(cmd.split(), shell=False, timeout=30)
        except subprocess.TimeoutExpired as ex:
            print(ex)


def write_sysfs(path, value):
    """
    write a value to sysfs file
    """
    with open(path, 'w') as file_obj:
        file_obj.write(str(value))


def hex_arg(hex_str):
    """
    convert hexadecimal string to decimal number
    """
    val = int(hex_str, 16)
    return val


def bytes_to_uuid(byte_list, reverse=True):
    """
    convert byte list to UUID format string
    """
    hex_list = ["{:02x}".format(int(i)) for i in byte_list]
    if reverse:
        hex_list.reverse()
    uuid_str = str(uuid.UUID("".join(hex_list)))
    return uuid_str


def normalize_bdf(bdf):
    """
    make PCI address normalized to format xxxx:xx:xx.d
    """
    if bdf is None:
        return None
    rem = re.match(LONG_BDF_PATTERN, bdf)
    if rem:
        return BDF_FORMAT.format(int(rem.group(1),16), int(rem.group(2),16),
                                 int(rem.group(3),16), int(rem.group(4),16))
    rem = re.match(SHORT_BDF_PATTERN, bdf)
    if rem:
        return BDF_FORMAT.format(0, int(rem.group(1),16),
                                 int(rem.group(2),16), int(rem.group(3),16))
    sys.stderr.write('Invalid PCI address!\n')
    sys.exit(E_INVALID_BDF)


def read_afu_id(bdf=''):
    """
    read AFU UUID from specified PAC FPGA
    """
    val = fpga.pci_read(bdf, 0)
    if val is None:
        return None

    vid = val & 0xffff
    did = (val >> 16) & 0xffff
    if vid != PAC_VID or did not in PAC_DID:
        return None

    val = fpga.pci_read(bdf, 4)
    if val is None:
        return None
    if (val & 0x2) == 0:
        val |= 0x2
        fpga.pci_write(bdf, 4, val)

    idx = None
    path = BAR_RESOURCE_FMT.format(bdf, 0)
    with open(path, "rb", 0) as file_obj:
        mem = mmap.mmap(file_obj.fileno(), MAP_SIZE, mmap.MAP_SHARED,
                        mmap.PROT_READ, 0, 0)
        num_ports = (mem[0x32] & 0x6) >> 1
        if num_ports > 0:
            port_implemented = (mem[0x3f] & 0x10) >> 4
            if port_implemented == 1:
                idx = mem[0x3c] & 0x7
        mem.close()

    if idx is None:
        return None

    path = BAR_RESOURCE_FMT.format(bdf, idx)
    with open(path, "rb", 0) as file_obj:
        mem = mmap.mmap(file_obj.fileno(), MAP_SIZE, mmap.MAP_SHARED,
                        mmap.PROT_READ, 0, 0)
        afu_offset = mem[0x18] | (mem[0x19] << 8) | (mem[0x1a] << 16)
        mem.close()
        if afu_offset in (0, 0xffffff):
            return None

        mem = mmap.mmap(file_obj.fileno(), MAP_SIZE, mmap.MAP_SHARED,
                        mmap.PROT_READ, 0, afu_offset & ~MAP_MASK)
        afu_id = mem[0x8:0x10] + mem[0x10:0x18]
        mem.close()

    return afu_id


def check_pac(bdf):
    """
    check specified PCI device is PAC FPGA
    """
    if bdf is None:
        sys.stderr.write('No specified PCI address!\n')
        sys.exit(E_BAD_USAGE)

    val = fpga.pci_read(bdf, 0)
    if val is None:
        sys.stderr.write('Failed to read PCI configuration space!\n')
        sys.exit(E_PROPERTY_ERR)

    vid = val & 0xffff
    did = (val >> 16) & 0xffff
    if vid != PAC_VID or did not in PAC_DID:
        sys.stderr.write('Not PAC card!\n')
        sys.exit(E_NOT_PAC)


def probe_pac(bdf, eal_param):
    """
    probe specified PAC FPGA with OPAE driver
    """
    check_pac(bdf)
    prop = fpga.get_property(bdf, PAC_PROP_PCI)
    if prop is None:
        sys.stderr.write('Failed to get PCI proptery of {}!\n'.format(bdf))
        sys.exit(E_PROPERTY_ERR)

    run_cmd('modprobe vfio-pci')
    if prop['driver'] != 'vfio-pci':
        ret = fpga.bind(bdf, 'vfio-pci')
        if ret < 0:
            sys.stderr.write('Failed to bind vfio-pci driver'\
                             'to {}!\n'.format(bdf))
            sys.exit(E_INVALID_DRV)

    ret = fpga.init_eal(eal_param)
    if ret < 0:
        sys.stderr.write('Failed to initialize EAL!\n')
        sys.exit(E_EAL_ERR)


class PACCmd():
    """
    base class of PAC command mechanism
    """
    commands = {}

    @classmethod
    def register_command(cls, subparsers, command_class):
        """
        register PAC sub-command
        """
        if command_class.name in cls.commands:
            sys.stderr.write('Command is already registered!\n')
        else:
            subparser = subparsers.add_parser(command_class.name)
            cls.commands[command_class.name] = command_class(subparser)

    def __init__(self, parser):
        self.parser = parser
        self.parser.set_defaults(func=self.run)
        self.def_args()

    def def_args(self):
        """
        define optional arguments for command
        """
        self.parser.add_argument('--log-level', type=int,
                                 choices=[0,1,2,3,4], metavar='INT',
                                 help='set logging level of OPAE API')
        self.parser.add_argument('--log-file', metavar='PATH',
                                 help='set logging file of OPAE API')
        self.parser.add_argument('--pci-address', metavar='BDF',
                                 help='PCI address of PAC FPGA in BDF format')
        self.parser.add_argument('--eal-parameter', metavar='STR',
                                 help='DPDK EAL initialization parameters')
        self.parser.add_argument('--json-indent', type=int,
                                 default=4, metavar='INT',
                                 help='indention of JSON output')

    @staticmethod
    def run(args):
        """
        perform operations according to the command
        """
        if args.log_level is not None:
            fpga.set_log_level(args.log_level)
        if args.log_file is not None:
            fpga.set_log_file(args.log_file)
        args.bdf = normalize_bdf(args.pci_address)
        if args.eal_parameter is None:
            args.eal_parameter = EAL_PARAM_FMT.format(*EAL_DEFAULT_PARAMS)
