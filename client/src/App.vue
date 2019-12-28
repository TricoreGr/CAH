<template>
  <div id="app">
    <router-view />
  </div>
</template>


<script>
export default {
   watch: {
      '$route' (to) {
        document.title = to.meta.title + " - CAH" || 'CAH'
      }
    },
}
</script>


<style lang="scss">
@import "@/styles/index.scss";

</style>
