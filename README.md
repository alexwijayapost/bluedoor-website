# The Blue Door website

The website of The Blue Door Consulting Agency, served at https://bluedoor.id.

## Folders

- `source/` is the single source of truth: one page (`index.html`), the bench portraits, the background music and the icon.
- `preview/` is the built site for the private preview link. It is hidden from search engines and is where every change is checked first.
- `live/` is the built public site. It only changes after the owner approves a preview.
- `tools/` holds three.js 0.160, which draws the 3D door, so the site does not depend on an outside server.

## Making a change

1. Edit `source/index.html`.
2. Run `python3 build-site.py` to rebuild `preview/`.
3. Commit and push, then in cPanel open Git Version Control, press "Update from Remote" and "Deploy HEAD Commit". Check the preview link.
4. After approval, run `python3 build-site.py --live` to rebuild `live/`, commit, push, and deploy the same way.

`.cpanel.yml` tells the hosting where the two built folders go.
