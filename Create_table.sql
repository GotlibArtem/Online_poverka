-- Таблица утвержденных типов СИ
CREATE TABLE approved_types (
    id_appr_type SERIAL,                                -- ID утвержденного типа СИ
    number_si VARCHAR(10) NOT NULL,                     -- Номер в госреестре
    name_si TEXT,                                       -- Наименование СИ
    designation_si TEXT,                                -- Обозначение типа СИ
    number_record INT NOT NULL,                         -- Номер записи
    id_arshin INT NOT NULL,                             -- ID записи на ФГИС АРШИН
    publication_date DATE,                              -- Дата опубликования
    manufacturer_si TEXT,                               -- Изготовитель СИ
    description_si TEXT,                                -- Описание типа (ссылка)
    method_verif_si TEXT,                               -- Методика поверки (ссылка)
    proced_si VARCHAR(30),                              -- Наименование процедуры поверки
    certificate_date DATE,                              -- Срок свидетельства
    mpi_si VARCHAR(20),                                 -- Межповерочный интервал СИ
    next_verif_si BOOLEAN,                              -- Наличие периодической поверки
    part_verif_si BOOLEAN,                              -- Допускается проверка партии
    status_si BOOLEAN,                                  -- Статус СИ
    PRIMARY KEY(id_appr_type) 
);

