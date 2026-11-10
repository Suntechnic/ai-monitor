# Цены

Дата проверки: 10.11.2026, 12:31 МСК. USD за 1 млн токенов; порядок ставок: обычный вход / cache read / выход. Для OpenRouter значения локального JSON умножены на 1 000 000 и сверены с websearch страниц моделей (где доступно). Цена относится к выбранному продавцу, налоги и покупка кредитов не включены.

## DeepSeek напрямую

| Модель | Поставщик | Точный ID | Вход / cache read / выход | Контекст | Тарифные условия | Официальный URL |
| --- | --- | --- | --- | --- | --- | --- |
| V4.1 Flash 1017 | DeepSeek напрямую | `deepseek-flash` | peak 0.30 / 0.006 / 1.20; off-peak 0.15 / 0.003 / 0.60 | 1M | Thinking по умолчанию, доступен non-thinking; tools, vision, max output 384K; peak: пн–пт 01:00–04:00 и 06:00–10:00 UTC кроме кит. праздников | https://api-docs.deepseek.com/quick_start/pricing/ |
| V4 Pro | DeepSeek напрямую | `deepseek-v4-pro` | peak 2.20 / — / 8.80; off-peak 1.10 / — / 4.40 | 1M | Запросы к V4 Pro маршрутизируются на V4.1 Flash по цене Flash до выхода V4.1 Pro | https://api-docs.deepseek.com/quick_start/pricing/ |

Peak: пн–пт 01:00–04:00 и 06:00–10:00 UTC, исключая китайские гос. праздники; остальное — off-peak, включая выходные. `deepseek-flash` сейчас разрешается в V4.1-Flash-1017; старые имена перенаправляются на неё по цене Flash. Search и Fetch — $0.75 за 1000 успешных запросов каждый, начало тарификации 31.10.2026 16:00 UTC. Цены подтверждены webfetch HTML страницы (manifest статус ok).

## OpenRouter

