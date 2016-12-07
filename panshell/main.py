
from panshell.core import Shell

from panshell.baidu import baiduFS
from panshell.local import localFS


def pansh():
    sh = Shell()
    sh.plugin(baiduFS)
    sh.plugin(localFS)
    sh.run()
