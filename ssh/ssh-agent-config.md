# Auto-load SSH Keys to Agent

**Category:** DevOps / Git
**Date:** 2026-01-09

If Git asks for the SSH key passphrase on every `git push`, you can configure SSH to automatically add the key to the agent so you only type the password once per session.

### The Fix

1. Create or edit `~/.ssh/config`:

```ssh
Host *
  AddKeysToAgent yes
  IdentityFile ~/.ssh/id_ed25519

```

*(Replace `id_ed25519` with `id_rsa` if using an older key type)*

2. **Crucial:** Secure the file permissions so SSH accepts it:

```bash
chmod 600 ~/.ssh/config

```


### Quick Tip for your Dotfiles
Since you maintain a **dotfiles** repository, you might be tempted to commit this file.
* **Safe to commit:** The config file itself (it contains no secrets, just paths and settings).
* **Do NOT commit:** The actual key files (`id_ed25519`).

