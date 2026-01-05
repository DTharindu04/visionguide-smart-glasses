from gtts import gTTS
import os
import time

# භාෂා 6 සඳහා සම්පූර්ණ පරිවර්තන සහ වාක්‍ය රටා
translations = {
    'si': { # Sinhala
        'living': "ඔබ ඉදිරියේ {label} සිටී",
        'non_living': "ඔබ ඉදිරියේ {label} තිබේ",
        'warning': "අවදානය යොමු කරන්න, ඉදිරියේ සිටින පුද්ගලයා {label} පසුවේ",
        'emotion': "ඉදිරියේ සිටින පුද්ගලයා {label} පසුවේ",
        'labels': {
            'person': 'පුද්ගලයෙක්', 'dog': 'බල්ලෙක්', 'cat': 'පූසෙක්', 'bird': 'කුරුල්ලෙක්', 'cow': 'හරකෙක්',
            'chair': 'පුටුවක්', 'table': 'මේසයක්', 'bottle': 'බෝතලයක්', 'car': 'වාහනයක්', 'bus': 'බස් රථයක්',
            'happy': 'සතුටින්', 'angry': 'කෝපයෙන්', 'fear': 'බියෙන්', 'smiling': 'සිනාසෙමින්',
            'laptop': 'ලැප්ටොප් එකක්', 'mobile': 'ජංගම දුරකථනයක්', 'cup': 'කෝප්පයක්' # අනෙක්වාද මෙලෙස එකතු කරන්න
        }
    },
    'en': { # English
        'living': "There is a {label} in front of you",
        'non_living': "There is a {label} ahead",
        'warning': "Warning, the person in front is {label}",
        'emotion': "The person in front is {label}",
        'labels': {
            'person': 'person', 'dog': 'dog', 'cat': 'cat', 'bird': 'bird', 'cow': 'cow',
            'chair': 'chair', 'table': 'table', 'bottle': 'bottle', 'car': 'car', 'bus': 'bus',
            'happy': 'happy', 'angry': 'angry', 'fear': 'scared', 'smiling': 'smiling',
            'laptop': 'laptop', 'mobile': 'mobile phone', 'cup': 'cup'
        }
    },
    'ta': { # Tamil
        'living': "உங்கள் முன்னே ஒரு {label} இருக்கிறார்",
        'non_living': "உங்கள் முன்னே ஒரு {label} உள்ளது",
        'warning': "எச்சரிக்கை, முன்னால் இருப்பவர் {label} ஆக இருக்கிறார்",
        'emotion': "முன்னால் இருப்பவர் {label} ஆக இருக்கிறார்",
        'labels': {
            'person': 'மனிதர்', 'dog': 'நாய்', 'cat': 'பூனை', 'bird': 'பறவை', 'cow': 'பசு',
            'chair': 'நாற்காலி', 'table': 'மேசை', 'bottle': 'பாட்டில்', 'car': 'கார்', 'bus': 'பேருந்து',
            'happy': 'மகிழ்ச்சியாக', 'angry': 'கோபமாக', 'fear': 'பயமாக', 'smiling': 'புன்னகைக்கிறார்'
        }
    },
    'hi': { # Hindi
        'living': "आपके सामने एक {label} है",
        'non_living': "वहां एक {label} है",
        'warning': "चेतावनी, सामने वाला व्यक्ति {label} है",
        'emotion': "सामने वाला व्यक्ति {label} है",
        'labels': {
            'person': 'व्यक्ति', 'dog': 'कुत्ता', 'cat': 'बिल्ली', 'bird': 'पक्षୀ', 'cow': 'गाय',
            'chair': 'कुर्सी', 'table': 'मेज', 'happy': 'खुश', 'angry': 'गुस्से में'
        }
    },
    'ja': { # Japanese
        'living': "目の前に {label} がいます",
        'non_living': "目の前に {label} があります",
        'warning': "警告、前の人は {label} です",
        'emotion': "前の人は {label} です",
        'labels': {
            'person': '人', 'dog': '犬', 'cat': '猫', 'bird': '鳥', 'cow': '牛',
            'chair': '椅子', 'table': 'テーブル', 'happy': '幸せ', 'angry': '怒って'
        }
    },
    'ko': { # Korean
        'living': "앞에 {label} 이(가) 있습니다",
        'non_living': "앞에 {label} 이(가) 있습니다",
        'warning': "경고, 앞에 있는 사람이 {label} 합니다",
        'emotion': "앞에 있는 사람이 {label} 합니다",
        'labels': {
            'person': '사람', 'dog': '개', 'cat': '고양이', 'bird': '새', 'cow': '소',
            'chair': '의자', 'table': '탁자', 'happy': '행복', 'angry': '화가 난'
        }
    }
}

living_list = ['person', 'dog', 'cat', 'bird', 'cow']
warning_list = ['angry', 'fear', 'disgust']
emotion_list = ['happy', 'sad', 'angry', 'surprised', 'neutral', 'fear', 'disgust', 'excited', 'bored', 'smiling']

print("--- Generating Audio Assets for 6 Languages ---")

for lang_code, content in translations.items():
    folder_path = f"assets/audio/{lang_code}"
    if not os.path.exists(folder_path): os.makedirs(folder_path)
    
    for label_key, translated_val in content['labels'].items():
        # වාක්‍යය තෝරාගැනීම
        if label_key in emotion_list:
            template = content['warning'] if label_key in warning_list else content['emotion']
        elif label_key in living_list:
            template = content['living']
        else:
            template = content['non_living']
        
        full_speech = template.format(label=translated_val)
        
        try:
            tts = gTTS(text=full_speech, lang=lang_code)
            tts.save(f"{folder_path}/{label_key}.mp3")
            print(f"Generated [{lang_code}]: {label_key}")
            time.sleep(0.1) # Connection errors වළක්වා ගැනීමට
        except Exception as e:
            print(f"Failed [{lang_code}] for {label_key}: {e}")

print("\n--- Process Complete! All 6 languages are localized. ---")