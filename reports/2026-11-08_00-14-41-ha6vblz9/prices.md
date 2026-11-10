# Цены

Дата проверки: 08.11.2026, 03:14 МСК. USD за 1 млн токенов; порядок ставок: обычный вход / cache read / выход. Для OpenRouter значения локального JSON умножены на 1 000 000 и сверены с webfetch страниц моделей (где доступно). Цена относится к выбранному продавцу, налоги и покупка кредитов не включены.

## DeepSeek напрямую

| Модель | Поставщик | Точный ID | Вход / cache read / выход | Контекст | Тарифные условия | Официальный URL |
| --- | --- | --- | --- | --- | --- | --- |
| V4.1 Flash 1017 | DeepSeek напрямую | `deepseek-flash` | peak 0.30 / 0.006 / 1.20; off-peak 0.15 / 0.003 / 0.60 | 1M | Thinking по умолчанию, доступен non-thinking; tools, vision, max output 384K; peak: пн–пт 01:00–04:00 и 06:00–10:00 UTC кроме кит. праздников | https://api-docs.deepseek.com/quick_start/pricing/ |

Peak: пн–пт 01:00–04:00 и 06:00–10:00 UTC, исключая китайские гос. праздники; остальное — off-peak, включая выходные. `deepseek-flash` сейчас разрешается в 1017; старые имена перенаправляются на неё по цене Flash. Search и Fetch — $0.75 за 1000 успешных запросов каждый, начало тарификации 31.10.2026 16:00 UTC (бесплатно до этой даты).

## OpenRouter

| Модель | Поставщик | Точный ID | Вход / cache read / выход | Контекст | Тарифные условия | Официальный URL |
| --- | --- | --- | --- | --- | --- | --- |
| Claude Haiku 5.5 | OpenRouter | `anthropic/claude-haiku-5.5` | 0.10 / 0.01 / 0.50 | 1M | ≤100K входа; выше: 0.50 / 0.05 / 2.50 на весь запрос; cache write 0.125 | https://openrouter.ai/anthropic/claude-haiku-5.5 |
| GPT-6 Luna | OpenRouter | `openai/gpt-6-luna` | 0.10 / 0.01 / 0.50 | 1 050 000 | Базовая ставка; есть строки с высоким контекстом (>272K): 0.20/0.02/0.75; cache write 0.125 | https://openrouter.ai/openai/gpt-6-luna |
| GPT-6.1 Terra | OpenRouter | `openai/gpt-6.1-terra` | 1.00 / 0.05 / 5.00 | 1 050 000 | Базовая ставка; >272K: 2.00/0.10/7.50; cache write 1.25 | https://openrouter.ai/openai/gpt-6.1-terra |
| Claude Sonnet 5.5 | OpenRouter | `anthropic/claude-sonnet-5.5` | 2.00 / 0.10 / 10.00 | 1M | 5 backend по 2/10; встречаются региональные 2.20/11; cache write 2.50 | https://openrouter.ai/anthropic/claude-sonnet-5.5 |
| Claude Opus 5.5 | OpenRouter | `anthropic/claude-opus-5.5` | 4.00 / 0.20 / 20.00 | 1M | Базовые 5 backend; встречаются 4.40/22 и 8/40; cache write 5.00 | https://openrouter.ai/anthropic/claude-opus-5.5 |
| Claude Fable 5.1 | OpenRouter | `anthropic/claude-fable-5.1` | 10.00 / 0.25 / 50.00 | 1M | Только дорогой tier; tools | https://openrouter.ai/anthropic/claude-fable-5.1 |
| Kimi K3.1 Pro | OpenRouter | `moonshotai/kimi-k3.1-pro` | 2.00 / 0.20 / 10.00 | 1 048 576 | Много backend; самые дешёвые 0.33/8.12 без гарантии качества; cache write 2.00 | https://openrouter.ai/moonshotai/kimi-k3.1-pro |
| MiniMax M3.1 Flash | OpenRouter | `minimax/minimax-m3.1-flash` | обычный 0.15/0.015/0.60; льготный 0.075/0.0075/0.30 | 1 048 576 | Льготное окно по UTC (JSON показывает 15:00–01:00); условия не детализированы на странице | https://openrouter.ai/minimax/minimax-m3.1-flash |
| DeepSeek V4.1 Flash 1017 | OpenRouter | `deepseek/deepseek-v4.1-flash-1017` | 0.15 / 0.003 / 0.60; peak 0.30/0.006/1.20 | 1 048 576 | Backend на выбор; у DeepSeek те же peak/off-peak условия | https://openrouter.ai/deepseek/deepseek-v4.1-flash-1017 |
| GLM-5.3 | OpenRouter | `z-ai/glm-5.3` | 1.40 / 0.26 / 4.40 | 1M | Дешёвые backend от 0.07/1.40 — не гарантия качества | https://openrouter.ai/z-ai/glm-5.3 |
| GLM-5.3-Flash | OpenRouter | `z-ai/glm-5.3-flash` | 0.15 / 0.03 / 0.50 | 1M | Ровная ставка у большинства backend | https://openrouter.ai/z-ai/glm-5.3-flash |
| Gemini 4 Argon | OpenRouter | `google/gemini-4-argon` | 2.00 / 0.10 / 10.00 | 1M | Скидка -50% до 30.11.2026; после: 4.00/0.20/20.00; cache write 0.1875 | https://openrouter.ai/google/gemini-4-argon |
| GPT-6.1 Sol | OpenRouter | `openai/gpt-6.1-sol` | 2.00 / 0.10 / 10.00 | 1 050 000 | OpenAI прямой 1/5; >272K входа: 4.00/0.20/15.00; cache write 2.50 | https://openrouter.ai/openai/gpt-6.1-sol |

