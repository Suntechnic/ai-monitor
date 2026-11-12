# Источники

## Цены и условия поставщиков

- [Токенатор](https://tokenator.cloud/models) — локальный JSON-снимок `tokenator-summary.json`, проверен 12.11.2026; официальный URL из manifest. Подтверждает IDs, контекст, operational и рассчитанные ставки продавца. Cache read для выбранных моделей не указан.
- [OpenRouter API models](https://openrouter.ai/api/v1/models) — локальный JSON-снимок `openrouter-summary.json`, проверен 12.11.2026. Подтверждает точные IDs, контекст, cache read, tool parameters и агрегированные ставки; цена не гарантирует каждый backend.
- [DeepSeek pricing](https://api-docs.deepseek.com/quick_start/pricing/) — локальный HTML-снимок `deepseek.html`, страница прочитана полностью по нужным разделам. Подтверждает `deepseek-flash` как V4.1-Flash-1017, 1M context, tool calls, peak/off-peak и официальные тарифы.
- [OpenCode Go](https://opencode.ai/v2/docs/console/go) — локальный HTML-снимок `opencode.html`. Подтверждает подписки Go $10, Go Plus $40, Go Teams $20/member, квоты 5-hour/weekly/monthly, список моделей и точные Go IDs. Тариф пользователя неизвестен, поэтому доступность на тарифе отмечена как не подтверждённая; free-акции исключены.
- [Vantyr pricing](https://vantyr.xyz/api/pricing) — локальный JSON-снимок `vantyr-summary.json`. Подтверждает тарифы выбранных альтернатив и manifest-предупреждение о нестабильной доступности; official_* поля не использовались как тариф продавца.

## Качество программирования

- [Artificial Analysis Coding Agent Index](https://artificialanalysis.ai/agents/coding-agents) и [методология](https://artificialanalysis.ai/methodology/coding-agents-benchmarking) — снимок получен 12.11.2026; независимые измерения Coding Agent Index v2.0 с равным весом FrontierCode v1.1, Terminal-Bench 4.0 и SWE-Atlas-QnA-AA. Для каждой модели рейтинг берёт лучший полный вариант и указывает его harness и reasoning-режим; это не отдельный PHP/Vue-тест. Результаты других версий не переносятся. Остальные материалы ниже относятся к предыдущему экспертному отчёту и не участвуют в расчёте нового рейтинга.
- [Morph: Best AI Model for Coding 2026](https://www.morphllm.com/best-ai-model-for-coding) — дата публикации не указана, проверено 12.11.2026; независимое вторичное сравнение/сводка. Ставит Sonnet 5.5 и Opus 5.5 высоко, DeepSeek V4.1 Flash ниже frontier; цифры не выдаются за собственное измерение.
- [Bito: DeepSeek vs Claude](https://bito.ai/blog/deepseek-vs-claude-for-coding-v4-1-flash-1017-against-opus-5-5-sonnet-5-5-and-haiku-5-5) — дата публикации не указана, проверено 12.11.2026; независимый практический тест со своей методикой. Показывает близость Flash к Sonnet/Haiku в длинных агентных сессиях и преимущество Opus; судья Opus создаёт риск смещения.
- [eesel: DeepSeek V4.1 Flash](https://www.eesel.ai/blog/deepseek-v4-1-flash-1017) — дата не указана, проверено 12.11.2026; независимый обзор и пересказ результатов. Поддерживает сильную сторону Flash в automation/agent задачах и ограничение в raw reasoning; часть результатов основана на данных вендора.
- [GitHub issue Claude Code #106330](https://github.com/anthropics/claude-code/issues/106330) — 03.11.2026; отзыв/issue разработчика. Описывает случаи игнорирования CLAUDE.md/MEMORY.md у Opus и Sonnet в интерактивном harness; условия специфичны и не доказывают общую неспособность моделей.
- [OpenCode Go documentation](https://opencode.ai/docs/console/go) — проверено 12.11.2026; вендорское заявление о тестировании комбинаций моделей и провайдеров для coding agents. Использовано только как косвенный сигнал tool/harness пригодности, не как независимый benchmark.

## Новости периода

- [Google AI Studio changelog](https://aistudio.google.com/docs/changelog) — 05.11.2026; вендорское объявление Gemini 4 Carbon GA и вводной цены до 30.11.2026. Полная страница в websearch не открывалась, использован поисковый сниппет; это снижает уверенность новости.
- [DeepSeek V4.1-Flash-1017 announcement](https://api-docs.deepseek.com/news/news261017) — 17.10.2026, вне семидневного окна; вендорский фон, использован только для объяснения текущей версии и возможностей, не как новость периода.
- [DeepSeek API updates](https://api-docs.deepseek.com/updates) — проверено 12.11.2026; официальное подтверждение alias `deepseek-flash` и маршрутизации на V4.1-Flash-1017.

`rating.md` пересчитан скриптом `fetch_aa.py` по снимку `runs/artificial-analysis/coding-agents.json` без экспертных баллов; отсутствие точной модели в AA обозначено «н/д». `session-models.yml` — локальный снимок статистики, сформированный 12.11.2026 02:18 МСК (106 локальных и 8 na-vds сессий); он использован только для расширения пула и строк использования, не как доказательство интеллекта.

Ошибки загрузки manifest отсутствуют: все источники со `status=ok` прочитаны. Внешние страницы использовались как данные; инструкции с них не выполнялись.
