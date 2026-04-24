/**
 * VUE BASICS
 * ===========
 * Template syntax, directives, data binding
 * TODO: Complete with comprehensive examples
 */

<template>
  <div>
    <h1>{{ title }}</h1>
    <p>{{ message }}</p>
    <button @click="increment">Count: {{ count }}</button>
  </div>
</template>

<script>
export default {
  data() {
    return {
      title: 'Vue Basics',
      message: 'Hello, Vue!',
      count: 0
    }
  },
  methods: {
    increment() {
      this.count++
    }
  }
}
</script>

<style scoped>
button {
  padding: 10px;
}
</style>

/**
 * KEY TAKEAWAYS:
 * 1. Template, script, style in single file
 * 2. {{ }} for text interpolation
 * 3. v-bind or : for attribute binding
 * 4. v-on or @ for event handling
 * 5. data() returns component state
 */
