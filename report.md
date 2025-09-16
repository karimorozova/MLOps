# Report: Containerization of ML Model

## Image comparison

| Type | Size    | Layers | Notes                                         |
| ---- | ------- | ------ | --------------------------------------------- |
| Fat  | ~1.2 GB | 8      | Включає всі залежності, середовище важке      |
| Slim | ~400 MB | 5      | Multi-stage build, тільки потрібні залежності |

## Optimization analysis

- Slim-образ у 3 рази менший за розміром
- Менше шарів та швидший деплой
- Відсутні непотрібні інструменти (`apt`, build-залежності)
- Можна ще оптимізувати:
  - Використати `torch==<cpu-only>` версію
  - Стиснути модель (`torch.quantization`)
  - Використати Alpine базовий образ
