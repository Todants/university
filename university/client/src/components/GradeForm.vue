<template>
  <div>
    <h2>Редактировать оценки для {{ student.name }}</h2>
    <form @submit.prevent="submitGrades">
      <div v-for="subject in subjects" :key="subject">
        <label>{{ subject }}:</label>
        <input type="number" v-model.number="grades[subject]" min="0" max="100" />
      </div>
      <button type="submit">Сохранить оценки</button>
    </form>
  </div>
</template>

<script>
export default {
  props: {
    student: Object,
  },
  data() {
    return {
      grades: { ...this.student.grades },
      subjects: ['Математика', 'История', 'Химия'], // Можете добавить другие предметы
    }
  },
  methods: {
    submitGrades() {
      this.$emit('submit-grades', { studentId: this.student.id, grades: this.grades })
    },
  },
}
</script>