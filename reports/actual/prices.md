# Цены
Дата проверки: 11.11.2026, 11:39 МСК. Ставки — USD за 1 млн токенов.

## Выбранные пары
| Модель | Поставщик | Точный ID | Обычный вход / cache read / выход, USD/1M | Контекст | Тарифные условия | Официальный URL |
| --- | --- | --- | --- | --- | --- | --- |
| Claude Haiku 5.5 | OpenRouter | `anthropic/claude-haiku-5.5` | 0.10 / 0.01 / 0.50 | 1,000,000 | При input >=100K действует override 0.50 / 0.05 / 2.50; профиль ниже порога | https://openrouter.ai/api/v1/models |
| DeepSeek V4.1 Flash 1017 | OpenRouter | `deepseek/deepseek-v4.1-flash-1017` | 0.006 / 0.005 / 0.50 | 1,048,576 | Обычный, не batch; агрегированная цена OpenRouter не гарантирует каждый backend | https://openrouter.ai/api/v1/models |
| Claude Sonnet 5.5 | Токенатор | `claude-sonnet-5.5` | 0.432 / н/д / 0.432 | 1,000,000 | Множитель 1.6; operational=true, unstable=false; кеш н/д | https://tokenator.cloud/models |
| Claude Opus 5.5 | Токенатор | `claude-opus-5.5` | 0.513 / н/д / 0.513 | 1,000,000 | Множитель 1.9; operational=true, unstable=false; кеш н/д | https://tokenator.cloud/models |
| Claude Sonnet 5.5 | Vantyr | `claude-sonnet-5-5` | 0.15 / 0.052 / 0.48 | н/д | tiered_expr; cache write 0.09, 1h 0.144; API нестабилен по manifest | https://vantyr.xyz/api/pricing |
| GPT-6.1 Sol | Vantyr | `gpt-6-1-sol` | 0.15 / 0.01 / 0.50 | н/д | tiered_expr; cache write 0.10; API нестабилен по manifest | https://vantyr.xyz/api/pricing |

## Существенные альтернативы
| Модель | Поставщик | Точный ID | Обычный вход / cache read / выход, USD/1M | Контекст | Условия и причина невыбора | Официальный URL |
| --- | --- | --- | --- | --- | --- | --- |
| Claude Fable 5.2 | OpenRouter | `anthropic/claude-fable-5.2` | 8.00 / 0.20 / 40.00 | 1,000,000 | Внешнее сравнение не показало достаточного выигрыша над Opus для переплаты | https://openrouter.ai/api/v1/models |
| MiniMax M3.1 Flash | OpenRouter | `minimax/minimax-m3.1-flash` | peak 0.15 / 0.015 / 0.60; off-peak 0.075 / 0.0075 / 0.30 | 1,048,576 | Сильный агентный кандидат, но независимый обзор ставит его ниже DeepSeek в coding | https://openrouter.ai/api/v1/models |
| GLM-5.3 | OpenCode Go | `glm-5.3` | включено в подписку | н/д | Модель есть в списке Go; доступность на тарифе не подтверждена | https://opencode.ai/v2/docs/console/go |

## Расчёты
Формула: `(input*input_price + cache_read*cache_price + output*output_price) / 1,000,000`. Если cache read н/д, расчёт сделан без кеша и это отмечено выше.

| Профиль | Роль | Модель / поставщик | Подстановка | USD/задача |
| --- | --- | --- | --- | ---: |
| Быстрые ответы | Основной | Haiku / OpenRouter | (2000×0.10 + 500×0.50)/1M | 0.00045 |
| Быстрые ответы | Бюджетный | DeepSeek / OpenRouter | (2000×0.006 + 500×0.50)/1M | 0.000262 |
| HTML/CSS | Основной | Sonnet / Токенатор | (8000+2000)×0.432/1M | 0.00432 |
| HTML/CSS | Бюджетный | Sonnet / Vantyr | (8000×0.15 + 2000×0.48)/1M | 0.00216 |
| JS/PHP/Vue | Основной | Sonnet / Токенатор | (356000+8000)×0.432/1M; кеш н/д | 0.157248 |
| JS/PHP/Vue | Бюджетный | Sonnet / Vantyr | (356000×0.15 + 307000×0.052 + 8000×0.48)/1M | 0.073204 |
| Planning | Основной | Opus / Токенатор | (2827000+46000)×0.513/1M; кеш н/д | 1.473849 |
| Planning | Бюджетный | DeepSeek / OpenRouter | (2827000×0.006 + 1735000×0.005 + 46000×0.50)/1M | 48.637 |
| Implementation | Основной | Sonnet / Токенатор | (2827000+46000)×0.432/1M; кеш н/д | 1.241136 |
| Implementation | Бюджетный | DeepSeek / OpenRouter | (2827000×0.006 + 1735000×0.005 + 46000×0.50)/1M | 48.637 |
| Review | Основной | Opus / Токенатор | (2827000+46000)×0.513/1M; кеш н/д | 1.473849 |
| Review | Бюджетный | GPT-6.1 Sol / Vantyr | 2827000×0.15 + 1735000×0.01 + 46000×0.50, /1M | 464.400 |

Профиль — усреднённая типовая задача-сессия целиком: реальные задачи отличаются от среднего в разы, а этапы одной большой задачи считаются вместе. Подписка OpenCode Go не включена в эти расчёты: для неё корректно писать «включено в подписку», а доступность на тарифе не подтверждена.
