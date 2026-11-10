# Цены

Дата проверки: 07.11.2026. USD за 1 млн токенов; порядок ставок: обычный вход / cache read / выход. Для OpenRouter значения локального JSON умножены на 1 000 000 и сверены с webfetch страниц моделей. Цена относится к выбранному продавцу, налоги и покупка кредитов не включены.

## DeepSeek напрямую

| Модель | Поставщик | Точный ID | Вход / cache read / выход | Контекст | Тарифные условия | Официальный URL |
| --- | --- | --- | --- | --- | --- | --- |
| V4.1 Flash 1017 | DeepSeek напрямую | `deepseek-flash` | peak 0.30 / 0.006 / 1.20; off-peak 0.15 / 0.003 / 0.60 | 1M | Thinking по умолчанию, доступен non-thinking; tools, vision, max output 384K | https://api-docs.deepseek.com/quick_start/pricing/ |

Peak: пн–пт 01:00–04:00 и 06:00–10:00 UTC, исключая китайские гос. праздники; остальное — off-peak, включая выходные. `deepseek-flash` сейчас разрешается в 1017; старые имена перенаправляются на неё по цене Flash. Search и Fetch — $0.75 за 1000 успешных запросов каждый. Цены веб-страницы содержательные, не оболочка.

## OpenRouter

| Модель | Поставщик | Точный ID | Вход / cache read / выход | Контекст | Тарифные условия | Официальный URL |
| --- | --- | --- | --- | --- | --- | --- |
| Claude Haiku 5.5 | OpenRouter | `anthropic/claude-haiku-5.5` | 0.10 / 0.01 / 0.50 | 1M | ≤100K входа; выше: 0.50 / 0.05 / 2.50 на весь запрос; cache write 0.125 | https://openrouter.ai/anthropic/claude-haiku-5.5 |
| GPT-6 Luna | OpenRouter | `openai/gpt-6-luna` | 0.10 / 0.01 / 0.50 | 1 050 000 | Базовая ставка; есть строки 0.05/0.25 и 0.20/1.00, условия не раскрыты | https://openrouter.ai/openai/gpt-6-luna |
| Claude Sonnet 5.5 | OpenRouter | `anthropic/claude-sonnet-5.5` | 2.00 / 0.10 / 10.00 | 1M | 5 backend по 2/10; региональные строки 2.20/11 | https://openrouter.ai/anthropic/claude-sonnet-5.5 |
| Claude Opus 5.5 | OpenRouter | `anthropic/claude-opus-5.5` | 4.00 / 0.20 / 20.00 | 1M | Базовые 5 backend; встречаются 4.40/22 и 8/40 | https://openrouter.ai/anthropic/claude-opus-5.5 |
| Claude Fable 5.1 | OpenRouter | `anthropic/claude-fable-5.1` | 10.00 / 0.25 / 50.00 | 1M | Только дорогой tier; tools | https://openrouter.ai/anthropic/claude-fable-5.1 |
| Kimi K3.1 Pro | OpenRouter | `moonshotai/kimi-k3.1-pro` | 2.00 / 0.20 / 10.00 | 1 048 576 | Много backend; самые дешёвые 0.33/8.12 без гарантии качества; cache write 2.00 | https://openrouter.ai/moonshotai/kimi-k3.1-pro |
| MiniMax M3.1 Flash | OpenRouter | `minimax/minimax-m3.1-flash` | 0.15 / 0.015 / 0.60; льготный 0.075/0.0075/0.30 | 1 048 576 | Льготное окно по UTC (в JSON 15:00–01:00); условия не детализированы | https://openrouter.ai/minimax/minimax-m3.1-flash |
| DeepSeek V4.1 Flash 1017 | OpenRouter | `deepseek/deepseek-v4.1-flash-1017` | 0.15 / 0.003 / 0.60; peak 0.30/0.006/1.20 | 1 048 576 | Backend на выбор; у DeepSeek те же peak/off-peak | https://openrouter.ai/deepseek/deepseek-v4.1-flash-1017 |
| GLM-5.3 | OpenRouter | `z-ai/glm-5.3` | 1.40 / 0.26 / 4.40 | 1M | Дешёвые backend от 0.07/1.40 — не гарантия качества | https://openrouter.ai/z-ai/glm-5.3 |
| GLM-5.3-Flash | OpenRouter | `z-ai/glm-5.3-flash` | 0.15 / 0.03 / 0.50 | 1M | Ровная ставка у большинства backend | https://openrouter.ai/z-ai/glm-5.3-flash |
| Gemini 4 Argon | OpenRouter | `google/gemini-4-argon` | 2.00 / 0.10 / 10.00 | 1M | AI Studio строки от 1/5; cache write 0.1875 | https://openrouter.ai/google/gemini-4-argon |
| GPT-6.1 Sol | OpenRouter | `openai/gpt-6.1-sol` | 2.00 / 0.10 / 10.00 | 1 050 000 | OpenAI прямой 1/5; >272K входа: 4/0.20/15 | https://openrouter.ai/openai/gpt-6.1-sol |
| Qwen3.8 Max Prime | OpenRouter | `qwen/qwen3.8-max-prime` | 4.00 / 0.50 / 12.00 | 1M | Один backend; cache write 2.50 | https://openrouter.ai/qwen/qwen3.8-max-prime |
| Hy4 | OpenRouter | `tencent/hy4` | 0.417 / 0.021 / 1.2505 | 1 048 576 | Только Tencent Cloud | https://openrouter.ai/tencent/hy4 |
| LongCat-2.0 | OpenRouter | `meituan/longcat-2.0` | 0.30 / 0.006 / 1.20 | 1 048 756 | Один backend | https://openrouter.ai/meituan/longcat-2.0 |

