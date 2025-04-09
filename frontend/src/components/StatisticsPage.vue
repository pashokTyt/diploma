<template>
  <div class="dashboard">
    <header>
      <h1>Дашборд</h1>
    </header>
    <main>
      <div class="row">
        <div class="col-md-4">
          <section class="stats">
            <div class="stat">
              <h2>Опубликованные НПА</h2>
              <p>{{ publishedNpasCount }}</p>
            </div>
            <div class="stat">
              <h2>Регионы</h2>
              <p>{{ regionsCount }}</p>
            </div>
            <div class="stat">
              <h2>Источники</h2>
              <p>{{ sourcesCount }}</p>
            </div>
            <div class="select-region">
              <select v-model="selectedRegion" @change="updateStats">
                <option value="all">Все регионы</option>
                <option v-for="region in regions" :key="region" :value="region">{{ region }}</option>
              </select>
            </div>
          </section>
        </div>
        <div class="col-md-8">
          <section class="charts">
            <h2>Последние опубликованные НПА</h2>
            <ul>
              <li v-for="npa in latestNpas" :key="npa.name">
                {{ npa.name }} ({{ npa.publishDate }})
              </li>
            </ul>

            <div class="chart-container">
              <img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQfaukuzKXQxLeUd8NqGpqHf49lTZmz1_TnkQ&s"
                alt="График 1" class="chart">
            </div>
          </section>
        </div>
      </div>

      <div class="row">
        <div class="col-md-6">
          <section class="charts">
            <h2>График 2</h2>
            <div class="chart-container">
              <img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQfaukuzKXQxLeUd8NqGpqHf49lTZmz1_TnkQ&s"
                alt="График 2" class="chart">
            </div>
          </section>
        </div>
        <div class="col-md-6">
          <section class="charts">
            <h2>График 3</h2>
            <div class="chart-container">
              <img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQfaukuzKXQxLeUd8NqGpqHf49lTZmz1_TnkQ&s"
                alt="График 3" class="chart">
            </div>
          </section>
        </div>
      </div>

      <div class="row">
        <div class="col-md-12">
          <section class="news">
            <h2>Последние новости</h2>
            <ul>
              <li v-for="news in latestNews" :key="news.title">
                {{ news.title }} ({{ news.date }})
              </li>
            </ul>
          </section>
        </div>
      </div>
    </main>
  </div>
</template>

<script>
import 'bootstrap/dist/css/bootstrap.min.css';

export default {
  data() {
    return {
      publishedNpasCount: 50,
      regionsCount: 10,
      sourcesCount: 5,
      latestNpas: [
        { name: "НПА 1", publishDate: "2023-01-01" },
        { name: "НПА 2", publishDate: "2023-01-15" },
        { name: "НПА 3", publishDate: "2023-02-01" },
      ],
      latestNews: [
        { title: "Новость 1", date: "2023-01-01" },
        { title: "Новость 2", date: "2023-01-15" },
        { title: "Новость 3", date: "2023-02-01" },
      ],
      regions: ["Москва", "Санкт-Петербург", "Орёл"],
      selectedRegion: "all",
    };
  },
  methods: {
    updateStats() {
      if (this.selectedRegion === "all") {
        this.publishedNpasCount = 50;
        this.regionsCount = 10;
        this.sourcesCount = 5;
      } else {
        this.publishedNpasCount = 10;
        this.regionsCount = 1;
        this.sourcesCount = 2;
      }
    },
  },
};
</script>

<style scoped>
.dashboard {
  max-width: 1200px;
  margin: auto;
  padding: 20px;
  background-color: #f9f9f9;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
}

header {
  background-color: #333;
  color: #fff;
  padding: 10px;
  text-align: center;
  border-radius: 5px 5px 0 0;
}

main {
  padding: 20px;
}

.stats {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-bottom: 20px;
}

.stat {
  background-color: #fff;
  padding: 20px;
  border-radius: 5px;
  width: 100%;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  margin-bottom: 10px;
}

.stat h2 {
  margin-top: 0;
}

.select-region {
  margin-top: 20px;
}

.select-region select {
  width: 100%;
  padding: 10px;
  border-radius: 5px;
  border: 1px solid #ddd;
}

.charts {
  margin-bottom: 20px;
}

.chart-container {
  margin-bottom: 20px;
}

.chart {
  width: 100%;
  height: auto;
  border-radius: 5px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
}

.news ul {
  list-style: none;
  padding: 0;
}

.news li {
  margin-bottom: 10px;
}

h2 {
  color: #333;
  margin-bottom: 10px;
}
</style>
