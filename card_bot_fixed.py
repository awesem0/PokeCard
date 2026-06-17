from PIL import Image, ImageDraw, ImageFont
from pilmoji import Pilmoji
from pilmoji.source import GoogleEmojiSource
import os
import numpy as np
import random
from googleapiclient.discovery import build
from google.oauth2 import service_account
import re

# Paths and credentials
base_path = "/Users/angelocacchione/Desktop/ELEMENTS/"
output_base = "/Users/angelocacchione/Desktop/"
font_path = os.path.join(base_path, "Arimo-mO92.ttf")
credentials_path = "/Users/angelocacchione/Desktop/ELEMENTS/valentinescardbot-credentials.json"
SPREADSHEET_ID = "1leI34BLexQyYO5LPMATii1v1WvLvN4Oc9GASHv3G81c"

# DPI conversion
DPI = 300
MM_TO_PX = DPI / 25.4

def mm_to_px(mm):
    return int(mm * MM_TO_PX)

def clean_alpha(image):
    img_array = np.array(image)
    r, g, b, a = img_array.T
    edge_pixels = (a > 0) & (a < 255)
    img_array[edge_pixels.T] = (0, 0, 0, 0)
    return Image.fromarray(img_array)

def has_emoji(text):
    emoji_pattern = re.compile("["
        u"\U0001F600-\U0001F64F"
        u"\U0001F300-\U0001F5FF"
        u"\U0001F680-\U0001F6FF"
        u"\U0001F1E0-\U0001F1FF"
        u"\U00002702-\U000027B0"
        u"\U000024C2-\U0001F251"
        u"\U0001F900-\U0001F9FF"
        u"\U0001FA00-\U0001FAFF"
        "]+", flags=re.UNICODE)
    return bool(emoji_pattern.search(text))

def draw_text_with_emoji(canvas, position, text, font, fill):
    try:
        with Pilmoji(canvas, source=GoogleEmojiSource) as pilmoji_draw:
            pilmoji_draw.text(position, text, font=font, fill=fill, emoji_position_offset=(0, -mm_to_px(0.4)))
    except Exception as e:
        print(f"Emoji rendering warning: {e}")
        draw = ImageDraw.Draw(canvas)
        draw.text(position, text, font=font, fill=fill)

