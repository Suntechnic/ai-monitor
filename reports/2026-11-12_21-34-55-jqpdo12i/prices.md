# Цены
Дата проверки: 12.11.2026. Цены в USD за 1 млн токенов, если не указано иное; локальные summary и pricing_notes manifest — основа тарифных данных.

## Выбранные пары

| Модель | Поставщик | Точный ID | Обычный вход / cache read / выход, USD/1M | Контекст | Тарифные условия | Официальный URL |
| --- | --- | --- | --- | --- | --- | --- |
| GPT-6.1 Sol | Vantyr | `gpt-6-1-sol` | 0.15 / 0.01 / 0.50 | н/д | Тариф Vantyr из summary; unstable API отмечен manifest | https://vantyr.xyz/api/pricing |
| Claude Fable 5.2 | Vantyr | `claude-fable-5-2` | 1.25 / 0.10 / 6.00 | н/д | Тариф Vantyr; нестабильная доступность | https://vantyr.xyz/api/pricing |
| DeepSeek V4.1 Flash 1017 | DeepSeek напрямую | `deepseek-flash` | peak 0.006 / 0.003 / 0.028; off-peak 0.003 / 0.0015 / 0.014 | 1,000,000 | Peak пн–пт 01–04 и 06–10 UTC, кроме китайских праздников; tool calls, vision, max output 384K | https://api-docs.deepseek.com/quick_start/pricing/ |
| Claude Haiku 5.5 | OpenRouter | `anthropic/claude-haiku-5.5` | 0.10 / 0.01 / 0.50 | 1,000,000 | prompt профиля ниже 100K; агрегированная цена не гарантирует каждый backend | https://openrouter.ai/api/v1/models |

## Существенные альтернативы

| Модель | Поставщик | Точный ID | Обычный вход / cache read / выход, USD/1M | Контекст | Условия и причина невыбора | Официальный URL |
| --- | --- | --- | --- | --- | --- | --- |
| GPT-6.1 Sol | OpenRouter | `openai/gpt-6.1-sol` | 2.00 / 0.10 / 10.00; при prompt ≥272K: 4.00 / 0.20 / 15.00 | 1,050,000 | Агрегированный маршрут; высокий tier применим к профилям с input выше 272K | https://openrouter.ai/api/v1/models |
| Claude Fable 5.2 | OpenRouter | `anthropic/claude-fable-5.2` | 8.00 / 0.20 / 40.00 | 1,000,000 | Дороже Vantyr; batch-цена не использована, потому что обычная интерактивная сессия | https://openrouter.ai/api/v1/models |
| DeepSeek V4.1 Flash 1017 | OpenRouter | `deepseek/deepseek-v4.1-flash-1017` | off-peak 0.15 / 0.003 / 0.60; peak 0.30 / 0.006 / 1.20 | 1,048,576 | Временные override из снимка; дороже прямого API, агрегированная цена не гарантирует backend | https://openrouter.ai/api/v1/models |
| DeepSeek V4.1 Flash 1017 | BazaarLink | `deepseek-v4.1-flash-1017` | 0.21225 / 0.021 / 0.84825 | 1,048,576 | Тариф продавца, не official; кэшированное чтение существенно дороже прямого тарифа | https://bazaarlink.ai/api/v1/models |
| Claude Haiku 5.5 | Токенатор | `claude-haiku-5.5` | 0.297 / н/д / 0.297 | 1,000,000 | Кеш не подтверждён, стоимость без кеша; общий множитель input/output по pricing_notes | https://tokenator.cloud/models |
| Claude Haiku 5.5 | OpenCode Go | `claude-haiku-5-5` | включено в подписку | н/д | Go $10/мес, Go Plus $40/мес; для каждой модели лимит 5h=20%, week=50%, month=100% от model limit. Haiku limit $60/month; тариф пользователя не подтверждён | https://opencode.ai/v2/docs/console/go |

## Расчёты

Формула: `(input × ставка_input + cache_read × ставка_cache + output × ставка_output) / 1,000,000`. Диапазон DeepSeek: off-peak / peak. Все входы взяты из профиля, без переноса токенов из прежнего отчёта.

