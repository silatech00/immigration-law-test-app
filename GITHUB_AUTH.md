# GitHub auth & push (silatech00)

Repo: **https://github.com/silatech00/immigration-law-test-app**

Your Mac is currently logged into GitHub as a different account (`mikhailkhutorskoy0-lgtm`). Use one of the methods below to push as **silatech00**.

---

## Option 1 — Personal Access Token (recommended, fastest)

### 1. Create a token (while signed in as silatech00)

1. Sign in at [github.com](https://github.com) as **silatech00**
2. Go to **Settings → Developer settings → Personal access tokens → Tokens (classic)**
3. **Generate new token (classic)**
4. Name: `immigration-law-test-app`
5. Expiration: your choice (90 days is fine for a demo)
6. Scopes: check **`repo`** (full control of private repositories)
7. Generate and **copy the token** (you won't see it again)

Direct link: https://github.com/settings/tokens

### 2. Clear the old cached credentials on Mac

Open **Keychain Access** (Spotlight → "Keychain Access"):

1. Search for `github.com`
2. Delete entries related to GitHub / git credentials (especially anything tied to the old account)

Or in Terminal:

```bash
git credential-osxkeychain erase
host=github.com
protocol=https

```

(Press Enter twice after the blank line)

### 3. Push from this folder

```bash
cd "/Users/mikhailkhutorskoy/Desktop/EU AUDIT/immigration-law-test-app-upload"
git push -u origin main
```

When prompted:

- **Username:** `silatech00`
- **Password:** paste your **PAT** (not your GitHub password)

---

## Option 2 — GitHub CLI

### 1. Install GitHub CLI (if needed)

```bash
brew install gh
```

### 2. Log in as silatech00

```bash
gh auth login
```

Choose:

- GitHub.com
- HTTPS
- Login with a web browser (or paste a token)
- **Make sure you complete login while signed into silatech00 in the browser**

### 3. Push

```bash
cd "/Users/mikhailkhutorskoy/Desktop/EU AUDIT/immigration-law-test-app-upload"
git push -u origin main
```

---

## Option 3 — SSH key for silatech00

### 1. Generate a key (skip if you already have one for this account)

```bash
ssh-keygen -t ed25519 -C "silatech00@github" -f ~/.ssh/id_ed25519_silatech00
```

### 2. Add the public key to GitHub

Copy the public key:

```bash
cat ~/.ssh/id_ed25519_silatech00.pub
```

On GitHub (as **silatech00**): **Settings → SSH and GPG keys → New SSH key** → paste and save.

### 3. Use SSH remote and push

```bash
cd "/Users/mikhailkhutorskoy/Desktop/EU AUDIT/immigration-law-test-app-upload"
git remote set-url origin git@github.com:silatech00/immigration-law-test-app.git
GIT_SSH_COMMAND='ssh -i ~/.ssh/id_ed25519_silatech00 -o IdentitiesOnly=yes' git push -u origin main
```

Optional: add to `~/.ssh/config`:

```
Host github.com-silatech00
  HostName github.com
  User git
  IdentityFile ~/.ssh/id_ed25519_silatech00
  IdentitiesOnly yes
```

Then:

```bash
git remote set-url origin git@github.com-silatech00:silatech00/immigration-law-test-app.git
git push -u origin main
```

---

## Verify after push

Open https://github.com/silatech00/immigration-law-test-app — you should see all project files on `main`.

Then deploy on Streamlit Cloud using the **silatech00** GitHub login.

---

## Troubleshooting

| Error | Fix |
|-------|-----|
| `403 Permission denied to silatech00/...` | Wrong account cached — clear Keychain (Option 1 step 2) and retry with PAT |
| `Permission denied (publickey)` | SSH key not added to silatech00 account, or wrong key used |
| `Repository not found` | Repo doesn't exist or you're not signed in as silatech00 |
| Push rejected (non-fast-forward) | Repo has commits from manual upload — run `git pull origin main --rebase` then push again |
