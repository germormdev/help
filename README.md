# Мануал VecturaBook — help.vecturabook.com

Источник — `/volume1/Gromoz/Help/Git/Help.git` на NAS. Пуш в `main` сам уходит на GitHub (`germormdev/help`, хук
`post-receive` → `Help/Git/push-to-github.sh`, ключ только на NAS `/volume1/secrets/github/id_ed25519_github_help`), GitHub
Pages собирает Jekyll и раздаёт с HTTPS.

## Адреса

`https://help.vecturabook.com/<язык>/<раздел>` — постоянные, на них ведёт экран «Помощь» приложения. Разделы и языки —
`_data/titles.json`; он не пишется руками, а берётся из строк приложения:
`python3 tools/titles_from_app.py <дерево приложения> > _data/titles.json`, затем `python3 tools/make_pages.py`.

## Как класть текст (Клод Мак)

- Страница раздела — `<язык>/<раздел>.md`, Markdown. В начале:

      ---
      layout: page
      lang: ru
      section: trip
      title: "Рейс: от погрузки до выгрузки"
      ---

  Без строки `stub: true` — это и есть признак настоящего текста: `make_pages.py` такой файл не трогает.
- Картинки — `<язык>/img/…` или общие `img/…`, ссылка относительная.
- Новый раздел — сначала в приложении (`HelpSections`), потом `titles_from_app.py` и `make_pages.py`.
- Проверка, что все адреса покрыты: `python3 tools/make_pages.py --check`.
