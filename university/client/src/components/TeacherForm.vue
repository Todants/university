<template>
  <div>
    <h2>{{ teacher.id ? 'Редактировать преподавателя' : 'Добавить преподавателя' }}</h2>
    <form @submit.prevent="submitForm">
      <div>
        <label>Имя:</label>
        <input v-model="teacher.name" required />
      </div>
      <!-- Добавьте другие поля по необходимости -->
      <button type="submit">{{ teacher.id ? 'Сохранить' : 'Добавить' }}</button>
    </form>
  </div>
</template>

<script>
export default {
  props: {
    teacherData: Object,
  },
  data() {
    return {
      teacher: this.teacherData ? { ...this.teacherData } : { name: '' },
    }
  },
  methods: {
    submitForm() {
      this.$emit('submit', this.teacher)
    },
  },
}
</script>