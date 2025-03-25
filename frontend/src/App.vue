<template>
  <nav>
    <Navigation />

    <router-view/>
  </nav>
</template>

<script>

import Navigation from './components/Navigation.vue'

export default {
  name: 'App',
  components: {
    Navigation
  },
}
</script>

<style>

</style>
