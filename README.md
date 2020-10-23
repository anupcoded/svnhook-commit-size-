# svnhook-commit-size-
svn hook to check commit size and stop uploads of files greater than maximum size set

Usage:

```
# pre-commit hook
set REPOS=%1
set TXN=%2
%~dp0check_size.py %REPOS% %TXN% || exit 1
```
