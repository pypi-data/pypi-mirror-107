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
sub-command module of setup operation
"""

import os
import sys
from pyopae import fpga
from pacutils import common


class SubCmd(common.PACCmd):
    """
    definition of sub-command
    """
    name = 'setup'

    def def_args(self):
        super().def_args()
        self.parser.add_argument('--vf-num', type=int, default=4,
                                 metavar='INT', help='number of VFs to create')

    @staticmethod
    def run(args):
        common.PACCmd.run(args)
        common.check_pac(args.bdf)
        afu_id = common.read_afu_id(args.bdf)
        if afu_id is None:
            sys.stderr.write('Failed to get AFU ID!\n')
            sys.exit(common.E_PROPERTY_ERR)

        afu_id = common.bytes_to_uuid(afu_id)
        afu_type = common.AFU_TABLE.get(afu_id, 'unknown')
        if afu_type == 'ovs':
            pf1_list = fpga.get_pf1(args.bdf)
            if pf1_list is None or len(pf1_list) == 0:
                sys.stderr.write('Failed to get PF1 of FPGA!\n')
                sys.exit(common.E_NO_PF1)

            path = os.path.join('/sys/bus/pci/devices', pf1_list[0],
                                'sriov_numvfs')
            common.run_cmd('service NetworkManager stop')
            common.write_sysfs(path, args.vf_num)
            common.run_cmd('service NetworkManager start')
