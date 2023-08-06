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
sub-command module of progress operation
"""

import sys
import json
from pyopae import fpga
from pacutils import common


PAC_STATUS = {0:'IDLE', 1:'PROGRAM', 2:'PROGRAM', 3:'PROGRAM', 4:'REBOOT'}
PROG_CAL = {0:0, 1:1, 2:1, 3:60, 4:50}

class SubCmd(common.PACCmd):
    """
    definition of sub-command
    """
    name = 'progress'

    @staticmethod
    def run(args):
        common.PACCmd.run(args)
        common.probe_pac(args.bdf, args.eal_parameter)
        stat = fpga.get_status(args.bdf)
        if stat is None:
            fpga.cleanup_eal()
            sys.stderr.write('Failed to get status of FPGA!\n')
            sys.exit(common.E_PROPERTY_ERR)
        prog = {}
        val = list(stat.values())
        prog['status'] = PAC_STATUS.get(val[0], 'UNKNOWN')
        num = PROG_CAL.get(val[0], 0)
        if val[0] == 2:
            num += val[1] * 3 // 5
        if val[0] == 3:
            num += val[1] * 2 // 5
        prog['progress'] = '{}%'.format(num)
        print(json.dumps(prog))
        fpga.cleanup_eal()
