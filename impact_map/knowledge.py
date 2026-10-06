"""Plain-language descriptions of brain regions, in English ("en") and Hindi ("hi").

General educational information only. What a tumor actually causes depends on
its exact location, size, type and the person; only a doctor can say that.
"""

REGIONS = {
    "frontal": {
        "name": {"en": "Frontal lobe", "hi": "फ्रंटल लोब (मस्तिष्क का अगला भाग)"},
        "functions": {
            "en": ["planning, decision-making and attention", "personality and behaviour",
                   "voluntary movement (motor cortex, at the back of this lobe)"],
            "hi": ["योजना बनाना, निर्णय लेना और ध्यान", "व्यक्तित्व और व्यवहार",
                   "इच्छा से की जाने वाली हरकतें (इस लोब का पिछला भाग)"],
        },
        "symptoms": {
            "en": ["changes in personality, mood or behaviour", "difficulty concentrating or planning",
                   "weakness on the opposite side of the body"],
            "hi": ["व्यक्तित्व, मूड या व्यवहार में बदलाव", "ध्यान लगाने या योजना बनाने में कठिनाई",
                   "शरीर के विपरीत तरफ कमज़ोरी"],
        },
    },
    "parietal": {
        "name": {"en": "Parietal lobe", "hi": "पैराइटल लोब (मस्तिष्क का ऊपरी-पिछला भाग)"},
        "functions": {
            "en": ["sense of touch, pain and temperature", "awareness of body position and space",
                   "reading, writing and calculation (often the left side)"],
            "hi": ["स्पर्श, दर्द और तापमान का एहसास", "शरीर की स्थिति और आसपास की जगह की समझ",
                   "पढ़ना, लिखना और गणना (अक्सर बायाँ भाग)"],
        },
        "symptoms": {
            "en": ["numbness or tingling on the opposite side of the body", "trouble judging distance or direction",
                   "ignoring one side of space (more common with right-side tumors)"],
            "hi": ["शरीर के विपरीत तरफ सुन्नपन या झनझनाहट", "दूरी या दिशा समझने में परेशानी",
                   "एक तरफ की चीज़ों पर ध्यान न जाना (दाईं तरफ के ट्यूमर में अधिक)"],
        },
    },
    "temporal": {
        "name": {"en": "Temporal lobe", "hi": "टेम्पोरल लोब (कनपटी के पास का भाग)"},
        "functions": {
            "en": ["hearing", "memory", "understanding speech (usually the left side)"],
            "hi": ["सुनना", "याददाश्त", "बोली गई बात को समझना (आमतौर पर बायाँ भाग)"],
        },
        "symptoms": {
            "en": ["seizures, sometimes with strange smells, déjà vu or staring spells",
                   "memory problems", "difficulty understanding words"],
            "hi": ["दौरे, कभी-कभी अजीब गंध, पहले देखा-सा लगना या एकटक घूरना",
                   "याददाश्त की समस्या", "शब्द समझने में कठिनाई"],
        },
    },
    "occipital": {
        "name": {"en": "Occipital lobe", "hi": "ऑक्सिपिटल लोब (सिर का पिछला भाग)"},
        "functions": {"en": ["vision: processing what the eyes see"],
                      "hi": ["देखना: आँखों से दिखी चीज़ों को समझना"]},
        "symptoms": {
            "en": ["loss of part of the field of vision", "visual disturbances such as flashing lights"],
            "hi": ["दृष्टि के एक हिस्से का चले जाना", "आँखों के सामने चमक जैसी दृष्टि संबंधी गड़बड़ी"],
        },
    },
    "frontoparietal": {
        "name": {"en": "Upper cortex (frontal / parietal area)", "hi": "ऊपरी कॉर्टेक्स (फ्रंटल / पैराइटल क्षेत्र)"},
        "functions": {
            "en": ["movement and sensation of the opposite side of the body", "planning and attention"],
            "hi": ["शरीर के विपरीत तरफ की हरकत और संवेदना", "योजना और ध्यान"],
        },
        "symptoms": {
            "en": ["weakness or numbness on the opposite side of the body", "seizures"],
            "hi": ["शरीर के विपरीत तरफ कमज़ोरी या सुन्नपन", "दौरे"],
        },
    },
    "deep": {
        "name": {"en": "Deep brain structures (basal ganglia, thalamus, ventricles)",
                 "hi": "मस्तिष्क की गहरी संरचनाएँ (बेसल गैंग्लिया, थैलेमस, वेंट्रिकल)"},
        "functions": {
            "en": ["relaying sensation and movement signals", "smooth control of movement",
                   "the ventricles hold the fluid that cushions the brain"],
            "hi": ["संवेदना और हरकत के संकेतों को आगे पहुँचाना", "हरकतों का सहज नियंत्रण",
                   "वेंट्रिकल में वह द्रव रहता है जो मस्तिष्क की रक्षा करता है"],
        },
        "symptoms": {
            "en": ["headache, nausea or vomiting if fluid flow is blocked", "weakness or numbness on one side",
                   "unusual movements"],
            "hi": ["द्रव का बहाव रुकने पर सिरदर्द, जी मिचलाना या उल्टी", "एक तरफ कमज़ोरी या सुन्नपन",
                   "असामान्य हरकतें"],
        },
    },
    "sellar": {
        "name": {"en": "Pituitary / sellar region", "hi": "पिट्यूटरी (सेलर) क्षेत्र"},
        "functions": {
            "en": ["the pituitary gland controls many hormones (growth, thyroid, stress, reproduction)",
                   "the nerves for vision cross just above it"],
            "hi": ["पिट्यूटरी ग्रंथि कई हार्मोन नियंत्रित करती है (विकास, थायरॉइड, तनाव, प्रजनन)",
                   "आँखों की नसें इसके ठीक ऊपर से गुज़रती हैं"],
        },
        "symptoms": {
            "en": ["hormone changes (weight, periods, milk production, tiredness)",
                   "loss of side (peripheral) vision", "headache"],
            "hi": ["हार्मोन में बदलाव (वज़न, मासिक धर्म, दूध बनना, थकान)",
                   "किनारे की (पेरिफेरल) दृष्टि कम होना", "सिरदर्द"],
        },
    },
    "cerebellum_brainstem": {
        "name": {"en": "Cerebellum / brainstem", "hi": "सेरिबैलम / ब्रेनस्टेम (मस्तिष्क का निचला-पिछला भाग)"},
        "functions": {
            "en": ["balance and coordination", "breathing, heart rate, swallowing (brainstem)"],
            "hi": ["संतुलन और तालमेल", "साँस, दिल की धड़कन, निगलना (ब्रेनस्टेम)"],
        },
        "symptoms": {
            "en": ["unsteady walking or clumsiness", "dizziness, double vision", "difficulty swallowing or speaking"],
            "hi": ["चलने में लड़खड़ाहट या भद्दापन", "चक्कर आना, दोहरा दिखना", "निगलने या बोलने में कठिनाई"],
        },
    },
}

