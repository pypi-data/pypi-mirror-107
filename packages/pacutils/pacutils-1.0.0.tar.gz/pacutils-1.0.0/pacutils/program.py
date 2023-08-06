#!/usr/bin/env python3
# Copyright(c) 2020, Intel Corporation
#
# Redistribution  and  use  in source  and  binary  forms,  with  or  without
# modification, are permitted provided that the following conditions are met:
#
# * Redistributions of  source code  must retain the  above copyright notice,
#   this list of conditions and the following disclaimer.
# * Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
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
sub-command module of program operation
"""

import sys
from pyopae import fpga
from pacutils import common


class SubCmd(common.PACCmd):
    """
    definition of sub-command
    """
    name = 'program'

    def def_args(self):
        super().def_args()
        self.parser.add_argument('--file', metavar='PATH',
                                 help='image file used to program')
        self.parser.add_argument('--reboot', action='store_true',
                                 help='reboot card after programming')

    @staticmethod
    def run(args):
        common.PACCmd.run(args)
        common.probe_pac(args.bdf, args.eal_parameter)
        proc_type = fpga.get_proc_type()
        if proc_type != common.PROC_PRIMARY:
            fpga.cleanup_eal()
            sys.stderr.write('Not primary process!\n')
            sys.exit(common.E_PROC_TYPE)

        if args.file is not None:
            ret = fpga.flash(args.bdf, args.file)
            if ret < 0:
                fpga.cleanup_eal()
                sys.stderr.write('Failed to update!\n')
                sys.exit(ret)
        if args.reboot:
            pf1_list = fpga.get_pf1(args.bdf)
            prop = fpga.get_property(pf1_list[0], common.PAC_PROP_PCI)
            pci_id = prop['id']
            if pci_id['vendor_id'] == common.VIRTIO_VID and \
               pci_id['device_id'] in common.VIRTIO_DID:
                common.run_cmd('rmmod virtio_net')
            ret = fpga.reboot(args.bdf)
            if ret < 0:
                fpga.cleanup_eal()
                sys.exit(ret)

        fpga.cleanup_eal()
