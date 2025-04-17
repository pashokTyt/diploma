<template>
  <div class="table-container">
    <div class="scrollable-table">
      <el-table :data="paginated_npas" style="width: 100%" height="600" :row-class-name="tableRowClassName">
        <el-table-column prop="name" label="Название" min-width="450"></el-table-column>
        <el-table-column prop="number" label="Номер" min-width="70"></el-table-column>
        <el-table-column prop="publish_date" label="Опубликован" sortable min-width="117"></el-table-column>
        <el-table-column prop="write_date" label="Подписан" sortable min-width="110"></el-table-column>

        <el-table-column prop="days_diff" label="Дней со дня подписания" sortable min-width="120">
          <template #default="{ row }">
            {{ row.days_diff }}
          </template>
        </el-table-column>

        <el-table-column prop="source.name" label="Источник" min-width="130"></el-table-column>
        <el-table-column prop="region.name" label="Регион" min-width="150"></el-table-column>
        <el-table-column label="Ссылка на скачивание" min-width="90">
          <template #default="{ row }">
            <a :href="row.link_to_download" class="download-link">Скачать</a>
          </template>
        </el-table-column>
        <el-table-column label="Опубликован" min-width="200">
          <template #default="{ row }">
            <span v-if="row.published">&#10004;</span>
            <span v-else>&#10006;</span>
          </template>
        </el-table-column>
      </el-table>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    paginated_npas: {
      type: Array,
      required: true,
    }
  },
  methods: {
    tableRowClassName({ row }) {
      if (row.days_diff >= 10) {
        return 'custom-orange'; // 🔶
      } else if (row.days_diff >= 9) {
        return 'danger-row';   // 🔴
      } else if (row.days_diff >= 5) {
        return 'warning-row';  // 🟡
      } else if (row.days_diff >= 3) {
        return 'info-row';     // 🔵
      } else if (row.days_diff === 0) {
        return 'success-row';  // 🐬 Бирюзовый
      } else {
        return 'success-row';  // 🟢
      }
    }
  }
};
</script>

<style scoped>
.table-container {
  width: 100%;
  margin-top: 1%;
}

.scrollable-table {
  max-height: 600px;
  overflow-y: auto;
}

:deep(.el-table .danger-row) {
  --el-table-tr-bg-color: var(--el-color-danger-light-9);
}

:deep(.el-table .warning-row) {
  --el-table-tr-bg-color: var(--el-color-warning-light-9);
}

:deep(.el-table .info-row) {
  --el-table-tr-bg-color: var(--el-color-info-light-9);
}

:deep(.el-table .success-row) {
  --el-table-tr-bg-color: var(--el-color-success-light-9);
}

:deep(.el-table .custom-purple) {
  --el-table-tr-bg-color: #e8eaf6;
  border-left: 3px solid #7e57c2;
}

:deep(.el-table .custom-orange) {
  --el-table-tr-bg-color: #ffecb3;
}

:deep(.el-table .custom-teal) {
  --el-table-tr-bg-color: #b2dfdb;
  font-weight: 500;
}

:deep(.el-table .custom-gray) {
  --el-table-tr-bg-color: #f5f5f5;
  color: #9e9e9e;
}

.download-link {
  color: var(--el-color-primary);
  text-decoration: none;
}

.download-link:hover {
  text-decoration: underline;
}
</style>
