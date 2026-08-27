# Putting omegasolarproducts.com live

The repository is already built, committed and sitting on your Mac at
`~/Documents/GitHub/omegasolarproducts`. Everything inside it is configured
for your domain. Two jobs are left, and neither needs technical knowledge:

1. **Publish it from GitHub Desktop** (about 3 minutes)
2. **Fix five DNS records at GoDaddy** (about 5 minutes)

Then wait for DNS to spread — usually 30 minutes, occasionally a few hours.

Do them in that order. GitHub needs to see the site before it will issue the
HTTPS certificate for your domain.

---

## Part 1 — GitHub Desktop (do this first)

The repository is already on your Mac at:

```
~/Documents/GitHub/omegasolarproducts
```

Every file is in place and already committed. You do not need to create
anything, copy anything or use the website upload.

### 1.1 Add it to GitHub Desktop

1. Open **GitHub Desktop**.
2. If you have not signed in yet: **GitHub Desktop → Settings → Accounts →
   Sign in**. Use your GitHub account.
3. Menu bar: **File → Add Local Repository…**
4. Click **Choose…** and pick
   `Documents → GitHub → omegasolarproducts`
5. Click **Add Repository**.

It should open showing "No local changes" — that is correct, everything is
already committed.

### 1.2 Publish it

1. Click the blue **Publish repository** button at the top.
2. Name: leave as `omegasolarproducts`.
3. **Untick "Keep this code private."**

   This matters: GitHub Pages does not work on private repositories with a
   free account. A website's files are public once the site is live anyway —
   just never put passwords or customer data in this folder.
4. Click **Publish repository**.

That is the upload done. Give it about thirty seconds.

### 1.3 Switch Pages on

1. In GitHub Desktop, menu bar: **Repository → View on GitHub**. Your browser
   opens at the repository.
2. Click **Settings** (top row of the repository, not your account settings).
3. Left sidebar: **Pages**.
4. Under **Build and deployment**:
   - Source: **Deploy from a branch**
   - Branch: **main** · folder: **/ (root)**
   - Click **Save**
5. Wait 1–2 minutes and refresh the page. A green tick appears with a link
   like `https://instackout.github.io/omegasolarproducts/`.

   **Open that link and check the site loads.** If it does, the hard part is
   over.

Because `CNAME` is already in the repository, the **Custom domain** box on
that same screen will fill itself in with `omegasolarproducts.com`. It will
show a DNS warning until you finish Part 2 — that is expected.

### 1.4 Note your username

Look at the address bar: `github.com/instackout/omegasolarproducts`.
Write down that username — you need it once, in step 2.4.

---

## Part 2 — GoDaddy DNS

### 2.1 Open the DNS screen

1. Sign in at **godaddy.com**.
2. Top right, your name → **My Products**.
3. Find **omegasolarproducts.com** → click **DNS** (or **Manage DNS**).

You are now on a page listing records — mostly a parked A record and a few
CNAMEs GoDaddy added.

### 2.2 Delete GoDaddy's parking records

I checked your domain's live DNS on 25 August 2026. It is currently parked,
and these three records are what is pointing it at GoDaddy's holding page.
**Delete exactly these:**

| Type  | Name | Current value              | Action |
|-------|------|----------------------------|--------|
| A     | @    | `76.223.105.230`           | Delete |
| A     | @    | `13.248.243.5`             | Delete |
| CNAME | www  | `omegasolarproducts.com`   | Delete |

Use the pencil or bin icon at the right of each row.

**Leave every MX, TXT and NS record exactly as it is.** Deleting an MX record
would stop email reaching you. You are only touching the two `@` A records and
the `www` CNAME.

If you see slightly different values when you get there, GoDaddy has rotated
its parking IPs — the rule still holds: remove every **A** record named `@`
and the **CNAME** named `www`, and leave everything else.

### 2.3 Add the four A records

Click **Add New Record** and enter each of these. Four separate records, all
with Name `@`:

| Type | Name | Value             | TTL      |
|------|------|-------------------|----------|
| A    | @    | `185.199.108.153` | 1 Hour   |
| A    | @    | `185.199.109.153` | 1 Hour   |
| A    | @    | `185.199.110.153` | 1 Hour   |
| A    | @    | `185.199.111.153` | 1 Hour   |

