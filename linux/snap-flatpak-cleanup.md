# Clean Up Snap and Flatpak Space

TIL - By default, Snap secretly keeps the last 2 or 3 versions of every app you install just in case an update breaks and you need to revert. Over time, this wastes gigabytes of space.

You can clean up old, disabled snaps using the following script:

```bash
set -eu
sudo snap list --all | awk '/disabled/{print $1, $3}' |
    while read snapname revision; do
        sudo snap remove "$snapname" --revision="$revision"
    done
```

Additionally, you can uninstall unused flatpak runtimes to save more space:

```bash
flatpak uninstall --unused
```
