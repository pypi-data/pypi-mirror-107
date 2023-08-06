"all modules"

from bot.krn import Kernel

import gcd.req
import gcd.slg
import gcd.sui
import gcd.trt
import gcd.wsd
import gcd.ver

Kernel.addmod(gcd.req)
Kernel.addmod(gcd.slg)
Kernel.addmod(gcd.sui)
Kernel.addmod(gcd.trt)
Kernel.addmod(gcd.wsd)
Kernel.addmod(gcd.ver)
