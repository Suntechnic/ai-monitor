# Рейтинг моделей

Данные Artificial Analysis от 2026-11-12T10:50:07.094910+03:00. Рейтинг основан на Coding Agent Index v2.0: равный вес компонентов измеряет изменения кода, работу в терминале и понимание репозитория. Это не отдельный PHP/Vue-бенчмарк; цена, скорость и локальная популярность в оценку не входят.

Для каждой модели выбран лучший публичный вариант с полным индексом. Результат относится к указанным agent harness и режиму reasoning; оценки других версий не переносятся.

| Место | Модель | AA Index | FrontierCode v1.1 Main | Terminal-Bench v4 | SWE-Atlas-QnA | Измеренный вариант | Уверенность |
| ---: | --- | ---: | ---: | ---: | ---: | --- | --- |
| 1 | Claude Opus 5.5 | 61.7 | 56.0 | 63.1 | 65.9 | Claude Code; Claude Opus 5.5 (Max, Default Fallback) | Точная версия; в настройке указан fallback |
| 2 | Gemini 4 Carbon | 59.4 | 50.9 | 63.6 | 63.7 | Antigravity CLI; Gemini 4 Carbon (High) | Прямое измерение точной версии |
| 3 | Claude Sonnet 5.5 | 59.3 | 47.6 | 66.2 | 64.2 | Claude Code; Claude Sonnet 5.5 (Max, Default Fallback) | Точная версия; в настройке указан fallback |
| 4 | GPT-6 Astra | 54.7 | 49.3 | 55.6 | 59.1 | Codex; GPT-6 Astra (Max) | Прямое измерение точной версии |
| 5 | GPT-6.1 Sol | 54.1 | 49.4 | 53.0 | 59.9 | Codex; GPT-6.1 Sol (Max) | Прямое измерение точной версии |
| 6 | Gemini 4 Argon | 53.2 | 48.6 | 56.1 | 55.1 | Antigravity CLI; Gemini 4 Argon (High) | Прямое измерение точной версии |
| 7 | GLM-5.3 | 48.9 | 48.2 | 39.9 | 58.6 | Opencode; GLM-5.3 (Max) | Прямое измерение точной версии |
| 8 | DeepSeek V4.1 Flash 1017 | 46.3 | 46.5 | 30.8 | 61.6 | DeepSeek Harness; DeepSeek V4.1 Flash 1017 (Max) | Прямое измерение точной версии |
| 9 | Claude Haiku 5.5 | 37.3 | 47.4 | 30.8 | 33.9 | Claude Code; Claude Haiku 5.5 (Max) | Прямое измерение точной версии |
| 10 | GPT-6 Luna | 31.2 | 39.5 | 15.7 | 38.4 | Codex; GPT-6 Luna (Max) | Прямое измерение точной версии |
| — | claude-sonet-5 | н/д | н/д | н/д | н/д | н/д | Нет данных AA |
| — | dashscope/qwen3.5-flash | н/д | н/д | н/д | н/д | н/д | Нет данных AA |
| — | gemma-4-31b-it | н/д | н/д | н/д | н/д | н/д | Нет данных AA |
| — | gpt-oss-120b | н/д | н/д | н/д | н/д | н/д | Нет данных AA |
| — | Hy4 | н/д | н/д | н/д | н/д | н/д | Нет данных AA |
| — | kimi-k3.1-pro | н/д | н/д | н/д | н/д | н/д | Нет данных AA |
| — | Qwen3.8 27B | н/д | н/д | н/д | н/д | н/д | Нет данных AA |

Claude Opus 5.5 > Gemini 4 Carbon ≈ Claude Sonnet 5.5 > GPT-6 Astra ≈ GPT-6.1 Sol > Gemini 4 Argon > GLM-5.3 > DeepSeek V4.1 Flash 1017 > Claude Haiku 5.5 > GPT-6 Luna

Обозначения: `>` — разница не менее 1 пункта AA Index; `≈` — разница меньше 1 пункта. Это правило представления сырых результатов, а не проверка статистической значимости. Модели с «н/д» в сравнение не входят.

Источник: https://artificialanalysis.ai/agents/coding-agents · [Методология](https://artificialanalysis.ai/methodology/coding-agents-benchmarking).
