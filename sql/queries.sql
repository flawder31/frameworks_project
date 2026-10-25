-- 1. Выборка всех счетчиков
SELECT code, name, unit, tariff FROM meters ORDER BY name;

-- 2. Фильтрация (WHERE): счетчики с тарифом не выше 50
SELECT code, name, tariff FROM meters WHERE tariff <= 50 ORDER BY tariff;

-- 3. JOIN: показания с названиями счетчиков
SELECT r.id, r.reading_date, m.name AS meter_name, r.consumption, r.cost 
FROM readings r
JOIN meters m ON r.meter_code = m.code
ORDER BY r.reading_date DESC;

-- 4. JOIN + фильтрация: только показания по электроэнергии (EL)
SELECT r.reading_date, m.name, r.consumption, r.cost
FROM readings r
JOIN meters m ON r.meter_code = m.code
WHERE m.code = 'EL'
ORDER BY r.reading_date;

-- 5. Агрегатная функция (COUNT): общее количество показаний
SELECT COUNT(*) AS total_readings FROM readings;

-- 6. Агрегатная функция (SUM): общая стоимость всех показаний
SELECT SUM(cost) AS total_cost FROM readings;

-- 7. Агрегатная функция (AVG): средний расход
SELECT AVG(consumption) AS avg_consumption FROM readings;

-- 8. Группировка (GROUP BY): статистика по каждому счетчику
SELECT m.name, COUNT(r.id) AS readings_count, SUM(r.cost) AS total_cost
FROM meters m
LEFT JOIN readings r ON m.code = r.meter_code
GROUP BY m.code, m.name
ORDER BY total_cost DESC;

-- 9. Фильтрация групп (HAVING): счетчики, по которым больше 1 показания
SELECT m.name, COUNT(r.id) AS readings_count
FROM meters m
JOIN readings r ON m.code = r.meter_code
GROUP BY m.code, m.name
HAVING COUNT(r.id) > 1;

-- 10. Сортировка и лимит: последние 5 показаний
SELECT * FROM readings ORDER BY reading_date DESC LIMIT 5;