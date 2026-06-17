# Adding New Images to PokeLove2

## Folder Structure

```
assets/
  scenes/          → background scene images (SCENEOPTION1.png … SCENEOPTION21.png)
  backgrounds/     → card colour backgrounds (CARDBACKGROUNDOPTION1.png … 14.png)
  sidekicks/
    left/          → left character Pokemon/pets (Option_1.png … Option_38.png)
    right/         → right character Pokemon/pets
  apparel/
    left/          → e.g. WHITELEFTCharacterApparel23.png, BLACKLEFTCharacterApparel23.png
    right/         → e.g. WHITERIGHTCharacterApparel23.png
  hair/
    left/          → e.g. OPTION8BROWNLEFT.png
    right/         → e.g. OPTION8BROWNRIGHT.png
  faces/
    left/          → e.g. MALEWHITELEFTBLUE.png
    right/         → e.g. FEMALEWHITERIGHTBLUE.png
  accessories/
    left/          → e.g. LEFTCAP.png, TIARALEFT.png
    right/         → e.g. RIGHTCAP.png, TIARARIGHT.png
  facial_hair/
    left/          → e.g. OPTION1BROWNLEFT.png
    right/         → e.g. OPTION1BROWNRIGHT.png
  borders/         → yellow.png, navy_blue.png, red.png, white.png, orange.png, baby_blue.png
  thumbs/          → dropdown preview thumbnails (sceneoption1.png, appareloption1.png, etc.)
  misc/            → logo.png, fourth_layer.png, back_card.png, speech_buble.png, 1STLAYER*.png
  element_map.json → maps image keys to file paths (UPDATE THIS when adding new images)
```

## Adding a New Scene

1. Add image to `assets/scenes/SCENEOPTION22.png`
2. Add thumbnail to `assets/thumbs/sceneoption22.png` (same image is fine)
3. Open `assets/element_map.json`, add entry:
   ```json
   "SCENE/SCENEOPTION22.png": "assets/scenes/SCENEOPTION22.png"
   ```
4. In `index.html` find `baseScenes`, change `length: 20` to `length: 21`
5. In `index.html` find `LOADED_RESOURCES`, add:
   ```
   'SCENEOPTION22': 'assets/thumbs/sceneoption22.png',
   ```
6. Commit and push → site updates automatically

## Adding a New Sidekick (Pokemon/Pet)

1. Add left version: `assets/sidekicks/left/Option_39.png`
2. Add right version: `assets/sidekicks/right/Option_39.png`
3. Add thumbnail: `assets/thumbs/sidekickoption39.png`
4. In `assets/element_map.json` add:
   ```json
   "Left Characters Pokemon:Pet/Option 39.png": "assets/sidekicks/left/Option_39.png",
   "Right Characters Pokemon:Pet/Option 39.png": "assets/sidekicks/right/Option_39.png"
   ```
5. In `index.html` find `baseSidekicks`, change `length: 38` to `length: 39`
6. In `index.html` find `LOADED_RESOURCES`, add:
   ```
   'SIDEKICKOPTION39': 'assets/thumbs/sidekickoption39.png',
   ```
7. Commit and push

## Adding New Apparel

Naming convention: `{ETHNICITY}{SIDE}CharacterApparel{NUMBER}.png`
- e.g. `WHITELEFTCharacterApparel36.png`, `BLACKRIGHTCharacterApparel36.png`

1. Add all 4 variants (WHITE/BLACK × LEFT/RIGHT) to correct folders
2. Add thumbnail: `assets/thumbs/appareloption36.png`
3. Update `element_map.json` with 4 entries
4. In `index.html` `baseApparel` array, add `{ value: 'Option 36', label: 'Apparel Option 36', key: 'APPARELOPTION36' }`
5. In `LOADED_RESOURCES` add `'APPARELOPTION36': 'assets/thumbs/appareloption36.png'`
6. Commit and push

## Adding New Hair Style

Naming: `OPTION{N}{COLOR}{SIDE}.png` — must add all 10 colors × 2 sides = 20 files

Colors: BLACK, BLOND, BLUE, BROWN, GINGER, GREEN, GREY_WHITE, PINK, PURPLE, RED

1. Add 20 files to `assets/hair/left/` and `assets/hair/right/`
2. Add thumbnail: `assets/thumbs/hair-option21.png`
3. Update `element_map.json` with 20 entries
4. In `baseHairStyles` add `{ value: 'Option 21', label: 'Hair Option 21', key: 'HAIR-OPTION21' }`
5. In `LOADED_RESOURCES` add `'HAIR-OPTION21': 'assets/thumbs/hair-option21.png'`
6. Commit and push

## Quick Git Commands

```bash
git add assets/
git commit -m "Add new [scene/sidekick/apparel] options"
git push
```

GitHub Pages deploys automatically within ~60 seconds of each push.