| Профиль | Роль | Модель / поставщик | Подстановка | USD/задача |
| --- | --- | --- | --- | ---: |
| Администрирование серверов | Основной | GPT-6.1 Sol / Vantyr | `(730407×.15 + 2164960×.01 + 29762×.5)/1M` | 0.1461 |
| Администрирование серверов | Бюджетный | DeepSeek / DeepSeek напрямую | `(730407×in + 2164960×cache + 29762×out)/1M` | 0.0059 / 0.0117 |
| AI-разработка | Основной | GPT-6.1 Sol / Vantyr | `(1410431×.15 + 2370387×.01 + 41092×.5)/1M` | 0.2558 |
| AI-разработка | Бюджетный | DeepSeek / DeepSeek напрямую | `(1410431×in + 2370387×cache + 41092×out)/1M` | 0.0084 / 0.0167 |
| Мониторинг | Основной | GPT-6.1 Sol / Vantyr | `(1064477×.15 + 89270×.01 + 16662×.5)/1M` | 0.1689 |
| Мониторинг | Бюджетный | DeepSeek / DeepSeek напрямую | `(1064477×in + 89270×cache + 16662×out)/1M` | 0.0038 / 0.0076 |
| Скрипты и автоматизация | Основной | Claude Fable 5.2 / Vantyr | `(1154284×1.25 + 3944616×.1 + 34670×6)/1M` | 0.7768 |
| Скрипты и автоматизация | Бюджетный | DeepSeek / DeepSeek напрямую | `(1154284×in + 3944616×cache + 34670×out)/1M` | 0.0099 / 0.0197 |
| Быстрые простые ответы | Основной | Claude Haiku 5.5 / OpenRouter | `(71122×.1 + 38418×.01 + 1954×.5)/1M` | 0.0085 |
| Быстрые простые ответы | Бюджетный | DeepSeek / DeepSeek напрямую | `(71122×in + 38418×cache + 1954×out)/1M` | 0.0003 / 0.0006 |
| Реализация этапа по плану | Основной | Claude Fable 5.2 / Vantyr | `(232782×1.25 + 3927520×.1 + 32802×6)/1M` | 0.8805 |
| Реализация этапа по плану | Бюджетный | DeepSeek / DeepSeek напрямую | `(232782×in + 3927520×cache + 32802×out)/1M` | 0.0526 / 0.1052 |
| Планирование этапа задачи | Основной | Claude Fable 5.2 / Vantyr | `(287634×1.25 + 1247787×.1 + 14733×6)/1M` | 0.5727 |
| Планирование этапа задачи | Бюджетный | DeepSeek / DeepSeek напрямую | `(287634×in + 1247787×cache + 14733×out)/1M` | 0.0031 / 0.0062 |
| Ревью задачи | Основной | Claude Fable 5.2 / Vantyr | `(722789×1.25 + 419354×.1 + 9992×6)/1M` | 1.0054 |
| Ревью задачи | Бюджетный | DeepSeek / DeepSeek напрямую | `(722789×in + 419354×cache + 9992×out)/1M` | 0.0035 / 0.0070 |

## Сравнение цен по моделям

Сценарий сравнения для каждой модели — администрирование серверов (`730407` input, `2164960` cache read, `29762` output); это одинаковая база для всех продавцов данной модели. Условная сессия целиком: реальные задачи отличаются от среднего в разы, а этапы одной большой задачи считаются вместе.

### GPT-6.1 Sol

| Поставщик | Точный API ID | Вход / cache read / выход, USD/1M | $/задача | Особенности |
| --- | --- | --- | ---: | --- |
| Vantyr | `gpt-6-1-sol` | 0.15 / 0.01 / 0.50 | 0.146 | Самый дешёвый из этих маршрутов; manifest отмечает нестабильность API |
| OpenRouter | `openai/gpt-6.1-sol` | 2.00 / 0.10 / 10.00 | 2.295 | Агрегированный backend; tier меняется при input ≥272K, данный профиль ниже порога |

Использование: `vantyr/gpt-6-1-sol` — 14 сессий, week 14, month 14. Vantyr заметно дешевле, но устойчивость ниже не подтверждена.