All four are needed — they are GitHub's four servers, and having all four
keeps the site up if one goes down.

### 2.4 Add the www record

One more record, so that `www.omegasolarproducts.com` also works and
redirects to the main address:

| Type  | Name | Value                          | TTL    |
|-------|------|--------------------------------|--------|
| CNAME | www  | `instackout.github.io`      | 1 Hour |

Replace `instackout` with your GitHub username, all lowercase.
**Include the trailing `.github.io`** and do not add `https://` or a slash.

Example: if your username is `ashvinpatel`, the value is
`ashvinpatel.github.io`

### 2.5 Optional but recommended — IPv6

Some Indian mobile networks are IPv6-only. Adding these four **AAAA** records
makes the site reachable on them. Same process, Name `@`:

| Type | Name | Value                  |
|------|------|------------------------|
| AAAA | @    | `2606:50c0:8000::153`  |
| AAAA | @    | `2606:50c0:8001::153`  |
| AAAA | @    | `2606:50c0:8002::153`  |
| AAAA | @    | `2606:50c0:8003::153`  |

Click **Save**.

---

## Part 3 — Turn on HTTPS

Wait 30 minutes, then:

1. Back in GitHub: **Settings → Pages**.
2. The custom domain box should now show a green tick instead of a warning.
3. Tick **Enforce HTTPS**.

If the tick box is greyed out, GitHub is still issuing the certificate. Come
back in a few hours. It can take up to 24 hours and needs no action from you.

Once it is on, `http://` visitors are redirected to `https://` automatically,
and the padlock appears in the browser.

---

## Checking it worked

Send me a message when the DNS is saved and I will run a check against the
live domain and tell you exactly what is and is not resolving yet — including
whether the leftover parking records have cleared.

Open these in order:

1. `https://omegasolarproducts.com` — the site, with a padlock
2. `https://www.omegasolarproducts.com` — should redirect to the address above
3. Send the link to yourself on WhatsApp — a preview card with your logo and
   product photos should appear

If step 3 shows no preview, WhatsApp has cached an earlier attempt. Add
`?1` to the end of the link (`https://omegasolarproducts.com/?1`) to force a
fresh fetch.

---

## If something is wrong

**"There isn't a GitHub Pages site here"**
Pages is not switched on, or the branch is wrong. Settings → Pages → Branch
must be `main` and folder `/ (root)`.

**Site loads but with no styling, or shows a file listing**
The `.nojekyll` file is missing. Add it: **Add file → Create new file**, name
it `.nojekyll`, leave it empty, commit.

**"Domain does not resolve to the GitHub Pages server"**
DNS has not spread yet, or a GoDaddy parking A record is still there. Go back
to 2.2 and check there is no leftover `@` A record other than the four
GitHub ones.

**Domain shows a GoDaddy parking page**
Same cause. GoDaddy sometimes also has a **Forwarding** setting that overrides
DNS — in the domain settings, look for **Forwarding** and remove any rule.

**The custom domain box in GitHub keeps emptying itself**
The `CNAME` file was deleted from the repository. Re-upload it — it must
contain exactly one line: `omegasolarproducts.com`

**Everything looks right but the browser still shows the old page**
Your browser or ISP cached it. Try the site on mobile data with the phone's
Wi-Fi off, or in a private window.

---

## After it is live — two free things worth doing

**Google Business Profile** — free, at `business.google.com`. For a supplier
in Kathwada GIDC this brings in more enquiries than the website does. Add the
address, both phone numbers, hours, and photographs of the store and stock.
Link it to omegasolarproducts.com.

**Google Search Console** — free, at `search.google.com/search-console`. Add
the domain, verify it with the TXT record they give you (added at GoDaddy the
same way as above), and submit `https://omegasolarproducts.com/sitemap.xml`.
Within a couple of weeks you will see exactly which part names people search
before landing on you — useful for deciding what to stock more of.

---

## Updating the site later

The whole site is one file, `index.html`.

With GitHub Desktop:

1. Replace `index.html` in `~/Documents/GitHub/omegasolarproducts` with the
   new version.
2. Open GitHub Desktop — it will show the change.
3. Type a short summary in the box at the bottom left, click
   **Commit to main**, then **Push origin**.
4. Live in about a minute.

Never delete `CNAME` or `.nojekyll` while doing it — the first keeps your
domain attached, the second keeps the site rendering.
