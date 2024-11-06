<template>
  <div>
    <h2>{{ student.id ? 'Редактировать студента' : 'Добавить студента' }}</h2>
    <form @submit.prevent="submitForm">
      <div>
        <label>Имя:</label>
        <input v-model="student.name" required />
      </div>
      <!-- Добавьте другие поля, например, возраст или курс -->
      <button type="submit">{{ student.id ? 'Сохранить' : 'Добавить' }}</button>
    </form>
  </div>
</template>

<script>
export default {
  props: {
    studentData: Object,
  },
  data() {
    return {
      student: this.studentData ? { ...this.studentData } : { name: '' },
    }
  },
  methods: {
    submitForm() {
      this.$emit('submit', this.student)
    },
  },
}
</script>