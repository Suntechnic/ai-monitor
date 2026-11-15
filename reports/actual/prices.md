# Цены
Дата проверки: 15.11.2026. Ставки в USD за 1 млн токенов; локальные summary и pricing_notes manifest — основа тарифов.

## Выбранные пары

| Модель | Поставщик | Точный ID | Обычный вход / cache read / выход, USD/1M | Контекст | Тарифные условия | Официальный URL |
| --- | --- | --- | --- | --- | --- | --- |
| Claude Fable 5.2 | Vantyr | `claude-fable-5-2` | 1.25 / 0.10 / 6.00 | 1,000,000 | Фиксированные ставки input/output из summary продавца; нестабильная доступность отмечена manifest | https://vantyr.xyz/api/pricing |
| DeepSeek V4.1 Flash 1017 | DeepSeek напрямую | `deepseek-flash` | peak 0.006 / 0.003 / 0.028; off-peak 0.003 / 0.0015 / 0.014 | 1,000,000 | Peak пн–пт 01–04 и 06–10 UTC, кроме китайских праздников; tool calls, max output 384K | https://api-docs.deepseek.com/quick_start/pricing/ |
| Claude Haiku 5.5 | OpenRouter | `anthropic/claude-haiku-5.5` | 0.10 / 0.01 / 0.50 | 1,000,000 | Цена входа действует для prompt <100K; при более длинном prompt тариф выше; агрегированный backend | https://openrouter.ai/api/v1/models |

## Существенные альтернативы

| Модель | Поставщик | Точный ID | Обычный вход / cache read / выход, USD/1M | Контекст | Условия и причина невыбора | Официальный URL |
| --- | --- | --- | --- | --- | --- | --- |
| Claude Fable 5.2 | OpenRouter | `anthropic/claude-fable-5.2` | 8.00 / 0.20 / 40.00 | 1,000,000 | Агрегированный маршрут; обычный тариф, не batch; дороже Vantyr | https://openrouter.ai/api/v1/models |
| Claude Fable 5.2 | BazaarLink | `claude-fable-5.2` | 8.00 / 0.20 / 40.00 | 1,000,000 | Тариф продавца; дороже Vantyr | https://bazaarlink.ai/api/v1/models |
| Claude Fable 5.2 | Токенатор | `claude-fable-5.2` | 3.24–6.48 / н/д / 3.24–6.48 | 1,000,000 | Общая ставка input/output по multiplier; cache read не подтверждён, стоимость без кеша | https://tokenator.cloud/models |
| DeepSeek V4.1 Flash 1017 | OpenRouter | `deepseek/deepseek-v4.1-flash-1017` | 0.020 / 0.007 / 0.108 | 1,048,576 | Ставки агрегированного маршрута; дешевле прямого API в этом snapshot, но backend не гарантирован | https://openrouter.ai/api/v1/models |
| DeepSeek V4.1 Flash 1017 | BazaarLink | `deepseek-v4.1-flash-1017` | 0.21225 / 0.021 / 0.84825 | 1,048,576 | Цена продавца, а не DeepSeek; значительно дороже прямого API | https://bazaarlink.ai/api/v1/models |
| Claude Haiku 5.5 | Токенатор | `claude-haiku-5.5` | 0.297 / н/д / 0.297 | 1,000,000 | Общая ставка input/output; cache неизвестен, цена задачи посчитана без cache_read | https://tokenator.cloud/models |
| Claude Haiku 5.5 | OpenCode Go | `claude-haiku-5-5` | включено в подписку | н/д | Go $10/мес, Go Plus $40/мес; модельный лимит $60/мес, 5h=20%, week=50%; доступность на тарифе пользователя не подтверждена | https://opencode.ai/v2/docs/console/go |

## Расчёты

Формула: `(input × ставка_input + cache_read × ставка_cache + output × ставка_output) / 1,000,000`. Для Fable через Vantyr применены ставки summary 1.25/0.10/6.00; DeepSeek дан как off-peak / peak. Для сравнения Vantyr с другими поставщиками Fable Tokenator посчитан без cache read. Задача — усреднённая типовая сессия: реальные задачи отличаются от среднего в разы, а этапы одной большой задачи считаются вместе.