SIDE_NOTES = {
    "left": {
        "en": "Left side: for most people this side controls language, and it moves and feels the RIGHT side of the body.",
        "hi": "बायाँ भाग: अधिकतर लोगों में यह भाषा को नियंत्रित करता है, और शरीर के दाएँ हिस्से की हरकत व संवेदना संभालता है।",
    },
    "right": {
        "en": "Right side: it moves and feels the LEFT side of the body and helps with spatial awareness.",
        "hi": "दायाँ भाग: यह शरीर के बाएँ हिस्से की हरकत व संवेदना संभालता है और जगह की समझ में मदद करता है।",
    },
    "midline": {
        "en": "Near the middle: it may affect both sides or the fluid pathways in the brain.",
        "hi": "बीच के पास: यह दोनों तरफ या मस्तिष्क के द्रव मार्गों को प्रभावित कर सकता है।",
    },
}

TEXT = {
    "title": {"en": "Brain Function Impact Map", "hi": "ब्रेन फ़ंक्शन इम्पैक्ट मैप"},
    "disclaimer": {
        "en": ("This is an educational research tool, NOT a medical diagnosis. The model was trained on a small "
               "dataset and the region mapping is approximate. Please consult a qualified doctor."),
        "hi": ("यह एक शैक्षिक शोध उपकरण है, चिकित्सीय निदान नहीं। मॉडल छोटे डेटासेट पर प्रशिक्षित है और क्षेत्र का "
               "अनुमान केवल लगभग है। कृपया किसी योग्य डॉक्टर से सलाह लें।"),
    },
    "no_tumor": {
        "en": "The model did not detect a tumor in this image, so no region map was made.",
        "hi": "मॉडल को इस चित्र में ट्यूमर नहीं मिला, इसलिए क्षेत्र मानचित्र नहीं बनाया गया।",
    },
    "tumor_prob": {"en": "Model tumor probability", "hi": "मॉडल के अनुसार ट्यूमर की संभावना"},
    "likely_region": {"en": "Most likely region", "hi": "सबसे संभावित क्षेत्र"},
    "functions": {"en": "What this area does", "hi": "यह क्षेत्र क्या करता है"},
    "symptoms": {"en": "Symptoms a doctor may check for", "hi": "लक्षण जिनकी डॉक्टर जाँच कर सकते हैं"},
    "also_involved": {"en": "Also partly involved", "hi": "आंशिक रूप से शामिल"},
    "low_confidence": {
        "en": "The model's attention is spread out or partly outside the brain, so this location is uncertain.",
        "hi": "मॉडल का ध्यान फैला हुआ है या आंशिक रूप से मस्तिष्क के बाहर है, इसलिए यह स्थान अनिश्चित है।",
    },
}