### Claude Fable 5.2

| Поставщик | Точный API ID | Вход / cache read / выход, USD/1M | $/задача | Особенности |
| --- | --- | --- | ---: | --- |
| Vantyr | `claude-fable-5-2` | 1.25 / 0.10 / 6.00 | 1.223 | Нестабильность API; цены summary продавца |
| OpenRouter | `anthropic/claude-fable-5.2` | 8.00 / 0.20 / 40.00 | 7.393 | Агрегированный маршрут; cache write не входит в сценарий |

Для одинакового профиля Vantyr существенно дешевле. AA 64.6 относится к версии Fable 5.2 в снимке, а не к продавцу или отдельному кодинг-тесту.

### DeepSeek V4.1 Flash 1017

| Поставщик | Точный API ID | Вход / cache read / выход, USD/1M | $/задача | Особенности |
| --- | --- | --- | ---: | --- |
| DeepSeek напрямую | `deepseek-flash` | off-peak 0.003 / 0.0015 / 0.014; peak 0.006 / 0.003 / 0.028 | 0.0059 / 0.0117 | Официальные временные ставки, tool calls, контекст 1M |
| OpenRouter | `deepseek/deepseek-v4.1-flash-1017` | off-peak 0.15 / 0.003 / 0.60; peak 0.30 / 0.006 / 1.20 | 1.319 / 2.638 | Временные override из снимка; агрегированная цена и backend могут различаться |
| BazaarLink | `deepseek-v4.1-flash-1017` | 0.21225 / 0.021 / 0.84825 | 0.210 | Тариф продавца, не официальный тариф DeepSeek |

Использование: `deepseek/deepseek-flash` — 8 сессий, week 8, month 8. Прямой маршрут дешевле; агрегированные значения показывают цену маршрута, а не гарантированную стоимость каждого backend.

### Claude Haiku 5.5

| Поставщик | Точный API ID | Вход / cache read / выход, USD/1M | $/задача | Особенности |
| --- | --- | --- | ---: | --- |
| OpenRouter | `anthropic/claude-haiku-5.5` | 0.10 / 0.01 / 0.50 | 0.0085 | Prompt ниже 100K tier; cache read есть |
| Токенатор | `claude-haiku-5.5` | 0.297 / н/д / 0.297 | 0.0221 | Кеш неизвестен, расчёт без cache_read |
| OpenCode Go | `claude-haiku-5-5` | включено в подписку | н/д | Go $10/mo; model monthly limit $60, 5h 20%, weekly 50%; доступность на тарифе не подтверждена |

Для измеряемой token-cost сессии OpenRouter дешевле; Go включает usage в платную подписку с квотами, поэтому его нельзя считать бесплатным или приравнять к цене вызова.

Использование: `opencode-go/claude-haiku-5-5` — 2 сессии, week 2, month 2; `opencode-go/deepseek-v4.1-flash` — 5 сессий, week 5, month 5; `openrouter/openai/gpt-6-luna` — 1 сессия, week 1, month 1; `opencode-go/kimi-k3.1-pro` — 6 сессий, week 5, month 6.

Недостаточно данных для сравнения: `freellmapi/auto` — неоднозначный ID; `ollama/qwen3:14b` — локальная модель; `tokenator/free-claude-opus-5.5`, `tokenator/free-gemini-4-argon`, `tokenator/free-gemini-4-carbon`, `tokenator/free-glm-5.3-flash`, `tokenator/free-gpt-6-astra`, `opencode/beam-free`, `opencode-go/beam-free`, `opencode-go/deepseek-v4.1-flash-free`, `opencode-go/glm-5.3-flash-free`, `opencode-go/longcat-2.5-preview-free` — бесплатные маршруты исключены; `timeweb/anthropic/claude-opus-5-5`, `timeweb/anthropic/claude-sonnet-5-5`, `timeweb/anthropic/claude-haiku-5-5` — тарифы этих продавцов отсутствуют в доступных ценовых снимках; `tokenator/hy4` — подтверждён только один сопоставимый тариф.
