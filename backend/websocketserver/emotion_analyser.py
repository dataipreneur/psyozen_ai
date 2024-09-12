from transformers import pipeline

def analyze_emotion(text):
  emotion_analyzer = pipeline("text-classification", model="j-hartmann/emotion-english-distilroberta-base", return_all_scores=True)
  emotions = emotion_analyzer(text)
  return emotions
