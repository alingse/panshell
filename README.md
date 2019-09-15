# panshell
shell everything /(shell for &lt;baidu> yunpan filesystem)


## 大概的设计

MVP:

满足浏览、重命名、移动 百度云盘数据

在 bash 中操作的命令

- pansh
- login xxx
- ls
- cd
- mv
- exit

main -> shell -> fs(login/exit) -> ls/cd/mv

不做的一些事情

1. 不支持本地 + 百度切换(多 FS)
2. 先不做下载、上传
3. 不支持存储 session / token
