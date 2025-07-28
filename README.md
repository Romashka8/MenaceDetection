⚠️Beta⚠️
# ✅About
Решение для парсинга актуальной информации из раздела "обсуждений" с сайтов банковских форумов. Нужно для анализа веб-ресурсов на предмет фрода и удобной бизнес-аналитики.
# ✅Установка
Для начала работы нужно скачать репозиторий и установить необходимые библиотеки из файла:
1) Скачиваем репозитоий: `git clone https://github.com/Romashka8/MenaceDetection.git`
2) Устанавливаем нужные библиотеки: `pip install -r requirements.txt`
# ✅Модуль parser

Класс OnlineParser предназначен для парсинга статических веб-ресурсов. Примеры, для которых OnlineParser будет хорошим решением:
1) https://finforums.ru/
2) https://findozor.net/forum/#banki.119
3) https://hranidengi.com/forums/banki-rf/
4) http://kupus.ru/

Содержит online_parser. Класс OnlineParser реализует следующие методы:
- parse_headers(url, deep) - парсинг заголовков(названий) тем, ссылок на них, даты старта и даты последнего сообщения по заданному адресу. Параметр deep указывает, сколько страниц из раздела нужно спарсить. Возвращает массив, элементами которого являются словари вида: {title: [link, date_start, date_last_message]}. Оптимально использовать для мониторинга активности в интересующем разделе форума.
- parse_comments(url, deep, verbose=False) - парсинг комментариев в выбранной теме, их содержания и времени отправки.
## Принцип работы

Статические сайты парсятса при помощи .json файлов конфигурации, их структура должна быть следующей:

{
    "header_links": [
        "Ссылка на заголовок интересующей темы"
    ],
    "header_map": {
        "Ссылка на заголовок интересующей темы": "Название темы"
    },
    "header_classes": [
        "html классы, в которые обернуты заголовки"
    ],
    "header_container": "html контейнер заголовка",
    "header_link_field": "html атрибут на ссылку с обсуждением темы заголовка",
    "header_prefix": "префиксное дополнение к ссылке на заголовок",
    "header_suffix": "суффиксное дополнение к ссылке на заголовок",
    "header_slice": "срез ссылки заголовка(для перехода на следующие страницы с темами)",
    "comment_classes": [
         "html классы, в которые обернуты заголовки"
    ],
    "comment_container": "html контейнер для заголовков",
    "comment_prefix": "префиксное дополнение к ссылке на комментарии",
    "comment_suffix": "суффиксное дополнение к ссылке на комментарии",
    "comment_slice": "срез ссылки комментария(для перехода на следующие страницы с темами)",
    "comment_text_container": "html контейнер с текстом комментария",
    "comment_date_container": "html контейнер с датой комментария",
    "comment_date_atr": "html атрибут с датой комментария",
    "skip_first": сколько комментариев пропускать
}

Реализованные конфигурации для парсинга можно найти в директории parser/config.

## Пример html страницы и конфигом для нее

`<!DOCTYPE html>`
`<html>`
`<head>`
    `<title>Форум банка - Обсуждение кредитных карт</title>`
    `<style>`
        `.thread-header { margin-bottom: 15px; }`
        `.thread-container { border: 1px solid #ddd; padding: 10px; margin: 10px 0; }`
        `.comment-block { background: #f9f9f9; padding: 12px; margin: 8px 0; border-radius: 4px; }`
        `.comment-content { margin: 5px 0; }`
        `.comment-meta { color: #666; font-size: 0.9em; }`
    `</style>`
`</head>`
`<body>`
    `<!-- Секция заголовков тем (header_container) -->`
    `<div id="threads-list">`
        `<!-- Элемент с header_classes -->`
        `<div class="thread-container thread-header">`
            `<!-- header_link_field = "href" -->`
            `<h2><a href="/forum/credit-cards/page-1" class="thread-link">Обсуждение кредитных карт Premium</a></h2>`
        `</div>`
        
        `<div class="thread-container thread-header">`
            `<h2><a href="/forum/mortgages/page-2" class="thread-link">Ипотека для молодых семей</a></h2>`
        `</div>`
    `</div>`

    `<!-- Секция комментариев -->`
    `<div id="comments-section">`
        `<!-- Элемент с comment_classes -->`
        `<div class="comment-block comment">`
            `<div class="comment-content">`
                `<p class="comment-text">Карта хорошая, но высокий процент</p>`
            `</div>`
            `<div class="comment-meta">`
                `<!-- comment_date_container + comment_date_atr -->`
                `<span class="comment-date" datetime="2023-10-01T14:30:00Z">01 октября 2023</span>`
            `</div>`
        `</div>`
        
        `<div class="comment-block comment">`
            `<div class="comment-content">`
                `<p class="comment-text">Одобрили ипотеку под 8%</p>`
            `</div>`
            `<div class="comment-meta">`
                `<span class="comment-date" datetime="2023-10-02T10:15:00Z">02 октября 2023</span>`
            `</div>`
        `</div>`
    `</div>`
`</body>`
`</html>`

config = {
    "header_links": [
        "/forum/credit-cards/page-1",
        "/forum/mortgages/page-2"
    ],
    "header_map": {
        "/forum/credit-cards/page-1": "Кредитные карты",
        "/forum/mortgages/page-2": "Ипотечные программы"
    },
    "header_classes": ["thread-header"],
    "header_container": "div.thread-container",
    "header_link_field": "href",
    "header_prefix": "https://example.com",
    "header_suffix": "?sort=newest",
    "header_slice": "/forum/(.+?)/page",
    "comment_classes": ["comment"],
    "comment_container": "div.comment-block",
    "comment_prefix": "#",
    "comment_suffix": "",
    "comment_slice": "comment-(\\d+)",
    "comment_text_container": "p.comment-text",
    "comment_date_container": "span.comment-date",
    "comment_date_atr": "datetime",
    "skip_first": 1
}
# ✅ Возможные проблемы

1) При попытке парсинга того или иного источника код может упасть с ошибкой ConnectionError на стороне сервера. В таком случае эту ошибку необходимо отлавливать и в случае ее возникновения повторно пытаться спарсить нужную страницу.
2) Не все комментарии даже на одной странице сайта могут быть обернуты в одинаковые теги. Хорошей практикой будет выработка индивидуального подхода под каждый из ресурсов с сохранением гибкости и идей основного кода.

# ✅ CookBook-и

1) collect_datasets.ipynb - парсинг и сборка датасетов. Рассмотрены случай для небольшого(меньше 1. тыс. комментариев в теме) и большого(больше 1. тыс. комментариев в теме) сайтов.
2) giga_map_topics.ipynb - разметка тем при помощи гигачата.
3) giga_detect_fraud.ipynb - поиск фрода при помощи гигачата. 
# ✅ Идеи/будущие улучшения

1) Улучшение качества парсинга текста при помощи регулярных выражений.
2) Полная автоматизация предложенных пайплайнов.
3) Добавление более сложной агентной среды.