| Модель | Поставщик | Точный ID | Вход / cache read / выход | Контекст | Тарифные условия | Официальный URL |
| --- | --- | --- | --- | --- | --- | --- |
| Claude Haiku 5.5 | OpenRouter | `anthropic/claude-haiku-5.5` | 0.10 / 0.01 / 0.50 | 1M | ≤100K входа; выше: 0.50 / 0.05 / 2.50 на весь запрос; cache write 0.125 | https://openrouter.ai/anthropic/claude-haiku-5.5 |
| GPT-6 Luna | OpenRouter | `openai/gpt-6-luna` | 0.10 / 0.01 / 0.50 | 1 050 000 | Базовая ставка; >272K: 0.20/0.02/0.75; cache write 0.125 | https://openrouter.ai/openai/gpt-6-luna |
| GPT-6.1 Terra | OpenRouter | `openai/gpt-6.1-terra` | 1.00 / 0.05 / 5.00 | 1 050 000 | Базовая ставка; >272K: 2.00/0.10/7.50; cache write 1.25 | https://openrouter.ai/openai/gpt-6.1-terra |
| Claude Sonnet 5.5 | OpenRouter | `anthropic/claude-sonnet-5.5` | 2.00 / 0.10 / 10.00 | 1M | 5 backend по 2/10; встречаются региональные 2.20/11; cache write 2.50 | https://openrouter.ai/anthropic/claude-sonnet-5.5 |
| Claude Opus 5.5 | OpenRouter | `anthropic/claude-opus-5.5` | 4.00 / 0.20 / 20.00 | 1M | Базовые 5 backend; встречаются 4.40/22 и 8/40; cache write 5.00 | https://openrouter.ai/anthropic/claude-opus-5.5 |
| Claude Fable 5.1 | OpenRouter | `anthropic/claude-fable-5.1` | 10.00 / 0.25 / 50.00 | 1M | Только дорогой tier; tools | https://openrouter.ai/anthropic/claude-fable-5.1 |
| Kimi K3.1 Pro | OpenRouter | `moonshotai/kimi-k3.1-pro` | 2.00 / 0.20 / 10.00 | 1 048 576 | Много backend; самые дешёвые 0.33/8.12 без гарантии качества; cache write 2.00 | https://openrouter.ai/moonshotai/kimi-k3.1-pro |
| MiniMax M3.1 Flash | OpenRouter | `minimax/minimax-m3.1-flash` | обычн 0.15/0.015/0.60; льготн 0.075/0.0075/0.30 | 1 048 576 | Льготное окно по UTC (JSON: 15:00–01:00); условия не детализированы на странице | https://openrouter.ai/minimax/minimax-m3.1-flash |
| DeepSeek V4.1 Flash 1017 | OpenRouter | `deepseek/deepseek-v4.1-flash-1017` | 0.15 / 0.003 / 0.60; peak 0.30/0.006/1.20 | 1 048 576 | Backend на выбор; у DeepSeek те же peak/off-peak условия | https://openrouter.ai/deepseek/deepseek-v4.1-flash-1017 |
| GLM-5.3 | OpenRouter | `z-ai/glm-5.3` | 1.40 / 0.26 / 4.40 | 1M | Дешёвые backend от 0.07/1.40 — не гарантия качества | https://openrouter.ai/z-ai/glm-5.3 |
| GLM-5.3-Flash | OpenRouter | `z-ai/glm-5.3-flash` | 0.15 / 0.03 / 0.50 | 1M | Ровная ставка у большинства backend | https://openrouter.ai/z-ai/glm-5.3-flash |
| Gemini 4 Argon | OpenRouter | `google/gemini-4-argon` | 2.00 / 0.10 / 10.00 | 1M | Скидка -50% до 30.11.2026; после: 4.00/0.20/20.00; cache write 0.1875 | https://openrouter.ai/google/gemini-4-argon |
| GPT-6.1 Sol | OpenRouter | `openai/gpt-6.1-sol` | 2.00 / 0.10 / 10.00 | 1 050 000 | OpenAI прямой 1/5; >272K входа: 4.00/0.20/15.00; cache write 2.50 | https://openrouter.ai/openai/gpt-6.1-sol |
| Hy4 | OpenRouter | `tencent/hy4` | 0.42 / 0.021 / 1.25 | 1 048 576 | 1M контекст, vision; впервые представлена; peak/off-peak в JSON (0.75/2.25 off-peak) | https://openrouter.ai/tencent/hy4 |

Агрегированная цена — не гарантия каждого backend. `:batch`, `:free`, `-pro`, `-prime` и `latest` — отдельные позиции, в расчёты не подставлялись. Низкая ставка сама по себе не признак устаревания.

## OpenCode Go: включённое использование

В таблице — учётные ставки, по которым вызов списывает allowance подписки, а **не** доплата за токены. Каждый вызов Go — **«включено в подписку»**, пока не исчерпан лимит модели.

| Модель | Поставщик | Точный ID | Вход / cache read / выход, учёт квоты | Месячный лимит (Go) | Условия | Официальный URL |
| --- | --- | --- | --- | --- | --- | --- |
| Claude Haiku 5.5 | OpenCode Go | `claude-haiku-5-5` | 0.10 / 0.01 / 0.50; >100K: 0.50/0.05/2.50 | $15 | 5 ч — 20%, неделя — 50%; cache write 0.125 | https://opencode.ai/docs/console/go |
| GPT-6 Luna | OpenCode Go | `gpt-6-luna` | 0.10 / 0.01 / 0.50; >272K: 0.20/0.02/0.75 | $22 | 5 ч — 20%, неделя — 50%; cache write 0.125 | https://opencode.ai/docs/console/go |
| GLM-5.3-Flash | OpenCode Go | `glm-5.3-flash` | 0.15 / 0.03 / 0.50 | $18 (возможно повышено до ~$60 по community-сигналам) | 5 ч — 20%, неделя — 50% | https://opencode.ai/docs/console/go |
| GLM-5.3 | OpenCode Go | `glm-5.3` | 1.40 / 0.26 / 4.40 | $15 | 5 ч — 20%, неделя — 50% | https://opencode.ai/docs/console/go |
| Kimi K3.1 Pro | OpenCode Go | `kimi-k3.1-pro` | 2.00 / 0.20 / 10.00; cache write 2.00 | $48 | 5 ч — 20%, неделя — 50% | https://opencode.ai/docs/console/go |
| DeepSeek V4.1 Flash | OpenCode Go | `deepseek-v4.1-flash` | peak 0.30/0.006/1.20; off-peak 0.15/0.003/0.60 | $100 (Go, подтверждено qcode.cc 05.11.2026) | 5 ч — 20%, неделя — 50%; ZDR до 30.11.2026 | https://opencode.ai/docs/console/go |
| MiniMax M3.1 Flash | OpenCode Go | `minimax-m3.1-flash` | обычн 0.15/0.015/0.60; льготн 0.075/0.0075/0.30 | $36 | 5 ч — 20%, неделя — 50% | https://opencode.ai/docs/console/go |
| DeepSeek V4 Pro | OpenCode Go | `deepseek-v4-pro` | peak 2.20/—/8.80; off-peak 1.10/—/4.40 | $24 | 5 ч — 20%, неделя — 50% | https://opencode.ai/docs/console/go |

