<!--Навигационная панель + 
основа приложения(app)
-->
<template>
    <div id="app">
        <div class="container-fluid">
            <div class="header-container">
                <img src="./assets/logo_no_background .png" alt="Логотип" />
                <div>
                    <h3>Pravo</h3>
                    <h4>Портал мониторинга пополнения банка нормативно-правовых актов субъектов РФ</h4>
                    <nav class="navbar navbar-expand-lg custom-navbar">
                        <button class="navbar-toggler" type="button" data-bs-toggle="collapse"
                            data-bs-target="#navbarNav" aria-expanded="false" aria-label="Toggle navigation">
                        </button>
                        <div class="collapse navbar-collapse" id="navbarNav">
                            <ul class="navbar-nav">
                                <li class="nav-item">
                                    <router-link to="/" class="nav-link custom-link" active-class="active"
                                        exact-active-class="active">
                                        <h6>Основная страница</h6>
                                    </router-link>
                                </li>
                                <li class="nav-item">
                                    <router-link to="/monitoring" class="nav-link custom-link" active-class="active">
                                        <h6>Мониторинг
                                            пополнения НПА</h6>
                                    </router-link>
                                </li>
                                <li class="nav-item">
                                    <router-link to="/statistics" class="nav-link custom-link" active-class="active">
                                        <h6>Статистика</h6>
                                    </router-link>
                                </li>
                            </ul>
                        </div>
                    </nav>
                </div>
            </div>
            <router-view></router-view>
        </div>
    </div>
</template>


<script>
export default {
    name: 'App',
};
</script>

<style scoped>
.custom-link {
    background-color: transparent;
    color: white;
    padding: 2px 30px;
    transition: all 0.5s ease;
    font-size: 18px;
}

.custom-link:hover {
    border-color: white;
    color: white;
}


.custom-link::after {
    content: '';
    display: block;
    height: 2px;
    width: 0;
    background-color: white;
    transition: width 0.3s ease;
}

.custom-link:hover::after {
    width: 100%;
}
</style>
