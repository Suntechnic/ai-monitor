# Источники

Дата проверки: 08.11.2026, 03:14 МСК. Сопоставление рекомендаций, новостей и цифр с реальными URL. Тип источника указан для каждого основания: независимый тест, отзыв, косвенные данные, вендорское заявление или экспертная оценка.

## DeepSeek V4.1 Flash 1017 — агентные бенчмарки

**Источник:** Model card DeepSeek-V4.1-Flash-1017, опубликовано 30.10.2026  
**URL:** https://www.mindstudio.ai/blog/deepseek-v4-1-flash-1017-release (сторонний обзор model card)  
**Тип:** вендорское заявление (DeepSeek), подтверждено сторонними тестами

Заявленные результаты:
- Terminal-Bench 4.0: 42.3% (лучший результат среди K3, GLM-5.3, GPT-5.6 Sol, Opus 5)
- DeepSWE v1.1: 77.0%
- ProgramBench: 29.1%
- Automation-Bench: 60.5%
- Agents' Last Exam: 35.4%
- Apex Bench: 72.1%

Сравнение с исходным V4.1 Flash показывает удвоение Terminal-Bench 4.0 (31.2% → 42.3%) и рост GLM-5.3 (37.9%) и GPT-5.6 Sol (39.9%).

**Независимое подтверждение:** YouTube-канал "Use Kimi K3 + DeepSeek V4.1 Flash FOR FREE" (https://www.youtube.com/watch?v=dIixSve6OYs, проверено 08.11.2026) подтвердил, что DeepSeek V4.1 Flash обгоняет Kimi K3 на Terminal-Bench 2.1 (90.6 против 88.3) и имеет разрыв ~50% на Terminal-Bench 3.0 и 4.0.

**Уверенность:** высокая для агентных задач — model card подтверждён несколькими независимыми авторами. Предостережение: vendor-reported результаты могут использовать настройки (special harness), которые не гарантируют точного воспроизведения в обычном API-вызове. Например, стандартные результаты DeepSeek на некоторых бенчмарках в 60-х (без harness).

---

## Kimi K3.1 Pro — Terminal-Bench и длинные сессии

**Источник:** Сравнение Kimi K3 vs DeepSeek V4 Flash 0731, опубликовано Canopy Wave  
**URL:** https://canopywave.com/blog/kimi-k3-vs-deepseek-v4-flash-0731  
**Тип:** сторонний анализ бенчмарков, косвенные данные (Terminal-Bench 2.1, не 4.0)

Kimi K3 (предшественник K3.1 Pro) показал:
- General intelligence: 57 против 50 у DeepSeek V4 Flash 0731
- Coding: 76 против 69
- Agentic & Tool Use: 50 против 46

Обзор указывает на стабильность в длинных multi-turn агентных циклах, но не даёт измерений K3.1 Pro на Terminal-Bench 4.0.

**Источник:** Artificial Analysis — Kimi K3.1 Pro Intelligence Index  
**URL:** упоминается в обзоре BenchLM (https://benchlm.ai/coding-plans), проверено 08.11.2026  
**Тип:** независимый бенчмарк (еще не завершён для K3.1 Pro)

Artificial Analysis поставил Kimi K3 на 4-е место Intelligence Index v4.1.1 с оценкой 60, но K3.1 Pro ещё не имеет полной оценки. Утверждение о Terminal-Bench ~67% для K3.1 Pro — экстраполяция от K3 и косвенных отзывов.

**Уверенность:** средняя — есть измерения K3, но K3.1 Pro еще не подтверждён независимыми полными бенчмарками. Используется как предварительная оценка на основе отзывов о длинных агентных сессиях (например, Bito test 71% длинных сессий, но это косвенное свидетельство).

---

## Claude Sonnet 5.5 — Terminal-Bench 4.0 и ревью кода

**Источник:** Anthropic model card Claude Sonnet 5.5, опубликовано 28.09.2026  
**URL:** https://www.anthropic.com/claude-sonnet-5-5  
**Тип:** вендорское заявление (Anthropic)

Заявленные результаты:
- Terminal-Bench 4.0: 70.6% (против Sonnet 5: 10.3%, Opus 5.5: ~66%)
- GDPval-AA: два балла ниже Opus 5.5
- Скорость вывода: +30%
- Стоимость на задачу: -30% против Sonnet 5

**Независимое подтверждение:** CodeRabbit обзор (https://www.coderabbit.ai/blog/opus-5-5-model-review, проверено 08.11.2026) подтвердил, что Sonnet 5.5 сокращает время ревью кода в два раза и снижает стоимость на 40% против Sonnet 5. Опыт на Signal benchmark (меньший, более сложный) показал сильную точность и покрытие.

**Источник:** Обзор Thomas Wiegold (https://thomas-wiegold.com/blog/claude-sonnet-5-5-review, проверено 08.11.2026)  
**Тип:** практический тест, отзыв

Тест на chess-задаче показал, что Sonnet 5.5 выдал код Opus-уровня, но тестовые данные были слабее. Рекомендация: Sonnet 5.5 для задач с проверкой выхода человеком, Opus 5.5 — где нужна гарантия безошибочности.

**Уверенность:** выше средней — множественные подтверждения от независимых авторов (CodeRabbit, Thomas Wiegold, Artificial Analysis).

---

## Claude Opus 5.5 — многочасовые агентные задачи

**Источник:** CodeRabbit обзор Opus 5.5 (https://www.coderabbit.ai/blog/opus-5-5-model-review, 22.09.2026)  
**Тип:** практический тест, отзыв

Opus 5.5 показал:
- Сильную точность и покрытие на Signal benchmark (меньший, сложный тест)
- Лучшую производительность на длинных, сложных задачах
- Снижение цены за токен на 20% против Opus 5 ($4/$20 против $5/$25)
- Снижение cached read на 60% ($0.20 против $0.50)

**Источник:** Anthropic model card Claude Opus 5.5  
**URL:** упоминается в системном обзоре Sonnet 5.5  
**Тип:** вендорское заявление

Opus 5.5 ведёт на SWE-Bench Pro с разрывом ~9 баллов от Sonnet 5.5 и ~11 баллов на GDPval-AA для длинных задач.

**Уверенность:** выше средней — подтверждено отзывами и практическими тестами длинных агентных сессий.

---

## MiniMax M3.1 Flash — 93% hallucination rate

**Источник:** Artificial Analysis, сообщено VentureBeat  
**URL:** https://venturebeat.com/technology/minimaxs-new-m3-1-flash-beats-deepseek-and-opus-5-on-a-key-business-benchmark-at-lower-cost-but-with-a-high-hallucination-rate (проверено 08.11.2026)  
**Тип:** независимый тест

Результаты:
- Intelligence Index: 42 (рост от M3: 29)
- Стоимость на задачу: $0.22 (снижение от M3: $0.51)
- Hallucination rate: 93% (критический показатель)

Artificial Analysis подтвердил сильное улучшение бенчмарков (Humanity's Last Exam 48% против 39% у M3, CritPt 22% против 4%), но выявил высокий hallucination rate, что делает модель ненадёжной для генеративной работы без проверки.

**Источник:** YouTube-обзор "I Tested NEW MiniMax-M3.1-Flash on 27 Coding Prompts" (https://www.youtube.com/watch?v=3zd9Vj96_nk, 20.10.2026)  
**Тип:** практический тест, отзыв

Обзор показал стабильность модели, но медленность и отсутствие улучшений против Space Bunny на практических задачах. Бесплатный доступ на OpenRouter и OpenCode подтверждает готовность инфраструктуры.

**Уверенность:** высокая для показателя hallucination rate — подтверждено Artificial Analysis, независимым бенчмарк-провайдером. Низкая уверенность для рекомендации на генеративную работу.

---

## GPT-6.1 Terra — cost efficiency frontier

**Источник:** Artificial Analysis, опубликовано 26.10.2026  
**URL:** https://artificialanalysis.ai/articles/gpt-6-1-terra-pushes-the-cost-efficiency-frontier  
**Тип:** независимый тест

Результаты:
- Coding Agent Index v2.0: 48 (против Sol: 54)
- Стоимость на задачу: варьируется по effort level
- Hallucination rate: -50 баллов против GPT-5.6 Terra, точность +2 балла
- Terminal-Bench 4.0: 50.3% на max effort (удвоение против GPT-5.6 Terra: 21.5%)

Artificial Analysis подтвердил, что GPT-6.1 Terra — первая Terra-класс модель с сильным улучшением cost efficiency: цена за токен снижена на 50% или больше против GPT-5.6 Terra ($1/$5 против $2/$12).

**Источник:** MyClaw.ai обзор (https://myclaw.ai/blog/gpt-6-1-terra-review, проверено 08.11.2026)  
**Тип:** сторонний обзор, косвенные данные

Подтверждает Intelligence Index 48 на max effort и стоимость около $0.40/задача на max effort (против Sol: $0.72).

**Уверенность:** выше средней — подтверждено Artificial Analysis (независимый провайдер) и несколькими сторонними обзорами.

---

## Gemini 4 Argon — скидка -50% до 30.11.2026

**Источник:** Google Cloud Blog, опубликовано 13.10.2026  
**URL:** https://cloud.google.com/blog/products/ai-machine-learning/gemini-4-argon-available-on-google-cloud  
**Тип:** официальное объявление (Google)

Тарифы:
- До 30.11.2026: $2/million input, $10/million output
- После 30.11.2026: $4/million input, $20/million output
- Cached input: скидка 95%

**Независимые отзывы:** ByteLand Technology обзор (https://byteland.app/blog/2026-10/gemini-4-argon-review, 14.10.2026)  
**Тип:** практический тест, отзыв

Обзор отмечает сильные результаты на сложных задачах, но смешанные ранние отзывы: некоторые разработчики сообщают о провалах на кодинге, что подтверждает необходимость осторожности при использовании Argon для критичной работы.

**Источник:** Google AI Developers Forum (https://discuss.ai.google.dev/t/how-bad-is-gemini-4-argon/190009)  
**Тип:** пользовательские отзывы

Отзывы разнообразны: часть пользователей считает Argon слабым для кодинга (примерно 1.2× лучше Gemini 3.8 Flash), другие отмечают успешное применение на длинных контекстах и визуальных задачах.

**Уверенность:** средняя — официальная информация о ценах подтверждена, но качество для кодинга вызывает споры. Рекомендация: тестировать на своих задачах до широкого использования.

---

## OpenCode Go — квоты и лимиты

**Источник:** OpenCode Go документация, обновлено 05.11.2026  
**URL:** https://opencode.ai/v2/docs/console/go/  
**Тип:** официальная документация

Подтверждённые изменения:
- DeepSeek V4.1 Flash: лимит увеличен с $15/мес до $60/мес (Go), с $7.50/мес до $30/мес (Go Plus)
- MiniMax M3.1 Flash добавлен с лимитом $36/мес (Go)
- Claude Haiku 5.5 добавлен с лимитом $15/мес (Go)
- Kimi K3.1 Pro: лимит $48/мес (Go)

**Источник:** BSWEN обзор (https://docs.bswen.com/blog/2026-09-04-opencode-go-models, проверено 08.11.2026)  
**Тип:** сторонний обзор

Подтверждает состав Go и Go Plus, лимиты $12/5 часов, $30/неделя, $60/месяц для Go. Также отмечает, что Go — это не фиксированное число запросов, а spending-style allowance.

**Источник:** Replicas.dev сравнение OpenCode Go vs Zen (https://replicas.dev/resources/opencode-go-vs-zen, 02.11.2026)  
**Тип:** сторонний обзор

Сравнивает Go ($10/мес подписка) и Zen (pay-as-you-go). Подтверждает отсутствие Sonnet 5.5 и Opus 5.5 в списке Go.

**Уверенность:** высокая — официальная документация OpenCode, подтверждённая несколькими сторонними обзорами.

---

## DeepSeek Search/Fetch API — тарификация с 31.10.2026

**Источник:** DeepSeek API Docs, проверено 08.11.2026  
**URL:** https://api-docs.deepseek.com/quick_start/pricing/  
**Тип:** официальная документация

Тарифы:
- Search: $0.75 за 1000 успешных запросов
- Fetch: $0.75 за 1000 успешных запросов
- Начало тарификации: 00:00 Beijing time 01.11.2026 (16:00 UTC 31.10.2026)

До 31.10.2026 Search/Fetch были бесплатны при использовании через DeepSeek Harness, Claude Code или Codex.

**Источник:** BenchLM.ai обзор DeepSeek API Pricing (https://benchlm.ai/deepseek/api-pricing, проверено 08.11.2026)  
**Тип:** сторонний обзор

Подтверждает дату начала тарификации и цены. Также отмечает, что для агента с 20 searches на задачу это добавляет $0.015/задача, что примерно равно выводу 25K deepseek-flash токенов на off-peak rate.

**Уверенность:** высокая — официальная документация DeepSeek, подтверждённая несколькими сторонними обзорами.

---

## OpenRouter — расширение каталога до 600+ моделей

**Источник:** PricingSaaS Pulse, проверено 02.11.2026  
**URL:** https://pricingsaas.com/companies/openrouter/diffs/2026W45  
**Тип:** сторонний мониторинг изменений

Изменение между 26.10.2026 и 02.11.2026: Model catalog count изменён с 500+ на 600+ моделей на Standard, Business и Enterprise планах.

**Уверенность:** средняя — изменение зафиксировано сторонним сервисом мониторинга, но не подтверждено официальным объявлением OpenRouter. Treat as signal.

---

## Слабые места и разногласия источников

1. **Kimi K3.1 Pro Terminal-Bench 4.0:** прямого измерения K3.1 Pro на Terminal-Bench 4.0 нет. Используются косвенные данные от K3 (Terminal-Bench 2.1: 88.3%) и отзывы о длинных сессиях. Утверждение ~67% — экспертная оценка, а не прямое измерение.

2. **MiniMax M3.1 Flash льготное окно:** OpenRouter JSON показывает `utc_start: 1500, utc_end: 100`, что предположительно 15:00–01:00 UTC, но точные условия не раскрыты на странице модели. Treat as directional.

3. **Gemini 4 Argon качество кодинга:** отзывы противоречивы. Google Developers Blog (https://developers.googleblog.com/optimizing-a-200000-line-python-codebase-overnight-with-gemini-4-argon) показывает успешную оптимизацию 200K-строчного Python-кодабазы, но форум Google AI Developers содержит жалобы на слабое качество. Рекомендация: тестировать на своих задачах.

4. **OpenRouter backend гарантии:** агрегированная цена OpenRouter — не гарантия каждого backend. Некоторые модели (например, Kimi K3.1 Pro) имеют дешёвые backend ($0.33/8.12), но без гарантии качества. Всегда проверяйте, какой backend выбран для вашего запроса.

5. **GPT-6.1 Sol vs Terra для кодинга:** OpenAI утверждает, что Sol остаётся лучше для самых сложных задач кодинга, но Artificial Analysis показывает, что Terra на max effort приближается к Sol на некоторых бенчмарках. Разрыв в Coding Agent Index v2.0 (54 для Sol против 48 для Terra) подтверждает, что Sol всё ещё впереди, но не на всех задачах.

---

## Перенос данных между задачами

**Reasoning effort:** бенчмарки Terminal-Bench и Intelligence Index часто измеряются на max effort. При использовании low/medium effort результаты могут быть значительно ниже. Например, Artificial Analysis показывает, что Sonnet 5.5 на max effort использует ~193K output tokens на задачу, что делает его дороже Opus 5.5 по стоимости за задачу, несмотря на более низкую цену за токен.

**SWE-bench vs Terminal-Bench:** SWE-bench измеряет решение issue в репозитории с многократными коммитами. Terminal-Bench измеряет выполнение команд в терминале за один проход. Результаты SWE-bench нельзя напрямую экстраполировать на Terminal-Bench, но высокая корреляция существует для агентных задач.

**Скорость ответа:** данные о latency и tokens/sec из предыдущего отчёта не обновлялись, так как новых измерений для всех кандидатов не найдено. Используются косвенные данные Artificial Analysis (например, DeepSeek V4.1 Flash max: 209.0 tok/s).

**Vendor benchmarks:** все vendor-stated результаты (DeepSeek model card, Anthropic system card, Google Argon announcement) отмечены как "вендорское заявление" и, где возможно, дополнены независимыми подтверждениями или отзывами.

---

## Итоговая таблица типов источников по рекомендациям

| Рекомендация | Основной источник | Тип | Подтверждение |
| --- | --- | --- | --- |
| DeepSeek V4.1 Flash 1017 — агентные задачи | DeepSeek model card | Вендорское заявление | YouTube-обзоры, сторонние тесты |
| Kimi K3.1 Pro — длинные сессии | Artificial Analysis | Косвенные данные (K3) | Отзывы о K3.1 Pro, экстраполяция |
| Claude Sonnet 5.5 — ревью кода | Anthropic model card | Вендорское заявление | CodeRabbit, Thomas Wiegold |
| Claude Opus 5.5 — сложные задачи | CodeRabbit, Anthropic | Практический тест, вендор | Множественные отзывы |
| MiniMax M3.1 Flash — hallucination rate | Artificial Analysis | Независимый тест | VentureBeat, YouTube-обзоры |
| GPT-6.1 Terra — cost efficiency | Artificial Analysis | Независимый тест | MyClaw.ai, сторонние обзоры |
| Gemini 4 Argon — скидка -50% | Google Cloud Blog | Официальное объявление | ByteLand, Google Developers Blog |
| OpenCode Go — квоты | OpenCode документация | Официальная документация | BSWEN, Replicas.dev |
| DeepSeek Search/Fetch — тарификация | DeepSeek API Docs | Официальная документация | BenchLM.ai |

**Примечание:** полная страница модели OpenRouter для многих кандидатов доступна, но не читалась webfetch из-за лимита запросов. Цены проверены через локальный OpenRouter JSON (openrouter-summary.json), умножены на 1M и сверены с доступными страницами.
