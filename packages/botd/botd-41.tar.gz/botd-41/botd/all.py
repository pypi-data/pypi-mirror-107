"all modules"

from botl.krn import Kernel

import botd.adm
import botd.fnd
import botd.log
import botd.rss
import botd.slg
import botd.tdo
import botd.udp

Kernel.addmod(botd.adm)
Kernel.addmod(botd.fnd)
Kernel.addmod(botd.log)
Kernel.addmod(botd.rss)
Kernel.addmod(botd.slg)
Kernel.addmod(botd.tdo)
Kernel.addmod(botd.udp)