Агрегированная цена — не гарантия каждого backend. `:batch`, `:free`, `-pro`, `-prime` и `latest` — отдельные позиции, в расчёты не подставлялись. Низкая ставка сама по себе не признак устаревания.

## OpenCode Go: включённое использование

В таблице — учётные ставки, по которым вызов списывает allowance подписки, а **не** доплата за токены. Каждый вызов Go — **«включено в подписку»**, пока не исчерпан лимит модели.

| Модель | Поставщик | Точный ID | Вход / cache read / выход, учёт квоты | Месячный лимит (Go) | Условия | Официальный URL |
| --- | --- | --- | --- | --- | --- | --- |
| Claude Haiku 5.5 | OpenCode Go | `claude-haiku-5-5` | 0.10 / 0.01 / 0.50; >100K: 0.50/0.05/2.50 | $15 | 5 ч — 20%, неделя — 50% | https://opencode.ai/v2/docs/console/go/ |
| GPT-6 Luna | OpenCode Go | `gpt-6-luna` | 0.10 / 0.01 / 0.50; >272K: 0.20/0.02/0.75 | $15 | То же | https://opencode.ai/v2/docs/console/go/ |
| GLM-5.3-Flash | OpenCode Go | `glm-5.3-flash` | 0.15 / 0.03 / 0.50 | $60 | То же | https://opencode.ai/v2/docs/console/go/ |
| GLM-5.3 | OpenCode Go | `glm-5.3` | 1.40 / 0.26 / 4.40 | $15 | То же | https://opencode.ai/v2/docs/console/go/ |
| Kimi K3.1 Pro | OpenCode Go | `kimi-k3.1-pro` | 2.00 / 0.20 / 10.00; cache write 2.00 | $15 | То же | https://opencode.ai/v2/docs/console/go/ |
| DeepSeek V4.1 Flash | OpenCode Go | `deepseek-v4.1-flash` | peak 0.30/0.006/1.20; off-peak вдвое ниже | $100 | Нужен регион Global в Privacy; ZDR через 30.11.2026 | https://opencode.ai/v2/docs/console/go/ |
| Hy4 | OpenCode Go | `hy4` | 0.834 / 0.042 / 2.501 | $60 | То же | https://opencode.ai/v2/docs/console/go/ |
| LongCat-2.0 | OpenCode Go | `longcat-2.0` | 0.30 / 0.006 / 1.20 | $60 | То же | https://opencode.ai/v2/docs/console/go/ |

Планы: Go $10/мес, Go Plus $40/мес, Go Teams $20/участник/мес. Лимит модели делится между задачами, использующими эту модель. Sonnet 5.5 и Opus 5.5 в списке Go отсутствуют — рекомендованы только через OpenRouter. Бесплатные модели и временные промо (Gemini 4 Argon −50% до 30.11.2026, free-модели) исключены из рекомендаций. Pay-as-you-go Console (сохранённый opencode.html) как тариф Go не использовался.

## Арифметика каждой рекомендации

Формула: `(вход × ставка входа + выход × ставка выхода) / 1 000 000`, без кеша.

| Задача и роль | Доступ, модель | Подстановка | Итог |
| --- | --- | --- | --- |
| Простые — Основной | OpenCode Go, Haiku | (2000×0.10 + 500×0.50)/1M | включено в подписку; allowance $0.00045 |
| Простые — Бюджетный | OpenRouter, Luna | (2000×0.10 + 500×0.50)/1M | $0.00045 |
| Простые — Усиленный | OpenRouter, Sonnet | (2000×2 + 500×10)/1M | $0.009 |
| Вёрстка — Основной | OpenRouter, Sonnet | (8000×2 + 2000×10)/1M | $0.036 |
| Вёрстка — Бюджетный | OpenRouter, MiniMax M3.1 Flash | (8000×0.15 + 2000×0.60)/1M | $0.0024; льготное окно $0.0012 |
| Вёрстка — Усиленный | OpenRouter, Opus | (8000×4 + 2000×20)/1M | $0.072 |
| Код — Основной | DeepSeek напрямую, Flash | peak (12000×0.30 + 3000×1.20)/1M; off-peak половина | $0.0072 / $0.0036 |
| Код — Бюджетный | OpenCode Go, GLM-5.3-Flash | (12000×0.15 + 3000×0.50)/1M | включено в подписку; allowance $0.0033 |
| Код — Усиленный | OpenRouter, Fable 5.1 | (12000×10 + 3000×50)/1M | $0.270 |
| Проекты — Основной | OpenRouter, Kimi K3.1 Pro | (50000×2 + 8000×10)/1M | $0.18 |
| Проекты — Бюджетный | OpenCode Go, GLM-5.3 | (50000×1.40 + 8000×4.40)/1M | включено в подписку; allowance $0.1052 |
| Проекты — Усиленный | OpenRouter, Opus | (50000×4 + 8000×20)/1M | $0.36 |

Сверено программой без сетевых вызовов. Один вызов не равен стоимости агентной задачи: история передаётся повторно, инструменты добавляют ходы, кеш снижает вход, reasoning и повторы увеличивают расход. Для Go: месячный лимит $15 у GLM-5.3 покрывает ~142 условных проектных вызова без кеша, но 5-часовой лимит — ~28.
