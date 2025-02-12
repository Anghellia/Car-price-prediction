# Car-price-prediction

## Описание набора данных

С сайта avito.ru по состоянию на 12 августа 2020 года я спарсила 20716 объявлений о продаже автомобилей в Нижегородской области.
Каждое объявление содержит технические характеристики автомобиля, а также цену продажи.  
Проект посвящен исследованию данных объявлений на предмет предсказания цены автомобиля на основании его технических характеристик.

### Описание признаков
- label - марка автомобиля
- model - модель
- generation - поколение
- modification - модификация
- year - год выпуска автомобиля
- mileage - пробег
- condition - состояние автомобиля (бинарный признак)
- doors_num - количество дверей
- body - тип кузова
- engine - тип двигателя
- transmission - коробка передач
- color - цвет автомобиля
- drive - тип привода
- wheel - руль
- package - комплектация
- price - цена, целевая переменная

## Структура проекта
```
Project/
  │
  ├── preprocessing.ipynb - ноутбук с препроцессингом данных
  ├── EDA.ipynb - исследование данных, построение графиков
  ├── predictions.ipynb - построение моделей машинного обучения для предсказания цены автомобиля 
  │
  ├── avito_parser.py - парсер объявлений о продаже автомобилей
  │
  └── data/
     ├── avito_cars.csv - данные, полученные с помощью avito_parser.py
     └── preprocessed_data.csv - очищенные данные, подготовленные для построения моделей
 ```
 
## Результаты

 Метрика\Модель            | Ridge model (Baseline) | RandomForest (Baseline) | Lasso (GridSearch) | Ridge (GridSearch) | ElasticNet (GridSearch) | Xgboost (Best model)
:--------------------------|:-----------------------|:------------------------|:-------------------|:-------------------|:-----------------------|:-----------------------
  MSE                      | 0.088                  | 0.085                   | 0.084              | 0.082              | 0.082                  | 0.078
  R2                       | 0.893                  | 0.897                   | 0.899              | 0.900              | 0.900                  | 0.905
  MAE (средняя абс. ошибка)| 64908 р.               | 64420 р.                | 62274 р.           | 62986 р.           | 63130 р.               | 60652 р.
 
