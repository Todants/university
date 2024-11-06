<template>
  <div>
    <h2>Студенты</h2>
    <table>
      <thead>
        <tr>
          <th>Имя</th>
          <th>Действия</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="student in students" :key="student.id">
          <td>{{ student.name }}</td>
          <td>
            <button @click="$emit('edit', student)">Редактировать</button>
            <button @click="$emit('delete', student.id)">Удалить</button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
export default {
  props: {
    students: Array
  }
}
</script>