Планы: Go $10/мес, Go Plus $40/мес, Go Teams $20/участник/мес. Лимит модели делится между задачами. Sonnet 5.5 и Opus 5.5 в списке Go отсутствуют — рекомендованы только через OpenRouter. Бесплатные модели и временные промо исключены из рекомендаций.

## Токенатор

Токенатор использует единую тарификацию: пакеты токенов с базовой ценой $0.27/млн. Множитель модели показывает, во сколько раз дороже её токены относительно базовых. Вход и выход тарифицируются одинаково по множителю — нет раздельных ставок.

Пакеты (по данным HTML 10.11.2026): 100M токенов — ₽2350 (~$26), 500M — ₽8300, 5M — ₽250, 3M — ₽150. Курс при расчёте ~90 руб/$.

| Модель | Поставщик | Точный ID | Множитель | Контекст | Тарифные условия | Официальный URL |
| --- | --- | --- | --- | --- | --- | --- |
| DeepSeek V4.1 Flash | Токенатор | `deepseek-v4.1-flash` | ×1.7 (подтверждено websearch) | 1.05M | Единая ставка по множителю; online | https://tokenator.cloud/models |
| Claude Sonnet 5 (не 5.5) | Токенатор | `claude-sonnet-5` | ×1.7 (подтверждено websearch) | 1M | online | https://tokenator.cloud/models |
| GPT-5.5 | Токенатор | `gpt-5.5` | ×1.8 (подтверждено websearch) | 1.05M | online | https://tokenator.cloud/models |
| Claude Opus 5 (не 5.5) | Токенатор | `claude-opus-5` | ×1.9 (подтверждено websearch) | 1M | online | https://tokenator.cloud/models |
| GLM 5.3 FlashX | Токенатор | `glm-5.3-flashx` | ×0.8 (подтверждено HTML) | 1.05M | online | https://tokenator.cloud/models |
| MiMo-V2.6-Flash | Токенатор | `mimo-v2.6-flash` | ×0.8 (подтверждено HTML) | 1.05M | online | https://tokenator.cloud/models |
| Hy4 | Токенатор | `hy4` | ×0.8 (подтверждено HTML) | 1.05M | online | https://tokenator.cloud/models |
| Claude Sonnet 4.6 | Токенатор | `claude-sonnet-4-6` | ×1.7 (подтверждено HTML) | 1M | online | https://tokenator.cloud/models |

Claude Sonnet 5.5 и Opus 5.5 в Tokenator: конкретные множители в HTML не отображены (страница SSR с JS-рендерингом каталога, карточки 5.5-версий обрезаны в сохранённом HTML). Ориентировочно по логике вендора множители должны быть аналогичны или выше предыдущих версий (Sonnet 5 ×1.7, Opus 5 ×1.9), но без подтверждения точных значений. Не приписываем.

## Vantyr

