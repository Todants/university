const store = createStore({
  state: {
    teachers: [],
    students: []
  },
  mutations: {
    setTeachers(state, teachers) {
      state.teachers = teachers
    },
    setStudents(state, students) {
      state.students = students
    },
    addTeacher(state, teacher) {
      state.teachers.push(teacher)
    },
    updateTeacher(state, teacher) {
      const index = state.teachers.findIndex(t => t.id === teacher.id)
      if (index !== -1) state.teachers.splice(index, 1, teacher)
    },
    deleteTeacher(state, teacherId) {
      state.teachers = state.teachers.filter(t => t.id !== teacherId)
    },
    addStudent(state, student) {
      state.students.push(student)
    },
    updateStudent(state, student) {
      const index = state.students.findIndex(s => s.id === student.id)
      if (index !== -1) state.students.splice(index, 1, student)
    },
    deleteStudent(state, studentId) {
      state.students = state.students.filter(s => s.id !== studentId)
    },
    updateGrades(state, { studentId, grades }) {
      const student = state.students.find(s => s.id === studentId)
      if (student) student.grades = grades
    }
  },
  actions: {
    fetchTeachers({ commit }) {
      // API вызов для получения преподавателей
      const teachers = [/* Данные преподавателей */]
      commit('setTeachers', teachers)
    },
    fetchStudents({ commit }) {
      // API вызов для получения студентов
      const students = [/* Данные студентов */]
      commit('setStudents', students)
    },
    addTeacher({ commit }, teacher) {
      // API вызов для добавления преподавателя
      commit('addTeacher', teacher)
    },
    updateTeacher({ commit }, teacher) {
      // API вызов для обновления преподавателя
      commit('updateTeacher', teacher)
    },
    deleteTeacher({ commit }, teacherId) {
      // API вызов для удаления преподавателя
      commit('deleteTeacher', teacherId)
    },
    addStudent({ commit }, student) {
      // API вызов для добавления студента
      commit('addStudent', student)
    },
    updateStudent({ commit }, student) {
      // API вызов для обновления студента
      commit('updateStudent', student)
    },
    deleteStudent({ commit }, studentId) {
      // API вызов для удаления студента
      commit('deleteStudent', studentId)
    },
    updateGrades({ commit }, payload) {
      // API вызов для обновления оценок студента
      commit('updateGrades', payload)
    }
  }
})