Агрегированная цена — не гарантия каждого backend. `:batch`, `:free`, `-pro`, `-prime` и `latest` — отдельные позиции, в расчёты не подставлялись. Низкая ставка сама по себе не признак устаревания. OpenRouter расширил каталог до 600+ моделей на всех платных планах (изменение между 26.10 и 02.11.2026).

## OpenCode Go: включённое использование

В таблице — учётные ставки, по которым вызов списывает allowance подписки, а **не** доплата за токены. Каждый вызов Go — **«включено в подписку»**, пока не исчерпан лимит модели.

| Модель | Поставщик | Точный ID | Вход / cache read / выход, учёт квоты | Месячный лимит (Go) | Условия | Официальный URL |
| --- | --- | --- | --- | --- | --- | --- |
| Claude Haiku 5.5 | OpenCode Go | `claude-haiku-5-5` | 0.10 / 0.01 / 0.50; >100K: 0.50/0.05/2.50 | $15 | 5 ч — 20%, неделя — 50%; cache write 0.125 | https://opencode.ai/v2/docs/console/go/ |
| GPT-6 Luna | OpenCode Go | `gpt-6-luna` | 0.10 / 0.01 / 0.50; >272K: 0.20/0.02/0.75 | $22 | 5 ч — 20%, неделя — 50%; cache write 0.125 | https://opencode.ai/v2/docs/console/go/ |
| GLM-5.3-Flash | OpenCode Go | `glm-5.3-flash` | 0.15 / 0.03 / 0.50 | $18 | 5 ч — 20%, неделя — 50% | https://opencode.ai/v2/docs/console/go/ |
| GLM-5.3 | OpenCode Go | `glm-5.3` | 1.40 / 0.26 / 4.40 | $15 | 5 ч — 20%, неделя — 50% | https://opencode.ai/v2/docs/console/go/ |
| Kimi K3.1 Pro | OpenCode Go | `kimi-k3.1-pro` | 2.00 / 0.20 / 10.00; cache write 2.00 | $48 | 5 ч — 20%, неделя — 50% | https://opencode.ai/v2/docs/console/go/ |
| DeepSeek V4.1 Flash | OpenCode Go | `deepseek-v4.1-flash` | peak 0.30/0.006/1.20; off-peak 0.15/0.003/0.60 | $60 (4× увеличение с 05.11.2026) | 5 ч — 20%, неделя — 50%; ZDR до 30.11.2026 | https://opencode.ai/v2/docs/console/go/ |
| MiniMax M3.1 Flash | OpenCode Go | `minimax-m3.1-flash` | обычный 0.15/0.015/0.60; льготный 0.075/0.0075/0.30 | $36 | 5 ч — 20%, неделя — 50% | https://opencode.ai/v2/docs/console/go/ |

