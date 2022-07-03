import re
import pymorphy2
import math


def read_text(file):
    text = []
    with open(file, "r") as f:
        text = re.sub(r'[^\w\s]', ' ', f.read()).lower().split()
    return text


def filter_and_normalize_text(text):
    stopwords_ru = []
    with open("stopwords_ru.txt", "r") as f:
        stopwords_ru = f.read().split()

    filtered_words = [word for word in text if not word in stopwords_ru]

    morph = pymorphy2.MorphAnalyzer()
    for i in range(len(filtered_words)):
        filtered_words[i] = morph.parse(filtered_words[i])[0].normal_form

    return set(filtered_words)


def read_keywords(file):
    keywords = []
    with open(file, "r") as f:
        keywords = f.read().split()
    return set(keywords)


def get_jaccard_coefficient(text, topic_keywords):
    union = text.union(topic_keywords)
    intersection = text.intersection(topic_keywords)
    jacaard_coefficient = len(intersection) / len(union)

    return intersection, jacaard_coefficient


def get_cosine_metric(words, topics_keywords):
    topics_vectors = []
    for topic_count in range(len(topics_keywords)):
        zero_vector = [0] * len(topics_keywords)
        zero_vector[topic_count] = 1
        topics_vectors.append(zero_vector)

    words_vector = [0] * len(topics_keywords)
    for topic_count in range(len(topics_keywords)):
        words_vector[topic_count] = len(words.intersection(topics_keywords[topic_count]))

    words_vector = [coordinate / max(words_vector) for coordinate in words_vector]

    cosine_metrics = []
    for topic_vector in topics_vectors:
        cosine_metrics.append(get_cosine(words_vector, topic_vector))

    return cosine_metrics


def get_cosine(vector1, vector2):
    numerator = 0
    for coordinate_count in range(len(vector1)):
        numerator += vector1[coordinate_count] * vector2[coordinate_count]

    length_vector1 = 0
    length_vector2 = 0

    for coordinate_count in range(len(vector1)):
        length_vector1 += math.pow(vector1[coordinate_count], 2)
        length_vector2 += math.pow(vector2[coordinate_count], 2)

    length_vector1 = math.sqrt(length_vector1)
    length_vector2 = math.sqrt(length_vector2)

    denominator = length_vector1 * length_vector2

    return numerator / denominator


def main():
    text = read_text("text.txt")
    words = filter_and_normalize_text(text)
    science_keywords = read_keywords("scence_keywords.txt")
    sport_keywords = read_keywords("sport_keywords.txt")
    shopping_keywords = read_keywords("shopping_keywords.txt")
    news_keywords = read_keywords("news_keywords.txt")

    science_topic_intersection, science_topic_jaccard_coefficient = get_jaccard_coefficient(words, science_keywords)
    sport_topic_intersection, sport_topic_jaccard_coefficient = get_jaccard_coefficient(words, sport_keywords)
    shopping_topic_intersection, shopping_topic_jaccard_coefficient = get_jaccard_coefficient(words, shopping_keywords)
    news_topic_intersection, news_topic_jaccard_coefficient = get_jaccard_coefficient(words, news_keywords)

    cosine_metrics = get_cosine_metric(words, [science_keywords, sport_keywords, shopping_keywords, news_keywords])

    print(
        f'Коэффициенты Жаккара:\n\nТема "Наука" - {science_topic_jaccard_coefficient}\nПересечение слов - {science_topic_intersection}\n\nТема "Спорт" - {sport_topic_jaccard_coefficient}\nПересечение слов - {sport_topic_intersection}\n\nТема "Шоппинг" - {shopping_topic_jaccard_coefficient}\nПересечение слов - {shopping_topic_intersection}\n\nТема "Новости" - {news_topic_jaccard_coefficient}\nПересечение слов - {news_topic_intersection}\n\n')
    print(
        f'Метрики Косинуса:\n\nТема "Наука" - {cosine_metrics[0]}\n\nТема "Спорт" - {cosine_metrics[1]}\n\nТема "Шоппинг" - {cosine_metrics[2]}\n\nТема "Новости" - {cosine_metrics[3]}')


if __name__ == '__main__':
    main()