| Профиль | Роль | Модель / поставщик | Подстановка | USD/задача |
| --- | --- | --- | --- | ---: |
| Администрирование серверов | Основной | Claude Fable 5.2 / Vantyr | `(730407×1.25 + 2164960×.10 + 29762×6)/1M` | 1.308 |
| Администрирование серверов | Бюджетный | DeepSeek / DeepSeek напрямую | `(730407×in + 2164960×cache + 29762×out)/1M` | 0.0059 / 0.0117 |
| AI-разработка | Основной | Claude Fable 5.2 / Vantyr | `(1410431×1.25 + 2370387×.10 + 41092×6)/1M` | 2.247 |
| AI-разработка | Бюджетный | DeepSeek / DeepSeek напрямую | `(1410431×in + 2370387×cache + 41092×out)/1M` | 0.0084 / 0.0167 |
| Мониторинг | Основной | Claude Fable 5.2 / Vantyr | `(1064477×1.25 + 89270×.10 + 16662×6)/1M` | 1.439 |
| Мониторинг | Бюджетный | DeepSeek / DeepSeek напрямую | `(1064477×in + 89270×cache + 16662×out)/1M` | 0.0036 / 0.0071 |
| Скрипты и автоматизация | Основной | Claude Fable 5.2 / Vantyr | `(1154284×1.25 + 3944616×.10 + 34670×6)/1M` | 2.045 |
| Скрипты и автоматизация | Бюджетный | DeepSeek / DeepSeek напрямую | `(1154284×in + 3944616×cache + 34670×out)/1M` | 0.0099 / 0.0197 |
| Быстрые простые ответы | Основной | Claude Haiku 5.5 / OpenRouter | `(71122×.10 + 38418×.01 + 1954×.50)/1M` | 0.0085 |
| Быстрые простые ответы | Бюджетный | DeepSeek / DeepSeek напрямую | `(71122×in + 38418×cache + 1954×out)/1M` | 0.0003 / 0.0006 |
| Реализация этапа по плану | Основной | Claude Fable 5.2 / Vantyr | `(232782×1.25 + 3927520×.10 + 32802×6)/1M` | 0.881 |
| Реализация этапа по плану | Бюджетный | DeepSeek / DeepSeek напрямую | `(232782×in + 3927520×cache + 32802×out)/1M` | 0.0070 / 0.0141 |
| Планирование этапа задачи | Основной | Claude Fable 5.2 / Vantyr | `(287634×1.25 + 1247787×.10 + 14733×6)/1M` | 0.573 |
| Планирование этапа задачи | Бюджетный | DeepSeek / DeepSeek напрямую | `(287634×in + 1247787×cache + 14733×out)/1M` | 0.0029 / 0.0059 |
| Ревью задачи | Основной | Claude Fable 5.2 / Vantyr | `(722789×1.25 + 419354×.10 + 9992×6)/1M` | 1.005 |
| Ревью задачи | Бюджетный | DeepSeek / DeepSeek напрямую | `(722789×in + 419354×cache + 9992×out)/1M` | 0.0029 / 0.0059 |

## Сравнение цен по моделям

Для всех таблиц сравнения выбран профиль «Администрирование серверов»: 730407 input, 2164960 cache read, 29762 output. Условия и ID продавцов указаны отдельно; агрегированный OpenRouter не гарантирует указанные цены каждому backend.

### Claude Fable 5.2

| Поставщик | Точный API ID | Вход / cache read / выход, USD/1M | $/задача | Особенности |
| --- | --- | --- | ---: | --- |
| Vantyr | `claude-fable-5-2` | 1.25 / 0.10 / 6.00 | 1.308 | Нестабильность API; ставки summary продавца |
| Токенатор | `claude-fable-5.2` | 3.24–6.48 / н/д / 3.24–6.48 | 2.463–4.926 без кеша | Cache read не известен; общая ставка input/output |
| OpenRouter | `anthropic/claude-fable-5.2` | 8.00 / 0.20 / 40.00 | 7.467 | Агрегированный API; обычный тариф |
| BazaarLink | `claude-fable-5.2` | 8.00 / 0.20 / 40.00 | 7.467 | Тариф продавца, не official тариф разработчика |

По snapshot Vantyr дешевле, но риск доступности требует резервного канала. У Токенатора цена не включает cache read, а у OpenRouter и BazaarLink тарифы заметно выше при том же типовом сценарии.

Использование: `vantyr/claude-opus-5-5` — 7 сессий, week 7, month 7; это другая модель, не переносить использование на Fable 5.2.

### DeepSeek V4.1 Flash 1017

| Поставщик | Точный API ID | Вход / cache read / выход, USD/1M | $/задача | Особенности |
| --- | --- | --- | ---: | --- |
| OpenRouter | `deepseek/deepseek-v4.1-flash-1017` | 0.020 / 0.007 / 0.108 | 0.033 | Агрегированный маршрут; цена из snapshot |
| DeepSeek напрямую | `deepseek-flash` | off-peak 0.003 / 0.0015 / 0.014; peak 0.006 / 0.003 / 0.028 | 0.0059 / 0.0117 | Официальные временные ставки; tool calls, контекст 1M |
| BazaarLink | `deepseek-v4.1-flash-1017` | 0.21225 / 0.021 / 0.84825 | 0.226 | Кеш есть, но тариф продавца существенно выше прямого API |