Планы: Go $10/мес, Go Plus $40/мес, Go Teams $20/участник/мес. Лимит модели делится между задачами. Sonnet 5.5 и Opus 5.5 в списке Go отсутствуют — рекомендованы только через OpenRouter. Бесплатные модели и временные промо исключены из рекомендаций.

## Арифметика каждой рекомендации

Формула: `(вход × ставка входа + выход × ставка выхода) / 1 000 000`, без кеша.

| Задача и роль | Доступ, модель | Подстановка | Итог |
| --- | --- | --- | --- |
| Простые — Основной | OpenCode Go, Haiku | (2000×0.10 + 500×0.50)/1M | включено в подписку; allowance $0.00045 |
| Простые — Бюджетный | OpenRouter, Luna | (2000×0.10 + 500×0.50)/1M | $0.00045 |
| Простые — Усиленный | OpenRouter, Sonnet | (2000×2 + 500×10)/1M | $0.009 |
| Вёрстка — Основной | OpenRouter, Sonnet | (8000×2 + 2000×10)/1M | $0.036 |
| Вёрстка — Бюджетный | OpenRouter, MiniMax M3.1 Flash | (8000×0.15 + 2000×0.60)/1M | $0.0024 обычный; $0.0012 льготный |
| Вёрстка — Усиленный | OpenRouter, Opus | (8000×4 + 2000×20)/1M | $0.072 |
| Код — Основной | DeepSeek напрямую, Flash | peak (12000×0.30 + 3000×1.20)/1M | peak $0.0072; off-peak $0.0036 |
| Код — Бюджетный | OpenCode Go, GLM-5.3-Flash | (12000×0.15 + 3000×0.50)/1M | включено в подписку; allowance $0.0033 |
| Код — Усиленный | OpenRouter, Fable 5.1 | (12000×10 + 3000×50)/1M | $0.270 |
| Планирование — Основной | OpenRouter, Kimi K3.1 Pro | (50000×2 + 8000×10)/1M | $0.18 |
| Планирование — Бюджетный | OpenCode Go, GLM-5.3 | (50000×1.40 + 8000×4.40)/1M | включено в подписку; allowance $0.1052 |
| Планирование — Усиленный | OpenRouter, Opus | (50000×4 + 8000×20)/1M | $0.36 |
| Реализация — Основной | DeepSeek напрямую, Flash | peak (50000×0.30 + 8000×1.20)/1M | peak $0.0246; off-peak $0.0123 |
| Реализация — Бюджетный | OpenCode Go, Kimi K3.1 Pro | (50000×2 + 8000×10)/1M | включено в подписку; allowance $0.18 |
| Реализация — Усиленный | OpenRouter, Opus | (50000×4 + 8000×20)/1M | $0.36 |
| Проверка — Основной | OpenRouter, Sonnet | (50000×2 + 8000×10)/1M | $0.18 |
| Проверка — Бюджетный | OpenRouter, GPT-6.1 Terra | (50000×1 + 8000×5)/1M | $0.09 |
| Проверка — Усиленный | OpenRouter, Opus | (50000×4 + 8000×20)/1M | $0.36 |

Сверено программой без сетевых вызовов. Один вызов не равен стоимости агентной задачи: история передаётся повторно, инструменты добавляют ходы, кеш снижает вход, reasoning и повторы увеличивают расход. Для Go: месячный лимит $15 у GLM-5.3 покрывает ~142 условных проектных вызова без кеша, но 5-часовой лимит — ~28. DeepSeek V4.1 Flash при новом лимите $60/мес покрывает ~488 кодовых вызовов (12K/3K) в off-peak и ~833 при пиковых часах.

Для OpenRouter и DeepSeek напрямую стоимость напрямую пересчитывается в реальные доллары. Для OpenCode Go allowance — это условная стоимость, которая вычитается из месячного и почасового лимита модели, но не равна реальной доплате за токены. Подробное пояснение условий Go и расчётов в официальной документации.
