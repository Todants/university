<template>
  <div>
    <h2>Преподаватели</h2>
    <table>
      <thead>
        <tr>
          <th>Имя</th>
          <th>Действия</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="teacher in teachers" :key="teacher.id">
          <td>{{ teacher.name }}</td>
          <td>
            <button @click="$emit('edit', teacher)">Редактировать</button>
            <button @click="$emit('delete', teacher.id)">Удалить</button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
export default {
  props: {
    teachers: Array
  }
}
</script>