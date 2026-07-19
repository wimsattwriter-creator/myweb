# Git Push Fix

If `git push` on this repo fails with a 403 ("Permission to wimsattwriter-creator/myweb.git denied to wimsattj"), the `gh` CLI's active account is set to the wrong one. The credential helper uses whichever `gh` account is active, and this repo is owned by `wimsattwriter-creator`, not `wimsattj`.

Fix — switch the active account, then push:

```
gh auth switch --user wimsattwriter-creator
git push
```

No need to touch the remote URL or SSH keys — the remote is already HTTPS and correctly configured.