def column_index_to_letter(index):
    if index < 26:
        return chr(65 + index)
    else:
        first = chr(65 + (index // 26 - 1))
        second = chr(65 + (index % 26))
        return first + second

def find_scene_file(scene_input):
    """Find scene file handling mixed .png / .jpg / .jpeg extensions, up to option 89."""
    scene_input = scene_input.strip()
    m = re.match(r'Option\s+(\d+)$', scene_input, re.IGNORECASE)
    if not m:
        print(f"Could not parse scene input '{scene_input}', defaulting to SCENEOPTION1.png")
        return "SCENEOPTION1.png"
    n = int(m.group(1))
    scene_dir = os.path.join(base_path, "SCENE")
    for ext in ['.png', '.jpg', '.jpeg']:
        fname = f"SCENEOPTION{n}{ext}"
        if os.path.exists(os.path.join(scene_dir, fname)):
            return fname
    print(f"Scene file not found for option {n}, defaulting to SCENEOPTION1.png")
    return "SCENEOPTION1.png"

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
creds = service_account.Credentials.from_service_account_file(credentials_path, scopes=SCOPES)
service = build('sheets', 'v4', credentials=creds)
sheet = service.spreadsheets()

def process_orders():
    result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range="Form Responses 1!A:AF").execute()
    values = result.get('values', [])
    if not values:
        print("No data found in the sheet.")
        return

    headers = values[0]
    rows = values[1:]
    processed_idx = headers.index("Processed") if "Processed" in headers else -1
    print(f"Headers: {headers}")
    print(f"Processed index: {processed_idx}")

    glasses_map = {
        "Blue Glasses": "BLUEGLASSES.png",
        "Pink Glasses": "PINKGLASSES.png",
        "Meme Glasses": "MEMEGLASSES.png",
        "Glasses": "GLASSES.png",
        "NO ACCESSORY": None,
        "None": None,
        "": None
    }

    accessory_map_left = {
        "Cap": "LEFTCAP.png",
        "PikaKap": "LEFTPIKAKAP.png",
        "Pika Kap": "LEFTPIKAKAP.png",
        "White Hat": "LEFTBEACHHAT.png",
        "Yellow Benie": "LEFTBEACHHAT.png",
        "Black and White Cap": "LEFTCAP.png",
        "RedCap": "LEFTREDCAP.png",
        "Red Cap": "LEFTREDCAP.png",
        "TruckerCap": "LEFTTRUCKERHAT.png",
        "Trucker Cap": "LEFTTRUCKERHAT.png",
        "Garland": "GARLANDLEFT.png",
        "Tiara": "TIARALEFT.png",
        "TopHat": "LEFTTOPHAT.png",
        "Top Hat": "LEFTTOPHAT.png",
        "BeachHat": "LEFTBEACHHAT.png",
        "Beach Hat": "LEFTBEACHHAT.png",
        "NO ACCESSORY": None,
        "None": None,
        "": None
    }

    accessory_map_right = {
        "Cap": "RIGHTCAP.png",
        "PikaKap": "RIGHTPIKAKAP.png",
        "Pika Kap": "RIGHTPIKAKAP.png",
        "White Hat": "RIGHTBEACHHAT.png",
        "Yellow Benie": "RIGHTBEACHHAT.png",
        "Black and White Cap": "RIGHTCAP.png",
        "RedCap": "RIGHTREDCAP.png",
        "Red Cap": "RIGHTREDCAP.png",
        "TruckerCap": "RIGHTTRUCKERHAT.png",
        "Trucker Cap": "RIGHTTRUCKERHAT.png",
        "Garland": "GARLANDRIGHT.png",
        "Tiara": "TIARARIGHT.png",
        "TopHat": "RIGHTTOPHAT.png",
        "Top Hat": "RIGHTTOPHAT.png",
        "BeachHat": "RIGHTBEACHHAT.png",
        "Beach Hat": "RIGHTBEACHHAT.png",
        "NO ACCESSORY": None,
        "None": None,
        "": None
    }

    hair_color_map = {
        "strawberry blond": "GINGER",
        "black": "BLACK",
        "brown": "BROWN",
        "blonde": "BLOND",
        "blond": "BLOND",
        "blue": "BLUE",
        "green": "GREEN",
        "red": "RED",
        "white": "WHITE",
        "grey": "WHITE",
        "pink": "PINK",
        "purple": "PURPLE"
    }

    facial_hair_map = {
        "Option 1": "Option 1",
        "Option 3": "Option 2",
        "Option 4": "Option 3",
        "Option 5": "Option 4"
    }

    def render_card(canvas, form_data, swap_sides=False):
        first_layer_map = {
            "Baby Blue": "1STLAYERBABYBLUE.png",
            "Blue": "1STLAYERBLUE.png",
            "Orange": "1STLAYERORANGE.png",
            "Red": "1STLAYERRED.png",
            "White": "1STLAYERWHITE.png",
            "Yellow": "1STLAYERYELLOW.png",
            "Navy Blue": "1STLAYERBLUE.png",
            "Oange": "1STLAYERORANGE.png"
        }
        first_layer_file = first_layer_map.get(form_data["Border/Card Color"], "1STLAYERBLUE.png")
        base_image = Image.open(os.path.join(base_path, first_layer_file)).convert("RGBA")
        base_width, base_height = base_image.size
        canvas.paste(base_image, (0, 0), base_image)

        layer2_map = {f"CARDBACKGROUNDOPTION{i}.png": f"Option {i}" for i in range(1, 15)}
        selected_layer2 = [f for f, opt in layer2_map.items() if opt == form_data["Card Background Color"]]
        layer2_file = selected_layer2[0] if selected_layer2 else "CARDBACKGROUNDOPTION1.png"
        layer2_img = Image.open(os.path.join(base_path, "CARDBACKGROUNDOPTIONS", layer2_file)).convert("RGBA")
        cleaned_layer2 = clean_alpha(layer2_img)
        canvas.paste(cleaned_layer2, (mm_to_px(3), mm_to_px(3)), cleaned_layer2)

        # Scene — dynamic extension lookup (supports options 1-89, .png/.jpg/.jpeg)
        scene_file = find_scene_file(form_data["Scene"])
        scene_img = Image.open(os.path.join(base_path, "SCENE", scene_file)).convert("RGBA")
        scene_width, _ = scene_img.size
        scene_width_mm = scene_width / MM_TO_PX
        center_x_mm = (base_width / MM_TO_PX / 2) - (scene_width_mm / 2)
        canvas.paste(scene_img, (mm_to_px(center_x_mm), mm_to_px(8.2)), scene_img)

        layer4_img = Image.open(os.path.join(base_path, "4THLAYER.png")).convert("RGBA")
        layer4_width, _ = layer4_img.size
        layer4_width_mm = layer4_width / MM_TO_PX
        center_x_mm = (base_width / MM_TO_PX / 2) - (layer4_width_mm / 2)
        canvas.paste(layer4_img, (mm_to_px(center_x_mm), mm_to_px(2.7)), layer4_img)

        if swap_sides:
            left_char = {
                "Character": form_data["Right Character"],
                "First Name": form_data["Right Character First Name"],
                "Eye Color": form_data["Right Character Eye Color"],
                "Hair Style": form_data["Right Character Hair Style"],
                "Hair Color": form_data["Right Character Hair Color"],
                "Eyewear": form_data["Right Character Eyewear"],
                "Apparel": form_data["Right Character Apparel"],
                "Ethnicity": form_data["Right Character Ethnicity"],
                "Pet": form_data["Right Pokemon/Pet"],
                "Facial Hair": form_data["Right Character Facial Hair"],
                "Accessory": form_data["Right Character Accessory"]
            }
            right_char = {
                "Character": form_data["Left Character"],
                "First Name": form_data["Left Character First Name"],
                "Eye Color": form_data["Left Character Eye Color"],
                "Hair Style": form_data["Left Character Hair Style"],
                "Hair Color": form_data["Left Character Hair Color"],
                "Eyewear": form_data["Left Character Eyewear"],
                "Apparel": form_data["Left Character Apparel"],
                "Ethnicity": form_data["Left Character Ethnicity"],
                "Pet": form_data["Left Pokemon/Pet"],
                "Facial Hair": form_data["Left Character Facial Hair"],
                "Accessory": form_data["Left Character Accessory"]
            }
        else:
            left_char = {
                "Character": form_data["Left Character"],
                "First Name": form_data["Left Character First Name"],
                "Eye Color": form_data["Left Character Eye Color"],
                "Hair Style": form_data["Left Character Hair Style"],
                "Hair Color": form_data["Left Character Hair Color"],
                "Eyewear": form_data["Left Character Eyewear"],
                "Apparel": form_data["Left Character Apparel"],
                "Ethnicity": form_data["Left Character Ethnicity"],
                "Pet": form_data["Left Pokemon/Pet"],
                "Facial Hair": form_data["Left Character Facial Hair"],
                "Accessory": form_data["Left Character Accessory"]
            }
            right_char = {
                "Character": form_data["Right Character"],
                "First Name": form_data["Right Character First Name"],
                "Eye Color": form_data["Right Character Eye Color"],
                "Hair Style": form_data["Right Character Hair Style"],
                "Hair Color": form_data["Right Character Hair Color"],
                "Eyewear": form_data["Right Character Eyewear"],
                "Apparel": form_data["Right Character Apparel"],
                "Ethnicity": form_data["Right Character Ethnicity"],
                "Pet": form_data["Right Pokemon/Pet"],
                "Facial Hair": form_data["Right Character Facial Hair"],
                "Accessory": form_data["Right Character Accessory"]
            }

        left_hair_color_normalized = hair_color_map.get(left_char["Hair Color"].lower(), left_char["Hair Color"].upper())
        right_hair_color_normalized = hair_color_map.get(right_char["Hair Color"].lower(), right_char["Hair Color"].upper())

        left_head_pos_y = mm_to_px(21)
        left_head_pos = (mm_to_px(5.6), left_head_pos_y)
        apparel_left = ''.join(filter(str.isdigit, left_char['Apparel'].strip()))
        left_body_pos_y = 245
        left_body_pos = (mm_to_px(5.6), left_body_pos_y)
        face1 = f"LEFTFACES/{left_char['Character'].upper()}{left_char['Ethnicity'].upper()}LEFT{left_char['Eye Color'].upper()}.png"
        wig1 = (f"LEFTCHARACTERWIGS/{left_char['Hair Style'].replace(' ', '').upper()}{left_hair_color_normalized}LEFT.png"
                if left_char['Hair Style'].lower() != "no hair" else None)
        body1 = f"LEFTCharacterApparel/{left_char['Ethnicity'].upper()}LEFTCharacterApparel{apparel_left}.png"

        try:
            face1_img = Image.open(os.path.join(base_path, face1)).convert("RGBA")
            canvas.paste(face1_img, left_head_pos, face1_img)
        except FileNotFoundError:
            print(f"Face missing for left character: {os.path.join(base_path, face1)}")

        if wig1:
            try:
                wig1_img = Image.open(os.path.join(base_path, wig1)).convert("RGBA")
                if "OPTION20" in wig1.upper():
                    wig1_pos = (left_head_pos[0], left_head_pos[1] + mm_to_px(0.35))
                elif "OPTION1" in wig1.upper() or "OPTION2" in wig1.upper():
                    wig1_pos = (left_head_pos[0], left_head_pos[1] + mm_to_px(0.5))
                else:
                    wig1_pos = (left_head_pos[0], left_head_pos[1])
                canvas.paste(wig1_img, wig1_pos, wig1_img)
            except FileNotFoundError:
                print(f"Wig missing for left character: {os.path.join(base_path, wig1)}")

        try:
            body1_img = Image.open(os.path.join(base_path, body1)).convert("RGBA")
            canvas.paste(body1_img, left_body_pos, body1_img)
        except FileNotFoundError:
            print(f"Body missing for left character: {os.path.join(base_path, body1)}")

        left_facial_hair = left_char["Facial Hair"]
        if left_facial_hair and left_facial_hair.lower() not in ("none", ""):
            mapped_facial_hair = facial_hair_map.get(left_facial_hair, left_facial_hair)
            style_tag = mapped_facial_hair.replace(" ", "").upper()
            fname = f"{style_tag}{left_hair_color_normalized}LEFT.png"
            path = os.path.join(base_path, "LEFTFACIALHAIR", fname)
            try:
                facial_hair_img = Image.open(path).convert("RGBA")
                canvas.paste(facial_hair_img, left_head_pos, facial_hair_img)
            except FileNotFoundError:
                print(f"Facial hair missing for left character: {path}")

        left_eyewear = left_char["Eyewear"].strip()
        if left_eyewear and left_eyewear.lower() in [k.lower() for k in glasses_map if glasses_map[k]]:
            eyewear_key = next(k for k in glasses_map if k.lower() == left_eyewear.lower())
            glasses_file = glasses_map[eyewear_key]
            glasses_path = os.path.join(base_path, "ACCESSORIESLEFT", f"LEFT{glasses_file}")
            try:
                glasses_img = Image.open(glasses_path).convert("RGBA")
                canvas.paste(glasses_img, (left_head_pos[0], left_head_pos[1] + mm_to_px(0.0)), glasses_img)
            except FileNotFoundError:
                print(f"Eyewear missing for left character: {glasses_path}")

        left_accessory = left_char["Accessory"].strip()
        if left_accessory and left_accessory.lower() in [k.lower() for k in accessory_map_left if accessory_map_left[k]]:
            accessory_key = next(k for k in accessory_map_left if k.lower() == left_accessory.lower())
            accessory_file = accessory_map_left[accessory_key]
            accessory_path = os.path.join(base_path, "ACCESSORIESLEFT", accessory_file)
            try:
                accessory_img = Image.open(accessory_path).convert("RGBA")
                canvas.paste(accessory_img, (left_head_pos[0], left_head_pos[1] - mm_to_px(0.5)), accessory_img)
            except FileNotFoundError:
                print(f"Accessory missing for left character: {accessory_path}")

        right_head_pos_y = mm_to_px(21)
        right_head_pos = (mm_to_px(23), right_head_pos_y)
        apparel_right = ''.join(filter(str.isdigit, right_char['Apparel'].strip()))
        right_body_pos_y = 245
        right_body_pos = (mm_to_px(23), right_body_pos_y)
        face2 = f"RIGHTFACES/{right_char['Character'].upper()}{right_char['Ethnicity'].upper()}RIGHT{right_char['Eye Color'].upper()}.png"
        wig2 = (f"RIGHTCHARACTERWIGS/{right_char['Hair Style'].replace(' ', '').upper()}{right_hair_color_normalized}RIGHT.png"
                if right_char['Hair Style'].lower() != "no hair" else None)
        body2 = f"RIGHTCharacterApparel/{right_char['Ethnicity'].upper()}RIGHTCharacterApparel{apparel_right}.png"

        try:
            face2_img = Image.open(os.path.join(base_path, face2)).convert("RGBA")
            canvas.paste(face2_img, right_head_pos, face2_img)
        except FileNotFoundError:
            print(f"Face missing for right character: {os.path.join(base_path, face2)}")

        if wig2:
            try:
                wig2_img = Image.open(os.path.join(base_path, wig2)).convert("RGBA")
                if "OPTION20" in wig2.upper():
                    wig2_pos = (right_head_pos[0], right_head_pos[1] + mm_to_px(0.35))
                elif "OPTION1" in wig2.upper() or "OPTION2" in wig2.upper():
                    wig2_pos = (right_head_pos[0], right_head_pos[1] + mm_to_px(0.5))
                else:
                    wig2_pos = (right_head_pos[0], right_head_pos[1])
                canvas.paste(wig2_img, wig2_pos, wig2_img)
            except FileNotFoundError:
                print(f"Wig missing for right character: {os.path.join(base_path, wig2)}")

        try:
            body2_img = Image.open(os.path.join(base_path, body2)).convert("RGBA")
            canvas.paste(body2_img, right_body_pos, body2_img)
        except FileNotFoundError:
            print(f"Body missing for right character: {os.path.join(base_path, body2)}")

        right_facial_hair = right_char["Facial Hair"]
        if right_facial_hair and right_facial_hair.lower() not in ("none", ""):
            mapped_facial_hair = facial_hair_map.get(right_facial_hair, right_facial_hair)
            style_tag = mapped_facial_hair.replace(" ", "").upper()
            fname = f"{style_tag}{right_hair_color_normalized}RIGHT.png"
            path = os.path.join(base_path, "RIGHTFACIALHAIR", fname)
            try:
                facial_hair_img = Image.open(path).convert("RGBA")
                canvas.paste(facial_hair_img, right_head_pos, facial_hair_img)
            except FileNotFoundError:
                print(f"Facial hair missing for right character: {path}")

        right_eyewear = right_char["Eyewear"].strip()
        if right_eyewear and right_eyewear.lower() in [k.lower() for k in glasses_map if glasses_map[k]]:
            eyewear_key = next(k for k in glasses_map if k.lower() == right_eyewear.lower())
            glasses_file = glasses_map[eyewear_key]
            glasses_path = os.path.join(base_path, "ACCESSORIESRIGHT", f"RIGHT{glasses_file}")
            try:
                glasses_img = Image.open(glasses_path).convert("RGBA")
                canvas.paste(glasses_img, (right_head_pos[0], right_head_pos[1] + mm_to_px(0.0)), glasses_img)
            except FileNotFoundError:
                print(f"Eyewear missing for right character: {glasses_path}")

        right_accessory = right_char["Accessory"].strip()
        if right_accessory and right_accessory.lower() in [k.lower() for k in accessory_map_right if accessory_map_right[k]]:
            accessory_key = next(k for k in accessory_map_right if k.lower() == right_accessory.lower())
            accessory_file = accessory_map_right[accessory_key]
            accessory_path = os.path.join(base_path, "ACCESSORIESRIGHT", accessory_file)
            try:
                accessory_img = Image.open(accessory_path).convert("RGBA")
                canvas.paste(accessory_img, (right_head_pos[0], right_head_pos[1] - mm_to_px(0.5)), accessory_img)
            except FileNotFoundError:
                print(f"Accessory missing for right character: {accessory_path}")

        left_pet_pos = (mm_to_px(6), mm_to_px(43))
        left_pet_choice = left_char["Pet"].strip()
        if left_pet_choice and left_pet_choice.lower() != "no sidekick":
            left_pet_path = os.path.join(base_path, "Left Characters Pokemon:Pet", f"{left_pet_choice}.png")
            try:
                left_pet_img = Image.open(left_pet_path).convert("RGBA")
                canvas.paste(left_pet_img, left_pet_pos, left_pet_img)
            except FileNotFoundError:
                print(f"Left pet missing: {left_pet_path}")

        right_pet_pos = (mm_to_px(37), mm_to_px(43))
        right_pet_choice = right_char["Pet"].strip()
        if right_pet_choice and right_pet_choice.lower() != "no sidekick":
            right_pet_path = os.path.join(base_path, "Right Characters Pokemon:Pet", f"{right_pet_choice}.png")
            try:
                right_pet_img = Image.open(right_pet_path).convert("RGBA")
                canvas.paste(right_pet_img, right_pet_pos, right_pet_img)
            except FileNotFoundError:
                print(f"Right pet missing: {right_pet_path}")

        speech_bubble_path = os.path.join(base_path, "speech buble.png")
        try:
            speech_bubble_img = Image.open(speech_bubble_path).convert("RGBA")
            speech_width, _ = speech_bubble_img.size
            speech_x_mm = (54 / 2) - (speech_width / MM_TO_PX / 2)
            canvas.paste(speech_bubble_img, (mm_to_px(speech_x_mm), mm_to_px(86 / 3)), speech_bubble_img)
        except FileNotFoundError:
            print(f"Speech bubble missing: {speech_bubble_path}")

        draw = ImageDraw.Draw(canvas)
        try:
            font = ImageFont.truetype(font_path, 24)
        except IOError:
            print(f"Font missing: {font_path}")
            font = ImageFont.load_default()

        gold_color = (180, 120, 0, 255)
        dark_gold_color = (160, 100, 0, 255)
        black_color = (0, 0, 0, 255)

        event_poems = {
            "Anniversary": ["On this day, our hearts align,", "Years of love, like vintage wine,", "Together strong, through storm and shine,", "Forever yours, forever mine."],
            "Birthday": ["A day to cheer, a year to grow,", "With love and joy in every glow,", "Candles flicker, wishes flow,", "Happy birthday, my heart's tableau."],
            "Engagement": ["A promise made, a future near,", "With every step, I hold you dear,", "Bound by love, so crystal clear,", "Our journey starts, right here."],
            "I LOVE YOU": ["Three words simple, yet so true,", "Every beat belongs to you,", "In your eyes, my world's in view,", "I love you, through and through."],
            "Just Because": ["No reason needed, just to say,", "You brighten up my every day,", "With you, my heart will always stay,", "Love's pure gift, in every way."],
            "Valentines Day": ["Through misty trails where wild winds play,", "Our love grows strong in the softest way,", "Like petals dancing in a sunlit fray,", "We chase our dreams in this vast array."],
            "Wedding": ["Two souls unite, a vow so grand,", "Hand in hand, across life's land,", "With rings we pledge, by love we stand,", "A timeless bond, forever planned."],
            "Get Well Soon": ["Rest and heal, take time to mend,", "My love and care will never end,", "Soon you'll rise, strong once again,", "Get well, my dearest friend."],
            "New Home": ["New walls, new dreams, a place to start,", "Together we'll make this house a heart,", "With every room, a brand new part,", "Of our love's journey, a work of art."],
            "Proposal": ["A question asked, a life to share,", "Will you take this ring I bear?", "Say yes, and let our love declare,", "A future bright, beyond compare."],
            "First Date": ["Our first night, a spark so bright,", "Laughter shared beneath the light,", "A moment sweet, a love begun,", "Together now, two hearts as one."],
            "Holiday Gift": ["A gift for you this festive day,", "Wrapped with love in every way,", "Joy and cheer to light your stay,", "Happy holidays, come what may."],
            "Father's Day": ["Your love and strength guide us each day,", "Wisdom shared in your warm, steady way,", "Through every storm, you light our way,", "Dad, you're our hero, forever and always."],
            "Mother's Day": ["Your love blooms, a guiding light,", "Gentle hands mend every plight,", "Heart so warm, our safe delight,", "Mom, you're our star, shining bright."],
            "Congratulations": ["Your success sparks joy so grand,", "Hard work won, you take a stand,", "Bright future lies in your hand,", "Cheers to triumphs, bold and planned."],
            "Sweet Oath": ["Your smile ignites my heart's flame", "Every day, I'll call your name", "Bound by joy, we'll never part", "Love's adventure, a work of art"],
            "My Vow": ["Together we'll soar, hearts entwined", "Through every storm, love's light shines", "With you, my world is complete", "Forever yours, in victory sweet"]
        }

        poem_choice = form_data["Poem Choice"].strip()
        custom_poem = form_data["Custom Poem"]
        poem_key = poem_choice.split('.', 1)[-1].strip() if '.' in poem_choice else poem_choice

        if poem_choice == "Add your own Poem / Select and personalise in the next section" and custom_poem:
            all_lines = custom_poem.split('\n')
            text_tag = all_lines[0].strip()
            poem_lines = [line.strip() for line in all_lines[1:] if line.strip()][:4]
        else:
            text_tag = poem_key
            poem_lines = event_poems.get(poem_key, event_poems["First Date"])

        draw_text_with_emoji(canvas, (mm_to_px(8.8), mm_to_px(56.45)), text_tag, font, black_color)

        hp_text = form_data["HP Value"].strip()
        if not hp_text:
            hp_text = str(random.randint(10, 999))
        draw_text_with_emoji(canvas, (mm_to_px(38.6), mm_to_px(56.55)), f"{hp_text} HP", font, black_color)

        if poem_lines:
            poem_center_x_mm = (5.7 + 48.3) / 2
            poem_y_start_original = mm_to_px(68.5)
            line_spacing = mm_to_px(3)
            total_height = line_spacing * 3
            num_lines = len(poem_lines)

            if num_lines < 4:
                used_height = line_spacing * (num_lines - 1)
                offset = (total_height - used_height) // 2
                poem_y_start = poem_y_start_original + offset
            else:
                poem_y_start = poem_y_start_original

            for i, line in enumerate(poem_lines[:4]):
                text_bbox = draw.textbbox((0, 0), line, font=font)
                line_width = text_bbox[2] - text_bbox[0]
                draw_text_with_emoji(canvas, (mm_to_px(poem_center_x_mm) - (line_width // 2), poem_y_start + (i * line_spacing)), line, font, black_color)

        name_positions = [
            (left_char["First Name"], 4.8, 18, 4.4, gold_color),
            (right_char["First Name"], 36.3, 49.3, 4.4, dark_gold_color),
            (left_char["First Name"], 7.4, 20.4, 61.45, black_color),
            (right_char["First Name"], 32.2, 46.3, 61.45, black_color)
        ]

        for name, x_start, x_end, y_mm, color in name_positions:
            text_bbox = draw.textbbox((0, 0), name, font=font)
            text_width = text_bbox[2] - text_bbox[0]
            x = mm_to_px((x_start + x_end) / 2) - (text_width // 2)
            draw_text_with_emoji(canvas, (x, mm_to_px(y_mm)), name, font, color)

        return canvas

    for row_idx, row in enumerate(rows, start=2):
        row = row + [''] * (len(headers) - len(row))
        print(f"Row {row_idx}: Processed value = '{row[processed_idx] if processed_idx != -1 else 'N/A'}'")
        if processed_idx != -1 and row[processed_idx] == "Yes":
            print(f"Skipping row {row_idx}: Already processed")
            continue

        form_data = {
            "Timestamp": row[headers.index("Timestamp")],
            "Order Number": row[headers.index("Enter Your Order Number or Character Names : )")],
            "Left Character": row[headers.index("Left Character ")],
            "Left Character First Name": row[headers.index("Left Characters First Name ")].title(),
            "Left Character Eye Color": row[headers.index("Left Character's eye Colour")],
            "Left Character Hair Style": row[headers.index("Hair Style for Left Character")],
            "Left Character Hair Color": row[headers.index("Hair Color for Left Character")],
            "Left Character Eyewear": row[headers.index("Eyewear for left Character")].strip(),
            "Left Character Apparel": row[headers.index("Left Character's Apparel ")],
            "Left Character Ethnicity": row[headers.index("Etnicity of the Left Character ")],
            "Left Pokemon/Pet": row[headers.index("Left Characters Pokemon/Pet")],
            "Right Character": row[headers.index("Right Character ")],
            "Right Character First Name": row[headers.index("Right Characters First Name")].title(),
            "Right Character Eye Color": row[headers.index("Right Character's eye Colour")],
            "Right Character Hair Style": row[headers.index("Hair Style for Right Character")],
            "Right Character Hair Color": row[headers.index("Hair Color for Right Character")],
            "Right Character Eyewear": row[headers.index("Eyewear for Right Character")].strip(),
            "Right Character Apparel": row[headers.index("Right Characters Apparel")],
            "Right Character Ethnicity": row[headers.index("Right Characters Etnicity")],
            "Right Pokemon/Pet": row[headers.index("Right Characters Pokemon/Pet")],
            "Border/Card Color": row[headers.index("Border/Card Color")],
            "Card Background Color": row[headers.index("Card Background Color")],
            "Scene": row[headers.index("Scene")],
            "Poem Choice": row[headers.index("Choose Occasion/Poem")],
            "Custom Poem": row[headers.index("Add your own Personalised Message as follows;\n\nA Title\n4 short lines or less for your Poem")],
            "Rear Card Option": row[headers.index("Rear/Back of Mini PokeMon Valentine Card")],
            "Right Character Facial Hair": row[headers.index("Right Character Facial Hair")].strip(),
            "Left Character Facial Hair": row[headers.index("Left Character Facial Hair")].strip(),
            "Left Character Accessory": row[headers.index("Accessories for left Character")].strip(),
            "Right Character Accessory": row[headers.index("Accessories for Right Character")].strip(),
            "HP Value": row[headers.index("HP Value")]
        }

        output_folder = os.path.join(output_base, form_data["Order Number"])
        os.makedirs(output_folder, exist_ok=True)

        canvas = Image.new("RGBA", (mm_to_px(54), mm_to_px(86)), (0, 0, 0, 0))
        canvas = render_card(canvas, form_data, swap_sides=False)
        canvas.save(os.path.join(output_folder, "front_card.png"), "PNG")

        canvas_swapped = Image.new("RGBA", (mm_to_px(54), mm_to_px(86)), (0, 0, 0, 0))
        canvas_swapped = render_card(canvas_swapped, form_data, swap_sides=True)
        canvas_swapped.save(os.path.join(output_folder, "front_card_swapped.png"), "PNG")

        rear_card_map = {
            "Option 1": "POKEMON REAR1.png",
            "Option 2": "POKEMON REAR2.png",
            "Option 3": "POKEMON REAR3.png",
            "Option 4": "POKEMON REAR4.png",
            "Option 5": "POKEMON REAR5.png",
            "Option 6": "POKEMON REAR6.png",
            "Option 7": "POKEMON REAR7.png",
            "Option 8": "POKEMON REAR8.png",
            "Option 9": "POKEMON REAR9.png",
            "Option 10": "POKEMON REAR10.png",
            "Option 11": "POKEMON REAR11.png",
            "Option 12": "POKEMON REAR12.png",
            "Option 13": "POKEMON REAR13.png",
            "Option 14": "POKEMON REAR14.png"
        }
        rear_card_option = form_data["Rear Card Option"].strip()
        rear_card_file = rear_card_map.get(rear_card_option, "POKEMON REAR7.png")
        rear_card_path = os.path.join(base_path, "REAR CARDS", rear_card_file)
        try:
            rear_card = Image.open(rear_card_path).convert("RGBA")
            if rear_card.size != canvas.size:
                rear_card = rear_card.resize(canvas.size, Image.LANCZOS)
            rear_card.save(os.path.join(output_folder, "rear_card.png"), "PNG")
        except FileNotFoundError:
            print(f"Rear card missing: {rear_card_path}")

        if processed_idx != -1 and not row[processed_idx]:
            try:
                sheet.values().update(
                    spreadsheetId=SPREADSHEET_ID,
                    range=f"Form Responses 1!{column_index_to_letter(processed_idx)}{row_idx}",
                    valueInputOption="RAW",
                    body={"values": [["Yes"]]}
                ).execute()
            except Exception as e:
                print(f"Error updating processed status for row {row_idx}: {e}")

process_orders()
