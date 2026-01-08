# Git: --force vs --force-with-lease

## TIL the difference between `--force` and `--force-with-lease`

### `--force`
- Overwrites remote branch unconditionally
- Ignores any changes others may have pushed
- Can lead to **lost commits** if teammates pushed while you were working
- Use with extreme caution

```bash
git push --force origin main
```

### `--force-with-lease`
- Safer alternative to `--force`
- Only overwrites if remote branch is in the expected state
- **Rejects push** if someone else pushed changes since your last fetch
- Protects against accidentally overwriting others' work

```bash
git push --force-with-lease origin main
```

### When to use
- **Prefer `--force-with-lease`** for most rebase/amend scenarios
- Only use `--force` when you're certain no one else is working on the branch

### Pro tip
Fetch before force-pushing to ensure `--force-with-lease` has the latest remote state:
```bash
git fetch
git push --force-with-lease origin main
```