Vantyr (vantyr.xyz) — JS-SPA, сохранённый HTML (vantyr.html) содержит только оболочку без отрендеренного контента. webfetch страницы pricing не вернул данных. websearch не дал конкретных цен Vantyr для отдельных моделей. Vantyr заявляет о продаже Claude, GPT и Codex моделей «по части официальной цены» с автоматической проверкой подлинности, но конкретные тарифы в сохранённых данных отсутствуют. Без подтверждения цен не включаем Vantyr в рекомендации.

## Арифметика каждой рекомендации

Формула: `(вход × ставка входа + выход × ставка выхода) / 1 000 000`, без кеша.

| Задача и роль | Доступ, модель | Подстановка | Итог |
| --- | --- | --- | --- |
| Простые — Основной | OpenCode Go, Haiku 5.5 | (2000×0.10 + 500×0.50)/1M | включено в подписку; allowance $0.00045 |
| Простые — Бюджетный | OpenRouter, GPT-6 Luna | (2000×0.10 + 500×0.50)/1M | $0.00045 |
| Простые — Усиленный | OpenRouter, Sonnet 5.5 | (2000×2 + 500×10)/1M | $0.009 |
| Вёрстка — Основной | OpenRouter, Sonnet 5.5 | (8000×2 + 2000×10)/1M | $0.036 |
| Вёрстка — Бюджетный | OpenRouter, MiniMax M3.1 Flash | (8000×0.15 + 2000×0.60)/1M | $0.0024 обычный; $0.0012 льготный |
| Вёрстка — Усиленный | OpenRouter, Opus 5.5 | (8000×4 + 2000×20)/1M | $0.072 |
| Код — Основной | DeepSeek напрямую, Flash 1017 | peak (12000×0.30 + 3000×1.20)/1M | peak $0.0072; off-peak $0.0036 |
| Код — Бюджетный | OpenCode Go, GLM-5.3-Flash | (12000×0.15 + 3000×0.50)/1M | включено в подписку; allowance $0.0033 |
| Код — Усиленный | OpenRouter, Fable 5.1 | (12000×10 + 3000×50)/1M | $0.270 |
| Планирование — Основной | OpenRouter, Kimi K3.1 Pro | (50000×2 + 8000×10)/1M | $0.18 |
| Планирование — Бюджетный | OpenCode Go, GLM-5.3 | (50000×1.40 + 8000×4.40)/1M | включено в подписку; allowance $0.1052 |
| Планирование — Усиленный | OpenRouter, Opus 5.5 | (50000×4 + 8000×20)/1M | $0.36 |
| Реализация — Основной | DeepSeek напрямую, Flash 1017 | peak (50000×0.30 + 8000×1.20)/1M | peak $0.0246; off-peak $0.0123 |
| Реализация — Бюджетный | OpenCode Go, Kimi K3.1 Pro | (50000×2 + 8000×10)/1M | включено в подписку; allowance $0.18 |
| Реализация — Усиленный | OpenRouter, Opus 5.5 | (50000×4 + 8000×20)/1M | $0.36 |
| Проверка — Основной | OpenRouter, Sonnet 5.5 | (50000×2 + 8000×10)/1M | $0.18 |
| Проверка — Бюджетный | OpenRouter, GPT-6.1 Terra | (50000×1 + 8000×5)/1M | $0.09 |
| Проверка — Усиленный | OpenRouter, Opus 5.5 | (50000×4 + 8000×20)/1M | $0.36 |

Все суммы сверен программой без сетевых вызовов. Один вызов не равен стоимости агентной задачи: история передаётся повторно, инструменты добавляют ходы, кеш снижает вход, reasoning и повторы увеличивают расход. Для Go: месячный лимит $15 у GLM-5.3 покрывает ~142 условных проектных вызова без кеша, но 5-часовой лимит — ~28. DeepSeek V4.1 Flash при новом лимите $100/мес покрывает ~813 кодовых вызовов (12K/3K) в off-peak и ~4065 при пиковых ценах.

Для OpenRouter и DeepSeek напрямую стоимость напрямую пересчитывается в реальные доллары. Для OpenCode Go allowance — это условная стоимость, которая вычитается из месячного и почасового лимита модели, но не равна реальной доплате за токены. Для Токенатора расчёт по множителю: один условный вызов 12000вх+3000вых = 15000 токенов × множитель / 1M × $0.27.
