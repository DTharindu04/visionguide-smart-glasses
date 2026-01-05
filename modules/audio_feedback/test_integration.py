# from audio_logic import SmartGlassAudio
# import time

# glass = SmartGlassAudio()

# print("--- SMART GLASS LANGUAGE SELECTION ---")
# print("1. Sinhala (si)")
# print("2. English (en)")
# print("3. Tamil (ta)")
# print("4. Hindi (hi)")
# print("5. Japanese (ja)")
# print("6. Korean (ko)")

# # පරිශීලකයාගෙන් භාෂාව ඇසීම
# choice = input("\nඔබට අවශ්‍ය භාෂාවේ අංකය ඇතුළත් කරන්න (1-6): ")

# # අංකයට අදාළ භාෂා කේතය තෝරාගැනීම
# lang_map = {'1': 'si', '2': 'en', '3': 'ta', '4': 'hi', '5': 'ja', '6': 'ko'}
# selected_lang = lang_map.get(choice, 'en') # වැරදි අංකයක් දුන්නොත් English තෝරාගනී

# glass.set_language(selected_lang)
# print(f"\n[තෝරාගත් භාෂාව]: {selected_lang.upper()}")

# # පරීක්ෂණයක් ලෙස වස්තූන් කිහිපයක් Play කිරීම
# test_labels = ['person', 'car', 'angry', 'chair']

# for label in test_labels:
#     print(f"ප්‍රතිචාරය ලබා දෙමින්: {label}")
#     glass.play_feedback(label)
#     time.sleep(2)

#--------------------

from audio_logic import SmartGlassAudio
import time

glass = SmartGlassAudio()

# ප්‍රමුඛතාවය අනුව ලේබල් වර්ගීකරණය
PRIORITY_MAP = {
    'car': 1, 'bus': 1, 'angry': 1, 'fear': 1,  # Emergency/Safety
    'person': 2, 'dog': 2, 'cow': 2,           # Living beings
    'chair': 3, 'table': 3, 'bottle': 3        # General objects
}

def process_detections(labels, lang_code):
    glass.set_language(lang_code)
    
    # ලේබල් වලට ප්‍රමුඛතාවය ලබා දී ලැයිස්තුවක් සැකසීම
    detected_items = []
    for label in labels:
        priority = PRIORITY_MAP.get(label, 3)
        detected_items.append({'label': label, 'priority': priority})
    
    # ප්‍රමුඛතාවය අනුව අඩු අගයේ සිට වැඩි අගයට (1 සිට 3 ට) පෙළගැස්වීම
    sorted_items = sorted(detected_items, key=lambda x: x['priority'])
    
    print(f"\n--- Processing {len(sorted_items)} items in [{lang_code.upper()}] ---")
    
    for item in sorted_items:
        print(f"Playing: {item['label']} (Priority: {item['priority']})")
        glass.play_feedback(item['label'])
        time.sleep(2)

# --- MAIN INTERFACE ---

print("=== SMART GLASS MULTILINGUAL PRIORITY SYSTEM ===")
print("Select Language: 1.si | 2.en | 3.ta | 4.hi | 5.ja | 6.ko")
choice = input("Enter choice (1-6): ")

lang_map = {'1': 'si', '2': 'en', '3': 'ta', '4': 'hi', '5': 'ja', '6': 'ko'}
selected_lang = lang_map.get(choice, 'en')

# Dummy Test Case: වස්තූන් කිහිපයක් එකවර හඳුනාගැනීම
# මෙහිදී 'bottle' මුලින් තිබුණත්, 'car' සහ 'person' ප්‍රමුඛතාවය මත මුලින් ඇසෙනු ඇත.
current_detections = ['bottle', 'car', 'person']

process_detections(current_detections, selected_lang)