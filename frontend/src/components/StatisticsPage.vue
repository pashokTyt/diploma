<template>
    <!--     <div class="container-fluid">
        <div class="row">
            <div class="col-md-2">
                <h2>Фильтры</h2>
                <div class="filter-panel">
                    <div class="filter-elements">
                        <div class="row">
                            <el-checkbox v-model="checked" label="Опубликованы" size="large" @change="fetchNpas"
                                border />
                        </div>
                        <p></p>
                        <div class="row">
                            <span>Дата публикации:</span>
                            <el-date-picker v-model="selectedWriteDateRange" type="daterange" range-separator="По"
                                start-placeholder="Начало" end-placeholder="Конец" :size="'small'" @change="fetchNpas"
                                format="DD.MM.YYYY" unlink-panels />
                        </div>
                        <p></p>
                        <div class="row">
                            <label for="source">Источник:</label>
                            <el-cascader v-model="selectedSource" :options="formattedSources" :props="cascaderProps"
                                clearable @change="fetchNpas" />
                        </div>
                        <p></p>
                        <div class="row">
                            <label for="region">Регион:</label>
                            <el-cascader v-model="selectedRegion" :options="formattedRegions" :props="cascaderProps"
                                clearable @change="fetchNpas" />
                        </div>
                    </div>
                </div>
            </div>
            
            <div class="col">
                <h2>Текст нормативно-правового документа</h2>
                <div class="syntax-container">
                    <div class="card">
                        <div class="card-header">
                            Указ Губернатора Орловской области от 03.03.2025 № 100
                            "О внесении изменений в указ Губернатора Орловской области от 27 декабря 2024 года № 786
                            "О создании комиссий муниципальных районов, муниципального и городских округов Орловской
                            области по первоначальной постановке граждан 2008 года рождения на воинский учет"
                        </div>
                        <div class="card-body">
                            <blockquote class="blockquote mb-0">
                                <p>В соответствии с Федеральным законом от 06.10.2003 № 131-ФЗ «Об общих
                                    принципах организации местного самоуправления в Российской Федерации», частью 17
                                    статьи
                                    161 <span class="color-text">Жилищного кодекса Российской Федерации,
                                        постановлением</span> Правительства Российской
                                    Федерации от 21.12.2018 № 1616 «Об утверждении Правил определения управляющей
                                    организации для управления многоквартирным домом, в отношении которого
                                    собственниками
                                    помещений в многоквартирном доме не выбран способ управления таким домом или
                                    выбранный
                                    способ управления не реализован, не определена управляющая организация, и о внесении
                                    изменений в некоторые акты правительства Российской Федерации», постановлением
                                    Правительства Российской Федерации от 03.04.2013 № 290 «О минимальном перечне услуг
                                    и
                                    работ, необходимых для обеспечения надлежащего содержания общего имущества в
                                    многоквартирном доме, и порядке их оказания и выполнения», постановлением
                                    администрации
                                    города Орла от 30.09.2019 № 4110 «Об утверждении Перечня управляющих организаций для
                                    управления многоквартирным домом, в отношении которого собственниками помещений в
                                    многоквартирном доме не выбран способ управления таким домом или выбранный способ
                                    управления не реализован, не определена управляющая организация», постановлением
                                    администрации города Орла от 15.11.2013 № 5213 «Об установлении размера платы за
                                    содержание жилого помещения для собственников жилых помещений, которые не приняли
                                    решение о выборе способа управления многоквартирным домом, решение об установлении
                                    размера платы за содержание жилого помещения» администрация города Орла
                                    постановляет:
                                    1. Определить ООО «УК «Алеся» управляющей организацией для управления
                                    многоквартирным
                                    домом № 31 по ул. МОПРа в городе Орле.
                                    2. Определить перечень работ и (или) услуг по управлению многоквартирным домом,
                                    указанным в пункте 1 настоящего постановления, услуг и работ по содержанию и ремонту
                                    общего имущества в многоквартирном доме, устанавливаемый в зависимости от
                                    конструктивных
                                    и технических параметров многоквартирного дома, включая требования к объемам,
                                    качеству,
                                    периодичности каждой из таких работ и услуг, сформированный из числа работ и услуг,
                                    указанных в минимальном перечне услуг и работ, необходимых для обеспечения
                                    надлежащего
                                    содержания общего имущества в многоквартирном доме, и размер платы за содержание
                                    жилого
                                    помещения согласно приложению к настоящему постановлению.
                                    3. Территориальному управлению по Заводскому району администрации города Орла
                                    уведомить
                                    собственников помещений многоквартирного дома, указанного в пункте 1 настоящего
                                    постановления, о принятом администрацией города Орла решении.
                                    4. Управлению по взаимодействию со средствами массовой информации и аналитической
                                    работе
                                    администрации города Орла (О. А. Храмченкова) опубликовать настоящее постановление в
                                    газете «Орловская городская газета» и разместить на официальном сайте администрации
                                    города Орла в сети Интернет.
                                    5. Контроль за исполнением настоящего постановления возложить на заместителя Мэра
                                    города
                                    Орла – начальника управления жилищно-коммунального хозяйства администрации города
                                    Орла
                                    С. Н. Филатова.



                                    Мэр города Орла Ю. Н. Парахин
                                </p>
                            </blockquote>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div> -->
    <div class="center-card">
        <div class="card" style="width: 30rem; margin: auto;">
            <img class="card-img-top"
                src="data:image/jpeg;base64,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"
                alt="Card image cap">
            <div class="card-body">
                <h5 class="card-title">Карта скала</h5>
                <p class="card-text">Вам стоит обратить внимание на работу с кризисными ситуациями: помощь людям.
                    находящимся в сложных обстоятельствах (развод, потери близких, люди на грани суицида), также
                    возможны различные виды опасной работы: работа в горячих точках, военное дело (например, работа
                    военкора или оружейный бизнес), работа спасателя; что-то связанное с экстримом или экстремальным
                    спортом.
                    В любом случае - это не спокойное сидение на месте, ниша, которая принесет вам максимальный доход -
                    взрывоопасная, это очень жесткая энергия.
                </p>
            </div>
            <ul class="list-group list-group-flush">
                <a href="#" ></a><li class="list-group-item"><a href="#" >#жить_здорово</a></li>
                <li class="list-group-item"><a href="#" >#правильное_питание</a></li>
                <li class="list-group-item"><a href="#" >#мать_героина</a></li>
            </ul>
            <div class="card-body">
                <div class="row justify-content-around">
                    <div class="col"> <a href="#" class="card-link">
                            <button type="button" class="btn btn-success">Нагнать порчу</button>
                        </a>
                    </div>
                    <div class="col"> <a href="#" class="card-link">
                            <button type="button" class="btn btn-danger">Простить грехи</button>
                        </a></div>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>

</script>

<style>
.color-text {
    color: red;
}

.syntax-container {
    max-height: 700px;
    overflow-y: auto;
}

.center-card {
    display: flex;

    height: 10px;
}
</style>