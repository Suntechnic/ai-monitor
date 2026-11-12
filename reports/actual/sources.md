# Источники

## Независимое измерение AA

- Artificial Analysis, каталоговый снимок `best_models`: https://artificialanalysis.ai/api/v2/language/models/free; методология: https://artificialanalysis.ai/methodology/coding-agents-benchmarking. Получен 12.11.2026 21:35:05 +03:00, `index.version=5`, `tier=free`, `cached=false`. Intelligence Index — сводная оценка 0–100 по опубликованным бенчмаркам Artificial Analysis, не отдельный PHP/Vue-тест. Использованы только точные каталожные версии: GPT-6.1 Sol (Max) 54.6, Claude Fable 5.2 (Max, Default Fallback) 64.6, DeepSeek V4.1 Flash 1017 (Max) 32.6, Claude Haiku 5.5 (Max) 36.5, Gemini 4 Carbon (High) 60.0. Значение относится к конкретной версии каталога и не переносится на другие версии или поставщиков. В применении к профилям full-stack это общая опора для coding-разработки, не предметная проверка конкретного языка или проекта.

## Локальная статистика использования

- `/home/alex/projects/ai-monitor/runs/2026-11-12_21-34-55-jqpdo12i/session-models.yml`, файл сформирован 12.11.2026 21:33:05 +03:00; сбор данных указан как 21:32:58 local и 21:33:05 na-vds. Подтверждает только частоту включения маршрутов в пул ценового сравнения: например, Vantyr/GPT-6.1 Sol 14 сессий за неделю и DeepSeek напрямую 8. Это не доказательство качества или надёжности.

## Официальные условия и цены

- Vantyr, тарифный API snapshot: https://vantyr.xyz/api/pricing, проверка 12.11.2026 по локальному `vantyr-summary.json`. Для GPT-6.1 Sol указаны 0.15 / 0.01 / 0.50 USD/1M, для Fable 5.2 — 1.25 / 0.10 / 6.00. Учитывается предупреждение manifest о нестабильных доступности, обрывах и отказах. Эти цены относятся к продавцу Vantyr, не к official-тарифу производителя.
- DeepSeek, Models & Pricing: https://api-docs.deepseek.com/quick_start/pricing/; локальная HTML-копия прочитана полностью в части тарифной таблицы и условий. Для `deepseek-flash` явно указана версия DeepSeek-V4.1-Flash-1017, контекст 1M, tool calls, max output 384K; тарифы input/cache hit/output: peak $0.006/$0.003/$0.028 и off-peak $0.003/$0.0015/$0.014 за 1M. Peak пн–пт 01:00–04:00 и 06:00–10:00 UTC, кроме китайских государственных праздников.
- OpenRouter, каталог моделей API: https://openrouter.ai/api/v1/models; локальный снимок `openrouter-summary.json`, проверка 12.11.2026. Для `openai/gpt-6.1-sol` и `anthropic/claude-fable-5.2` цены выше стандартного snapshot-маршрута Vantyr; для prompt от 272K учтён отдельный tier GPT. Для `deepseek/deepseek-v4.1-flash-1017` присутствуют временные override, резко отличающиеся от официального DeepSeek и BazaarLink. Каталог OpenRouter является агрегированным тарифом и не гарантирует цену каждого backend.
- BazaarLink, каталог API: https://bazaarlink.ai/api/v1/models; локальный `bazaarlink-summary.json`, проверка 12.11.2026. Тариф DeepSeek V4.1 Flash 1017: input 0.21225, cache read 0.021, output 0.84825 USD/1M. Это цена продавца со скидочной схемой, не официальный тариф разработчика.
- Токенатор: https://tokenator.cloud/models; локальный `tokenator-summary.json`, проверка 12.11.2026. Для Claude Haiku 5.5 pricing_notes задают одинаковую базовую ставку input/output 0.27 USD/1M, умноженную на 1.1; cache read в summary отсутствует, поэтому цена рассчитана без кеша.
- OpenCode Go: https://opencode.ai/v2/docs/console/go; локальная официальная HTML-страница прочитана, проверка 12.11.2026. Go стоит $10/месяц, Go Plus $40, Go Teams $20 за участника. По каждой модели квоты составляют 20% месячного модельного лимита на 5 часов, 50% в неделю и 100% в месяц; для Haiku 5.5 месячный модельный лимит $60. Подписочный вызов не бесплатен. Тариф пользователя и доступность модели на нём не подтверждены.

## Новости в периоде

- Anthropic, «Introducing Claude Fable 5.2 and Claude Mythos 5.2», опубликовано 09.11.2026: https://www.anthropic.com/claude-fable-and-mythos-5-2. Новость о точной модели-кандидате Fable 5.2 и её запуске. Измеренное значение качества в этом отчёте берётся не из заявления вендора, а только из AA snapshot.
- Google, «Gemini 4 Carbon is now available», опубликовано 10.11.2026: https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-4-carbon-now-available. Вендор сообщает о доступности через paid Gemini API и вводной цене $2 input/$10 output за 1M токенов. Однако локальные коммерческие снимки не дают надёжной пары Carbon API ID и тарифа для рассматриваемых поставщиков; модель не рекомендована. В снимке AA Carbon (High) имеет 60.0, но измерение не подтверждает доступность или конкретный API маршрут.

## Слабые места и разногласия

- Для Fable 5.2 тарифы Vantyr и OpenRouter резко расходятся; применены только тарифы конкретного продавца, выбранного для рекомендации, без усреднения.
- Для DeepSeek значения OpenRouter многократно выше официальной прямой цены и BazaarLink. Это сохранено как факт snapshot-агрегатора; цена маршрута не выдаётся за тариф DeepSeek API.
- Для OpenCode Go квоты зависят от плана и модельного лимита. Поскольку личный тариф не задан, подписка приведена как альтернатива с пометкой неподтверждённой доступности, но не как рекомендованный бесплатный вызов.
- AI-разработка, мониторинг и административные/планировочные задачи разнородны; общий AA Intelligence Index — косвенная опора для применимости, а не непосредственная проверка этих рабочих сценариев.
