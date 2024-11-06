<template>
  <div id="app">
    <h1>Моё приложение</h1>
    <router-view /> <!-- Здесь будут отображаться страницы в зависимости от маршрута -->
  </div>
</template>

<script>
export default {
  name: 'App'
}
</script>
<template>
  <div id="app">
    <h1>Управление студентами и преподавателями</h1>
    <SearchFilter @search="filterData"/>

    <!-- Кнопки для добавления преподавателя и студента -->
    <button @click="openTeacherForm">Добавить преподавателя</button>
    <button @click="openStudentForm">Добавить студента</button>

    <TeacherTable
      :teachers="filteredTeachers"
      @edit="openTeacherForm"
      @delete="deleteTeacher" />

    <StudentTable
      :students="filteredStudents"
      @edit="openStudentForm"
      @delete="deleteStudent"
      @edit-grades="openGradeForm" />

    <!-- Модальные окна для форм -->
    <TeacherForm v-if="showTeacherForm" :teacherData="currentTeacher" @submit="submitTeacherForm" />
    <StudentForm v-if="showStudentForm" :studentData="currentStudent" @submit="submitStudentForm" />
    <GradeForm v-if="showGradeForm" :student="currentStudent" @submit-grades="submitGradesForm" />
  </div>
</template>

<script>
import TeacherTable from './components/TeacherTable.vue'
import StudentTable from './components/StudentTable.vue'
import TeacherForm from './components/TeacherForm.vue'
import StudentForm from './components/StudentForm.vue'
import GradeForm from './components/GradeForm.vue'
import SearchFilter from './components/SearchFilter.vue'
import { mapState } from 'vuex'

export default {
  name: 'App',
  components: {
    TeacherTable,
    StudentTable,
    TeacherForm,
    StudentForm,
    GradeForm,
    SearchFilter
  },
  data() {
    return {
      showTeacherForm: false,
      showStudentForm: false,
      showGradeForm: false,
      currentTeacher: null,
      currentStudent: null,
      searchQuery: ''
    }
  },
  computed: {
    ...mapState(['teachers', 'students']),
    filteredTeachers() {
      return this.teachers.filter(teacher => teacher.name.toLowerCase().includes(this.searchQuery.toLowerCase()))
    },
    filteredStudents() {
      return this.students.filter(student => student.name.toLowerCase().includes(this.searchQuery.toLowerCase()))
    }
  },
  methods: {
    filterData(query) {
      this.searchQuery = query
    },
    openTeacherForm(teacher = null) {
      this.currentTeacher = teacher
      this.showTeacherForm = true
    },
    submitTeacherForm(teacher) {
      if (teacher.id) {
        this.$store.dispatch('updateTeacher', teacher)
      } else {
        this.$store.dispatch('addTeacher', teacher)
      }
      this.showTeacherForm = false
    },
    deleteTeacher(teacherId) {
      this.$store.dispatch('deleteTeacher', teacherId)
    },
    openStudentForm(student = null) {
      this.currentStudent = student
      this.showStudentForm = true
    },
    submitStudentForm(student) {
      if (student.id) {
        this.$store.dispatch('updateStudent', student)
      } else {
        this.$store.dispatch('addStudent', student)
      }
      this.showStudentForm = false
    },
    deleteStudent(studentId) {
      this.$store.dispatch('deleteStudent', studentId)
    },
    openGradeForm(student) {
      this.currentStudent = student
      this.showGradeForm = true
    },
    submitGradesForm({ studentId, grades }) {
      this.$store.dispatch('updateGrades', { studentId, grades })
      this.showGradeForm = false
    }
  },
  mounted() {
    this.$store.dispatch('fetchTeachers')
    this.$store.dispatch('fetchStudents')
  }
}
</script>