Прямой API самый дешёвый для этого типового сценария; OpenRouter дороже примерно в 2.8 раза, а BazaarLink — примерно в 19 раз. Для отдельного точного Snapshot 1017 прямой API обслуживает это имя через текущий `deepseek-flash`.

Использование: `deepseek/deepseek-flash` — 10 сессий, week 8, month 10; `opencode-go/deepseek-v4.1-flash` — 5 сессий, week 5, month 5.

### Claude Haiku 5.5

| Поставщик | Точный API ID | Вход / cache read / выход, USD/1M | $/задача | Особенности |
| --- | --- | --- | ---: | --- |
| OpenRouter | `anthropic/claude-haiku-5.5` | 0.10 / 0.01 / 0.50 | 0.0085 | Prompt меньше 100K; выше действует тарифный override |
| Токенатор | `claude-haiku-5.5` | 0.297 / н/д / 0.297 | 0.226 без кеша | Cache read не подтверждён |
| OpenCode Go | `claude-haiku-5-5` | включено в подписку | н/д | Лимиты 5h/week/month; тариф пользователя неизвестен |

OpenRouter дешевле среди маршрутов с вычислимой оплатой за токены и подтверждённым cache read. Go — включённая услуга подписки с квотами, а не бесплатный вызов.

Использование: `opencode-go/claude-haiku-5-5` — 2 сессии, week 0, month 2; `timeweb/anthropic/claude-haiku-5-5` — 45 сессий, week 24, month 43.

### GPT-6.1 Sol

| Поставщик | Точный API ID | Вход / cache read / выход, USD/1M | $/задача | Особенности |
| --- | --- | --- | ---: | --- |
| Vantyr | `gpt-6-1-sol` | 0.15 / 0.010 / 0.50 | 0.146 | Нестабильный API; тариф summary |
| OpenRouter | `openai/gpt-6.1-sol` | 2.00 / 0.10 / 10.00 | 1.975 | Агрегированный маршрут; профиль ниже порога 272K input |

Vantyr дешевле, но ниже по надёжности; OpenRouter — более дорогой резервный маршрут. Модель не выбрана основной в текущих профилях, поскольку Fable 5.2 имеет более высокий AA Index.

Использование: `vantyr/gpt-6-1-sol` — 15 сессий, week 15, month 15; `timeweb/openai/gpt-6.1-sol` — 1 сессия, week 1, month 1.

### Kimi K3.1 Pro

| Поставщик | Точный API ID | Вход / cache read / выход, USD/1M | $/задача | Особенности |
| --- | --- | --- | ---: | --- |
| OpenRouter | `moonshotai/kimi-k3.1-pro` | 0.2403 / 0.20 / 8.4023 | 0.859 | Агрегированный API, cache read подтверждён |
| Vantyr | `kimi-k3.1-pro` | 0.25 / 0.03 / 0.85 | 0.273 | Нестабильность Vantyr; тариф summary |
| OpenCode Go | `kimi-k3.1-pro` | включено в подписку | н/д | Go: модельный лимит $15/мес; 5h 20%, week 50%; тариф пользователя не подтверждён |

Vantyr дешевле для заданного сценария, но с риском доступности. У OpenCode Go оплата считается в рамках платной подписки и ограничена модельной квотой.

Использование: `opencode-go/kimi-k3.1-pro` — 6 сессий, week 5, month 6.

## Недостаточно данных для сравнения

- `freellmapi/auto` — неоднозначный ID.
- `ollama/qwen3:14b` — локальная модель.
- `tokenator/free-claude-opus-5.5`, `tokenator/free-gemini-4-argon`, `tokenator/free-gemini-4-carbon`, `tokenator/free-glm-5.3-flash`, `tokenator/free-gpt-6-astra`, `opencode/beam-free`, `opencode-go/beam-free`, `opencode-go/deepseek-v4.1-flash-free`, `opencode-go/glm-5.3-flash-free`, `opencode-go/longcat-2.5-preview-free` — бесплатные маршруты исключены.
- `timeweb/anthropic/claude-opus-5-5`, `timeweb/anthropic/claude-sonnet-5-5`, `timeweb/anthropic/claude-haiku-5-5` — цены Timeweb отсутствуют в доступных ценовых снимках.
- `tokenator/hy4` — подтверждён только один сопоставимый тариф; `openrouter/openai/gpt-6-luna` — в доступных снимках нет второго сопоставимого платного маршрута.
