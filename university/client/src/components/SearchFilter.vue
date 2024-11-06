<template>
  <div>
    <input v-model="query" @input="search" placeholder="Ïîèñê..." />
  </div>
</template>

<script>
export default {
  data() {
    return {
      query: ''
    }
  },
  methods: {
    search() {
      this.$emit('search', this.query)
    }
  }
}
</script>